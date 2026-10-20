
use crate::error::QuorumError;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct FitReport {
    pub model_name: String,
    pub parameters: Vec<f64>,
    pub param_names: Vec<String>,
    pub confidence_intervals_95: Vec<(f64, f64)>,
    pub r_squared: f64,
    pub reduced_chi_squared: f64,
    pub aic: f64,
    pub aicc: f64,
    pub residuals: Vec<f64>,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct ModelSelectionResult {
    pub langmuir_fit: FitReport,
    pub freundlich_fit: FitReport,
    pub selected_model: String,
    pub delta_aic: f64,
}

pub fn vant_hoff_correction(k_ref: f64, delta_h_ads_j_mol: f64, t_kelvin: f64, t_ref_kelvin: f64) -> f64 {
    const R: f64 = 8.31446261815324;
    let exponent = -(delta_h_ads_j_mol / R) * (1.0 / t_kelvin - 1.0 / t_ref_kelvin);
    k_ref * exponent.exp()
}

pub fn fit_langmuir_with_stats(concentrations: &[f64], loadings: &[f64]) -> Result<FitReport, QuorumError> {
    let n = concentrations.len();
    if n < 3 {
        return Err(QuorumError::IsothermFit("Require >= 3 data points for statistical inference".into()));
    }
    let p = 2;

    let mut q_max = loadings.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let c_mean = concentrations.iter().sum::<f64>() / n as f64;
    let mut k = if c_mean > 0.0 { 1.0 / c_mean } else { 1.0 };
    let mut lambda = 1e-3_f64;

    for _ in 0..1000 {
        let mut jtj = [[0.0_f64; 2]; 2];
        let mut jtr = [0.0_f64; 2];
        let mut ssr = 0.0_f64;

        for i in 0..n {
            let c = concentrations[i];
            let denom = 1.0 + k * c;
            let pred = q_max * k * c / denom;
            let r = loadings[i] - pred;
            let j = [k * c / denom, q_max * c / (denom * denom)];

            for row in 0..2 {
                for col in 0..2 {
                    jtj[row][col] += j[row] * j[col];
                }
                jtr[row] += j[row] * r;
            }
            ssr += r * r;
        }

        jtj[0][0] += lambda;
        jtj[1][1] += lambda;

        let det = jtj[0][0] * jtj[1][1] - jtj[0][1] * jtj[1][0];
        if det.abs() < 1e-30 {
            break;
        }

        let d_qmax = (jtr[0] * jtj[1][1] - jtr[1] * jtj[0][1]) / det;
        let d_k = (jtj[0][0] * jtr[1] - jtj[1][0] * jtr[0]) / det;

        let q_max_new = (q_max + d_qmax).max(1e-15);
        let k_new = (k + d_k).max(1e-15);

        let new_ssr: f64 = (0..n)
            .map(|i| {
                let r = loadings[i] - (q_max_new * k_new * concentrations[i] / (1.0 + k_new * concentrations[i]));
                r * r
            })
            .sum();

        if new_ssr < ssr {
            q_max = q_max_new;
            k = k_new;
            lambda *= 0.1;
        } else {
            lambda *= 10.0;
        }

        if (d_qmax * d_qmax + d_k * d_k).sqrt() < 1e-10 {
            break;
        }
    }

    let mut jtj = [[0.0_f64; 2]; 2];
    let mut ssr = 0.0_f64;
    let mut residuals = Vec::with_capacity(n);
    let q_mean = loadings.iter().sum::<f64>() / n as f64;
    let mut sst = 0.0_f64;

    for i in 0..n {
        let c = concentrations[i];
        let denom = 1.0 + k * c;
        let pred = q_max * k * c / denom;
        let r = loadings[i] - pred;
        residuals.push(r);
        ssr += r * r;
        sst += (loadings[i] - q_mean).powi(2);

        let j = [k * c / denom, q_max * c / (denom * denom)];
        for row in 0..2 {
            for col in 0..2 {
                jtj[row][col] += j[row] * j[col];
            }
        }
    }

    let det = jtj[0][0] * jtj[1][1] - jtj[0][1] * jtj[1][0];
    let s2 = ssr / (n - p) as f64;
    let (var_qmax, var_k) = if det.abs() > 1e-30 {
        (
            (jtj[1][1] / det * s2).max(0.0),
            (jtj[0][0] / det * s2).max(0.0),
        )
    } else {
        (0.0, 0.0)
    };

    let ci_qmax = 1.96 * var_qmax.sqrt();
    let ci_k = 1.96 * var_k.sqrt();

    let r_squared = if sst > 0.0 { 1.0 - ssr / sst } else { 0.0 };
    let reduced_chi_squared = s2;

    let aic = 2.0 * p as f64 + (n as f64) * (ssr / n as f64).ln();
    let aicc = aic + (2.0 * p as f64 * (p as f64 + 1.0)) / ((n - p - 1) as f64);

    Ok(FitReport {
        model_name: "Langmuir".to_string(),
        parameters: vec![q_max, k],
        param_names: vec!["q_max_mol_kg".to_string(), "K_m3_mol".to_string()],
        confidence_intervals_95: vec![
            (q_max - ci_qmax, q_max + ci_qmax),
            (k - ci_k, k + ci_k),
        ],
        r_squared,
        reduced_chi_squared,
        aic,
        aicc,
        residuals,
    })
}

pub fn fit_freundlich_with_stats(concentrations: &[f64], loadings: &[f64]) -> Result<FitReport, QuorumError> {
    let n = concentrations.len();
    if n < 3 {
        return Err(QuorumError::IsothermFit("Require >= 3 data points".into()));
    }
    let p = 2;

    let mut k_f = 1.0_f64;
    let mut inv_n = 0.5_f64;
    let mut lambda = 1e-3_f64;

    for _ in 0..1000 {
        let mut jtj = [[0.0_f64; 2]; 2];
        let mut jtr = [0.0_f64; 2];
        let mut ssr = 0.0_f64;

        for i in 0..n {
            let c = concentrations[i].max(1e-12);
            let pred = k_f * c.powf(inv_n);
            let r = loadings[i] - pred;
            let j = [c.powf(inv_n), k_f * c.powf(inv_n) * c.ln()];

            for row in 0..2 {
                for col in 0..2 {
                    jtj[row][col] += j[row] * j[col];
                }
                jtr[row] += j[row] * r;
            }
            ssr += r * r;
        }

        jtj[0][0] += lambda;
        jtj[1][1] += lambda;

        let det = jtj[0][0] * jtj[1][1] - jtj[0][1] * jtj[1][0];
        if det.abs() < 1e-30 {
            break;
        }

        let d_kf = (jtr[0] * jtj[1][1] - jtr[1] * jtj[0][1]) / det;
        let d_invn = (jtj[0][0] * jtr[1] - jtj[1][0] * jtr[0]) / det;

        let k_f_new = (k_f + d_kf).max(1e-15);
        let inv_n_new = (inv_n + d_invn).clamp(1e-5, 2.0);

        let new_ssr: f64 = (0..n)
            .map(|i| {
                let r = loadings[i] - k_f_new * concentrations[i].max(1e-12).powf(inv_n_new);
                r * r
            })
            .sum();

        if new_ssr < ssr {
            k_f = k_f_new;
            inv_n = inv_n_new;
            lambda *= 0.1;
        } else {
            lambda *= 10.0;
        }

        if (d_kf * d_kf + d_invn * d_invn).sqrt() < 1e-10 {
            break;
        }
    }

    let mut jtj = [[0.0_f64; 2]; 2];
    let mut ssr = 0.0_f64;
    let mut residuals = Vec::with_capacity(n);
    let q_mean = loadings.iter().sum::<f64>() / n as f64;
    let mut sst = 0.0_f64;

    for i in 0..n {
        let c = concentrations[i].max(1e-12);
        let pred = k_f * c.powf(inv_n);
        let r = loadings[i] - pred;
        residuals.push(r);
        ssr += r * r;
        sst += (loadings[i] - q_mean).powi(2);

        let j = [c.powf(inv_n), k_f * c.powf(inv_n) * c.ln()];
        for row in 0..2 {
            for col in 0..2 {
                jtj[row][col] += j[row] * j[col];
            }
        }
    }

    let det = jtj[0][0] * jtj[1][1] - jtj[0][1] * jtj[1][0];
    let s2 = ssr / (n - p) as f64;
    let (var_kf, var_invn) = if det.abs() > 1e-30 {
        (
            (jtj[1][1] / det * s2).max(0.0),
            (jtj[0][0] / det * s2).max(0.0),
        )
    } else {
        (0.0, 0.0)
    };

    let ci_kf = 1.96 * var_kf.sqrt();
    let ci_invn = 1.96 * var_invn.sqrt();

    let r_squared = if sst > 0.0 { 1.0 - ssr / sst } else { 0.0 };
    let reduced_chi_squared = s2;
    let aic = 2.0 * p as f64 + (n as f64) * (ssr / n as f64).ln();
    let aicc = aic + (2.0 * p as f64 * (p as f64 + 1.0)) / ((n - p - 1) as f64);

    Ok(FitReport {
        model_name: "Freundlich".to_string(),
        parameters: vec![k_f, inv_n],
        param_names: vec!["K_F".to_string(), "1_over_n".to_string()],
        confidence_intervals_95: vec![
            (k_f - ci_kf, k_f + ci_kf),
            (inv_n - ci_invn, inv_n + ci_invn),
        ],
        r_squared,
        reduced_chi_squared,
        aic,
        aicc,
        residuals,
    })
}

pub fn compare_and_select_isotherm(concentrations: &[f64], loadings: &[f64]) -> Result<ModelSelectionResult, QuorumError> {
    let lang = fit_langmuir_with_stats(concentrations, loadings)?;
    let freund = fit_freundlich_with_stats(concentrations, loadings)?;

    let delta_aic = freund.aicc - lang.aicc;
    let selected_model = if lang.aicc <= freund.aicc {
        "Langmuir".to_string()
    } else {
        "Freundlich".to_string()
    };

    Ok(ModelSelectionResult {
        langmuir_fit: lang,
        freundlich_fit: freund,
        selected_model,
        delta_aic,
    })
}
