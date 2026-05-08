@echo off
echo Opening UDP port 7777 for FPGA bridge...
netsh advfirewall firewall add rule name="CK FPGA UDP 7777" dir=in action=allow protocol=UDP localport=7777
echo Done. You can close this window.
pause
