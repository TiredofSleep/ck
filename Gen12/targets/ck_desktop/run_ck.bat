@echo off
REM ============================================================
REM  CK Coherence Machine -- R16 Desktop Launcher (Windows)
REM ============================================================
REM  CK runs WHOLE. Full GUI with all organs at 50Hz.
REM  He auto-starts studying when launched.
REM
REM  First time setup:
REM    pip install kivy numpy sounddevice requests beautifulsoup4 psutil
REM
REM  CK writes his notes to: %USERPROFILE%\.ck\writings\
REM  CK saves his state to:  %USERPROFILE%\.ck\
REM ============================================================

echo.
echo   ================================
echo   CK Coherence Machine -- R16
echo   ================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ first.
    pause
    exit /b 1
)

REM Install deps if needed
pip show kivy >nul 2>&1
if errorlevel 1 (
    echo [CK] Installing dependencies...
    pip install kivy numpy sounddevice requests beautifulsoup4 psutil
)

REM Suppress Kivy's verbose logging (only show warnings/errors)
set KCFG_KIVY_LOG_LEVEL=warning
set KIVY_NO_CONSOLELOG=1

echo [CK] Starting CK on the R16 (full body + GUI)...
echo [CK] CK will auto-study. Talk to him anytime.
echo [CK] Chat: type to talk to CK
echo [CK] Study: "study physics for 8 hours"
echo [CK] Self: "read your heartbeat"
echo [CK] Status: "how are you"
echo.

python -m ck_sim.ck_sim_app --study "harmony coherence physics mathematics" --hours 8

pause
