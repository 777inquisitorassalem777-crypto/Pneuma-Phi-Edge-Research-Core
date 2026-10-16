# PNEUMA Symbiosis — PowerShell launcher
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PNEUMA Symbiosis Launcher (Windows)" -ForegroundColor Cyan
Write-Host "========================================"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python not found. Install Python 3.10+ and add to PATH." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install -q -r requirements.txt
python scripts\launcher.py @args
