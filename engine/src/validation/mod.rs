
use pyo3::prelude::*;
use std::collections::HashMap;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct CifValidationResult {
    pub is_valid: bool,
    pub errors: Vec<String>,
    pub warnings: Vec<String>,
    pub num_t_sites: usize,
    pub average_coordination: f64,
}

pub fn validate_cif_structure(cif_text: &str) -> CifValidationResult {
    let mut errors = Vec::new();
    let mut warnings = Vec::new();

    if cif_text.trim().is_empty() {
        errors.push("CIF content is completely empty".to_string());
        return CifValidationResult {
            is_valid: false,
            errors,
            warnings,
            num_t_sites: 0,
            average_coordination: 0.0,
        };
    }

    if !cif_text.contains("_atom_site_label") {
        errors.push("Missing required CIF tag: '_atom_site_label' (mandatory for MAZE-sim T-site enumeration)".to_string());
    }

    if !cif_text.contains("_cell_length_a") || !cif_text.contains("_cell_length_b") || !cif_text.contains("_cell_length_c") {
        errors.push("Missing required unit cell dimensions (_cell_length_a, _cell_length_b, _cell_length_c)".to_string());
    }

    for line in cif_text.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("_cell_length_") {
            let parts: Vec<&str> = trimmed.split_whitespace().collect();
            if parts.len() >= 2 {
                let clean_val = parts[1].split('(').next().unwrap_or("0");
                if let Ok(len) = clean_val.parse::<f64>() {
                    if len > 50.0 {
                        errors.push(format!("Unit cell dimension {} A exceeds 50 A limit; cluster would exceed 200 atoms", len));
                    }
                }
            }
        }
    }

    let mut t_site_count = 0;
    let mut oxygen_count = 0;
    let mut in_atom_loop = false;

    for line in cif_text.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("loop_") {
            in_atom_loop = false;
        } else if trimmed.starts_with("_atom_site_") {
            in_atom_loop = true;
        } else if in_atom_loop && !trimmed.is_empty() && !trimmed.starts_with('#') {
            let parts: Vec<&str> = trimmed.split_whitespace().collect();
            if !parts.is_empty() {
                let label = parts[0].to_uppercase();
                if label.starts_with("SI") || label.starts_with("AL") || label.starts_with('T') {
                    t_site_count += 1;
                } else if label.starts_with('O') {
                    oxygen_count += 1;
                }
            }
        }
    }

    if t_site_count == 0 && errors.is_empty() {
        warnings.push("No explicit Si/Al/T labels parsed in atom loop; framework symmetry will use standard IZA convention".to_string());
        t_site_count = 1;
    }

    let avg_coord = if t_site_count > 0 && oxygen_count > 0 {
        (2.0 * oxygen_count as f64) / t_site_count as f64
    } else {
        4.0
    };

    if avg_coord < 3.5 && oxygen_count > 0 {
        errors.push(format!("Implausible tetrahedral connectivity: average T-O coordination is {:.2} (< 4.0 minimum for zeolites)", avg_coord));
    }

    let is_valid = errors.is_empty();

    CifValidationResult {
        is_valid,
        errors,
        warnings,
        num_t_sites: t_site_count,
        average_coordination: avg_coord,
    }
}

#[pyfunction]
pub fn py_validate_cif(cif_content: &str) -> PyResult<HashMap<String, String>> {
    let res = validate_cif_structure(cif_content);
    let mut map = HashMap::new();
    map.insert("valid".to_string(), res.is_valid.to_string());
    map.insert("errors".to_string(), res.errors.join("; "));
    map.insert("warnings".to_string(), res.warnings.join("; "));
    map.insert("num_t_sites".to_string(), res.num_t_sites.to_string());
    map.insert("average_coordination".to_string(), format!("{:.2}", res.average_coordination));
    Ok(map)
}
