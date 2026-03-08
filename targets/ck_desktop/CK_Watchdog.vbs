' CK Watchdog Launcher (invisible)
' Runs ck_watchdog.py in the background with no visible window.
' Place this in the Startup folder for auto-start.

Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"
WshShell.Run "pythonw ck_watchdog.py", 0, False
