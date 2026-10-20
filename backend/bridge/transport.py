"""Python bridge to Rust 1D transport solver (quorum_engine.py_solve_transport_1d).

Thin wrapper — all numerical computation in Rust. This handles config dict
assembly and result unpacking.
"""

from __future__ import annotations
import quorum_engine

def solve_transport_1d(
    nz: int,
    length_m: float,
    velocity_m_s: float,
    porosity: float,
    d_z_m2_s: float,
    k_ldf_1_s: float,
    q_max_mol_kg: float,
    k_langmuir_m3_mol: float,
    c_feed_mol_m3: float,
    t_end_s: float,
    dt_s: float,
    framework_density_kg_m3: float,
    snapshot_interval_s: float,
) -> dict:
    """Run the 1D transport solver via the Rust engine.

    Returns dict with: time_s, effluent_concentration_mol_m3,
    snapshots_c_flat, snapshots_q_flat, snapshot_times_s,
    mass_balance_residual, nz, n_snapshots.
    """
    config = {
        "nz": nz,
        "length_m": length_m,
        "velocity_m_s": velocity_m_s,
        "porosity": porosity,
        "d_z_m2_s": d_z_m2_s,
        "k_ldf_1_s": k_ldf_1_s,
        "q_max_mol_kg": q_max_mol_kg,
        "k_langmuir_m3_mol": k_langmuir_m3_mol,
        "c_feed_mol_m3": c_feed_mol_m3,
        "t_end_s": t_end_s,
        "dt_s": dt_s,
        "framework_density_kg_m3": framework_density_kg_m3,
        "snapshot_interval_s": snapshot_interval_s,
    }
    return quorum_engine.py_solve_transport_1d(config)
