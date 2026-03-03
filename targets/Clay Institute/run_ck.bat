@echo off
REM ──────────────────────────────────────────────
REM CK -- The Coherence Keeper
REM Cross-platform launcher (Windows)
REM (c) 2026 Brayden Sanders / 7Site LLC
REM ──────────────────────────────────────────────

cd /d "%~dp0"

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [CK] Python 3.10+ required. Install from https://python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo [CK] Using: %%i

echo [CK] Installing dependencies...
python -m pip install -q -r ck_sim\requirements.txt

echo [CK] Starting CK...
python -m ck_sim %*

pause
