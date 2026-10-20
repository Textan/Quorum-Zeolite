
pub struct NumericalSchemes;

impl NumericalSchemes {

    pub fn minmod(a: f64, b: f64) -> f64 {
        if a * b <= 0.0 {
            0.0
        } else if a.abs() < b.abs() {
            a
        } else {
            b
        }
    }

    pub fn muscl_face_reconstruction(c_jm1: f64, c_j: f64, c_jp1: f64) -> (f64, f64) {
        let delta_minus = c_j - c_jm1;
        let delta_plus = c_jp1 - c_j;
        let slope = Self::minmod(delta_minus, delta_plus);

        let c_left_face = c_j + 0.5 * slope;
        let c_right_face = c_jp1 - 0.5 * slope;

        (c_left_face, c_right_face)
    }
}

#[derive(Debug, Clone)]
pub struct PidTimeStepController {
    pub tolerance: f64,
    pub cfl_max: f64,
    pub dt_min: f64,
    pub dt_max: f64,
    pub prev_error: f64,
    pub dt_history: Vec<f64>,
}

impl PidTimeStepController {
    pub fn new(tolerance: f64, cfl_max: f64, dt_min: f64, dt_max: f64) -> Self {
        Self {
            tolerance,
            cfl_max,
            dt_min,
            dt_max,
            prev_error: tolerance,
            dt_history: Vec::new(),
        }
    }

    pub fn compute_next_dt(
        &mut self,
        current_dt: f64,
        local_truncation_error: f64,
        dz_m: f64,
        u_max_m_s: f64,
    ) -> f64 {
        let lte = local_truncation_error.max(1e-12);

        let k_p = 0.075;
        let k_i = 0.175;

        let factor = (self.tolerance / lte).powf(k_p) * (self.prev_error / lte).powf(k_i);
        let factor_clamped = factor.clamp(0.2, 2.0);
        let mut next_dt = current_dt * factor_clamped;

        if u_max_m_s > 1e-12 {
            let dt_cfl = self.cfl_max * dz_m / u_max_m_s;
            if next_dt > dt_cfl {
                next_dt = dt_cfl;
            }
        }

        let final_dt = next_dt.clamp(self.dt_min, self.dt_max);
        self.prev_error = lte;
        self.dt_history.push(final_dt);
        final_dt
    }
}
