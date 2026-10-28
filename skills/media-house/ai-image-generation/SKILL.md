---
name: ai-image-generation
description: Generate and edit images with AI — Flux 2 (Klein/Pro/Dev/Flash/Turbo/Max), Nano Banana 2/Pro, GPT Image 2, Qwen Image, Seedream 4/5, Dreamina 4-0, Midjourney, Ideogram, Stable Diffusion, Recraft, and more. Covers text-to-image, image-to-image, inpainting, outpainting, relighting, upscaling, typography rendering, brand styling, and multi-reference composition. Triggers on: generate image, text to image, AI image, image generation, flux, nano banana, gpt image, midjourney, ideogram, stable diffusion, seedream, dreamina, i2i, edit image, inpaint, outpaint, upscale, typography, brand styling, product photography.
---

# AI Image Generation

Generate and edit images using AI models via RunComfy, local Stable Diffusion, or cloud APIs. Covers the full image model catalog, prompting patterns per model, and when to route to each model based on the user's actual intent.

## When to trigger

- User wants to generate an image from a text prompt
- User wants to edit/restyle an existing image
- User mentions Flux, Nano Banana, GPT Image, Midjourney, Ideogram, Stable Diffusion, Seedream, Dreamina
- User needs product photography, hero images, social graphics, typography, or brand assets
- User wants inpainting (fill region) or outpainting (extend canvas)

## Model catalog & routing guide

| Model | Best for | Strengths | Not for |
|---|---|---|---|
| **Flux 2 Pro** | Premium quality, complex scenes | Best overall fidelity, prompt adherence | Sub-second iteration |
| **Flux 2 Dev** | Open-weight, local hosting | Strong quality, controllable | Fast iteration |
| **Flux 2 Schnell / Flash / Turbo** | Speed | Sub-second generation | Maximum fidelity |
| **Flux 2 Max** | Ultra-high resolution | Largest output, detail | Speed, cost |
| **Flux 2 Klein** | Distilled fast variant | 4-8 steps iteration, brand styling | Polished final (use ~25 steps) |
| **Nano Banana 2** | Rapid iteration, typography | In-image text rendering, predictable framing | Complex artistic scenes |
| **Nano Banana Pro** | Premium editing | Character reference, identity preservation | Text-to-image from scratch |
| **GPT Image 2** | Typography, layout, precision | In-image text, multi-ref up to 10 images, design | Photorealism (use Flux) |
| **Qwen Image** | General purpose | Strong Chinese/English understanding | Specialized styles |
| **Seedream 4 / 5** | Aesthetic, stylized | Artistic, fashion, cinematic | Technical diagrams |
| **Dreamina 4-0** | Marketing, ads | Product shots, e-commerce | Fine art |
| **Ideogram** | Typography, logos | Best-in-class text in images | Photoreal humans |
| **Midjourney v6** | Artistic, cinematic | Aesthetic quality, style consistency | API access limited |
| **Stable Diffusion XL** | Local, controllable | LoRA, ControlNet, custom models | Out-of-box quality |

## Text-to-image (t2i)

### Flux 2 via RunComfy CLI
```bash
runcomfy run blackforestlabs/flux-2-klein/9b/text-to-image \
  --prompt "A cinematic portrait of a cyberpunk street vendor at night, neon signs, volumetric fog, 35mm film, shot on Leica M6" \
  --resolution 1024x1024 --steps 8 --output-dir ./outputs
```

### OpenAI GPT Image 2
```python
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="gpt-image-2",
    prompt="A minimalist landing page hero image, clean typography, whitespace, soft shadows",
    size="1024x1024",
    quality="high",
    n=1
)
image_url = response.data[0].url
```

### Midjourney (via Discord or API)
```
/imagine prompt: cyberpunk street vendor at night, neon signs, volumetric fog, 35mm film --ar 16:9 --v 6.0 --style raw
```

## Image-to-image (i2i) / edit

### Nano Banana Edit (batch, identity-preserving)
```bash
runcomfy run google/nano-banana-2/edit \
  --image input.jpg \
  --prompt "Change the background to a rainy Tokyo street, keep the subject identical" \
  --batch-up-to 20
```

### Flux Kontext Pro (single-reference, precise local edit)
```bash
runcomfy run blackforestlabs/flux-1-kontext/pro/edit \
  --image input.jpg \
  --prompt "Replace the coffee cup with a glowing crystal, keep everything else identical"
```

### GPT Image 2 Edit
```python
response = client.images.edit(
    model="gpt-image-2",
    image=open("input.png", "rb"),
    prompt="Rewrite the headline text to 'Summer Sale 50% Off', keep the layout identical",
    mask=open("mask.png", "rb"),  # optional mask for region
    n=1
)
```

## Inpainting (mask-driven region edit)

### Z-Image Turbo Inpaint
```bash
runcomfy run tongyi/z-image-turbo/inpaint \
  --image input.jpg \
  --mask mask.png \
  --prompt "Remove the watermark, fill with matching texture"
```

### Nano Banana 2 Edit (no mask, spatial language)
```bash
runcomfy run google/nano-banana-2/edit \
  --image input.jpg \
  --prompt "Remove the person in the background, fill with cafe interior"
```

## Outpainting (extend canvas)

### Nano Banana 2 Edit (default)
```bash
runcomfy run google/nano-banana-2/edit \
  --image square.jpg \
  --prompt "Extend this to 16:9 widescreen, add cinematic environment around the subject"
```

### GPT Image 2 Edit (multi-ref style matching)
```bash
runcomfy run openai/gpt-image-2/edit \
  --image portrait.jpg \
  --prompt "Outpaint to landscape orientation, preserve subject identity and lighting"
```

## Upscaling

### Fal Upscale
```bash
runcomfy run fal/upscale \
  --image lowres.jpg \
  --scale 4 --output-dir ./outputs
```

## Typography & brand styling

### Flux 2 Klein (brand styling, 4-8 steps)
```bash
runcomfy run blackforestlabs/flux-2-klein/4b/text-to-image \
  --prompt "Minimalist brand poster, 'AURORA' in bold sans-serif typography, deep navy background, gold accent line, premium aesthetic" \
  --steps 6
```

### GPT Image 2 (in-image text precision)
```python
response = client.images.generate(
    model="gpt-image-2",
    prompt="A coffee shop menu board with handwritten chalk text: 'Daily Special - Lavender Latte $5', warm wooden background, natural lighting"
)
```

## Product photography

### Studio shot
```
Product shot of [product], studio lighting, clean white background, soft shadows, 85mm lens, f/2.8, high resolution, commercial photography
```

### Lifestyle scene
```
[Product] in a cozy living room, natural window light, lifestyle aesthetic, shallow depth of field, warm tones, editorial photography
```

### Virtual try-on / model wearing
```
A diverse model wearing [clothing item], studio lighting, neutral expression, full body shot, commercial fashion photography
```

## Prompting best practices

| Element | Guidance |
|---|---|
| Subject first | Lead with the main subject, then environment |
| Lighting | Specify (studio softbox, window light, golden hour, neon, volumetric) |
| Camera | Lens (35mm, 85mm, 24mm), aperture, film stock (Kodak Portra, Fujifilm) |
| Style | Cinematic, editorial, minimalist, brutalist, anime, photorealistic |
| Negative | Avoid "blurry, low quality, distorted, extra fingers" unless using SD |
| Aspect ratio | Match target (1:1 social, 16:9 video, 9:16 mobile/stories) |

## Multi-reference composition

### GPT Image 2 (up to 10 reference images)
```python
response = client.images.edit(
    model="gpt-image-2",
    image=[ref1.png, ref2.png, ref3.png],
    prompt="Combine the character from image 1, the outfit from image 2, and the pose from image 3 into a single cohesive scene",
)
```

### Nano Banana Pro (identity preservation)
Best for keeping a specific person/character consistent across multiple generated images.

## Decision checklist

- [ ] Intent identified (t2i vs i2i vs inpaint vs outpaint vs upscale)
- [ ] Model chosen based on quality/speed/use-case trade-off
- [ ] Aspect ratio set for target platform
- [ ] Reference images gathered (if multi-ref or identity preservation)
- [ ] Typography needs identified (GPT Image 2 or Flux Klein)
- [ ] Output resolution and steps configured
- [ ] Negative prompt considered (for SD models)

## Related Workshop skills

- `image-edit` — smart router for image edit models
- `image-inpainting` — mask-driven region editing
- `image-outpainting` — canvas extension
- `image-to-code` — turn generated images into websites
- `imagegen-frontend-web` — premium landing page design references (one image per section)
- `imagegen-frontend-mobile` — premium mobile app screen concepts
- `media-use` — resolve and manage image assets
- `og-image-design` — social sharing image design
- `youtube-thumbnail-design` — YouTube thumbnail design
