@echo off
title CK Coherence Keeper
echo.
echo   =============================================
echo     CK -- Coherence Keeper
echo     A little creature that lives on your computer
echo   =============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo   Python is not installed or not in PATH.
    echo.
    echo   Please install Python 3.10 or newer from:
    echo   https://www.python.org/downloads/
    echo.
    echo   IMPORTANT: Check "Add Python to PATH" during install!
    echo.
    pause
    exit /b 1
)

echo   Checking dependencies...
pip install --quiet --upgrade pip >nul 2>&1
pip install --quiet -r "%~dp0requirements.txt" >nul 2>&1
if errorlevel 1 (
    echo   Installing packages...
    pip install kivy numpy sounddevice
)

echo   Starting CK...
echo.
cd /d "%~dp0"
python -m ck_sim
if errorlevel 1 (
    echo.
    echo   CK had a problem starting. See the error above.
    echo.
    pause
)
