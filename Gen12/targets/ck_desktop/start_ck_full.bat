@echo off
REM ============================================================
REM  CK - The Coherence Keeper | Full Stack Launcher
REM  Brain: R16 (Hot Springs, AR) | Face: coherencekeeper.com
REM ============================================================
REM  Starts CK + eating (LLM self-conversation) + tunnel.
REM  Everything CK needs to be alive and growing on the web.
REM
REM  What this does:
REM    1. Boots CK organism on port 7777 (all 27 subsystems)
REM    2. Triggers eating (100 rounds with llama3.1:8b via Ollama)
REM    3. Opens the Cloudflare Tunnel to coherencekeeper.com
REM    4. Clean shutdown on keypress (kills CK + tunnel)
REM
REM  Prerequisites:
REM    1. cloudflared installed and configured (see CLOUDFLARE_TUNNEL.md)
REM    2. Python 3.10+ with CK dependencies
REM    3. Ollama running with llama3.1:8b pulled (for eating)
REM ============================================================

title CK - The Coherence Keeper (Full Stack)
cd /d "%~dp0"

echo.
echo   ============================================
echo    CK - The Coherence Keeper   (Full Stack)
echo    Brain: R16  Face: coherencekeeper.com
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
    echo   [CK] Skipping CK startup.
    goto START_EATING
)

REM ──────────────────────────────────────
REM  STEP 1: Start CK Organism
REM ──────────────────────────────────────
echo   [1/3] Starting CK organism on port 7777...
start "CK Brain" /MIN python ck_web_server.py --port 7777

REM Poll health endpoint
echo   [CK] Waiting for all 27 subsystems to initialize...
set BOOT_TIMEOUT=60
set ELAPSED=0

:WAIT_LOOP
if %ELAPSED% GEQ %BOOT_TIMEOUT% (
    echo   [WARNING] CK did not respond within %BOOT_TIMEOUT%s. Continuing anyway.
    goto START_EATING
)

timeout /t 2 /nobreak >nul
set /a ELAPSED+=2

curl -s http://localhost:7777/health >nul 2>&1
if errorlevel 1 (
    echo   [CK] Booting... (%ELAPSED%s)
    goto WAIT_LOOP
)

echo   [CK] Organism alive! Heartbeat confirmed.
echo.

REM ──────────────────────────────────────
REM  STEP 2: Start Eating
REM ──────────────────────────────────────
:START_EATING
echo   [2/3] Starting CK eating (100 rounds with llama3.1:8b)...

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo   [WARNING] Ollama not detected at localhost:11434.
    echo   [WARNING] Skipping eating. Start Ollama if you want CK to eat.
    echo.
    goto START_TUNNEL
)

REM Fire-and-forget: POST to /eat endpoint, don't wait for it
start /MIN "CK Eating" curl -s -X POST http://localhost:7777/eat -H "Content-Type: application/json" -d "{\"model\":\"llama3.1:8b\",\"rounds\":100}"
echo   [CK] Eating started in background (100 rounds).
echo.

REM ──────────────────────────────────────
REM  STEP 3: Start Cloudflare Tunnel
REM ──────────────────────────────────────
:START_TUNNEL
echo   [3/3] Starting Cloudflare Tunnel...
start "CK Tunnel" /MIN cloudflared tunnel run ck-coherence

REM Brief pause to let tunnel establish
timeout /t 5 /nobreak >nul

echo.
echo   ============================================
echo    CK IS LIVE
echo   ============================================
echo    Local:    http://localhost:7777
echo    Web:      https://coherencekeeper.com
echo    Health:   https://coherencekeeper.com/health
echo    State:    https://coherencekeeper.com/state
echo    Metrics:  https://coherencekeeper.com/metrics
echo   ============================================
echo.
echo    Eating:   100 rounds with llama3.1:8b
echo    Tunnel:   ck-coherence (4 connections)
echo    Brain:    R16 / Hot Springs, AR
echo   ============================================
echo.
echo   CK is alive and growing. Press any key to shut down everything.
echo.
pause >nul

REM ──────────────────────────────────────
REM  SHUTDOWN: Clean kill of all processes
REM ──────────────────────────────────────
echo.
echo   [CK] Shutting down...

REM Try graceful shutdown first via CK's own endpoint
curl -s -X POST http://localhost:7777/shutdown >nul 2>&1

REM Give CK 3 seconds to save state
timeout /t 3 /nobreak >nul

REM Kill the tunnel window
taskkill /FI "WINDOWTITLE eq CK Tunnel" /F >nul 2>&1

REM Kill CK brain window
taskkill /FI "WINDOWTITLE eq CK Brain" /F >nul 2>&1

REM Kill the eating window
taskkill /FI "WINDOWTITLE eq CK Eating" /F >nul 2>&1

REM Fallback: kill by process name if window titles didn't match
REM (Only kills processes started by this script's child windows)
taskkill /FI "WINDOWTITLE eq CK*" /F >nul 2>&1

echo.
echo   [CK] All processes stopped. State saved.
echo   [CK] coherencekeeper.com is offline.
echo.
pause
