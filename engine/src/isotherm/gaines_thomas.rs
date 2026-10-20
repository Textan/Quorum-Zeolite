
pub struct GainesThomasExchange;

impl GainesThomasExchange {

    pub fn select_1_1(e_cs: f64, a_cs: f64, a_na: f64) -> f64 {
        let e_na = 1.0 - e_cs;
        if e_na <= 1e-12 || a_cs <= 1e-12 {
            return 0.0;
        }
        (e_cs * a_na) / (e_na * a_cs)
    }

    pub fn equilibrium_e_cs(k_gt: f64, a_cs: f64, a_na: f64) -> f64 {
        if a_na <= 1e-12 {
            return 1.0;
        }
        let r = k_gt * (a_cs / a_na);
        r / (1.0 + r)
    }

    pub fn select_2_1(e_sr: f64, a_sr: f64, a_na: f64) -> f64 {
        let e_na = 1.0 - e_sr;
        if e_na <= 1e-12 || a_sr <= 1e-12 {
            return 0.0;
        }
        (e_sr * a_na * a_na) / (e_na * e_na * a_sr)
    }

    pub fn equilibrium_e_sr(k_gt: f64, a_sr: f64, a_na: f64) -> f64 {
        if a_na <= 1e-12 {
            return 1.0;
        }
        let b = k_gt * (a_sr / (a_na * a_na));
        if b <= 1e-12 {
            return 0.0;
        }
        let disc = 4.0 * b + 1.0;
        let root = (2.0 * b + 1.0 - disc.sqrt()) / (2.0 * b);
        root.clamp(0.0, 1.0)
    }
}
