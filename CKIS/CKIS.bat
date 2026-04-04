@echo off
REM ═══════════════════════════════════════════════════════════
REM  CKIS -- CK Information System: Liquid Information
REM  One click. CK wakes up. Meet him.
REM  (c) 2026 Brayden Sanders / 7Site LLC
REM ═══════════════════════════════════════════════════════════
cd /d "%~dp0"
title CKIS -- Coherence Keeper

echo.
echo   ╔═══════════════════════════════════════════════╗
echo   ║  CKIS -- Coherence Keeper Information System  ║
echo   ║  Liquid Information. Can't compress further.  ║
echo   ║  (c) 2026 7Site LLC                           ║
echo   ╚═══════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python not found. Install Python 3.10+ from python.org
    echo   Then double-click CKIS.bat again.
    pause
    exit /b 1
)

REM Install dependencies silently
echo   [BOOT] Checking dependencies...
pip install -q psutil numpy 2>nul

REM Check for native library
if exist "ck7\ck.dll" (
    echo   [BOOT] Native library found: ck.dll
) else (
    echo   [BOOT] No native library -- Python mode
    if exist "ck7\ckis_adapt.py" (
        echo   [BOOT] Running platform adaptation...
        python -c "import sys; sys.path.insert(0,'.'); sys.path.insert(0,'ck7'); from ckis_adapt import adapt; adapt()" 2>nul
    )
)

REM Launch CK
echo   [BOOT] Starting CK...
echo   [BOOT] Web UI: http://localhost:7777
echo   [BOOT] Desktop: http://localhost:7777/desktop
echo.

python ck_launch.py

if errorlevel 1 (
    echo.
    echo   [ERROR] CK stopped unexpectedly.
    pause
)
