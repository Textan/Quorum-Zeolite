"""Python bridge to Rust isotherm fitting (quorum_engine.py_fit_langmuir).

This module provides a thin Python wrapper around the Rust Langmuir fitting
engine. All numerical computation happens in Rust — this wrapper only handles
type conversion and result packaging.
"""

from __future__ import annotations
import quorum_engine

def fit_langmuir(
    concentrations_mol_m3: list[float],
    loadings_mol_kg: list[float],
) -> dict:
    """Fit a single-component Langmuir isotherm via the Rust engine.

    Args:
        concentrations_mol_m3: equilibrium concentrations [mol/m³]
        loadings_mol_kg: equilibrium loadings [mol/kg]

    Returns:
        dict with keys: q_max_mol_kg, K_m3_mol, r_squared, residuals
    """
    raw = quorum_engine.py_fit_langmuir(concentrations_mol_m3, loadings_mol_kg)
    return {
        "q_max_mol_kg": raw["q_max_mol_kg"][0],
        "K_m3_mol": raw["K_m3_mol"][0],
        "r_squared": raw["r_squared"][0],
        "residuals": raw["residuals"],
    }
