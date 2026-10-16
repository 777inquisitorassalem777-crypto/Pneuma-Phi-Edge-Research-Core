@echo off
chcp 65001 >nul
title PNEUMA Symbiosis
cd /d "%~dp0\.."

echo ========================================
echo   PNEUMA Symbiosis Launcher (Windows)
echo ========================================
echo.

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found in PATH.
    echo Install Python 3.10+ from https://www.python.org/downloads/
    echo Enable "Add python.exe to PATH" during setup.
    pause
    exit /b 1
)

python -c "import sys; assert sys.version_info >= (3,10)" 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Need Python 3.10 or newer.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install -q -r requirements.txt

echo.
echo Starting PNEUMA Symbiosis...
echo.
python scripts\launcher.py %*

echo.
pause
