"""Material Protocol — the extensibility contract for Quorum-Zeolite (Python side).

Adding a new material type (MOF, mesoporous silica, clay mineral, AI-generated
structure) requires ONLY implementing this protocol — zero changes to QM runner,
bridge, worker, or API code.
"""

from __future__ import annotations
from typing import Protocol, runtime_checkable
from dataclasses import dataclass

@dataclass
class ExchangeSite:
    """A crystallographic exchange site within a material framework."""
    label: str
    fractional_coords: tuple[float, float, float]
    degeneracy: int

@dataclass
class Ion:
    """Ion species with physical parameters for QM calculations."""
    symbol: str
    charge: int
    ionic_radius_pm: float
    coordination_number: int

@runtime_checkable
class Material(Protocol):
    """Material protocol — every material type MUST implement this.

    The QM layer, bridge, and worker operate exclusively through this protocol.
    They never know the concrete material type.
    """

    def name(self) -> str:
        """Human-readable name of the material."""
        ...

    def build_cluster(self, site: ExchangeSite, ion: Ion, n_water: int):
        """Build an atomic cluster for QM calculation at the given site.

        Returns an ASE Atoms object: framework cluster + ion + explicit water molecules.
        Cut bonds are H-capped.
        """
        ...

    def enumerate_sites(self) -> list[ExchangeSite]:
        """Enumerate all crystallographically distinct exchange sites."""
        ...

    def site_degeneracy(self, site: ExchangeSite) -> int:
        """Return the crystallographic degeneracy (multiplicity) of the given site."""
        ...
