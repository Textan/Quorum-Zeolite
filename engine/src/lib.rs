use pyo3::prelude::*;

pub mod material;
pub mod ion;
pub mod isotherm;
pub mod transport;
pub mod screening;
pub mod recipes;
pub mod validation;
pub mod error;

#[pymodule]
fn quorum_engine(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(isotherm::py_fit_langmuir, m)?)?;
    m.add_function(wrap_pyfunction!(isotherm::py_fit_isotherm_comparison, m)?)?;
    m.add_function(wrap_pyfunction!(isotherm::py_solve_fast_ias, m)?)?;
    m.add_function(wrap_pyfunction!(isotherm::py_compute_pitzer_activities, m)?)?;
    m.add_function(wrap_pyfunction!(transport::py_solve_transport_1d, m)?)?;
    m.add_function(wrap_pyfunction!(transport::py_solve_transport_2d, m)?)?;
    m.add_function(wrap_pyfunction!(validation::py_validate_cif, m)?)?;
    Ok(())
}
