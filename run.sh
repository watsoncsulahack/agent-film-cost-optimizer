#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ ! -d ".venv" ]; then
    echo "Setting up virtual environment..."
    if command -v uv >/dev/null 2>&1; then
        uv venv .venv
        uv pip install --python .venv -r requirements.txt
    else
        python3 -m venv .venv
        .venv/bin/pip install --upgrade pip
        .venv/bin/pip install -r requirements.txt
    fi
fi

source .venv/bin/activate
echo "Starting Cost Optimizer Agent on http://localhost:8000..."
python web_app.py
