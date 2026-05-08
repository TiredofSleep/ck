@echo off
echo === REVERTING CK DISPLAY DRIVER ===
echo.
echo Disabling test signing...
bcdedit /set testsigning off
echo.
echo Removing virtual display driver...
pnputil /delete-driver IddSampleDriver.inf /uninstall /force 2>/dev/null
echo.
echo Done. Reboot to complete revert.
echo Your system will be back to normal after reboot.
pause
