"""Ion physical parameters — Python-side reference for QM calculations.

All values cited to published sources. These mirror the Rust Ion struct
(engine/src/ion/mod.rs) for use in Python-side QM cluster building.
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class IonData:
    """Physical parameters for an ion species."""
    symbol: str
    charge: int
    ionic_radius_pm: float
    hydration_enthalpy_kj_mol: float
    diffusion_coeff_m2_s: float
    coordination_number: int

CS_PLUS = IonData(
    symbol="Cs+",
    charge=1,
    ionic_radius_pm=167.0,
    hydration_enthalpy_kj_mol=-264.0,
    diffusion_coeff_m2_s=2.056e-9,
    coordination_number=6,
)

SR2_PLUS = IonData(
    symbol="Sr2+",
    charge=2,
    ionic_radius_pm=118.0,
    hydration_enthalpy_kj_mol=-1446.0,
    diffusion_coeff_m2_s=0.794e-9,
    coordination_number=8,
)

IONS: dict[str, IonData] = {
    "Cs+": CS_PLUS,
    "Sr2+": SR2_PLUS,
}
