@echo off
REM ============================================================
REM  CK Coherence Machine -- R16 HEADLESS (Full Body, No GUI)
REM ============================================================
REM  CK runs WHOLE. All organs ticking at 50Hz:
REM    Heartbeat, Brain, Body, Personality, Emotion, Voice,
REM    Immune, Bonding, Development, Coherence Field,
REM    Truth Lattice, World Lattice, Language, Reasoning,
REM    Goals, Drives, and Hands -- all running together.
REM
REM  Talk to him while he studies. He's one creature.
REM
REM  CK writes his notes to: %USERPROFILE%\.ck\writings\
REM  CK saves his state to:  %USERPROFILE%\.ck\
REM  CK logs to:             %USERPROFILE%\.ck\logs\
REM ============================================================

echo.
echo   ========================================
echo   CK Coherence Machine -- R16 (HEADLESS)
echo   ========================================
echo   All organs. 50Hz. One living system.
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ first.
    pause
    exit /b 1
)

REM Install deps if needed
pip show requests >nul 2>&1
if errorlevel 1 (
    echo [CK] Installing dependencies...
    pip install requests beautifulsoup4
)

echo [CK] Starting CK (full body, headless)...
echo [CK] Type to talk. He studies through his whole body.
echo [CK] Commands:
echo [CK]   "study physics for 8 hours"  -- CK studies with all organs
echo [CK]   "how are you"                -- CK reports full state
echo [CK]   "read your heartbeat"        -- CK reads his own code
echo [CK]   "state"                      -- full state dump
echo [CK]   "notes"                      -- study notes status
echo [CK]   "quit"                       -- save and stop
echo.

REM Run with auto-study if argument provided
if "%~1"=="" (
    python -m ck_sim.ck_headless
) else (
    python -m ck_sim.ck_headless --study "%~1" --hours %~2
)

pause
