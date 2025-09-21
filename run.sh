#!/bin/bash
# Simple script to run the Inference Server

set -euo pipefail

# Always run from the repo root (directory of this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Starting Inference Server..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

# Ensure uv is available (and in PATH) for env and install management
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
if ! command -v uv >/dev/null 2>&1; then
	echo "uv not found. Installing uv..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
	# Add freshly installed uv to PATH for the current shell
	export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

# Create or activate the virtual environment using uv
if [[ -d ".venv" && -f ".venv/bin/activate" ]]; then
	echo "Activating existing virtual environment (.venv)"
else
	echo "Creating new virtual environment with uv at .venv"
	uv venv
fi

# Activate the environment
source .venv/bin/activate

# Install dependencies into the active environment
if [[ -f "requirements.txt" ]]; then
	echo "Installing dependencies from requirements.txt (via uv pip)"
	uv pip install -r requirements.txt
else
	echo "No requirements.txt found; skipping dependency install"
fi

# Launch the server as before
python3 app.py