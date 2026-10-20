use thiserror::Error;
use pyo3::exceptions::PyValueError;
use pyo3::PyErr;

#[derive(Error, Debug)]
pub enum QuorumError {
    #[error("CIF validation failed: {0}")]
    CifValidation(String),

    #[error("Isotherm fitting failed: {0}")]
    IsothermFit(String),

    #[error("Transport solver failed: {0}")]
    TransportSolver(String),

    #[error("Mass balance check failed: residual {residual:.2e} exceeds tolerance {tolerance:.2e} for ion {ion}")]
    MassBalanceExceeded {
        ion: String,
        residual: f64,
        tolerance: f64,
    },

    #[error("Material error: {0}")]
    Material(String),

    #[error("Recipe cache error: {0}")]
    RecipeCache(String),

    #[error("Numerical error: {0}")]
    Numerical(String),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

impl From<QuorumError> for PyErr {
    fn from(err: QuorumError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}
