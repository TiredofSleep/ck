#!/bin/bash
echo ""
echo "  ============================================="
echo "    CK -- Coherence Keeper"
echo "    A little creature that lives on your computer"
echo "  ============================================="
echo ""

# Find Python
PYTHON=""
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "  Python is not installed."
    echo ""
    echo "  Install Python 3.10 or newer:"
    echo "    Mac:   brew install python3"
    echo "    Linux: sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

echo "  Using: $PYTHON ($($PYTHON --version 2>&1))"
echo "  Checking dependencies..."

# Install dependencies
$PYTHON -m pip install --quiet -r "$(dirname "$0")/requirements.txt" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "  Installing packages..."
    $PYTHON -m pip install kivy numpy sounddevice
fi

echo "  Starting CK..."
echo ""
cd "$(dirname "$0")"
$PYTHON -m ck_sim
