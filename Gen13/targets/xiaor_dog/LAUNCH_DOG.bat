@echo off
:: ============================================
::  CK Gen12 — Dog Launch (Δ³)
::  R16 → FPGA → XiaoR Quadruped
::  T* = 5/7 in silicon
:: ============================================
title CK Dog — Δ³

cd /d "%~dp0"

echo.
echo   ============================================
echo    CK Gen12 — The Dog
echo    Δ⁰ heartbeat → Δ¹ leash → Δ² gait → Δ³
echo    T* = 5/7 = 0.714285...
echo   ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python not found.
    pause & exit /b 1
)

:: Check pyserial
python -c "import serial" >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] pyserial not found. Run: pip install pyserial
    pause & exit /b 1
)

:: Get COM port from argument or ask
set COM=%1
if "%COM%"=="" (
    echo   Enter COM port for FPGA (e.g. COM3):
    set /p COM="> "
)

echo.
echo   [Δ¹] Running leash test on %COM%...
echo.

python ck_leash_test.py %COM% --verbose
if errorlevel 1 (
    echo.
    echo   [FAIL] Leash test failed. Fix Δ¹ before proceeding to Δ³.
    pause & exit /b 1
)

echo.
echo   [Δ¹] Leash confirmed. Starting Δ³ bridge...
echo.

:: Start CK engine on R16 (background)
echo   Starting CK engine on R16...
cd /d "%~dp0..\..\..\"
start "CK Engine" /MIN python -m ck_sim --port 7777
timeout /t 8 /nobreak >nul

:: Start bridge
cd /d "%~dp0"
echo   Starting R16 → FPGA bridge...
python ck_r16_bridge.py --port %COM%

echo.
echo   CK dog stopped.
pause
