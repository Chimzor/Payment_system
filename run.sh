#!/bin/bash
# One-click runner: sets up the environment and runs the full pipeline.
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi
source .venv/bin/activate

echo "Installing dependencies (first run only)..."
pip install --quiet -r requirements.txt

echo "Running the K-Means clustering pipeline..."
python main.py

echo "Done. Results are in the results/ folder."
