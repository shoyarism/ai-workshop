@echo off
setlocal
set SCRIPT_DIR=%~dp0
set BACKUP_PS1=%SCRIPT_DIR%..\..\Backup\backup.ps1
if exist "%BACKUP_PS1%" (
    powershell -ExecutionPolicy Bypass -File "%BACKUP_PS1%"
) else (
    echo [!] Backup script not found at %BACKUP_PS1%
)
endlocal
