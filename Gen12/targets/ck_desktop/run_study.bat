@echo off
REM ============================================================
REM  CK Autodidact Runner -- Headless Study Mode
REM ============================================================
REM  Let CK study overnight without the GUI.
REM  He fetches pages from trusted sites, processes through D2,
REM  writes voice notes, and saves curves.
REM
REM  Usage:
REM    run_study.bat              -- Quick study (5 cycles)
REM    run_study.bat --hours 8    -- 8 hour study session
REM    run_study.bat --resume     -- Resume previous session
REM ============================================================

echo.
echo   ================================
echo   CK Autodidact -- Overnight Study
echo   ================================
echo.

echo [CK] CK will study from trusted sites only.
echo [CK] Notes saved to: %USERPROFILE%\.ck\autodidact\
echo [CK] Press Ctrl+C to stop (state saves automatically).
echo.

python -m ck_sim.ck_autodidact_runner %*

pause
