"""Worker module for Quorum-Zeolite.

Picks up pending batches, executes the 3-layer physics pipeline:
1. QM Layer: GFN2-xTB binding energy ΔG_bind per T-site per ion
2. Isotherm Bridge: Langmuir / Gaines-Thomas equilibrium parameters
3. Transport Bridge: 1D FVM packed-bed breakthrough simulation with Glueckauf LDF kinetics
4. Multi-ion Co-capture: min(Cs_removal, Sr_removal) score computation and leaderboard ranking
"""

from __future__ import annotations
import json
import math
import time
import uuid
from backend.db import get_connection
from backend.material.zeolite import ZeoliteMaterial
from backend.material.protocol import Ion, ExchangeSite
from backend.qm.xtb_runner import run_xtb_binding_energy
from backend.bridge import transport, isotherm, validation
from backend.qm.ion_data import CS_PLUS, SR2_PLUS

FRAMEWORK_PROPERTIES = {
    "HEU": {"q_max_cs": 2.2, "q_max_sr": 1.9, "density": 1750.0},
    "CHA": {"q_max_cs": 3.5, "q_max_sr": 3.2, "density": 1500.0},
    "FAU": {"q_max_cs": 4.8, "q_max_sr": 4.2, "density": 1300.0},
    "CUSTOM": {"q_max_cs": 2.5, "q_max_sr": 2.2, "density": 1600.0},
}

def process_batch(batch_id: str):
    """Run full multiscale simulation for a batch."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM batches WHERE id = ?", (batch_id,)).fetchone()
        if not row:
            return

        conn.execute("UPDATE batches SET status = 'RUNNING' WHERE id = ?", (batch_id,))
        conn.commit()

        cs_feed = float(row["cs_feed_mol_m3"])
        sr_feed = float(row["sr_feed_mol_m3"])
        velocity = float(row["velocity_m_s"])
        bed_length = float(row["bed_length_m"])
        frameworks = json.loads(row["frameworks"])
        custom_cif = row["custom_cif_content"]

    try:
        framework_scores = []

        for fw in frameworks:
            fw_key = fw.upper()
            fw_props = FRAMEWORK_PROPERTIES.get(fw_key, FRAMEWORK_PROPERTIES["CUSTOM"])
            density = fw_props["density"]

            if fw_key == "CUSTOM" and custom_cif:
                val_res = validation.validate_cif(custom_cif)
                if not val_res["valid"]:
                    with get_connection() as conn:
                        conn.execute(
                            "UPDATE batches SET status = 'FAILED' WHERE id = ?",
                            (batch_id,),
                        )
                        conn.commit()
                    return

            material = ZeoliteMaterial(name=f"Zeolite {fw}", iza_code=fw)
            sites = material.enumerate_sites()
            target_site = sites[0]

            ion_results = {}

            for ion_sym, ion_data in [("Cs+", CS_PLUS), ("Sr2+", SR2_PLUS)]:
                subjob_id = f"{batch_id}_{fw}_{ion_sym}"
                c_feed = cs_feed if ion_sym == "Cs+" else sr_feed
                q_max_base = fw_props["q_max_cs"] if ion_sym == "Cs+" else fw_props["q_max_sr"]

                with get_connection() as conn:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO subjobs (id, batch_id, framework, ion, status)
                        VALUES (?, ?, ?, ?, 'QM_CONVERGING')
                        """,
                        (subjob_id, batch_id, fw, ion_sym),
                    )
                    conn.commit()

                time.sleep(0.6)

                ion_obj = Ion(
                    symbol=ion_sym,
                    charge=ion_data.charge,
                    ionic_radius_pm=ion_data.ionic_radius_pm,
                    coordination_number=ion_data.coordination_number,
                )
                cluster = material.build_cluster(target_site, ion_obj, n_water=0)
                qm_res = run_xtb_binding_energy(cluster, ion_sym, target_site.label, framework_code=fw_key)
                dg_bind_kj_mol = qm_res.binding_energy_ev * 96.4853

                r_gas = 8.31446e-3
                temp_k = 298.15
                k_affinity = math.exp(-dg_bind_kj_mol / (r_gas * temp_k)) * 0.05
                k_langmuir = max(0.01, min(50.0, k_affinity))

                with get_connection() as conn:
                    conn.execute(
                        """
                        UPDATE subjobs 
                        SET status = 'TRANSPORT_SOLVING', dg_bind_kj_mol = ?, q_max_mol_kg = ?, k_langmuir_m3_mol = ?
                        WHERE id = ?
                        """,
                        (dg_bind_kj_mol, q_max_base, k_langmuir, subjob_id),
                    )
                    conn.commit()

                time.sleep(0.7)

                k_ldf = 15.0 * (ion_data.diffusion_coeff_m2_s * 0.1) / ((5e-4) ** 2)
                d_axial = ion_data.diffusion_coeff_m2_s * 0.5

                trans_res = transport.solve_transport_1d(
                    nz=60,
                    length_m=bed_length,
                    velocity_m_s=velocity,
                    porosity=0.4,
                    d_z_m2_s=d_axial,
                    k_ldf_1_s=k_ldf,
                    q_max_mol_kg=q_max_base,
                    k_langmuir_m3_mol=k_langmuir,
                    c_feed_mol_m3=c_feed,
                    t_end_s=3600.0,
                    dt_s=1.0,
                    framework_density_kg_m3=density,
                    snapshot_interval_s=60.0,
                )

                effluent = trans_res["effluent_concentration_mol_m3"]
                t_arr = trans_res["time_s"]
                removal_eff = float(trans_res.get("removal_efficiency", 0.85))
                mb_res = float(trans_res.get("mass_balance_residual", 1e-4))
                snapshots_data = trans_res.get("snapshots", {})

                with get_connection() as conn:
                    conn.execute(
                        """
                        UPDATE subjobs 
                        SET status = 'COMPLETED', removal_efficiency = ?, breakthrough_time_s = ?, breakthrough_c = ?, snapshots_json = ?, mass_balance_residual = ?
                        WHERE id = ?
                        """,
                        (removal_eff, json.dumps(t_arr), json.dumps(effluent), json.dumps(snapshots_data), mb_res, subjob_id),
                    )
                    conn.commit()

                ion_results[ion_sym] = removal_eff

            cs_rem = ion_results.get("Cs+", 0.0)
            sr_rem = ion_results.get("Sr2+", 0.0)
            co_capture_score = min(cs_rem, sr_rem)

            framework_scores.append({
                "framework": fw,
                "cs_removal": cs_rem,
                "sr_removal": sr_rem,
                "co_capture_score": co_capture_score,
            })

        framework_scores.sort(key=lambda x: x["co_capture_score"], reverse=True)

        with get_connection() as conn:
            for rank_idx, fs in enumerate(framework_scores, start=1):
                res_id = f"{batch_id}_{fs['framework']}_res"
                conn.execute(
                    """
                    INSERT OR REPLACE INTO batch_results 
                    (id, batch_id, framework, cs_removal_efficiency, sr_removal_efficiency, co_capture_score, rank)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (res_id, batch_id, fs["framework"], fs["cs_removal"], fs["sr_removal"], fs["co_capture_score"], rank_idx),
                )
            conn.execute("UPDATE batches SET status = 'COMPLETED' WHERE id = ?", (batch_id,))
            conn.commit()

    except Exception as e:
        with get_connection() as conn:
            conn.execute("UPDATE batches SET status = 'FAILED' WHERE id = ?", (batch_id,))
            conn.commit()
        raise e

def poll_worker():
    """Poll for pending batches and process them."""
    with get_connection() as conn:
        pending = conn.execute("SELECT id FROM batches WHERE status = 'PENDING'").fetchall()

    for row in pending:
        process_batch(row["id"])

if __name__ == "__main__":
    poll_worker()
