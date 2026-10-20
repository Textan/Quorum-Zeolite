
pub struct MassTransferKinetics;

impl MassTransferKinetics {

    pub fn effective_diffusivity_m2_s(
        d_pore_m2_s: f64,
        particle_porosity: f64,
        tortuosity: f64,
    ) -> f64 {
        d_pore_m2_s * particle_porosity / tortuosity
    }

    pub fn k_ldf_1_s(d_eff_m2_s: f64, particle_radius_m: f64) -> f64 {
        15.0 * d_eff_m2_s / (particle_radius_m * particle_radius_m)
    }

    pub fn axial_dispersion_m2_s(
        u_mean_m_s: f64,
        r_p_m: f64,
        d_mol_m2_s: f64,
    ) -> f64 {
        if d_mol_m2_s <= 1e-15 || u_mean_m_s <= 1e-15 {
            return 1e-7;
        }
        let pe = u_mean_m_s * r_p_m / d_mol_m2_s;
        if pe <= 1e-12 {
            return d_mol_m2_s;
        }
        d_mol_m2_s * (0.5 + 0.3 * pe) / pe
    }

    pub fn radial_dispersion_m2_s(d_z_m2_s: f64) -> f64 {
        d_z_m2_s / 6.7
    }
}
