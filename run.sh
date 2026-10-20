#!/usr/bin/env bash
set -e

if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
elif [ -f "./.venv/bin/python" ]; then
    PY_CMD="./.venv/bin/python"
else
    echo "[ERROR] Python not found."
    exit 1
fi

echo "========================================================"
echo "Starting Quorum-Zeolite Local Server..."
echo "Web UI: http://127.0.0.1:8000/submit"
echo "========================================================"

$PY_CMD -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
