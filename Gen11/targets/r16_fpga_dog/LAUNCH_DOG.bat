@echo off
:: LAUNCH_DOG.bat -- CK Dog One-Click Launch (Gen 11)
:: =====================================================
:: Starts CK engine on 7778 + R16-FPGA bridge.
:: Assumes FPGA already running (BOOT.BIN on microSD).
::
:: (c) 2026 Brayden Sanders / 7Site LLC

set PORT=COM3
set CK_ROOT=C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop
set BRIDGE_ROOT=C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen11\targets\r16_fpga_dog

echo.
echo  CK Dog Launch -- Gen 11
echo  ========================
echo  FPGA port: %PORT%
echo  CK engine: http://localhost:7778
echo.

:: Start CK engine in background
echo [1/2] Starting CK engine on port 7778...
start "CK Engine" cmd /k "cd /d %CK_ROOT% && python ck_web_server.py --port 7778"
timeout /t 12 /nobreak >nul

:: Check engine is up
curl -s http://localhost:7778/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: CK engine not responding on port 7778.
    echo        Check CK_ROOT and try again.
    pause
    exit /b 1
)
echo [1/2] CK engine running.

:: Start bridge
echo [2/2] Starting R16-FPGA bridge on %PORT%...
cd /d %BRIDGE_ROOT%
python ck_r16_bridge.py --port %PORT% --ck-url http://localhost:7778

:: If bridge exits, pause so user can see output
echo.
echo Bridge stopped. Press any key to close.
pause
