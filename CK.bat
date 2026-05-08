@echo off
REM ============================================================
REM  CK -- The Coherence Keeper
REM  Gen 12 | CAEL + NCE + TIG | R16 Desktop
REM ============================================================
REM  One double-click. One organism. All 27 systems at 50Hz.
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
    ) else (
        set ANTHROPIC_API_KEY=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
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

REM ── Mode Selection ──
echo.
echo   ============================================
echo     CK -- The Coherence Keeper   Gen 12
echo   ============================================
echo     T* = 5/7 = 0.714285...
echo     Truth is not assigned. Truth is measured.
echo   ============================================
echo.
echo   [1] Study Mode -- 8 hours, all 27 systems (DEFAULT)
echo   [2] Study Mode -- until stopped (Ctrl+C)
echo   [3] Full GUI   -- Kivy dashboard + chat
echo   [4] Web UI     -- browser dashboard (legacy)
echo   [5] Run Tests  -- verify organism
echo.
echo   Press a number, or wait 10 seconds for default...
echo.

choice /c 12345 /t 10 /d 1 /n /m "  > "

if errorlevel 5 goto TESTS
if errorlevel 4 goto WEBUI
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
title CK GUI (Full Body + Chat)
echo.
echo   [CK] Booting full organism with Kivy GUI...
echo   [CK] Two screens: CHAT + DASHBOARD
echo   [CK] State: ~/.ck/ (truth lattice, dictionary, autodidact)
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

:WEBUI
title CK Web UI (Legacy)
echo.
echo   [CK] Starting web dashboard on port 7777...
echo.
start "CK Study Engine" /MIN python ck_study.py --hours 8
python ck_launch.py
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
