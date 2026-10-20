mod zeolite;

pub use zeolite::ZeoliteMaterial;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PoreGeometry {
    Channel1D,
    Channel2D,
    Cage3D,
}

#[derive(Debug, Clone)]
pub struct ExchangeSite {
    pub label: String,
    pub fractional_coords: [f64; 3],
    pub degeneracy: u32,
}

pub trait Material: Send + Sync {
    fn name(&self) -> &str;
    fn iza_code(&self) -> Option<&str>;
    fn pore_geometry(&self) -> PoreGeometry;
    fn framework_density_kg_m3(&self) -> f64;
    fn particle_radius_m(&self) -> f64;
    fn exchange_capacity_mol_kg(&self) -> f64;
}
