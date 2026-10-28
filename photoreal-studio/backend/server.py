# -*- coding: utf-8 -*-
"""
FastAPI Server for the Ultra-Realistic AI Image Generation System (Photoreal Studio).
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from engine.photoreal_engine import PhotorealEngine
from engine.prompt_enhancer import RealismPromptEnhancer
from backend.generator import PhotorealGenerator

app = FastAPI(
    title="Ultra-Realistic AI Image Generation Studio",
    description="Photographic Physics & Optical Realism Engine",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENV_FILE = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_FILE):
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k:
                        os.environ[k] = v
    except Exception as e:
        print(f"Warning: could not read .env: {e}")

engine = PhotorealEngine()
enhancer = RealismPromptEnhancer()
generator = PhotorealGenerator()

runtime_config = {
    "gemini_api_key": os.environ.get("GEMINI_API_KEY", ""),
    "hf_token": os.environ.get("HF_TOKEN", "")
}


class SynthesizeRequest(BaseModel):
    subject: str
    camera_key: str = "leica_m11"
    lens_key: str = "zeiss_otus_85"
    aperture: str = "f/1.8"
    lighting_key: str = "rembrandt"
    film_stock_key: str = "kodak_portra_400"
    include_skin_realism: bool = True
    include_material_physics: bool = True
    aspect_ratio: str = "3:4"
    custom_shutter: str = "1/250s"
    custom_iso: int = 200
    extra_mood: Optional[str] = None


class EnhanceRequest(BaseModel):
    subject: str


class GenerateRequest(BaseModel):
    subject: str
    camera_key: str = "leica_m11"
    lens_key: str = "zeiss_otus_85"
    aperture: str = "f/1.8"
    lighting_key: str = "rembrandt"
    film_stock_key: str = "kodak_portra_400"
    include_skin_realism: bool = True
    include_material_physics: bool = True
    aspect_ratio: str = "3:4"
    custom_shutter: str = "1/250s"
    custom_iso: int = 200
    extra_mood: Optional[str] = None
    provider: str = "flux_dev_realism"
    seed: Optional[int] = None
    custom_positive_prompt: Optional[str] = None
    custom_negative_prompt: Optional[str] = None


class SettingsRequest(BaseModel):
    gemini_api_key: Optional[str] = None
    hf_token: Optional[str] = None


@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "engine_version": "2.0.0",
        "default_provider": "flux_dev_realism",
        "available_providers": [
            {
                "id": "flux_dev_realism",
                "name": "FLUX.1-Dev Realism (Hugging Face - State of the Art)",
                "requires_key": False,
                "recommended": True
            },
            {
                "id": "hf_flux_schnell",
                "name": "FLUX.1-Schnell (Hugging Face - 4-Step Turbo)",
                "requires_key": False,
                "recommended": False
            },
            {
                "id": "imagen3",
                "name": "Google Imagen 3 (SOTA Studio Quality)",
                "requires_key": True,
                "recommended": True,
                "active": bool(runtime_config["gemini_api_key"])
            }
        ],
        "has_gemini_key": bool(runtime_config["gemini_api_key"]),
        "has_hf_token": bool(runtime_config["hf_token"]),
        "preset_count": len(engine.presets),
        "total_gallery_images": len(generator.list_gallery())
    }


@app.get("/api/presets")
def get_presets():
    return engine.presets


@app.get("/api/presets/{preset_key}")
def get_preset(preset_key: str, subject: Optional[str] = None):
    try:
        return engine.load_preset(preset_key, custom_subject=subject)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/options")
def get_options():
    cameras = [
        {"id": k, "name": v.name, "sensor": v.sensor_phrase}
        for k, v in engine.cameras.items()
    ]
    lenses = [
        {"id": k, "name": v.name, "focal_length": v.focal_length, "optical": v.optical_phrase}
        for k, v in engine.lenses.items()
    ]
    lighting = [
        {"id": k, "name": v.name, "phrase": v.phrase}
        for k, v in engine.lighting.items()
    ]
    film_stocks = [
        {"id": k, "name": v.name, "phrase": v.phrase}
        for k, v in engine.film_stocks.items()
    ]
    apertures = ["f/1.2", "f/1.4", "f/1.8", "f/2.0", "f/2.8", "f/4.0", "f/5.6", "f/8.0"]
    aspect_ratios = [
        {"ratio": "1:1", "label": "1:1 Square (1024x1024)", "width": 1024, "height": 1024},
        {"ratio": "4:5", "label": "4:5 Classic Portrait (864x1080)", "width": 864, "height": 1080},
        {"ratio": "3:4", "label": "3:4 Editorial Portrait (896x1152)", "width": 896, "height": 1152},
        {"ratio": "16:9", "label": "16:9 Cinematic Widescreen (1280x720)", "width": 1280, "height": 720},
        {"ratio": "21:9", "label": "21:9 Anamorphic Ultrawide (1344x576)", "width": 1344, "height": 576},
        {"ratio": "9:16", "label": "9:16 Fullscreen Vertical (720x1280)", "width": 720, "height": 1280}
    ]

    return {
        "cameras": cameras,
        "lenses": lenses,
        "lighting": lighting,
        "film_stocks": film_stocks,
        "apertures": apertures,
        "aspect_ratios": aspect_ratios
    }


@app.post("/api/synthesize")
def synthesize(req: SynthesizeRequest):
    return engine.synthesize_prompt(
        subject=req.subject,
        camera_key=req.camera_key,
        lens_key=req.lens_key,
        aperture=req.aperture,
        lighting_key=req.lighting_key,
        film_stock_key=req.film_stock_key,
        include_skin_realism=req.include_skin_realism,
        include_material_physics=req.include_material_physics,
        aspect_ratio=req.aspect_ratio,
        custom_shutter=req.custom_shutter,
        custom_iso=req.custom_iso,
        extra_mood=req.extra_mood
    )


@app.post("/api/enhance")
def enhance(req: EnhanceRequest):
    if not req.subject or not req.subject.strip():
        raise HTTPException(status_code=400, detail="Subject cannot be empty.")
    return enhancer.enhance(req.subject, gemini_api_key=runtime_config["gemini_api_key"])


@app.post("/api/generate")
def generate(req: GenerateRequest):
    if not req.subject or not req.subject.strip():
        raise HTTPException(status_code=400, detail="Subject cannot be empty.")

    synth = engine.synthesize_prompt(
        subject=req.subject,
        camera_key=req.camera_key,
        lens_key=req.lens_key,
        aperture=req.aperture,
        lighting_key=req.lighting_key,
        film_stock_key=req.film_stock_key,
        include_skin_realism=req.include_skin_realism,
        include_material_physics=req.include_material_physics,
        aspect_ratio=req.aspect_ratio,
        custom_shutter=req.custom_shutter,
        custom_iso=req.custom_iso,
        extra_mood=req.extra_mood
    )

    if req.custom_positive_prompt and req.custom_positive_prompt.strip():
        synth["positive_prompt"] = req.custom_positive_prompt.strip()
    if req.custom_negative_prompt and req.custom_negative_prompt.strip():
        synth["negative_prompt"] = req.custom_negative_prompt.strip()

    result = generator.generate(
        synthesized_data=synth,
        provider=req.provider,
        seed=req.seed,
        gemini_api_key=runtime_config["gemini_api_key"],
        hf_token=runtime_config["hf_token"]
    )
    return result


@app.get("/api/gallery")
def get_gallery():
    return generator.list_gallery()


@app.post("/api/settings")
def update_settings(req: SettingsRequest):
    if req.gemini_api_key is not None:
        runtime_config["gemini_api_key"] = req.gemini_api_key.strip()
        os.environ["GEMINI_API_KEY"] = req.gemini_api_key.strip()
    if req.hf_token is not None:
        runtime_config["hf_token"] = req.hf_token.strip()
        os.environ["HF_TOKEN"] = req.hf_token.strip()

    # Persist to local .env file
    try:
        lines = []
        if runtime_config["gemini_api_key"]:
            lines.append(f"GEMINI_API_KEY={runtime_config['gemini_api_key']}")
        if runtime_config["hf_token"]:
            lines.append(f"HF_TOKEN={runtime_config['hf_token']}")
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:
        print(f"Warning: could not write .env: {e}")

    return {
        "status": "updated",
        "has_gemini_key": bool(runtime_config["gemini_api_key"]),
        "has_hf_token": bool(runtime_config["hf_token"])
    }


OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"message": "Photoreal Studio API running."})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.server:app", host="127.0.0.1", port=8000, reload=True)