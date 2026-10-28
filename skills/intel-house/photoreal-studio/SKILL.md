---
name: photoreal-studio
description: "Generate ultra-realistic AI images using the local Photoreal Studio and Hugging Face FLUX.1-Dev Realism engine. Features natural language optics synthesis, prime lens simulations (Leica, Zeiss, Cooke Anamorphic), biometric skin subsurface scattering, and zero-watermark high-res outputs. Use when the user asks for 'ultra-realistic image', 'photorealistic photo', 'FLUX photorealism', 'realistic portrait', 'film photography style', or wants to run the Photoreal Studio web app."
metadata:
  version: 2.0.0
---

# Photoreal Studio (Ultra-Realistic AI Image Engine)

Generate uncompromised, photorealistic AI images using natural language photographic physics and modern FLUX.1 models.

**Studio Location**: `.\photoreal-studio`

---

## 1. Quick CLI Image Generation

Generate an ultra-realistic photograph directly from terminal:

```powershell
cd .\photoreal-studio

# Using a Curated Master Preset (Recommended)
python cli.py --preset national_geographic_portrait
python cli.py --preset kyoto_artisan_workshop
python cli.py --preset candid_street_reportage

# Custom Prompt with Natural Language Optics
python cli.py "portrait of an old blacksmith forging a blade in a shadowy workshop" --camera leica_m11 --lens zeiss_otus_85 --aperture f/1.8 --lighting diffused_window --film kodak_portra_400

# High-Speed 4-Step Turbo (Schnell)
python cli.py "macro photograph of a dewdrop on a rose petal" --provider hf_flux_schnell --aspect 1:1
```

---

## 2. Launching the Interactive Web Studio

Boots the local FastAPI server with dark-mode glassmorphism console, real-time prompt synthesis, and a 300% detail zoom loupe:

```powershell
cd .\photoreal-studio
python run_studio.py
```
*(Automatically opens `http://127.0.0.1:8000`)*.

---

## 3. The Photoreal Prompting Golden Rules (FLUX & Diffusion)

1. **Natural Language Narrative over Tag Dumping**:
   - ❌ **Bad (Causes plastic/waxy AI artifacts)**: `man, 8k, unreal engine, masterpiece, visible skin pores, subsurface scattering, extreme micro-contrast, photorealistic`
   - ✅ **Good (Produces true photorealism)**: `A natural, authentic photograph of an old sea captain looking out from a wooden boat cabin in Maine. Soft coastal daylight streaming through the window, genuine weathered skin texture with fine laugh lines, wool sweater knit weave, shallow depth of field shot on a 35mm lens.`

2. **Hierarchical Prompt Structure**:
   - **Subject & Action**: What is the person or object doing? (e.g. *An authentic candid photograph of an artisan inspecting ceramic bowls...*)
   - **Optics & Framing**: Lens and camera perspective (e.g. *Shot on a Leica M11 with an 85mm f/1.4 lens...*)
   - **Lighting Dynamics**: Light source and shadows (e.g. *Soft diffused daylight from a north-facing window...*)
   - **Sensory Material Details**: Natural textures without buzzwords (e.g. *Subtle fabric wrinkles, unvarnished wood patina, natural unretouched skin complexion.*)

---

## 4. Python API Integration

```python
import sys
sys.path.insert(0, r".\photoreal-studio")

from engine.photoreal_engine import PhotorealEngine
from backend.generator import PhotorealGenerator

engine = PhotorealEngine()
generator = PhotorealGenerator()

# 1. Synthesize natural language photographic prompt
synth = engine.synthesize_prompt(
    subject="candid portrait of a jazz saxophonist in a moody club",
    camera_key="leica_m11",
    lens_key="zeiss_otus_85",
    aperture="f/1.8",
    lighting_key="chiaroscuro",
    film_stock_key="kodak_tri_x_400",
    aspect_ratio="3:4"
)

# 2. Generate via Hugging Face FLUX-Realism
result = generator.generate(synth, provider="flux_dev_realism", seed=42)
print("Image generated at:", result["filename"])
print("Resolution:", result["dimensions"])
```