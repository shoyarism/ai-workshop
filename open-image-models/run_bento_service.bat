@echo off
title BentoML Diffusion Service
echo ==============================================================================
echo Booting BentoML Image Generation Service on http://127.0.0.1:3000
echo Swagger UI / OpenAPI docs available at: http://127.0.0.1:3000
echo ==============================================================================

set CURRENT_DIR=%~dp0
call "%CURRENT_DIR%.venv\Scripts\activate.bat"
cd /d "%CURRENT_DIR%"

bentoml serve service:ImageGenService --port 3000

pause
