"""ZeoliteMaterial — concrete Material implementation (Python side).

Owns QM cluster building via MAZE-sim. The Rust ZeoliteMaterial handles
structural parameters; this Python counterpart handles the atomic-level
cluster construction that feeds into tblite/ASE QM calculations.
"""

from __future__ import annotations
from .protocol import Material, ExchangeSite, Ion

class ZeoliteMaterial:
    """Zeolite framework material for ion-exchange QM calculations.

    For Milestone 1: single T-site stub. Full MAZE-sim enumeration in Milestone 2.
    """

    def __init__(self, name: str, iza_code: str, cif_path: str | None = None):
        self._name = name
        self._iza_code = iza_code
        self._cif_path = cif_path

    def name(self) -> str:
        return self._name

    def enumerate_sites(self) -> list[ExchangeSite]:
        """Enumerate T-sites from the framework.

        Milestone 1: returns a single representative T-site for the thin slice.
        Milestone 2: uses MAZE-sim PerfectZeolite.build_from_cif_with_labels
        for full symmetry-distinct site enumeration.
        """
        return [
            ExchangeSite(
                label="T1",
                fractional_coords=(0.25, 0.25, 0.25),
                degeneracy=4,
            )
        ]

    def site_degeneracy(self, site: ExchangeSite) -> int:
        return site.degeneracy

    def build_cluster(self, site: ExchangeSite, ion: Ion, n_water: int):
        """Build atomic cluster for QM calculation.

        Milestone 1: builds a minimal Si-O tetrahedron cluster with the ion.
        Milestone 2: uses MAZE-sim for realistic cluster extraction with H-capping.
        """
        positions = [
            (0.0, 0.0, 0.0),
            (1.61, 0.0, 0.0),
            (-1.61, 0.0, 0.0),
            (0.0, 1.61, 0.0),
            (0.0, -1.61, 0.0),
        ]
        symbols = ["Si", "O", "O", "O", "O"]

        ion_pos = (0.0, 0.0, 3.0)
        if ion.symbol == "Cs+":
            symbols.append("Cs")
        elif ion.symbol == "Sr2+":
            symbols.append("Sr")
        else:
            symbols.append(ion.symbol.rstrip("+").rstrip("2"))
        positions.append(ion_pos)

        try:
            from ase import Atoms
            return Atoms(symbols=symbols, positions=positions)
        except ImportError:
            class MockAtoms:
                def __init__(self, symbols, positions):
                    self.symbols = symbols
                    self.positions = positions
            return MockAtoms(symbols=symbols, positions=positions)
