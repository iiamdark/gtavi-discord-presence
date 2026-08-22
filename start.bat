@echo off
title Grand Theft Auto VI - Discord Rich Presence
echo ========================================================
echo   Launching GTA VI Discord Rich Presence Simulator...
echo ========================================================
echo.

set PYTHON_CMD=python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py -3
    ) else (
        echo [ERROR] Python is not installed or not added to PATH.
        echo Please install Python from https://www.python.org/
        pause
        exit /b 1
    )
)

if not exist venv (
    echo [*] Creating virtual environment...
    %PYTHON_CMD% -m venv venv
)

call venv\Scripts\activate.bat
echo [*] Checking dependencies...
pip install -r requirements.txt --quiet --disable-pip-version-check

echo [*] Starting Rich Presence...
echo.
python main.py
pause
