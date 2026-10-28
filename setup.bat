@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo             WORKSHOP OS - PORTABLE ONBOARDING BOOTSTRAP
echo ======================================================================
echo Workshop Root: %~dp0

:: 1. Ensure uv is available
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] uv package manager not found on PATH.
    echo [*] Installing uv automatically...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%USERPROFILE%\.cargo\bin;%PATH%"
    where uv >nul 2>nul
    if %errorlevel% neq 0 (
        echo [!] Failed to auto-install uv. Please install Python or uv manually.
        pause
        exit /b 1
    )
    echo [✓] uv installed successfully.
) else (
    echo [✓] uv is available.
)

:: 2. Run Workshop Onboard
echo [*] Mounting skills and initializing local harness configuration...
cd /d "%~dp0"
uv run python scripts/workshop_onboard.py

:: 3. Run Doctor Health Check
echo [*] Running Workshop Doctor verification...
uv run python scripts/workshop.py doctor

echo ======================================================================
echo       WORKSHOP OS READY! Plug and play on this machine.
echo ======================================================================
