@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\ck7"
echo Compiling CK Gen7 (Phase 3.5 + hi-res timer)...
cl /O2 /LD /Fe:ck.dll being.c becoming_host.c observer.c ck_ffi.c vendor\cJSON.c /I. /Ivendor /link iphlpapi.lib psapi.lib
echo.
echo Exit code: %ERRORLEVEL%
if exist ck.dll (
    echo SUCCESS: ck.dll built
    dir ck.dll
) else (
    echo FAILED: ck.dll not found
)
