@echo off
setlocal
cd /d "%~dp0"
title Quorum-Zeolite Engine

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=python"
) else if exist ".\.venv\Scripts\python.exe" (
    set "PY_CMD=.\.venv\Scripts\python.exe"
) else (
    echo [ERROR] Python not found on PATH or in .venv.
    pause
    exit /b 1
)

echo ========================================================
echo Starting Quorum-Zeolite Local Server...
echo Web UI: http://127.0.0.1:8000/submit
echo ========================================================

start "" http://127.0.0.1:8000/submit
%PY_CMD% -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
pause
