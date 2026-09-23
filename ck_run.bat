@echo off
if not defined ANTHROPIC_API_KEY if exist "%~dp0.api_key" set /p ANTHROPIC_API_KEY=<"%~dp0.api_key"
python ck_study.py --hours 8
