
use crate::error::QuorumError;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct MassBalanceReport {
    pub ion_symbol: String,
    pub mass_in_mol: f64,
    pub mass_out_mol: f64,
    pub mass_adsorbed_bed_mol: f64,
    pub mass_fluid_bed_mol: f64,
    pub mass_balance_residual: f64,
    pub is_converged: bool,
    pub tolerance: f64,
}

impl MassBalanceReport {
    pub const TOLERANCE: f64 = 1e-4;

    pub fn compute(
        ion_symbol: &str,
        mass_in_mol: f64,
        mass_out_mol: f64,
        mass_adsorbed_bed_mol: f64,
        mass_fluid_bed_mol: f64,
    ) -> Result<Self, QuorumError> {
        let total_retained = mass_adsorbed_bed_mol + mass_fluid_bed_mol;
        let residual = if mass_in_mol > 1e-15 {
            (mass_in_mol - mass_out_mol - total_retained).abs() / mass_in_mol
        } else {
            0.0
        };

        let is_converged = residual <= Self::TOLERANCE;

        Ok(Self {
            ion_symbol: ion_symbol.to_string(),
            mass_in_mol,
            mass_out_mol,
            mass_adsorbed_bed_mol,
            mass_fluid_bed_mol,
            mass_balance_residual: residual,
            is_converged,
            tolerance: Self::TOLERANCE,
        })
    }
}
