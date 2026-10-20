
use crate::error::QuorumError;
use crate::isotherm::ias::{solve_fast_ias, SingleComponentLangmuir};
use super::mesh::CylindricalMesh2D;
use super::schemes::{NumericalSchemes, PidTimeStepController};
use super::mass_balance::MassBalanceReport;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct TransportResult2D {
    pub time_s: Vec<f64>,
    pub effluent_cs_mol_m3: Vec<f64>,
    pub effluent_sr_mol_m3: Vec<f64>,
    pub snapshots_cs_c_flat: Vec<f64>,
    pub snapshots_cs_q_flat: Vec<f64>,
    pub snapshots_sr_c_flat: Vec<f64>,
    pub snapshots_sr_q_flat: Vec<f64>,
    pub snapshot_times_s: Vec<f64>,
    pub mass_balance_cs: MassBalanceReport,
    pub mass_balance_sr: MassBalanceReport,
    pub nr: usize,
    pub nz: usize,
    pub n_snapshots: usize,
    pub cs_removal_efficiency: f64,
    pub sr_removal_efficiency: f64,
    pub co_capture_score: f64,
}

pub struct TransportResult1D {
    pub time_s: Vec<f64>,
    pub effluent_c: Vec<f64>,
    pub snapshots_c: Vec<Vec<f64>>,
    pub snapshots_q: Vec<Vec<f64>>,
    pub snapshot_times: Vec<f64>,
    pub mass_balance_residual: f64,
}

fn q_star_langmuir(c: f64, q_max: f64, k: f64) -> f64 {
    q_max * k * c / (1.0 + k * c)
}

#[allow(clippy::too_many_arguments)]
pub fn solve_1d(
    nz: usize,
    length_m: f64,
    velocity: f64,
    porosity: f64,
    d_z: f64,
    k_ldf: f64,
    q_max: f64,
    k_langmuir: f64,
    c_feed: f64,
    t_end: f64,
    dt: f64,
    rho_s: f64,
    snapshot_interval: f64,
) -> Result<TransportResult1D, QuorumError> {
    let dz = length_m / nz as f64;
    let cfl = velocity * dt / dz;
    if cfl > 0.8 {
        return Err(QuorumError::TransportSolver(format!(
            "CFL = {:.4} exceeds limit 0.8; reduce dt or increase nz",
            cfl
        )));
    }

    let mut c = vec![0.0_f64; nz];
    let mut q = vec![0.0_f64; nz];
    let mut time_s = Vec::new();
    let mut effluent_c = Vec::new();
    let mut snapshots_c = Vec::new();
    let mut snapshots_q = Vec::new();
    let mut snapshot_times = Vec::new();

    let mut t = 0.0_f64;
    let mut next_snapshot = 0.0_f64;
    let mut mass_in = 0.0_f64;
    let mut mass_out = 0.0_f64;

    let n_steps = (t_end / dt).ceil() as usize;

    for _ in 0..n_steps {
        t += dt;
        mass_in += velocity * c_feed * dt;
        mass_out += velocity * c[nz - 1] * dt;

        for i in 0..nz {
            let q_eq = q_star_langmuir(c[i], q_max, k_langmuir);
            q[i] += dt * k_ldf * (q_eq - q[i]);
        }

        let c_old = c.clone();
        for i in 0..nz {
            let c_left = if i == 0 { c_feed } else { c_old[i - 1] };
            let advection = -velocity * (c_old[i] - c_left) / dz;

            let c_im1 = if i == 0 { c_feed } else { c_old[i - 1] };
            let c_ip1 = if i + 1 < nz { c_old[i + 1] } else { c_old[i] };
            let dispersion = d_z * (c_ip1 - 2.0 * c_old[i] + c_im1) / (dz * dz);

            let q_eq = q_star_langmuir(c_old[i], q_max, k_langmuir);
            let dqdt = k_ldf * (q_eq - q[i]);
            let adsorption_sink = -(1.0 - porosity) / porosity * rho_s * dqdt;

            c[i] = c_old[i] + dt / porosity * (advection + dispersion) + dt * adsorption_sink / porosity;
            if c[i] < 0.0 {
                c[i] = 0.0;
            }
        }

        time_s.push(t);
        effluent_c.push(c[nz - 1]);

        if t >= next_snapshot {
            snapshots_c.push(c.clone());
            snapshots_q.push(q.clone());
            snapshot_times.push(t);
            next_snapshot += snapshot_interval;
        }
    }

    let mass_bed: f64 = (0..nz)
        .map(|i| ((1.0 - porosity) * rho_s * q[i] + porosity * c[i]) * dz)
        .sum();

    let mass_balance_residual = if mass_in > 0.0 {
        (mass_in - mass_out - mass_bed).abs() / mass_in
    } else {
        0.0
    };

    Ok(TransportResult1D {
        time_s,
        effluent_c,
        snapshots_c,
        snapshots_q,
        snapshot_times,
        mass_balance_residual,
    })
}

#[allow(clippy::too_many_arguments)]
pub fn solve_2d_coupled(
    nr: usize,
    nz: usize,
    r_bed_m: f64,
    length_m: f64,
    u_mean_m_s: f64,
    porosity: f64,
    rho_s_kg_m3: f64,
    d_z_cs: f64,
    d_r_cs: f64,
    k_ldf_cs: f64,
    q_max_cs: f64,
    k_cs: f64,
    c_feed_cs: f64,
    d_z_sr: f64,
    d_r_sr: f64,
    k_ldf_sr: f64,
    q_max_sr: f64,
    k_sr: f64,
    c_feed_sr: f64,
    t_end_s: f64,
    initial_dt_s: f64,
    snapshot_interval_s: f64,
) -> Result<TransportResult2D, QuorumError> {
    let mesh = CylindricalMesh2D::new(nr, nz, r_bed_m, length_m);
    let u_r = mesh.velocity_profile(u_mean_m_s);
    let u_max = 2.0 * u_mean_m_s;

    let comp_cs = SingleComponentLangmuir { q_max: q_max_cs, k: k_cs };
    let comp_sr = SingleComponentLangmuir { q_max: q_max_sr, k: k_sr };
    let components = [comp_cs, comp_sr];

    let mut c_cs = vec![vec![0.0_f64; nz]; nr];
    let mut q_cs = vec![vec![0.0_f64; nz]; nr];
    let mut c_sr = vec![vec![0.0_f64; nz]; nr];
    let mut q_sr = vec![vec![0.0_f64; nz]; nr];

    let mut time_s = Vec::new();
    let mut effluent_cs = Vec::new();
    let mut effluent_sr = Vec::new();

    let mut flat_snapshots_c_cs = Vec::new();
    let mut flat_snapshots_q_cs = Vec::new();
    let mut flat_snapshots_c_sr = Vec::new();
    let mut flat_snapshots_q_sr = Vec::new();
    let mut snapshot_times = Vec::new();

    let mut t = 0.0_f64;
    let mut next_snapshot = 0.0_f64;
    let mut n_snapshots = 0;

    let mut mass_in_cs = 0.0_f64;
    let mut mass_out_cs = 0.0_f64;
    let mut mass_in_sr = 0.0_f64;
    let mut mass_out_sr = 0.0_f64;

    const PI: f64 = std::f64::consts::PI;
    let total_cross_section = PI * r_bed_m * r_bed_m;

    let mut dt_controller = PidTimeStepController::new(1e-4, 0.8, 1e-4, initial_dt_s);
    let mut dt = initial_dt_s;

    while t < t_end_s {
        let step_dt = dt.min(t_end_s - t);
        t += step_dt;

        for i in 0..nr {
            let r_in = i as f64 * mesh.dr_m;
            let r_out = (i + 1) as f64 * mesh.dr_m;
            let a_ring = PI * (r_out * r_out - r_in * r_in);
            let flux_vol = u_r[i] * a_ring * step_dt;
            mass_in_cs += flux_vol * c_feed_cs;
            mass_in_sr += flux_vol * c_feed_sr;
            mass_out_cs += flux_vol * c_cs[i][nz - 1];
            mass_out_sr += flux_vol * c_sr[i][nz - 1];
        }

        for i in 0..nr {
            for j in 0..nz {
                let concs = [c_cs[i][j], c_sr[i][j]];
                let ias_res = solve_fast_ias(&components, &concs)?;
                let q_star_cs = ias_res.component_loadings[0];
                let q_star_sr = ias_res.component_loadings[1];

                q_cs[i][j] += step_dt * k_ldf_cs * (q_star_cs - q_cs[i][j]);
                q_sr[i][j] += step_dt * k_ldf_sr * (q_star_sr - q_sr[i][j]);
            }
        }

        let c_old_cs = c_cs.clone();
        let c_old_sr = c_sr.clone();

        for i in 0..nr {
            let u_i = u_r[i];
            let r_i = mesh.r_cell_centers_m[i];

            for j in 0..nz {

                let (c_jm1_cs, c_jp1_cs) = (
                    if j == 0 { c_feed_cs } else { c_old_cs[i][j - 1] },
                    if j + 1 < nz { c_old_cs[i][j + 1] } else { c_old_cs[i][j] },
                );
                let (c_left_cs, _) = NumericalSchemes::muscl_face_reconstruction(
                    if j > 1 { c_old_cs[i][j - 2] } else { c_feed_cs },
                    c_jm1_cs,
                    c_old_cs[i][j],
                );
                let advection_z_cs = -u_i * (c_old_cs[i][j] - c_left_cs) / mesh.dz_m;
                let disp_z_cs = d_z_cs * (c_jp1_cs - 2.0 * c_old_cs[i][j] + c_jm1_cs) / (mesh.dz_m * mesh.dz_m);

                let c_im1_cs = if i == 0 { c_old_cs[0][j] } else { c_old_cs[i - 1][j] };
                let c_ip1_cs = if i + 1 < nr { c_old_cs[i + 1][j] } else { c_old_cs[i][j] };
                let disp_r_cs = if r_i > 1e-12 {
                    d_r_cs * ((c_ip1_cs - 2.0 * c_old_cs[i][j] + c_im1_cs) / (mesh.dr_m * mesh.dr_m)
                        + (c_ip1_cs - c_im1_cs) / (2.0 * r_i * mesh.dr_m))
                } else {
                    4.0 * d_r_cs * (c_old_cs[1][j] - c_old_cs[0][j]) / (mesh.dr_m * mesh.dr_m)
                };

                let concs_cs = [c_old_cs[i][j], c_old_sr[i][j]];
                let ias_cs = solve_fast_ias(&components, &concs_cs)?;
                let dqdt_cs = k_ldf_cs * (ias_cs.component_loadings[0] - q_cs[i][j]);
                let sink_cs = -(1.0 - porosity) / porosity * rho_s_kg_m3 * dqdt_cs;

                c_cs[i][j] = (c_old_cs[i][j]
                    + (step_dt / porosity) * (advection_z_cs + disp_z_cs + disp_r_cs)
                    + (step_dt / porosity) * sink_cs)
                    .max(0.0);

                let (c_jm1_sr, c_jp1_sr) = (
                    if j == 0 { c_feed_sr } else { c_old_sr[i][j - 1] },
                    if j + 1 < nz { c_old_sr[i][j + 1] } else { c_old_sr[i][j] },
                );
                let (c_left_sr, _) = NumericalSchemes::muscl_face_reconstruction(
                    if j > 1 { c_old_sr[i][j - 2] } else { c_feed_sr },
                    c_jm1_sr,
                    c_old_sr[i][j],
                );
                let advection_z_sr = -u_i * (c_old_sr[i][j] - c_left_sr) / mesh.dz_m;
                let disp_z_sr = d_z_sr * (c_jp1_sr - 2.0 * c_old_sr[i][j] + c_jm1_sr) / (mesh.dz_m * mesh.dz_m);

                let c_im1_sr = if i == 0 { c_old_sr[0][j] } else { c_old_sr[i - 1][j] };
                let c_ip1_sr = if i + 1 < nr { c_old_sr[i + 1][j] } else { c_old_sr[i][j] };
                let disp_r_sr = if r_i > 1e-12 {
                    d_r_sr * ((c_ip1_sr - 2.0 * c_old_sr[i][j] + c_im1_sr) / (mesh.dr_m * mesh.dr_m)
                        + (c_ip1_sr - c_im1_sr) / (2.0 * r_i * mesh.dr_m))
                } else {
                    4.0 * d_r_sr * (c_old_sr[1][j] - c_old_sr[0][j]) / (mesh.dr_m * mesh.dr_m)
                };

                let dqdt_sr = k_ldf_sr * (ias_cs.component_loadings[1] - q_sr[i][j]);
                let sink_sr = -(1.0 - porosity) / porosity * rho_s_kg_m3 * dqdt_sr;

                c_sr[i][j] = (c_old_sr[i][j]
                    + (step_dt / porosity) * (advection_z_sr + disp_z_sr + disp_r_sr)
                    + (step_dt / porosity) * sink_sr)
                    .max(0.0);
            }
        }

        let mut total_flux_vol = 0.0_f64;
        let mut weighted_c_cs = 0.0_f64;
        let mut weighted_c_sr = 0.0_f64;

        for i in 0..nr {
            let r_in = i as f64 * mesh.dr_m;
            let r_out = (i + 1) as f64 * mesh.dr_m;
            let a_ring = PI * (r_out * r_out - r_in * r_in);
            let fv = u_r[i] * a_ring;
            total_flux_vol += fv;
            weighted_c_cs += fv * c_cs[i][nz - 1];
            weighted_c_sr += fv * c_sr[i][nz - 1];
        }

        let eff_cs = if total_flux_vol > 0.0 { weighted_c_cs / total_flux_vol } else { 0.0 };
        let eff_sr = if total_flux_vol > 0.0 { weighted_c_sr / total_flux_vol } else { 0.0 };

        time_s.push(t);
        effluent_cs.push(eff_cs);
        effluent_sr.push(eff_sr);

        if t >= next_snapshot {
            for i in 0..nr {
                for j in 0..nz {
                    flat_snapshots_c_cs.push(c_cs[i][j]);
                    flat_snapshots_q_cs.push(q_cs[i][j]);
                    flat_snapshots_c_sr.push(c_sr[i][j]);
                    flat_snapshots_q_sr.push(q_sr[i][j]);
                }
            }
            snapshot_times.push(t);
            n_snapshots += 1;
            next_snapshot += snapshot_interval_s;
        }

        let mut max_diff = 0.0_f64;
        for i in 0..nr {
            for j in 0..nz {
                let diff_cs = (c_cs[i][j] - c_old_cs[i][j]).abs() / (c_feed_cs.max(1e-12));
                let diff_sr = (c_sr[i][j] - c_old_sr[i][j]).abs() / (c_feed_sr.max(1e-12));
                if diff_cs > max_diff { max_diff = diff_cs; }
                if diff_sr > max_diff { max_diff = diff_sr; }
            }
        }
        dt = dt_controller.compute_next_dt(step_dt, max_diff, mesh.dz_m, u_max);
    }

    let mut bed_mass_adsorbed_cs = 0.0_f64;
    let mut bed_mass_fluid_cs = 0.0_f64;
    let mut bed_mass_adsorbed_sr = 0.0_f64;
    let mut bed_mass_fluid_sr = 0.0_f64;

    for i in 0..nr {
        for j in 0..nz {
            let v = mesh.cell_volumes_m3[i][j];
            bed_mass_adsorbed_cs += (1.0 - porosity) * rho_s_kg_m3 * q_cs[i][j] * v;
            bed_mass_fluid_cs += porosity * c_cs[i][j] * v;
            bed_mass_adsorbed_sr += (1.0 - porosity) * rho_s_kg_m3 * q_sr[i][j] * v;
            bed_mass_fluid_sr += porosity * c_sr[i][j] * v;
        }
    }

    let mb_cs = MassBalanceReport::compute(
        "Cs+",
        mass_in_cs,
        mass_out_cs,
        bed_mass_adsorbed_cs,
        bed_mass_fluid_cs,
    )?;

    let mb_sr = MassBalanceReport::compute(
        "Sr2+",
        mass_in_sr,
        mass_out_sr,
        bed_mass_adsorbed_sr,
        bed_mass_fluid_sr,
    )?;

    let cs_removal = if mass_in_cs > 0.0 { ((mass_in_cs - mass_out_cs) / mass_in_cs).clamp(0.0, 1.0) } else { 0.0 };
    let sr_removal = if mass_in_sr > 0.0 { ((mass_in_sr - mass_out_sr) / mass_in_sr).clamp(0.0, 1.0) } else { 0.0 };

    let co_capture_score = cs_removal.min(sr_removal);

    Ok(TransportResult2D {
        time_s,
        effluent_cs_mol_m3: effluent_cs,
        effluent_sr_mol_m3: effluent_sr,
        snapshots_cs_c_flat: flat_snapshots_c_cs,
        snapshots_cs_q_flat: flat_snapshots_q_cs,
        snapshots_sr_c_flat: flat_snapshots_c_sr,
        snapshots_sr_q_flat: flat_snapshots_q_sr,
        snapshot_times_s: snapshot_times,
        mass_balance_cs: mb_cs,
        mass_balance_sr: mb_sr,
        nr,
        nz,
        n_snapshots,
        cs_removal_efficiency: cs_removal,
        sr_removal_efficiency: sr_removal,
        co_capture_score,
    })
}
