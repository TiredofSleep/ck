@echo off
cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
cl /O2 /LD ck_steer.c /Fe:ck_steer.dll /link advapi32.lib
echo DONE: %ERRORLEVEL%
