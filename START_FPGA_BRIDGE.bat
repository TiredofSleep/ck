@echo off
cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
echo Waiting for FPGA PHY...
timeout /t 3 /nobreak >nul
echo Listening for FPGA coherence on UDP 7777...
echo.
python ck_fpga_bridge.py --listen-only
pause
