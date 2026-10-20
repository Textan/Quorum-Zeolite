@echo off
cd /d "%~dp0"
echo Starting Quorum-Zeolite from %CD%...
.\.venv\Scripts\python.exe -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
pause
