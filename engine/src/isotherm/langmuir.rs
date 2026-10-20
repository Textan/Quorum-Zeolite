use crate::error::QuorumError;

pub struct LangmuirResult {
    pub q_max: f64,
    pub k: f64,
    pub r_squared: f64,
    pub residuals: Vec<f64>,
}

fn langmuir_model(c: f64, q_max: f64, k: f64) -> f64 {
    q_max * k * c / (1.0 + k * c)
}

pub fn fit_langmuir(
    concentrations: &[f64],
    loadings: &[f64],
) -> Result<LangmuirResult, QuorumError> {
    let n = concentrations.len();
    if n < 2 {
        return Err(QuorumError::IsothermFit("need >= 2 data points".into()));
    }
    if n != loadings.len() {
        return Err(QuorumError::IsothermFit("length mismatch".into()));
    }

    let q_max_init = loadings.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let c_mean: f64 = concentrations.iter().sum::<f64>() / n as f64;
    let k_init = if c_mean > 0.0 { 1.0 / c_mean } else { 1.0 };

    let mut q_max = q_max_init;
    let mut k = k_init;
    let mut lambda = 1e-3_f64;

    for _ in 0..1000 {
        let mut jtj = [[0.0_f64; 2]; 2];
        let mut jtr = [0.0_f64; 2];
        let mut ssr = 0.0_f64;

        for i in 0..n {
            let c = concentrations[i];
            let denom = 1.0 + k * c;
            let r = loadings[i] - q_max * k * c / denom;
            let j = [k * c / denom, q_max * c / (denom * denom)];

            for row in 0..2 {
                for col in 0..2 { jtj[row][col] += j[row] * j[col]; }
                jtr[row] += j[row] * r;
            }
            ssr += r * r;
        }

        jtj[0][0] += lambda;
        jtj[1][1] += lambda;

        let det = jtj[0][0] * jtj[1][1] - jtj[0][1] * jtj[1][0];
        if det.abs() < 1e-30 {
            return Err(QuorumError::IsothermFit("singular Jacobian".into()));
        }

        let d_qmax = (jtr[0] * jtj[1][1] - jtr[1] * jtj[0][1]) / det;
        let d_k = (jtj[0][0] * jtr[1] - jtj[1][0] * jtr[0]) / det;

        let param_norm = (q_max * q_max + k * k).sqrt();
        let step_norm = (d_qmax * d_qmax + d_k * d_k).sqrt();

        let q_max_new = (q_max + d_qmax).max(1e-15);
        let k_new = (k + d_k).max(1e-15);

        let new_ssr: f64 = (0..n)
            .map(|i| { let r = loadings[i] - langmuir_model(concentrations[i], q_max_new, k_new); r * r })
            .sum();

        if new_ssr < ssr {
            q_max = q_max_new;
            k = k_new;
            lambda *= 0.1;
        } else {
            lambda *= 10.0;
        }

        if step_norm / (param_norm + 1e-30) < 1e-10 { break; }
    }

    let q_mean: f64 = loadings.iter().sum::<f64>() / n as f64;
    let mut ss_res = 0.0;
    let mut ss_tot = 0.0;
    let mut residuals = Vec::with_capacity(n);

    for i in 0..n {
        let r = loadings[i] - langmuir_model(concentrations[i], q_max, k);
        residuals.push(r);
        ss_res += r * r;
        ss_tot += (loadings[i] - q_mean).powi(2);
    }

    Ok(LangmuirResult {
        q_max,
        k,
        r_squared: if ss_tot > 0.0 { 1.0 - ss_res / ss_tot } else { 0.0 },
        residuals,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_langmuir_fit_perfect_data() {
        let cs: Vec<f64> = (1..=20).map(|i| i as f64 * 0.5).collect();
        let qs: Vec<f64> = cs.iter().map(|&c| langmuir_model(c, 2.0, 0.5)).collect();
        let r = fit_langmuir(&cs, &qs).unwrap();
        assert!((r.q_max - 2.0).abs() < 1e-6);
        assert!((r.k - 0.5).abs() < 1e-6);
        assert!(r.r_squared > 0.9999);
    }
}
