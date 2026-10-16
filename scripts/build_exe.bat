@echo off
chcp 65001 >nul
title Build PNEUMA Symbiosis EXE
cd /d "%~dp0\.."

echo ========================================
echo   Build Windows EXE (PyInstaller)
echo ========================================
echo.

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found.
    pause
    exit /b 1
)

if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install -q -r requirements.txt
python -m pip install -q pyinstaller

echo.
echo Building one-file EXE...
pyinstaller --noconfirm --clean ^
  --onefile ^
  --name "PNEUMA-Symbiosis" ^
  --paths "." ^
  --hidden-import pneuma ^
  --hidden-import pneuma.cli ^
  --hidden-import pneuma.sensors.simulator ^
  --hidden-import pneuma.analytics.engine ^
  --hidden-import pneuma.reflection.module ^
  --hidden-import pneuma.intuition.module ^
  --hidden-import pneuma.ethics.core ^
  --hidden-import pneuma.archetypal.layer ^
  --hidden-import pneuma.safety.guard ^
  --hidden-import pneuma.reporting.report ^
  --hidden-import sophia ^
  --hidden-import sophia.blue_matrix ^
  --hidden-import sophia.blue_matrix.matrix ^
  --hidden-import sophia.blue_matrix.channels ^
  --hidden-import sophia.blue_matrix.filters ^
  --hidden-import sophia.blue_matrix.adapters ^
  --hidden-import sophia.wisdom.layer ^
  --hidden-import sophia.evolution.loop ^
  --hidden-import sophia.passport.identity ^
  --hidden-import symbiosis.orchestrator ^
  --console ^
  scripts\launcher.py

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   OK: dist\PNEUMA-Symbiosis.exe
echo ========================================
echo.
echo Copy EXE anywhere and run. First run may be slower (unpack).
echo Example:
echo   PNEUMA-Symbiosis.exe --mode archetypal --steps 60 --scenario stress
echo.
pause
