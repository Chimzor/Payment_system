@echo off
REM One-click runner for Windows: sets up the environment and runs the pipeline.
cd /d "%~dp0"

if not exist ".venv" (
  echo Creating virtual environment...
  python -m venv .venv
)
call .venv\Scripts\activate.bat

echo Installing dependencies (first run only)...
pip install --quiet -r requirements.txt

echo Running the K-Means clustering pipeline...
python main.py

echo Done. Results are in the results/ folder.
pause
