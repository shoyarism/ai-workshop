@echo off
title ComfyUI - Open-Source Diffusion Workshop (GTX 1650 4GB Optimized)
echo ==============================================================================
echo Booting ComfyUI with Low-VRAM flag for NVIDIA GeForce GTX 1650 (4GB)
echo URL: http://127.0.0.1:8188
echo ==============================================================================

set CURRENT_DIR=%~dp0
call "%CURRENT_DIR%.venv\Scripts\activate.bat"
cd /d "%CURRENT_DIR%ComfyUI"

python main.py --lowvram --preview-method auto --listen 127.0.0.1 --port 8188

pause
