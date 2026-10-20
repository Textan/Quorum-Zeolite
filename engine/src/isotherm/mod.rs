pub mod langmuir;
pub mod ias;
pub mod pitzer;
pub mod gaines_thomas;
pub mod fitting;

use pyo3::prelude::*;
use pyo3::types::PyDict;

#[pyfunction]
pub fn py_fit_langmuir(
    concentrations_mol_m3: Vec<f64>,
    loadings_mol_kg: Vec<f64>,
) -> PyResult<std::collections::HashMap<String, Vec<f64>>> {
    let result = langmuir::fit_langmuir(&concentrations_mol_m3, &loadings_mol_kg)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    let mut out = std::collections::HashMap::new();
    out.insert("q_max_mol_kg".to_string(), vec![result.q_max]);
    out.insert("K_m3_mol".to_string(), vec![result.k]);
    out.insert("r_squared".to_string(), vec![result.r_squared]);
    out.insert("residuals".to_string(), result.residuals);
    Ok(out)
}

#[pyfunction]
pub fn py_fit_isotherm_comparison(
    concentrations: Vec<f64>,
    loadings: Vec<f64>,
) -> PyResult<String> {
    let result = fitting::compare_and_select_isotherm(&concentrations, &loadings)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    serde_json::to_string(&result)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
}

#[pyfunction]
pub fn py_solve_fast_ias(
    q_max_list: Vec<f64>,
    k_list: Vec<f64>,
    concentrations: Vec<f64>,
) -> PyResult<std::collections::HashMap<String, Vec<f64>>> {
    let components: Vec<ias::SingleComponentLangmuir> = q_max_list
        .into_iter()
        .zip(k_list.into_iter())
        .map(|(q_max, k)| ias::SingleComponentLangmuir { q_max, k })
        .collect();

    let result = ias::solve_fast_ias(&components, &concentrations)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    let mut out = std::collections::HashMap::new();
    out.insert("spreading_pressure".to_string(), vec![result.spreading_pressure]);
    out.insert("total_loading_mol_kg".to_string(), vec![result.total_loading]);
    out.insert("component_loadings_mol_kg".to_string(), result.component_loadings);
    out.insert("adsorbed_fractions".to_string(), result.adsorbed_fractions);
    out.insert("iterations".to_string(), vec![result.iterations as f64]);
    Ok(out)
}

#[pyfunction]
pub fn py_compute_pitzer_activities(
    m_cs: f64,
    m_sr: f64,
    m_na: f64,
) -> PyResult<std::collections::HashMap<String, f64>> {
    let mut out = std::collections::HashMap::new();
    out.insert("activity_cs".to_string(), pitzer::PitzerModel::activity_cs_plus(m_cs));
    out.insert("activity_sr".to_string(), pitzer::PitzerModel::activity_sr2_plus(m_sr));
    out.insert("activity_na".to_string(), pitzer::PitzerModel::activity_na_plus(m_na));
    Ok(out)
}
