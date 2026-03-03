@echo off
REM Load API key from .api_key file if not already set
if not defined ANTHROPIC_API_KEY (
    if exist ".api_key" (
        set /p ANTHROPIC_API_KEY=<.api_key
    ) else (
        echo [CK] No API key found. Set ANTHROPIC_API_KEY or create .api_key file.
        pause
        exit /b 1
    )
)
python ck_study.py --hours 8
