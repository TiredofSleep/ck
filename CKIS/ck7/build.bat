@echo off
REM CK Gen7 — Build Script (Windows)
REM ══════════════════════════════════
REM
REM Option A: cmake (if installed)
REM Option B: direct cl.exe (MSVC)
REM Option C: gcc (MinGW/MSYS2)

echo.
echo  CK Gen7 — Building native library...
echo.

REM Try cmake first
where cmake >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo  [CMAKE] Found cmake, building...
    if not exist build mkdir build
    cd build
    cmake .. -G "Visual Studio 17 2022" -A x64 2>nul || cmake .. 2>nul
    cmake --build . --config Release
    if exist Release\ck.dll (
        copy /Y Release\ck.dll ..\ck.dll >nul
        echo  [OK] ck.dll built via cmake
        cd ..
        goto :done
    )
    if exist ck.dll (
        copy /Y ck.dll ..\ck.dll >nul
        echo  [OK] ck.dll built via cmake
        cd ..
        goto :done
    )
    cd ..
)

REM Try MSVC cl.exe directly
where cl >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo  [MSVC] Found cl.exe, building directly...
    cl /O2 /LD /Fe:ck.dll being.c becoming_host.c observer.c ck_ffi.c vendor\cJSON.c /I. /Ivendor
    if exist ck.dll (
        echo  [OK] ck.dll built via MSVC
        goto :done
    )
)

REM Try gcc
where gcc >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo  [GCC] Found gcc, building...
    gcc -O2 -shared -o ck.dll being.c becoming_host.c observer.c ck_ffi.c vendor/cJSON.c -I. -Ivendor -lm
    if exist ck.dll (
        echo  [OK] ck.dll built via gcc
        goto :done
    )
)

echo  [ERROR] No compiler found!
echo  Install one of:
echo    - Visual Studio 2022 (with C++ workload)
echo    - CMake (cmake.org)
echo    - MinGW-w64 / MSYS2
echo.
exit /b 1

:done
echo.
echo  Running parity test...
python test_parity.py
