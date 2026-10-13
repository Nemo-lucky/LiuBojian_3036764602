@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" code/local_app.py
) else (
  python code/local_app.py
)
pause
