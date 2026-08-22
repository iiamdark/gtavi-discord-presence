#!/usr/bin/env bash

set -e

echo "========================================================"
echo "  Launching GTA VI Discord Rich Presence Simulator..."
echo "========================================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "[*] Checking dependencies..."
pip install -r requirements.txt --quiet --disable-pip-version-check

echo "[*] Starting Rich Presence..."
echo ""
python3 main.py
