---
name: multimodal-vision-and-media-inspector
description: Inspect, analyze, OCR, storyboard, and transcribe images, videos, audio, and documents across the Workshop. Empowers text-only and multimodal AI models to see and understand visual media.
---

# Multimodal Vision & Media Inspector Skill

This skill governs how any autonomous agent (Antigravity, Claude Code, OpenCode, OpenClaw, or text-only LLMs) inspects, visualizes, deconstructs, and understands media (images, UI screenshots, video recordings, audio tracks, and documents) in the Workshop.

---

## 1. Quick Master Commands

```bash
# 👁️ 1. Smart Multi-Pass Inspector (Auto-detects Image / Video / Audio / Directory)
python scripts/workshop.py see "<path_to_media>"
python scripts/workshop.py see "path/to/screenshot.png"
python scripts/workshop.py see "path/to/demo.mp4"

# 📝 2. High-Precision ONNX OCR & Spatial Layout Decomposition
python scripts/workshop.py vision ocr "<image_path>"
python scripts/workshop.py vision ocr "<image_path>" --json

# 🔍 3. Visual & Theme Deconstruction for Text-Only LLMs (Theme, Dimensions, Palette, UI regions)
python scripts/workshop.py vision describe "<image_path>"

# 🖼️ 4. ASCII Luminance Art (View shapes and charts in plain text)
python scripts/workshop.py vision ascii "<image_path>" --width 60

# 🎬 5. Video Keyframe Extraction & Storyboard Contact Sheet
python scripts/workshop.py vision frames "<video_path>" --count 8
python scripts/workshop.py vision storyboard "<video_path>" --cols 3 --rows 3

# ⏱️ 6. Video OCR Text Timeline (Chronological UI and text changes over time)
python scripts/workshop.py vision video-ocr "<video_path>" --count 8

# 🎙️ 7. Audio Extraction & Speech-to-Text Transcription
python scripts/workshop.py vision transcribe "<audio_or_video_path>"
python scripts/workshop.py vision transcribe "<audio_or_video_path>" --model base
```

---

## 2. Multi-Pass Visual Inspection Protocol for AI Agents

When tasked with reviewing a UI layout, inspecting an image, or analyzing a video demonstration:

1. **Reconnaissance & Visual Decomposition**:
   - Run `python scripts/workshop.py see "<file>"` or `python scripts/workshop.py vision describe "<image>"` to get dimensions, theme (Dark/Light mode), dominant color hex codes, and ANSI preview.
2. **Text & OCR Verification**:
   - Run `python scripts/workshop.py vision ocr "<image>"` to extract all text lines along with their spatial screen zones (`[top-left]`, `[middle-center]`, `[bottom-right]`).
3. **Video Storyboarding & Timeline**:
   - For video demonstrations, generate a storyboard contact sheet (`python scripts/workshop.py vision storyboard "<video>"`) and extract the chronological text timeline (`python scripts/workshop.py vision video-ocr "<video>"`).
4. **Speech Understanding**:
   - For screencasts or audio recordings, run `python scripts/workshop.py vision transcribe "<media>"` to generate timecoded transcriptions.
