#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with Python 3.11..."
    uv venv .venv --python 3.11
    uv pip install --python .venv -r requirements.txt fastapi uvicorn pytest
fi

source .venv/bin/activate
echo "Starting AI Film Cost Optimizer Web App on Python $(python --version)..."
python web_app.py
