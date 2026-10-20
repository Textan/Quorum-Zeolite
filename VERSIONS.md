# Quorum-Zeolite Dependency Pins & Provenance

All dependencies are strictly pinned to exact versions to ensure physical reproducibility and build integrity. No range or caret (`^`, `~`) specifiers are permitted on load-bearing components. Any change to these pins must be documented in `STATUS.md` with a justified technical rationale.

## Rust Crates (`engine/Cargo.toml`)
- `pyo3` = "=0.23.5"
- `pyo3-build-config` = "=0.23.5"
- `ndarray` = "=0.16.1"
- `rayon` = "=1.10.0"
- `serde` = "=1.0.219"
- `serde_json` = "=1.0.140"
- `thiserror` = "=2.0.12"
- `levenberg-marquardt` = "=0.14.0"
- `sled` = "=0.34.7"

## Python Environment (`backend/requirements.txt`)
- `python` = "3.11.9"
- `ase` = "3.23.0"
- `tblite` = "0.3.0"
- `tblite-python` = "0.3.0"
- `maze-sim` = "commit:a9f3b8c" # Pinned commit from github.com/ma-group/maze-sim
- `fastapi` = "0.115.6"
- `uvicorn` = "0.34.0"
- `pydantic` = "2.10.4"
- `psycopg2-binary` = "2.9.10"
- `numpy` = "1.26.4"
- `scipy` = "1.14.1"
- `maturin` = "1.8.2"

## Frontend & Node.js (`frontend/package.json`)
- `node` = "20.18.0"
- `next` = "14.2.23"
- `react` = "18.3.1"
- `react-dom` = "18.3.1"
- `three` = "0.172.0"
- `@types/three` = "0.172.0"
- `lucide-react` = "0.469.0"
- `typescript` = "5.7.3"
