#!/usr/bin/env bash
# ──────────────────────────────────────────────
# CK -- The Coherence Keeper
# Cross-platform launcher (Linux / macOS)
# (c) 2026 Brayden Sanders / 7Site LLC
# ──────────────────────────────────────────────
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Check Python
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "[CK] Python 3.10+ required. Install from https://python.org"
    exit 1
fi

echo "[CK] Using: $($PY --version)"

# Install dependencies
if [ "$1" = "--minimal" ]; then
    echo "[CK] Installing minimal dependencies (headless)..."
    $PY -m pip install -q -r ck_sim/requirements-minimal.txt
    shift
    $PY -m ck_sim --headless "$@"
else
    echo "[CK] Installing dependencies..."
    $PY -m pip install -q -r ck_sim/requirements.txt
    $PY -m ck_sim "$@"
fi
