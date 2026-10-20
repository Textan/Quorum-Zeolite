"""MAZE-sim wrapper for zeolite cluster extraction and T-site enumeration.

Milestone 1: stub returning a single T-site cluster.
Milestone 2: full MAZE-sim PerfectZeolite.build_from_cif_with_labels integration
for crystallographically distinct site enumeration with symmetry-derived degeneracies.
"""

from __future__ import annotations
from backend.material.protocol import ExchangeSite

def enumerate_tsites(iza_code: str, cif_path: str | None = None) -> list[ExchangeSite]:
    """Enumerate all crystallographically distinct T-sites in a zeolite framework.

    Milestone 1: returns a single representative T-site.
    Milestone 2: uses MAZE-sim symmetry analysis for all distinct T-sites.
    """
    return [
        ExchangeSite(
            label="T1",
            fractional_coords=(0.25, 0.25, 0.25),
            degeneracy=4,
        )
    ]
