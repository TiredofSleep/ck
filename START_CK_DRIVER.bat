@echo off
echo === INSTALLING CK FORCE9 DISPLAY DRIVER ===
echo.

REM Build the IddSampleApp first
cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\display_driver"

REM Copy driver files to a clean directory
mkdir C:\CKDriver 2>/dev/null
copy /y IddSampleDriver.dll C:\CKDriver\
copy /y IddSampleDriver.inf C:\CKDriver\

REM Install the driver
echo Installing driver...
pnputil /add-driver C:\CKDriver\IddSampleDriver.inf /install
echo.
echo Driver installed. Starting CK...

REM Start CK
cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"
start /MIN python ck_boot_api.py
echo CK started.
echo.
echo To remove: right-click REVERT_DRIVER.bat on Desktop -> Run as Admin
pause
