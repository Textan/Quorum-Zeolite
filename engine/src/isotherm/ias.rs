
use crate::error::QuorumError;

#[derive(Debug, Clone)]
pub struct SingleComponentLangmuir {
    pub q_max: f64,
    pub k: f64,
}

impl SingleComponentLangmuir {

    pub fn spreading_pressure(&self, c: f64) -> f64 {
        self.q_max * (1.0 + self.k * c).ln()
    }

    pub fn standard_concentration(&self, psi: f64) -> f64 {
        ((psi / self.q_max).exp() - 1.0) / self.k
    }

    pub fn standard_loading(&self, psi: f64) -> f64 {
        self.q_max * (1.0 - (-psi / self.q_max).exp())
    }
}

#[derive(Debug, Clone)]
pub struct CompetitiveIASResult {
    pub spreading_pressure: f64,
    pub adsorbed_fractions: Vec<f64>,
    pub total_loading: f64,
    pub component_loadings: Vec<f64>,
    pub iterations: usize,
}

pub fn solve_fast_ias(
    components: &[SingleComponentLangmuir],
    concentrations: &[f64],
) -> Result<CompetitiveIASResult, QuorumError> {
    let n = components.len();
    if n != concentrations.len() {
        return Err(QuorumError::Numerical("Components and concentrations length mismatch".into()));
    }

    let any_positive = concentrations.iter().any(|&c| c > 1e-15);
    if !any_positive {
        return Ok(CompetitiveIASResult {
            spreading_pressure: 0.0,
            adsorbed_fractions: vec![0.0; n],
            total_loading: 0.0,
            component_loadings: vec![0.0; n],
            iterations: 0,
        });
    }

    let mut psi = 1e-3_f64;
    for (comp, &c) in components.iter().zip(concentrations.iter()) {
        if c > 1e-15 {
            let p = comp.spreading_pressure(c);
            if p > psi {
                psi = p;
            }
        }
    }

    let tol = 1e-10_f64;
    let max_iter = 1000;
    let mut iter = 0;

    while iter < max_iter {
        iter += 1;

        let mut f_val = -1.0_f64;
        let mut f_prime = 0.0_f64;

        for (comp, &c) in components.iter().zip(concentrations.iter()) {
            if c <= 1e-15 {
                continue;
            }
            let c0 = comp.standard_concentration(psi);
            if c0 <= 1e-30 {
                continue;
            }
            let x_i = c / c0;
            f_val += x_i;

            let q0 = comp.standard_loading(psi);
            if q0 > 1e-30 {
                f_prime -= x_i / (c0 * q0);
            }
        }

        if f_prime.abs() < 1e-30 {
            break;
        }

        let delta_psi = f_val / f_prime;
        psi -= delta_psi;
        if psi < 1e-12 {
            psi = 1e-12;
        }

        if delta_psi.abs() < tol {
            break;
        }
    }

    let mut adsorbed_fractions = vec![0.0; n];
    let mut inv_qt = 0.0_f64;

    for (i, (comp, &c)) in components.iter().zip(concentrations.iter()).enumerate() {
        if c > 1e-15 {
            let c0 = comp.standard_concentration(psi);
            if c0 > 1e-30 {
                let x_i = c / c0;
                adsorbed_fractions[i] = x_i;
                let q0 = comp.standard_loading(psi);
                if q0 > 1e-30 {
                    inv_qt += x_i / q0;
                }
            }
        }
    }

    let total_loading = if inv_qt > 1e-30 { 1.0 / inv_qt } else { 0.0 };
    let mut component_loadings = vec![0.0; n];
    for i in 0..n {
        component_loadings[i] = adsorbed_fractions[i] * total_loading;
    }

    Ok(CompetitiveIASResult {
        spreading_pressure: psi,
        adsorbed_fractions,
        total_loading,
        component_loadings,
        iterations: iter,
    })
}
