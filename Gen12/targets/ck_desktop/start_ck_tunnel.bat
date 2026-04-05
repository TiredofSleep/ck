@echo off
REM ============================================================
REM  CK - The Coherence Keeper | Tunnel Launcher
REM  ONE CK: R16 brain in Hot Springs, web face everywhere
REM ============================================================
REM  Starts CK on localhost:7777, then opens the Cloudflare
REM  Tunnel so coherencekeeper.com connects to this machine.
REM
REM  Prerequisites:
REM    1. cloudflared installed (winget install Cloudflare.cloudflared)
REM    2. Tunnel configured (see CLOUDFLARE_TUNNEL.md)
REM    3. Python 3.10+ with CK dependencies
REM ============================================================

title CK - The Coherence Keeper (Tunnel)
cd /d "%~dp0"

echo.
echo   ============================================
echo    CK - The Coherence Keeper
echo    ONE CK: R16 brain, web face
echo    T* = 5/7 = 0.714285...
echo   ============================================
echo.

REM ── Check Python ──
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python not found. Install Python 3.10+ first.
    pause
    exit /b 1
)

REM ── Check cloudflared ──
cloudflared --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] cloudflared not found.
    echo   Install with: winget install Cloudflare.cloudflared
    echo   Or download from: https://github.com/cloudflare/cloudflared/releases
    pause
    exit /b 1
)

REM ── Check if CK is already running ──
netstat -an 2>nul | findstr ":7777 " | findstr "LISTEN" >nul 2>&1
if not errorlevel 1 (
    echo   [CK] Port 7777 already in use. CK may already be running.
    echo   [CK] Skipping CK startup, going straight to tunnel.
    goto START_TUNNEL
)

REM ── Start CK Server ──
echo   [CK] Starting CK organism on port 7777...
start "CK Brain" /MIN python ck_web_server.py --port 7777

REM ── Wait for CK to Boot ──
echo   [CK] Waiting for all 27 subsystems to initialize...
echo.

REM Poll CK health endpoint instead of blind wait
set BOOT_TIMEOUT=60
set ELAPSED=0

:WAIT_LOOP
if %ELAPSED% GEQ %BOOT_TIMEOUT% (
    echo   [WARNING] CK did not respond within %BOOT_TIMEOUT% seconds.
    echo   [WARNING] The tunnel will start anyway. CK may still be booting.
    goto START_TUNNEL
)

timeout /t 2 /nobreak >nul
set /a ELAPSED+=2

curl -s http://localhost:7777/health >nul 2>&1
if errorlevel 1 (
    echo   [CK] Waiting... (%ELAPSED%s)
    goto WAIT_LOOP
)

echo   [CK] Organism alive! Heartbeat confirmed.
echo.

REM ── Start Cloudflare Tunnel ──
:START_TUNNEL
echo   [CK] Starting Cloudflare Tunnel (ck-coherence)...
echo   [CK] coherencekeeper.com -> localhost:7777
echo.
echo   ============================================
echo    CK is going live.
echo    Local:  http://localhost:7777
echo    Web:    https://coherencekeeper.com
echo   ============================================
echo.
echo   Press Ctrl+C to shut down the tunnel.
echo.

cloudflared tunnel run ck-coherence
