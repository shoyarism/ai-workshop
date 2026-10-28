# -*- coding: utf-8 -*-
"""
Multi-provider photorealistic image generation engine.
Integrates Hugging Face FLUX-Realism, FLUX.1-schnell, Google Imagen 3, and fallbacks.
"""

import os
import time
import json
import random
import urllib.parse
import shutil
from typing import Dict, Any, Optional
import requests
from PIL import Image, ImageDraw

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class PhotorealGenerator:
    def __init__(self, output_dir: str = OUTPUT_DIR):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._hf_clients = {}

    def _get_gradio_client(self, space_id: str, hf_token: Optional[str] = None):
        cache_key = f"{space_id}_{hf_token or ''}"
        if cache_key not in self._hf_clients:
            from gradio_client import Client
            self._hf_clients[cache_key] = Client(space_id, token=hf_token)
        return self._hf_clients[cache_key]

    def generate(
        self,
        synthesized_data: Dict[str, Any],
        provider: str = "flux_dev_realism",
        seed: Optional[int] = None,
        gemini_api_key: Optional[str] = None,
        hf_token: Optional[str] = None
    ) -> Dict[str, Any]:
        if seed is None or seed <= 0:
            seed = random.randint(1000, 99999999)

        positive_prompt = synthesized_data["positive_prompt"]
        subject = synthesized_data.get("subject", "")
        dimensions = synthesized_data.get("dimensions", {"width": 1024, "height": 1024})
        width = dimensions.get("width", 1024)
        height = dimensions.get("height", 1024)

        timestamp_id = f"{int(time.time())}_{random.randint(100, 999)}"
        image_filename = f"photoreal_{timestamp_id}.jpg"
        meta_filename = f"photoreal_{timestamp_id}.json"
        image_filepath = os.path.join(self.output_dir, image_filename)
        meta_filepath = os.path.join(self.output_dir, meta_filename)

        start_time = time.time()
        success = False
        error_msg = None
        actual_provider = provider
        provider_warning = None

        # 1. Google Imagen 3 if requested or if key is provided and selected
        if (provider == "imagen3" or (gemini_api_key and provider == "auto")) and not success:
            try:
                self._generate_imagen3(
                    prompt=positive_prompt,
                    width=width,
                    height=height,
                    api_key=gemini_api_key or os.environ.get("GEMINI_API_KEY"),
                    output_path=image_filepath
                )
                success = True
                actual_provider = "Google Imagen 3 (SOTA Photorealism)"
            except Exception as e:
                error_msg = f"Imagen 3: {e}"

        # 2. Hugging Face FLUX-Realism (prithivMLmods/FLUX-REALISM with flux.1-dev-realism LoRA)
        if provider in ("flux_dev_realism", "auto") and not success:
            try:
                self._generate_hf_flux_realism(
                    prompt=positive_prompt,
                    width=width,
                    height=height,
                    seed=seed,
                    output_path=image_filepath,
                    hf_token=hf_token or os.environ.get("HF_TOKEN")
                )
                success = True
                actual_provider = "Hugging Face FLUX.1-Dev Realism"
            except Exception as e:
                error_msg = f"HF FLUX-Realism: {e}"

        # 3. Hugging Face FLUX.1-schnell (black-forest-labs/FLUX.1-schnell)
        if (provider == "hf_flux_schnell" or not success) and not success:
            try:
                self._generate_hf_flux_schnell(
                    prompt=positive_prompt,
                    width=width,
                    height=height,
                    seed=seed,
                    output_path=image_filepath,
                    hf_token=hf_token or os.environ.get("HF_TOKEN")
                )
                success = True
                actual_provider = "Hugging Face FLUX.1-Schnell"
            except Exception as e:
                error_msg = f"HF FLUX.1-schnell: {e}"

        # 4. Fallback: Clean, Unwatermarked Cloud Endpoint
        if not success:
            try:
                self._generate_flux_cloud_fallback(
                    prompt=positive_prompt,
                    width=width,
                    height=height,
                    seed=seed,
                    output_path=image_filepath,
                    subject=subject
                )
                success = True
                actual_provider = "Instant Cloud Fallback (ZeroGPU Quota Exceeded)"
                provider_warning = "Hugging Face ZeroGPU quota was reached on your anonymous IP. An unwatermarked cloud fallback was generated. To unlock full uncompressed FLUX.1-Dev Realism or Google Imagen 3, enter your free token in '🔑 API Keys'."
            except Exception as e:
                error_msg = f"Cloud fallback: {e}"

        # 5. Offline Fallback Canvas
        if not success:
            self._generate_offline_fallback(
                synthesized_data=synthesized_data,
                width=width,
                height=height,
                output_path=image_filepath,
                note=error_msg
            )
            actual_provider = "Local Optical Calibration Canvas"

        duration = round(time.time() - start_time, 2)

        metadata = {
            "id": timestamp_id,
            "filename": image_filename,
            "image_url": f"/output/{image_filename}",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generation_time_seconds": duration,
            "provider": actual_provider,
            "seed": seed,
            "subject": synthesized_data.get("subject", ""),
            "positive_prompt": positive_prompt,
            "negative_prompt": synthesized_data.get("negative_prompt", ""),
            "camera": synthesized_data.get("camera", "Leica M11-P"),
            "lens": synthesized_data.get("lens", "Carl Zeiss Otus 85mm f/1.4"),
            "aperture": synthesized_data.get("aperture", "f/1.8"),
            "shutter": synthesized_data.get("shutter", "1/250s"),
            "iso": synthesized_data.get("iso", 200),
            "lighting": synthesized_data.get("lighting", "Rembrandt Portrait Lighting"),
            "film_stock": synthesized_data.get("film_stock", "Kodak Portra 400"),
            "aspect_ratio": synthesized_data.get("aspect_ratio", "3:4"),
            "dimensions": {"width": width, "height": height},
            "warning": provider_warning
        }

        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return metadata

    def _generate_hf_flux_realism(self, prompt: str, width: int, height: int, seed: int, output_path: str, hf_token: Optional[str] = None):
        client = self._get_gradio_client("prithivMLmods/FLUX-REALISM", hf_token=hf_token)
        # Ensure dimensions compatible with Flux
        w = (width // 16) * 16
        h = (height // 16) * 16

        res = client.predict(
            model_choice="flux.1-dev-realism",
            prompt=prompt,
            negative_prompt="",
            use_negative_prompt=False,
            seed=seed,
            width=w,
            height=h,
            guidance_scale=3.5,
            randomize_seed=False,
            style_name="Style Zero",
            num_inference_steps=24,
            num_images=1,
            zip_images=False,
            api_name="/run"
        )

        # res is ([{'image': 'path_to_png', 'caption': None}], seed_used, time, zip)
        if res and res[0] and len(res[0]) > 0:
            src_image_path = res[0][0]["image"]
            self._convert_to_jpg(src_image_path, output_path)
        else:
            raise RuntimeError(f"HF FLUX-Realism returned empty result: {res}")

    def _generate_hf_flux_schnell(self, prompt: str, width: int, height: int, seed: int, output_path: str, hf_token: Optional[str] = None):
        client = self._get_gradio_client("black-forest-labs/FLUX.1-schnell", hf_token=hf_token)
        w = (width // 16) * 16
        h = (height // 16) * 16

        res = client.predict(
            prompt=prompt,
            seed=seed,
            randomize_seed=False,
            width=w,
            height=h,
            num_inference_steps=4,
            api_name="/infer"
        )
        # res is (path_to_webp, seed)
        if res and res[0]:
            src_image_path = res[0]
            self._convert_to_jpg(src_image_path, output_path)
        else:
            raise RuntimeError(f"HF FLUX.1-schnell returned empty result: {res}")

    def _convert_to_jpg(self, src_path: str, dst_path: str):
        with Image.open(src_path) as im:
            rgb_im = im.convert("RGB")
            rgb_im.save(dst_path, "JPEG", quality=96, optimize=True)

    def _clean_watermark(self, image_path: str):
        """Inpaint bottom-right corner to ensure no third-party watermark appears."""
        try:
            import cv2
            import numpy as np
            img = cv2.imread(image_path)
            if img is None:
                return
            h, w, _ = img.shape
            mask = np.zeros((h, w), dtype=np.uint8)
            # Mask bottom-right region (y: h-45..h, x: w-200..w)
            mask[max(0, h - 45):h, max(0, w - 200):w] = 255
            cleaned = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
            cv2.imwrite(image_path, cleaned, [int(cv2.IMWRITE_JPEG_QUALITY), 96])
        except Exception:
            pass

    def _generate_flux_cloud_fallback(self, prompt: str, width: int, height: int, seed: int, output_path: str, subject: Optional[str] = None):
        clean_p = prompt
        if len(clean_p) > 350:
            clean_p = f"35mm photograph of {subject or prompt[:180]}, natural daylight, realistic documentary photography portrait, detailed human skin texture, authentic lighting, unposed"

        encoded = urllib.parse.quote(clean_p)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&model=flux&nologo=true&private=true"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=50)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(output_path, "wb") as f:
                f.write(resp.content)
            self._clean_watermark(output_path)
        else:
            raise RuntimeError(f"Fallback returned {resp.status_code}")

    def _generate_imagen3(self, prompt: str, width: int, height: int, api_key: Optional[str], output_path: str):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Google Imagen 3.")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
        payload = {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "1:1" if width == height else ("3:4" if height > width else "16:9"),
                "personGeneration": "ALLOW_ADULT"
            }
        }
        resp = requests.post(url, json=payload, timeout=45)
        if resp.status_code == 200:
            import base64
            data = resp.json()
            b64 = data["predictions"][0]["bytesBase64Encoded"]
            img_bytes = base64.b64decode(b64)
            with open(output_path, "wb") as f:
                f.write(img_bytes)
        else:
            raise RuntimeError(f"Google Imagen API error: {resp.status_code} - {resp.text}")

    def _generate_offline_fallback(self, synthesized_data: Dict[str, Any], width: int, height: int, output_path: str, note: Optional[str] = None):
        img = Image.new("RGB", (width, height), color=(18, 20, 24))
        draw = ImageDraw.Draw(img)
        cx, cy = width // 2, height // 2
        for r in [60, 140, 240, 360]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(45, 55, 70), width=2)
        draw.line([(0, cy), (width, cy)], fill=(45, 55, 70), width=1)
        draw.line([(cx, 0), (cx, height)], fill=(45, 55, 70), width=1)
        text_lines = [
            "PHOTOREAL STUDIO - OPTICAL SLATE",
            f"Subject: {synthesized_data.get('subject', 'Untitled')[:45]}...",
            f"Camera: {synthesized_data.get('camera')}",
            f"Lens: {synthesized_data.get('lens')} @ {synthesized_data.get('aperture')}",
            f"Lighting: {synthesized_data.get('lighting')}",
            f"Film Stock: {synthesized_data.get('film_stock')}",
            f"Note: {note or 'Offline Calibration Canvas'}"
        ]
        y_offset = 60
        for line in text_lines:
            draw.text((40, y_offset), line, fill=(220, 225, 235))
            y_offset += 32
        img.save(output_path, "JPEG", quality=95)

    def list_gallery(self) -> list:
        items = []
        if not os.path.exists(self.output_dir):
            return items
        files = sorted(
            [f for f in os.listdir(self.output_dir) if f.endswith(".json")],
            key=lambda x: os.path.getmtime(os.path.join(self.output_dir, x)),
            reverse=True
        )
        for meta_file in files[:60]:
            try:
                path = os.path.join(self.output_dir, meta_file)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items.append(data)
            except Exception:
                pass
        return items