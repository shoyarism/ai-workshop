#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Image Generation CLI & API Engine (BentoML Guide & Multi-Provider Architecture)
Supports:
  1. Local Diffusion: SDXL-Lightning (4-step ultra-fast) & SD 1.5 with 4GB low-VRAM optimizations.
  2. Cloud Engines: Google Imagen 3 / Gemini, Nano Banana, and FLUX Cloud.
"""

import os
import sys
import time
import random
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Ensure output directory
ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_local_diffusion(
    prompt: str,
    negative_prompt: str = "",
    model_id: str = "ByteDance/SDXL-Lightning",
    steps: int = 4,
    guidance_scale: float = 0.0,
    width: int = 1024,
    height: int = 1024,
    seed: Optional[int] = None,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Run local diffusion inference using Hugging Face Diffusers.
    Optimized for consumer GPUs (e.g. GTX 1650 4GB VRAM) via:
      - float16 precision
      - model CPU offload (enable_model_cpu_offload)
      - VAE slicing & attention slicing
    """
    import torch
    from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
    from huggingface_hub import hf_hub_download

    if seed is None or seed < 0:
        seed = random.randint(1000, 99999999)
    generator = torch.Generator(device="cpu").manual_seed(seed)

    print(f"[Local Diffusion] Initializing {model_id}...")
    base = "stabilityai/stable-diffusion-xl-base-1.0"
    repo = "ByteDance/SDXL-Lightning"
    ckpt = "sdxl_lightning_4step_unet.safetensors"

    print("[Local Diffusion] Loading UNet checkpoint & base pipeline with low-VRAM optimizations...")
    unet = UNet2DConditionModel.from_config(base, subfolder="unet").to(torch.float16)
    unet.load_state_dict(torch.load(hf_hub_download(repo, ckpt), map_location="cpu"))
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        base,
        unet=unet,
        torch_dtype=torch.float16,
        variant="fp16"
    )
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")

    # Low-VRAM 4GB optimizations
    if torch.cuda.is_available():
        print("[Local Diffusion] Enabling GPU model CPU offload and attention slicing for GTX 1650 (4GB)...")
        pipe.enable_model_cpu_offload()
        pipe.enable_vae_slicing()
        pipe.enable_attention_slicing()
    else:
        print("[Local Diffusion] CUDA unavailable, using CPU fallback...")
        pipe.to("cpu")

    print(f"[Local Diffusion] Generating image ({steps} steps, seed={seed})...")
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=steps,
        guidance_scale=guidance_scale,
        width=width,
        height=height,
        generator=generator
    ).images[0]

    if output_path is None:
        ts = int(time.time())
        output_path = OUTPUT_DIR / f"local_sdxl_{ts}_{seed}.png"
    
    image.save(output_path)
    print(f"[Local Diffusion] Successfully saved image to: {output_path}")
    return output_path


def generate_gemini_imagen3(
    prompt: str,
    aspect_ratio: str = "1:1",
    api_key: Optional[str] = None,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Generate ultra-photorealistic image via Google Gemini / Imagen 3 API.
    Zero local GPU load, pure cloud execution.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY not found in environment or arguments. Set GEMINI_API_KEY to use Gemini Imagen 3.")

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        print(f"[Cloud Gemini] Requesting Imagen 3 generation for: '{prompt[:60]}...'")
        result = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
                output_mime_type="image/jpeg",
            )
        )
        if not result.generated_images:
            raise RuntimeError("No image returned from Gemini Imagen 3 API.")

        image_bytes = result.generated_images[0].image.image_bytes
        if output_path is None:
            ts = int(time.time())
            output_path = OUTPUT_DIR / f"gemini_imagen3_{ts}.jpg"
        
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"[Cloud Gemini] Successfully saved Imagen 3 output to: {output_path}")
        return output_path

    except Exception as e:
        # Fallback to google-generativeai package if new genai SDK differs
        print(f"[Cloud Gemini] Retrying via generativeai fallback ({e})...")
        import google.generativeai as gai
        gai.configure(api_key=key)
        imagen = gai.ImageGenerationModel("imagen-3.0-generate-002")
        result = imagen.generate_images(prompt=prompt, number_of_images=1, aspect_ratio=aspect_ratio)
        if output_path is None:
            ts = int(time.time())
            output_path = OUTPUT_DIR / f"gemini_imagen3_{ts}.jpg"
        result.images[0].save(str(output_path))
        print(f"[Cloud Gemini] Successfully saved Imagen 3 output to: {output_path}")
        return output_path


def generate_cloud_flux(
    prompt: str,
    aspect_ratio: str = "1:1",
    seed: Optional[int] = None,
    hf_token: Optional[str] = None,
    output_path: Optional[Path] = None
) -> Path:
    """
    Generate via FLUX.1 / FLUX.2 Cloud inference.
    No local GPU load.
    """
    import urllib.parse
    import urllib.request
    import json

    token = hf_token or os.environ.get("HF_TOKEN")
    print(f"[Cloud FLUX] Invoking cloud FLUX inference space...")
    
    try:
        from gradio_client import Client
        client = Client("black-forest-labs/FLUX.1-schnell", hf_token=token)
        res = client.predict(
            prompt=prompt,
            seed=seed or random.randint(0, 999999),
            randomize_seed=True,
            width=1024,
            height=1024,
            num_inference_steps=4,
            api_name="/infer"
        )
        img_path = res[0]
        if output_path is None:
            ts = int(time.time())
            output_path = OUTPUT_DIR / f"cloud_flux_{ts}.webp"
        
        import shutil
        shutil.copyfile(img_path, output_path)
        print(f"[Cloud FLUX] Successfully saved FLUX output to: {output_path}")
        return output_path
    except Exception as err:
        print(f"[Cloud FLUX] Gradio space fallback to direct cloud stream: {err}")
        clean_p = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{clean_p}?model=flux&width=1024&height=1024&nologo=true"
        if output_path is None:
            ts = int(time.time())
            output_path = OUTPUT_DIR / f"cloud_flux_{ts}.jpg"
        import requests
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=60)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(resp.content)
        print(f"[Cloud FLUX] Successfully retrieved cloud FLUX image to: {output_path}")
        return output_path


def generate_nano_banana(
    prompt: str,
    output_path: Optional[Path] = None
) -> Path:
    """
    Fast creative cloud generation (Nano Banana / turbo preset).
    """
    import urllib.parse
    import requests

    print(f"[Nano Banana] Generating with creative fast model for: '{prompt[:50]}...'")
    clean_p = urllib.parse.quote(f"{prompt}, high aesthetic, ultra detailed, award winning")
    url = f"https://image.pollinations.ai/prompt/{clean_p}?model=turbo&width=1024&height=1024&nologo=true"
    if output_path is None:
        ts = int(time.time())
        output_path = OUTPUT_DIR / f"nano_banana_{ts}.jpg"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=60)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(resp.content)
    print(f"[Nano Banana] Image saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Universal Open-Source & Cloud Image Generator")
    parser.add_argument("--prompt", type=str, required=True, help="Image prompt description")
    parser.add_argument("--negative-prompt", type=str, default="", help="Negative prompt")
    parser.add_argument(
        "--provider",
        type=str,
        default="cloud_flux",
        choices=["local", "gemini", "imagen3", "cloud_flux", "nano_banana"],
        help="Generation provider: 'local' (SDXL-Lightning on GPU), 'gemini' / 'imagen3' (Google Cloud), 'cloud_flux' (FLUX Cloud), or 'nano_banana'"
    )
    parser.add_argument("--steps", type=int, default=4, help="Inference steps (default: 4 for lightning)")
    parser.add_argument("--aspect-ratio", type=str, default="1:1", choices=["1:1", "3:4", "4:3", "16:9", "9:16"])
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")
    parser.add_argument("--api-key", type=str, default=None, help="Gemini API Key (optional)")

    args = parser.parse_args()

    out_p = Path(args.output) if args.output else None

    if args.provider == "local":
        generate_local_diffusion(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            steps=args.steps,
            seed=args.seed,
            output_path=out_p
        )
    elif args.provider in ("gemini", "imagen3"):
        generate_gemini_imagen3(
            prompt=args.prompt,
            aspect_ratio=args.aspect_ratio,
            api_key=args.api_key,
            output_path=out_p
        )
    elif args.provider == "cloud_flux":
        generate_cloud_flux(
            prompt=args.prompt,
            aspect_ratio=args.aspect_ratio,
            seed=args.seed,
            output_path=out_p
        )
    elif args.provider == "nano_banana":
        generate_nano_banana(
            prompt=args.prompt,
            output_path=out_p
        )


if __name__ == "__main__":
    main()
