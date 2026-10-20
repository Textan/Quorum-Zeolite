"""Python bridge to Rust CIF validation (quorum_engine.py_validate_cif)."""

from __future__ import annotations
import quorum_engine

def validate_cif(cif_content: str) -> dict:
    """Validate CIF file content via the Rust engine.

    Returns dict with: valid (bool), errors (str).
    """
    raw = quorum_engine.py_validate_cif(cif_content)
    return {
        "valid": raw["valid"] == "true",
        "errors": raw["errors"] if raw["errors"] else None,
    }
