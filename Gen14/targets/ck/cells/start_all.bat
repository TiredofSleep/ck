@echo off
REM Start all CK cells as separate windows.
REM Each cell is its own python process; close a window to stop one cell.
REM Set CK_DISABLE_HEAVY_DAEMONS=all in your server-cell boot before running.

set PY=C:\ck_venv\lora312\Scripts\python.exe
set CELLS=%~dp0

REM Below-normal priority via "start /BELOWNORMAL" keeps the server cell snappy.
start "ck:bible" /BELOWNORMAL "%PY%" -X utf8 -u "%CELLS%bible_cell.py"
start "ck:scripture" /BELOWNORMAL "%PY%" -X utf8 -u "%CELLS%scripture_cell.py"
start "ck:poetry" /BELOWNORMAL "%PY%" -X utf8 -u "%CELLS%poetry_cell.py"
start "ck:domain" /BELOWNORMAL "%PY%" -X utf8 -u "%CELLS%domain_cell.py"
start "ck:web" /BELOWNORMAL "%PY%" -X utf8 -u "%CELLS%web_cell.py"
start "ck:listener" /BELOWNORMAL "%PY%" -X utf8 -u "%CELLS%listener_cell.py"
start "ck:writer" /BELOWNORMAL "%PY%" -X utf8 -u "%CELLS%writer_cell.py"

echo.
echo All 7 cells started in separate windows (below-normal priority).
echo Close a window to stop that cell.
echo Server cell should be started SEPARATELY with:
echo   set CK_DISABLE_HEAVY_DAEMONS=all
echo   python Gen12\targets\ck_desktop\ck_boot_api.py
