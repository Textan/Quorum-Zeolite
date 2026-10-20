
pub struct PitzerModel;

impl PitzerModel {

    pub const A_PHI: f64 = 0.3915;

    pub const B: f64 = 1.2;

    pub const ALPHA_1: f64 = 2.0;

    pub fn gamma_1_1(m: f64, beta_0: f64, beta_1: f64, c_phi: f64) -> f64 {
        if m <= 1e-12 {
            return 1.0;
        }
        let i = m;
        let sqrt_i = i.sqrt();

        let f_gamma = -Self::A_PHI
            * (sqrt_i / (1.0 + Self::B * sqrt_i)
                + (2.0 / Self::B) * (1.0 + Self::B * sqrt_i).ln());

        let z = Self::ALPHA_1 * sqrt_i;
        let b_gamma = 2.0 * beta_0
            + (2.0 * beta_1 / (Self::ALPHA_1 * Self::ALPHA_1 * i))
                * (1.0 - (1.0 + z - 0.5 * z * z) * (-z).exp());

        let c_gamma = 1.5 * c_phi;

        let ln_gamma = f_gamma + m * b_gamma + m * m * c_gamma;
        ln_gamma.exp()
    }

    pub fn gamma_2_1(m: f64, beta_0: f64, beta_1: f64, c_phi: f64) -> f64 {
        if m <= 1e-12 {
            return 1.0;
        }
        let i = 3.0 * m;
        let sqrt_i = i.sqrt();

        let f_gamma = -2.0
            * Self::A_PHI
            * (sqrt_i / (1.0 + Self::B * sqrt_i)
                + (2.0 / Self::B) * (1.0 + Self::B * sqrt_i).ln());

        let z = Self::ALPHA_1 * sqrt_i;
        let b_gamma = 2.0 * beta_0
            + (2.0 * beta_1 / (Self::ALPHA_1 * Self::ALPHA_1 * i))
                * (1.0 - (1.0 + z - 0.5 * z * z) * (-z).exp());

        let ln_gamma = f_gamma + (4.0 / 3.0) * m * b_gamma + (2.0 * 2.0_f64.sqrt() / 3.0) * m * m * c_phi;
        ln_gamma.exp()
    }

    pub fn activity_cs_plus(molality_mol_kg: f64) -> f64 {

        let gamma = Self::gamma_1_1(molality_mol_kg, 0.0300, 0.0558, 0.00038);
        gamma * molality_mol_kg
    }

    pub fn activity_sr2_plus(molality_mol_kg: f64) -> f64 {

        let gamma = Self::gamma_2_1(molality_mol_kg, 0.2858, 1.6670, -0.00130);
        gamma * molality_mol_kg
    }

    pub fn activity_na_plus(molality_mol_kg: f64) -> f64 {

        let gamma = Self::gamma_1_1(molality_mol_kg, 0.0765, 0.2664, 0.00127);
        gamma * molality_mol_kg
    }
}
