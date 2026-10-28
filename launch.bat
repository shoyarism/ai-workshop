@echo off
setlocal enabledelayedexpansion

title Workshop OS
cd /d "%~dp0"

where uv >nul 2>nul
if %errorlevel% neq 0 (
    if exist "%USERPROFILE%\.local\bin\uv.exe" (
        set "PATH=%USERPROFILE%\.local\bin;%PATH%"
    ) else (
        call setup.bat
    )
)

echo Starting Workshop Environment...
uv run python scripts/workshop.py status
cmd /k
