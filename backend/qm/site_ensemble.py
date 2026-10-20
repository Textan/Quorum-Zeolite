"""Degeneracy-weighted ensemble average of ΔG_exchange across all T-sites.

ΔG_bind_avg = Σ(g_i × ΔG_bind_i) / Σ(g_i)
where g_i is the crystallographic degeneracy of site i.

Milestone 1: trivial (single site).
Milestone 2: full multi-site ensemble with all T-sites from MAZE-sim.
"""

from __future__ import annotations
from backend.qm.xtb_runner import QMResult

def ensemble_average(results: list[tuple[int, QMResult]]) -> float:
    """Compute degeneracy-weighted average binding energy.

    Args:
        results: list of (degeneracy, QMResult) tuples

    Returns:
        Weighted average binding energy in eV
    """
    total_weight = sum(deg for deg, _ in results)
    if total_weight == 0:
        raise ValueError("Total degeneracy is zero — no valid sites")

    weighted_sum = sum(deg * r.binding_energy_ev for deg, r in results)
    return weighted_sum / total_weight
