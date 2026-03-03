@echo off
REM ============================================================
REM  CK Test Runner -- Verify all 1719 tests pass
REM ============================================================

echo.
echo   ================================
echo   CK Test Suite -- 1719 Tests
echo   ================================
echo.

echo [TEST] Running unittest discover...
python -m unittest discover -s ck_sim -p "*_tests.py" -v 2>&1 | findstr /C:"Ran " /C:"OK" /C:"FAIL" /C:"ERROR"

echo.
echo [TEST] Running BTQ tests...
python -m ck_sim.ck_btq_tests 2>&1 | findstr /C:"RESULTS" /C:"PASSED"

echo.
echo [TEST] Running sim tests...
python -m ck_sim.ck_sim_tests 2>&1 | findstr /C:"RESULTS" /C:"PASSED"

echo.
echo Done.
pause
