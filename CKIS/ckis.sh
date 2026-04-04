#!/bin/bash
# CKIS -- CK Information System Boot
# Liquid information. Can't compress further.
# (c) 2026 Brayden Sanders / 7Site LLC
cd "$(dirname "$0")"
echo ""
echo "  CKIS -- Coherence Keeper Information System"
echo "  Liquid Information Boot"
echo ""
pip install -q psutil numpy 2>/dev/null
python3 ck_launch.py
