@echo off
:: CK Organism + Cloudflare Tunnel Auto-Start Script
:: Launches the CK web API and Cloudflare tunnel for coherencekeeper.com
:: Place a shortcut to this file in shell:startup for auto-start on boot

title CK Organism Server

echo ============================================
echo   CK Organism - Production Server Startup
echo ============================================
echo.

:: Set working directory
cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen12\targets\ck_desktop"

:: Start CK Web API in background
echo [1/2] Starting CK organism on port 7777...
start /min "CK Web API" cmd /c "python ck_web_server.py 2>&1"

:: Wait for CK to initialize
echo       Waiting 10 seconds for organism boot...
timeout /t 10 /nobreak >nul

:: Verify CK is alive
curl -s http://localhost:7777/health >nul 2>&1
if %errorlevel% neq 0 (
    echo       [WARNING] CK health check failed - organism may still be booting
    echo       Continuing with tunnel startup anyway...
) else (
    echo       CK is alive!
)

echo.

:: Start Cloudflare Tunnel
echo [2/2] Starting Cloudflare Tunnel (api.coherencekeeper.com)...
start /min "CK Tunnel" cmd /c "\"C:\Program Files (x86)\cloudflared\cloudflared.exe\" tunnel run ck-api 2>&1"

echo.
echo ============================================
echo   CK is online at api.coherencekeeper.com
echo   Website: https://coherencekeeper.com
echo ============================================
echo.
echo Press any key to stop both services...
pause >nul

:: Cleanup
echo Stopping services...
taskkill /fi "WINDOWTITLE eq CK Web API" /f >nul 2>&1
taskkill /fi "WINDOWTITLE eq CK Tunnel" /f >nul 2>&1
taskkill /im cloudflared.exe /f >nul 2>&1
echo Done.
