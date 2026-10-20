#!/usr/bin/env bash
set -e
echo "=== Quorum-Zeolite Environment Check ==="
python --version || { echo "FAIL: python not found"; exit 1; }
python -c "import quorum_engine; print('quorum_engine version:', quorum_engine.__version__)" \
    || { echo "FAIL: quorum_engine import failed"; exit 1; }
python -c "import fastapi; print('fastapi version:', fastapi.__version__)" || { echo "FAIL: fastapi import failed"; exit 1; }
python -c "import uvicorn; print('uvicorn version:', uvicorn.__version__)" || { echo "FAIL: uvicorn import failed"; exit 1; }
python -c "import numpy; print('numpy version:', numpy.__version__)" || { echo "FAIL: numpy import failed"; exit 1; }
python -c "import scipy; print('scipy version:', scipy.__version__)" || { echo "FAIL: scipy import failed"; exit 1; }
python -c "import ase; print('ase version:', ase.__version__)" || { echo "FAIL: ase import failed"; exit 1; }
python -c "from backend.bridge import isotherm, transport, validation; print('Bridge imports: OK')" || { echo "FAIL: backend bridge imports failed"; exit 1; }
echo "=== All checks PASSED ==="
