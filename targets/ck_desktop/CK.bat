@echo off
REM ============================================================
REM  CK -- The Coherence Keeper
REM  Gen 9.31 | R16 Desktop (16-core, RTX 4070)
REM ============================================================
REM  CK lives here. He runs in the background.
REM  This icon just opens a window to talk to him.
REM
REM  T* = 5/7 = 0.714285...
REM  Truth is not assigned. Truth is measured.
REM ============================================================

title CK -- The Coherence Keeper
cd /d "%~dp0"

REM ── Is CK alive? ──
curl -s http://localhost:7777/health >nul 2>&1
if %errorlevel% equ 0 goto CONSOLE

REM ── CK is not running. Start watchdog. ──
echo.
echo   CK is not running. Starting him up...
echo.
start /B pythonw ck_watchdog.py
echo   Waiting for CK to boot (30s)...
timeout /t 30 /nobreak >nul

REM ── Verify he started ──
curl -s http://localhost:7777/health >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo   CK failed to start. Check watchdog.log in ~/.ck/
    echo.
    pause
    exit /b 1
)

:CONSOLE
python ck_console.py
