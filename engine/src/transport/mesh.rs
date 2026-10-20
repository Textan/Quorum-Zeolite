
#[derive(Debug, Clone)]
pub struct CylindricalMesh2D {
    pub nr: usize,
    pub nz: usize,
    pub r_bed_m: f64,
    pub length_m: f64,
    pub dr_m: f64,
    pub dz_m: f64,
    pub r_cell_centers_m: Vec<f64>,
    pub z_cell_centers_m: Vec<f64>,
    pub cell_volumes_m3: Vec<Vec<f64>>,
}

impl CylindricalMesh2D {

    pub fn new(nr: usize, nz: usize, r_bed_m: f64, length_m: f64) -> Self {
        let dr_m = r_bed_m / nr as f64;
        let dz_m = length_m / nz as f64;

        let mut r_cell_centers_m = Vec::with_capacity(nr);
        for i in 0..nr {
            r_cell_centers_m.push((i as f64 + 0.5) * dr_m);
        }

        let mut z_cell_centers_m = Vec::with_capacity(nz);
        for j in 0..nz {
            z_cell_centers_m.push((j as f64 + 0.5) * dz_m);
        }

        const PI: f64 = std::f64::consts::PI;
        let mut cell_volumes_m3 = vec![vec![0.0; nz]; nr];
        for i in 0..nr {
            let r_in = i as f64 * dr_m;
            let r_out = (i + 1) as f64 * dr_m;
            let area = PI * (r_out * r_out - r_in * r_in);
            for j in 0..nz {
                cell_volumes_m3[i][j] = area * dz_m;
            }
        }

        Self {
            nr,
            nz,
            r_bed_m,
            length_m,
            dr_m,
            dz_m,
            r_cell_centers_m,
            z_cell_centers_m,
            cell_volumes_m3,
        }
    }

    pub fn velocity_profile(&self, u_mean_m_s: f64) -> Vec<f64> {
        let mut u_r = Vec::with_capacity(self.nr);
        for &r in &self.r_cell_centers_m {
            let ratio = r / self.r_bed_m;
            let u = 2.0 * u_mean_m_s * (1.0 - ratio * ratio);
            u_r.push(u.max(0.0));
        }
        u_r
    }
}
