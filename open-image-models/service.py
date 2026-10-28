# -*- coding: utf-8 -*-
"""
BentoML Image Generation Service for Open-Source & Cloud Models.
Compatible with BentoML 1.3+ / 1.4+ service decorator standard.
"""

import os
import bentoml
from pathlib import Path
from typing import Optional
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@bentoml.service(
    name="image_generation_service",
    resources={"gpu": 1}
)
class ImageGenService:
    def __init__(self):
        self.pipe = None

    def _get_pipeline(self):
        if self.pipe is None:
            import torch
            from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
            from huggingface_hub import hf_hub_download

            base = "stabilityai/stable-diffusion-xl-base-1.0"
            repo = "ByteDance/SDXL-Lightning"
            ckpt = "sdxl_lightning_4step_unet.safetensors"

            unet = UNet2DConditionModel.from_config(base, subfolder="unet").to(torch.float16)
            unet.load_state_dict(torch.load(hf_hub_download(repo, ckpt), map_location="cpu"))

            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                base,
                unet=unet,
                torch_dtype=torch.float16,
                variant="fp16"
            )
            self.pipe.scheduler = EulerDiscreteScheduler.from_config(
                self.pipe.scheduler.config,
                timestep_spacing="trailing"
            )
            if torch.cuda.is_available():
                self.pipe.enable_model_cpu_offload()
                self.pipe.enable_vae_slicing()
                self.pipe.enable_attention_slicing()
            else:
                self.pipe.to("cpu")
        return self.pipe

    @bentoml.api
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        steps: int = 4,
        guidance_scale: float = 0.0,
        seed: Optional[int] = None
    ) -> Image.Image:
        """
        Generate image using SDXL-Lightning 4-step via BentoML API.
        """
        import torch
        pipe = self._get_pipeline()
        generator = torch.Generator(device="cpu").manual_seed(seed) if seed else None
        
        result = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        return result.images[0]
