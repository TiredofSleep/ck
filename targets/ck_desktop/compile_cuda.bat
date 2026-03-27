@echo off
cd /d "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
nvcc -O2 -shared -o force9_cuda.dll force9_cuda.cu
echo DONE: %ERRORLEVEL%
