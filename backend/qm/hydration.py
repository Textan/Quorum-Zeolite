"""Explicit water shell placement for ion hydration in QM calculations.

N_water per ion:
  Cs+ -> 6 (Marcus 1988, Chem Rev 88:1475)
  Sr2+ -> 8 (Persson 2010, Pure Appl Chem 82:1901)

Distances from ion to water oxygen:
  Cs-O: 3.15 A (Ohtaki & Radnai 1993, Chem Rev 93:1157)
  Sr-O: 2.64 A (Persson 2010, Pure Appl Chem 82:1901)
"""

from __future__ import annotations
import math
import numpy as np

COORDINATION_NUMBERS: dict[str, int] = {
    "Cs+": 6,
    "Sr2+": 8,
}

ION_WATER_DISTANCES_ANGSTROM: dict[str, float] = {
    "Cs+": 3.15,
    "Sr2+": 2.64,
}

def generate_fibonacci_sphere_points(n_points: int, radius: float) -> list[tuple[float, float, float]]:
    """Uniformly distribute N points on a sphere using the Fibonacci spiral."""
    points = []
    phi = math.pi * (3.0 - math.sqrt(5.0))

    for i in range(n_points):
        y = 1.0 - (i / float(n_points - 1)) * 2.0 if n_points > 1 else 0.0
        r_at_y = math.sqrt(max(0.0, 1.0 - y * y))
        theta = phi * i

        x = math.cos(theta) * r_at_y
        z = math.sin(theta) * r_at_y
        points.append((x * radius, y * radius, z * radius))

    return points

def add_hydration_shell(cluster_atoms, ion_center: tuple[float, float, float], ion_symbol: str):
    """Add explicit first-coordination-sphere water molecules around the ion."""
    try:
        from ase import Atoms
    except ImportError:
        raise ImportError("ASE is required for hydration shell construction")

    n_water = COORDINATION_NUMBERS.get(ion_symbol, 6)
    r_mo = ION_WATER_DISTANCES_ANGSTROM.get(ion_symbol, 3.0)
    o_positions = generate_fibonacci_sphere_points(n_water, r_mo)

    water_symbols = []
    water_positions = []

    r_oh = 0.9572
    half_angle_rad = math.radians(104.52 / 2.0)

    for ox, oy, oz in o_positions:
        abs_ox = ion_center[0] + ox
        abs_oy = ion_center[1] + oy
        abs_oz = ion_center[2] + oz

        water_symbols.append("O")
        water_positions.append((abs_ox, abs_oy, abs_oz))

        norm = math.sqrt(ox * ox + oy * oy + oz * oz)
        ux, uy, uz = ox / norm, oy / norm, oz / norm

        h1 = (
            abs_ox + ux * r_oh * math.cos(half_angle_rad) + 0.2 * math.sin(half_angle_rad),
            abs_oy + uy * r_oh * math.cos(half_angle_rad),
            abs_oz + uz * r_oh * math.cos(half_angle_rad),
        )
        h2 = (
            abs_ox + ux * r_oh * math.cos(half_angle_rad) - 0.2 * math.sin(half_angle_rad),
            abs_oy + uy * r_oh * math.cos(half_angle_rad),
            abs_oz + uz * r_oh * math.cos(half_angle_rad),
        )

        water_symbols.extend(["H", "H"])
        water_positions.extend([h1, h2])

    water_atoms = Atoms(symbols=water_symbols, positions=water_positions)
    return cluster_atoms + water_atoms
