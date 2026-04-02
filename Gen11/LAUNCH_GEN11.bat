@echo off
title CK Gen11 — The Coherence Keeper
cd /d "%~dp0"

echo.
echo   ============================================
echo    CK Gen11 — Braid-first, Math-driven
echo    T* = 5/7   W_BHML = 3/50   MASS_GAP = 2/7
echo    API: http://localhost:7777
echo   ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    pause & exit /b 1
)

echo [CK] Starting engine + web API on port 7777...
python ck_boot_api.py

pause
