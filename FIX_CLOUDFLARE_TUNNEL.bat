@echo off
:: ============================================
::  Fix Cloudflare Tunnel Service
::  Run as Administrator
:: ============================================
echo Fixing cloudflared service...

sc config cloudflared binPath= "\"C:\Program Files (x86)\cloudflared\cloudflared.exe\" --config \"C:\Users\brayd\.cloudflared\config.yml\" tunnel run"
echo Service binary path updated.

sc stop cloudflared
timeout /t 3 /nobreak >nul

sc start cloudflared
timeout /t 5 /nobreak >nul

echo.
echo Tunnel status:
cloudflared tunnel info ck-api

echo.
echo Done. coherencekeeper.com should be live.
pause
