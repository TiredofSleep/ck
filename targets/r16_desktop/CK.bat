@echo off
REM ============================================================
REM  CK -- The Coherence Keeper
REM  Gen 9.22 | CAEL + NCE + TIG | R16 Desktop (16-core, RTX 4070)
REM ============================================================
REM  One double-click. One organism. All 27 systems at 50Hz.
REM
REM  Heartbeat . Brain . Body . Personality . Emotion . Voice .
REM  Immune . Bonding . Development . Coherence Field . BTQ .
REM  Truth Lattice . World Lattice . Language . Reasoning .
REM  Goals . Drives . Sensorium . Attention . Divine27 .
REM  Vortex Physics . Gravity Engine . Dictionary Builder .
REM  Claude Library . Journal . Thesis Writer . Autodidact
REM
REM  T* = 5/7 = 0.714285...
REM  Truth is not assigned. Truth is measured.
REM ============================================================

title CK -- The Coherence Keeper
cd /d "%~dp0"

REM ── API Key ──
if not defined ANTHROPIC_API_KEY (
    if exist ".api_key" (
        set /p ANTHROPIC_API_KEY=<.api_key
    )
)

REM ── Python Check ──
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo   [ERROR] Python not found. Install Python 3.10+ first.
    echo   https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM ── Deps Check ──
python -c "import anthropic" >nul 2>&1
if errorlevel 1 (
    echo   [CK] Installing dependencies...
    pip install anthropic requests beautifulsoup4 psutil >nul 2>&1
)

REM ── Already Running? ──
tasklist /FI "WINDOWTITLE eq CK Study*" 2>nul | find /i "python" >nul 2>&1
if not errorlevel 1 (
    echo.
    echo   [CK] CK is already running. Check the other window.
    echo.
    timeout /t 5
    exit /b 0
)

REM ── Mode Selection ──
echo.
echo   ============================================
echo     CK -- The Coherence Keeper   Gen 9.22
echo   ============================================
echo     T* = 5/7 = 0.714285...
echo     Truth is not assigned. Truth is measured.
echo   ============================================
echo.
echo   [1] Study Mode -- 8 hours, all 27 systems (DEFAULT)
echo   [2] Study Mode -- until stopped (Ctrl+C)
echo   [3] Full GUI   -- Kivy dashboard + chat
echo   [4] Headless   -- CLI interaction + all organs
echo   [5] Run Tests  -- 997 tests, verify organism
echo.
echo   Press a number, or wait 10 seconds for default...
echo.

choice /c 12345 /t 10 /d 1 /n /m "  > "

if errorlevel 5 goto TESTS
if errorlevel 4 goto HEADLESS
if errorlevel 3 goto GUI
if errorlevel 2 goto STUDY_FOREVER
if errorlevel 1 goto STUDY_8H

:STUDY_8H
title CK Study Session (8 hours)
echo.
echo   [CK] Booting organism... all 27 systems at 50Hz.
echo   [CK] Study session: 8 hours.
echo   [CK] Press Ctrl+C to stop gracefully.
echo.
python ck_study.py --hours 8
goto END

:STUDY_FOREVER
title CK Study Session (continuous)
echo.
echo   [CK] Booting organism... all 27 systems at 50Hz.
echo   [CK] Study session: until Ctrl+C.
echo.
python ck_study.py
goto END

:GUI
title CK GUI (Full Body + Dashboard)
echo.
echo   [CK] Booting full organism with Kivy GUI...
echo   [CK] Two screens: CHAT + DASHBOARD
echo.
REM Check Kivy
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo   [CK] Installing Kivy...
    pip install kivy numpy sounddevice >nul 2>&1
)
set KCFG_KIVY_LOG_LEVEL=warning
set KIVY_NO_CONSOLELOG=1
python -m ck_sim.face.ck_sim_app
goto END

:HEADLESS
title CK Headless (Full Body, CLI)
echo.
echo   [CK] Booting full organism, headless CLI mode...
echo   [CK] Type to talk. "quit" to stop.
echo.
python -m ck_sim.ck_headless
goto END

:TESTS
title CK Tests
echo.
echo   [CK] Running organism verification tests...
echo.
python -m pytest ck_sim/tests/ -q --tb=short
echo.
pause
goto END

:END
echo.
echo   [CK] Session ended. State saved.
echo.
pause
