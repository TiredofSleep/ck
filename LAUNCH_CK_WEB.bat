@echo off
:: ============================================
::  CK - The Coherence Keeper
::  Web Server + Browser Launch
:: ============================================
title CK Web Server

cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"

echo.
echo   ============================================
echo    CK - The Coherence Keeper
echo    T* = 5/7 = 0.714285...
echo   ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python not found.
    pause
    exit /b 1
)

:: Start web server
echo   Starting CK organism on port 7777...
start "CK Web" /MIN python ck_web_server.py --port 7777

:: Wait for boot
echo   Waiting for boot...
timeout /t 8 /nobreak >nul

:: Open browser
echo   Opening browser...
start http://localhost:7777

echo.
echo   CK is alive at http://localhost:7777
echo   Press any key to shut down.
echo.
pause >nul

:: Shutdown
curl -s -X POST http://localhost:7777/shutdown >nul 2>&1
timeout /t 2 /nobreak >nul
taskkill /FI "WINDOWTITLE eq CK Web" /F >nul 2>&1
echo   CK stopped.
pause
