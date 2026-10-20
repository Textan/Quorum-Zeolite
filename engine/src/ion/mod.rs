#[derive(Debug, Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct PitzerParams {
    pub beta_0: f64,
    pub beta_1: f64,
    pub beta_2: f64,
    pub c_phi: f64,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct Ion {
    pub symbol: &'static str,
    pub charge: i8,
    // [Shannon 1976, Acta Cryst A32:751] crystal ionic radius in pm
    pub ionic_radius_pm: f64,
    // [Marcus 1991, Chem Rev 91:750] standard molar enthalpy of hydration in kJ/mol
    pub hydration_enthalpy_kj_mol: f64,
    // [Li & Gregory 1974, Geochim Cosmochim Acta 38:703] tracer diffusion coefficient in water at 298.15 K in m^2/s
    pub diffusion_coeff_m2_s: f64,
    pub pitzer: PitzerParams,
    // [Marcus 1988, Chem Rev 88:1475; Persson 2010, Pure Appl Chem 82:1901] first coordination sphere hydration number
    pub coordination_number: u32,
}

// [Shannon 1976, Acta Cryst A32:751; Marcus 1991, Chem Rev 91:750; Li & Gregory 1974, Geochim Cosmochim Acta 38:703; Silvester & Pitzer 1977, J Phys Chem 81:1822; Marcus 1988, Chem Rev 88:1475]
pub static ION_CS_PLUS: Ion = Ion {
    symbol: "Cs+",
    charge: 1,
    ionic_radius_pm: 167.0,
    hydration_enthalpy_kj_mol: -264.0,
    diffusion_coeff_m2_s: 2.056e-9,
    // [Silvester & Pitzer 1977, J Phys Chem 81:1822] 25 °C parameters for CsCl
    pitzer: PitzerParams {
        beta_0: 0.0300,
        beta_1: 0.0558,
        beta_2: 0.0,
        c_phi: 0.00038,
    },
    coordination_number: 6,
};

// [Shannon 1976, Acta Cryst A32:751; Marcus 1991, Chem Rev 91:750; Li & Gregory 1974, Geochim Cosmochim Acta 38:703; Rard & Miller 1981, J Chem Eng Data 26:33; Persson 2010, Pure Appl Chem 82:1901]
pub static ION_SR2_PLUS: Ion = Ion {
    symbol: "Sr2+",
    charge: 2,
    ionic_radius_pm: 118.0,
    hydration_enthalpy_kj_mol: -1446.0,
    diffusion_coeff_m2_s: 0.794e-9,
    // [Rard & Miller 1981, J Chem Eng Data 26:33] 25 °C parameters for SrCl2
    pitzer: PitzerParams {
        beta_0: 0.2858,
        beta_1: 1.6670,
        beta_2: 0.0,
        c_phi: -0.00130,
    },
    coordination_number: 8,
};

// [Shannon 1976, Acta Cryst A32:751; Marcus 1991, Chem Rev 91:750; Li & Gregory 1974, Geochim Cosmochim Acta 38:703; Pitzer 1973, J Phys Chem 77:268; Marcus 1988, Chem Rev 88:1475]
pub static ION_NA_PLUS: Ion = Ion {
    symbol: "Na+",
    charge: 1,
    ionic_radius_pm: 102.0,
    hydration_enthalpy_kj_mol: -406.0,
    diffusion_coeff_m2_s: 1.334e-9,
    // [Pitzer 1973, J Phys Chem 77:268] 25 °C parameters for NaCl
    pitzer: PitzerParams {
        beta_0: 0.0765,
        beta_1: 0.2664,
        beta_2: 0.0,
        c_phi: 0.00127,
    },
    coordination_number: 6,
};
