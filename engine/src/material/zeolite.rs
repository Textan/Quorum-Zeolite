use super::{Material, PoreGeometry};

pub struct ZeoliteMaterial {
    pub name: String,
    pub iza_code: String,
    pub pore_geometry: PoreGeometry,
    pub framework_density_kg_m3: f64,
    pub particle_radius_m: f64,
    pub exchange_capacity_mol_kg: f64,
}

impl ZeoliteMaterial {

    pub fn clinoptilolite() -> Self {
        ZeoliteMaterial {
            name: "Clinoptilolite".to_string(),
            iza_code: "HEU".to_string(),
            pore_geometry: PoreGeometry::Channel2D,

            framework_density_kg_m3: 2150.0,
            particle_radius_m: 0.5e-3,

            exchange_capacity_mol_kg: 2.15,
        }
    }

    pub fn chabazite() -> Self {
        ZeoliteMaterial {
            name: "Chabazite".to_string(),
            iza_code: "CHA".to_string(),
            pore_geometry: PoreGeometry::Cage3D,

            framework_density_kg_m3: 1940.0,
            particle_radius_m: 0.5e-3,

            exchange_capacity_mol_kg: 2.50,
        }
    }

    pub fn faujasite() -> Self {
        ZeoliteMaterial {
            name: "Faujasite".to_string(),
            iza_code: "FAU".to_string(),
            pore_geometry: PoreGeometry::Cage3D,

            framework_density_kg_m3: 1380.0,
            particle_radius_m: 0.5e-3,

            exchange_capacity_mol_kg: 3.40,
        }
    }

    pub fn zsm5() -> Self {
        ZeoliteMaterial {
            name: "ZSM-5".to_string(),
            iza_code: "MFI".to_string(),
            pore_geometry: PoreGeometry::Channel1D,

            framework_density_kg_m3: 1800.0,
            particle_radius_m: 0.5e-3,

            exchange_capacity_mol_kg: 0.80,
        }
    }

    pub fn from_iza_code(code: &str) -> Option<Self> {
        match code {
            "HEU" => Some(Self::clinoptilolite()),
            "CHA" => Some(Self::chabazite()),
            "FAU" => Some(Self::faujasite()),
            "MFI" => Some(Self::zsm5()),
            _ => None,
        }
    }
}

impl Material for ZeoliteMaterial {
    fn name(&self) -> &str {
        &self.name
    }
    fn iza_code(&self) -> Option<&str> {
        Some(&self.iza_code)
    }
    fn pore_geometry(&self) -> PoreGeometry {
        self.pore_geometry
    }
    fn framework_density_kg_m3(&self) -> f64 {
        self.framework_density_kg_m3
    }
    fn particle_radius_m(&self) -> f64 {
        self.particle_radius_m
    }
    fn exchange_capacity_mol_kg(&self) -> f64 {
        self.exchange_capacity_mol_kg
    }
}
