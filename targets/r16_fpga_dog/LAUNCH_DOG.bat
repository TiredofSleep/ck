@echo off
REM ================================================================
REM LAUNCH_DOG.bat -- CK Dog Long-Leash Launcher
REM R16 + Zynq-7020 FPGA + XiaoR GEEK Quadruped
REM ================================================================
REM Operator: PROGRESS (3) -- let's walk.
REM
REM Usage:
REM   LAUNCH_DOG.bat              (uses COM3 default)
REM   LAUNCH_DOG.bat COM5         (specify FPGA port)
REM   LAUNCH_DOG.bat COM3 COM5    (FPGA port, servo port)
REM
REM What this launches:
REM   1. CK admin engine on port 7777 (if not already running)
REM   2. Dog bridge thread (R16 <-> FPGA UART)
REM   3. Status check every 10s
REM
REM Prerequisites:
REM   - ck_full.bit programmed to Zybo Z7-20
REM   - USB cable: R16 -> Zybo PROG/UART
REM   - Run ck_leash_test.py first to verify
REM ================================================================

setlocal

set FPGA_PORT=%1
if "%FPGA_PORT%"=="" set FPGA_PORT=COM3

set SERVO_PORT=%2

set ROOT=C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED
set GEN10=%ROOT%\Gen10
set DOG_TARGET=%GEN10%\targets\r16_fpga_dog
set PYTHON=python

echo.
echo [DOG] ==========================================
echo [DOG]  CK Dog Launcher -- Long-Leash Mode
echo [DOG]  FPGA port:  %FPGA_PORT%
if not "%SERVO_PORT%"=="" echo [DOG]  Servo port: %SERVO_PORT%
echo [DOG] ==========================================
echo.

REM ── Check FPGA port exists ──────────────────────────────────────
echo [DOG] Checking FPGA port %FPGA_PORT%...
mode %FPGA_PORT% >nul 2>&1
if errorlevel 1 (
    echo [DOG] ERROR: Port %FPGA_PORT% not found.
    echo [DOG] Check Device Manager for the correct COM port.
    echo [DOG] Plug in the Zybo Z7-20 USB cable first.
    pause
    exit /b 1
)
echo [DOG] Port %FPGA_PORT% found.
echo.

REM ── Run leash test ───────────────────────────────────────────────
echo [DOG] Running leash test...
cd /d "%DOG_TARGET%"
%PYTHON% ck_leash_test.py %FPGA_PORT%
if errorlevel 1 (
    echo.
    echo [DOG] Leash test FAILED. Fix issues above before continuing.
    echo [DOG] Do NOT attach XiaoR servos until leash test passes.
    pause
    exit /b 1
)
echo.

REM ── Check if CK engine is already running ────────────────────────
echo [DOG] Checking CK engine (port 7777)...
curl -s http://localhost:7777/health >nul 2>&1
if errorlevel 1 (
    echo [DOG] CK engine not running. Starting admin cell...
    cd /d "%GEN10%"
    start "CK Engine 7777" cmd /k "python ck_cell.py --port 7777 --type default"
    echo [DOG] Waiting 8s for engine to boot...
    timeout /t 8 /nobreak >nul
) else (
    echo [DOG] CK engine already running on port 7777.
)
echo.

REM ── Launch dog bridge ────────────────────────────────────────────
echo [DOG] Starting dog bridge on %FPGA_PORT%...
cd /d "%DOG_TARGET%"
start "CK Dog Bridge" cmd /k "%PYTHON% ck_dog_bridge.py %FPGA_PORT% --verbose"

echo.
echo [DOG] ==========================================
echo [DOG]  Dog bridge running.
echo [DOG]
echo [DOG]  Monitor:
echo [DOG]    curl http://localhost:7777/corridor
echo [DOG]    curl http://localhost:7777/state
echo [DOG]
if not "%SERVO_PORT%"=="" (
    echo [DOG]  Servo positions:
    echo [DOG]    python ck_xiaor_servo.py %SERVO_PORT% read
    echo [DOG]
)
echo [DOG]  To stop: close the bridge window
echo [DOG]  Emergency: close bridge window (sends ESTOP on exit)
echo [DOG] ==========================================
echo.

endlocal
