pub mod solver;
pub mod mesh;
pub mod ldf;
pub mod schemes;
pub mod mass_balance;

use pyo3::prelude::*;
use pyo3::types::PyDict;

#[pyfunction]
pub fn py_solve_transport_1d(config: &Bound<'_, PyDict>) -> PyResult<std::collections::HashMap<String, Vec<f64>>> {
    let get_f64 = |key: &str| -> PyResult<f64> {
        config
            .get_item(key)?
            .ok_or_else(|| pyo3::exceptions::PyKeyError::new_err(format!("missing: {}", key)))?
            .extract::<f64>()
    };
    let get_usize = |key: &str| -> PyResult<usize> {
        config
            .get_item(key)?
            .ok_or_else(|| pyo3::exceptions::PyKeyError::new_err(format!("missing: {}", key)))?
            .extract::<usize>()
    };

    let result = solver::solve_1d(
        get_usize("nz")?,
        get_f64("length_m")?,
        get_f64("velocity_m_s")?,
        get_f64("porosity")?,
        get_f64("d_z_m2_s")?,
        get_f64("k_ldf_1_s")?,
        get_f64("q_max_mol_kg")?,
        get_f64("k_langmuir_m3_mol")?,
        get_f64("c_feed_mol_m3")?,
        get_f64("t_end_s")?,
        get_f64("dt_s")?,
        get_f64("framework_density_kg_m3")?,
        get_f64("snapshot_interval_s")?,
    )
    .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    let mut out = std::collections::HashMap::new();
    out.insert("time_s".to_string(), result.time_s);
    out.insert("effluent_concentration_mol_m3".to_string(), result.effluent_c);
    out.insert("snapshot_times_s".to_string(), result.snapshot_times);
    out.insert("mass_balance_residual".to_string(), vec![result.mass_balance_residual]);

    let mut flat_c = Vec::new();
    for snap in &result.snapshots_c {
        flat_c.extend_from_slice(snap);
    }
    out.insert("snapshots_c_flat".to_string(), flat_c);

    let mut flat_q = Vec::new();
    for snap in &result.snapshots_q {
        flat_q.extend_from_slice(snap);
    }
    out.insert("snapshots_q_flat".to_string(), flat_q);

    out.insert("nz".to_string(), vec![result.nz as f64]);
    out.insert("n_snapshots".to_string(), vec![result.snapshots_c.len() as f64]);
    Ok(out)
}

#[pyfunction]
pub fn py_solve_transport_2d(config: &Bound<'_, PyDict>) -> PyResult<String> {
    let get_f64 = |key: &str| -> PyResult<f64> {
        config
            .get_item(key)?
            .ok_or_else(|| pyo3::exceptions::PyKeyError::new_err(format!("missing: {}", key)))?
            .extract::<f64>()
    };
    let get_usize = |key: &str| -> PyResult<usize> {
        config
            .get_item(key)?
            .ok_or_else(|| pyo3::exceptions::PyKeyError::new_err(format!("missing: {}", key)))?
            .extract::<usize>()
    };

    let result = solver::solve_2d_coupled(
        get_usize("nr")?,
        get_usize("nz")?,
        get_f64("r_bed_m")?,
        get_f64("length_m")?,
        get_f64("u_mean_m_s")?,
        get_f64("porosity")?,
        get_f64("rho_s_kg_m3")?,
        get_f64("d_z_cs")?,
        get_f64("d_r_cs")?,
        get_f64("k_ldf_cs")?,
        get_f64("q_max_cs")?,
        get_f64("k_cs")?,
        get_f64("c_feed_cs")?,
        get_f64("d_z_sr")?,
        get_f64("d_r_sr")?,
        get_f64("k_ldf_sr")?,
        get_f64("q_max_sr")?,
        get_f64("k_sr")?,
        get_f64("c_feed_sr")?,
        get_f64("t_end_s")?,
        get_f64("initial_dt_s")?,
        get_f64("snapshot_interval_s")?,
    )
    .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    serde_json::to_string(&result)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
}
