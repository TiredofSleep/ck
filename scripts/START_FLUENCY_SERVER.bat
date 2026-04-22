@echo off
REM ============================================================================
REM   START_FLUENCY_SERVER.bat
REM
REM   Hands-on-wheel launcher for the CK Ollama learn-loop (Option A).
REM   Governance: G6 hands-on-wheel posture -- no autostart, explicit boot,
REM   shows scope before launch, requires keystroke to proceed.
REM
REM   What this script does:
REM     1. Prints the scope (loopback only, no model modification, append-only log).
REM     2. Checks that Ollama is running on http://localhost:11434.
REM     3. Asks for explicit keystroke confirmation.
REM     4. Launches Flask server on 127.0.0.1:7778 with --i-mean-it flag.
REM
REM   What this script does NOT do:
REM     - Start Ollama automatically (you run 'ollama serve' in a separate window).
REM     - Download model weights.
REM     - Open a firewall port or cut over the Cloudflare tunnel.
REM     - Bind to 0.0.0.0.
REM
REM   Stop the server with Ctrl-C in the window.  Log lives under
REM   ck\fluency\logs\corrections_YYYY_MM_DD.jsonl (UTC-rotated, fsynced).
REM ============================================================================

setlocal

echo.
echo ============================================================================
echo   CK FLUENCY SERVER -- Ollama learn-loop (Option A)
echo ============================================================================
echo.
echo   Scope:
echo     - Binds to 127.0.0.1:7778 (loopback only; not reachable off machine).
echo     - Ollama client refuses any non-loopback host (ck/fluency/ollama_client.py).
echo     - No model weight modification.  Learning lives in append-only JSONL.
echo     - Log path: ck\fluency\logs\corrections_YYYY_MM_DD.jsonl (UTC).
echo     - Stop with Ctrl-C in this window.
echo.
echo   Prereqs:
echo     1. Ollama running at http://localhost:11434 ('ollama serve' in another window).
echo     2. Model llama3.1:8b pulled ('ollama pull llama3.1:8b' once).
echo     3. Flask installed in your active Python env ('pip install flask').
echo.
echo ============================================================================
echo.

REM --- 1. Probe Ollama -------------------------------------------------------
echo   Probing Ollama at http://localhost:11434/api/tags ...
python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:11434/api/tags',timeout=2).status==200 else 1)" 2>nul
if errorlevel 1 (
    echo   [FAIL] Ollama is not reachable at http://localhost:11434.
    echo          Start it with 'ollama serve' and re-run this script.
    echo.
    pause
    exit /b 3
)
echo   [OK]   Ollama is reachable.
echo.

REM --- 2. Ask for confirmation ----------------------------------------------
set /p CONFIRM=Start CK fluency server on 127.0.0.1:7778? [y/N]
if /i not "%CONFIRM%"=="y" (
    echo   Cancelled.  No server started.
    exit /b 0
)

echo.
echo ============================================================================
echo   Starting server with --i-mean-it ...  (Ctrl-C in this window to stop)
echo ============================================================================
echo.

REM --- 3. Launch -------------------------------------------------------------
python -m ck.fluency.fluency_server --i-mean-it --host 127.0.0.1 --port 7778 --ollama-host http://localhost:11434 --ollama-model llama3.1:8b

endlocal
