---
name: ocr-and-multimodal-vision-deconstructor
description: Complete OCR, spatial UI decomposition, video keyframe analysis, and speech transcription allowing text-only and multimodal AI agents to read, inspect, and understand images, screenshots, videos, and audio.
---

# OCR & Multimodal Vision Deconstruction Engine

This skill empowers **any AI model or agent** (including text-only models without native vision capabilities) to inspect, read, deconstruct, and understand visual media in the Workshop.

## Core Capabilities

1. **High-Precision OCR**: Extracts text from screenshots, UI mockups, documents, and diagrams using RapidOCR (ONNX) with exact bounding boxes and confidence scores.
2. **Spatial UI Decomposition**: Maps text blocks into spatial screen regions (`top-left`, `top-right`, `middle-center`, `bottom-left`) to reconstruct UI layouts, buttons, and navigation bars.
3. **Visual & Theme Deconstruction**: Analyzes dimensions, aspect ratio, dark vs light theme, and dominant 6-color palettes with hex codes.
4. **ANSI & ASCII Terminal Perception**: Renders 24-bit ANSI color previews and high-resolution ASCII luminance art so text-only agents can perceive shapes and diagrams directly in the terminal.
5. **Video OCR & Timeline**: Samples keyframes across video duration, detects UI text changes, and generates a chronological event timeline.
6. **Speech-to-Text Transcription**: Extracts audio with `ffmpeg` and transcribes speech with `faster-whisper` including exact timestamps.

---

## CLI Commands for AI Agents

```bash
# 👁️ 1. Smart Universal Inspector (Auto-detects image, video, audio, or directory)
python scripts/workshop.py see "<path_to_media_or_dir>"

# 📝 2. High-Precision OCR & Spatial Bounding Boxes
python scripts/workshop.py vision ocr "path/to/screenshot.png"
python scripts/workshop.py vision ocr "path/to/screenshot.png" --json

# 🔍 3. Visual Deconstruction for Text-Only Agents (Theme, Palette, Layout)
python scripts/workshop.py vision describe "path/to/ui_mockup.png"

# 🖼️ 4. ASCII Luminance Art Rendering (View visual shapes in text)
python scripts/workshop.py vision ascii "path/to/diagram.png" --width 60

# 🎬 5. Video Storyboard Contact Sheet
python scripts/workshop.py vision storyboard "path/to/demo.mp4" --cols 3 --rows 3

# ⏱️ 6. Video OCR Text Timeline (Chronological UI state changes over time)
python scripts/workshop.py vision video-ocr "path/to/screencast.mp4" --count 8

# 🎙️ 7. Speech-to-Text Audio & Video Transcription
python scripts/workshop.py vision transcribe "path/to/meeting.mp4"
python scripts/workshop.py vision transcribe "path/to/audio.wav" --model base
```

---

## Python API Usage for Autonomous Agents

```python
from scripts.workshop_vision import (
    ocr_image,
    deconstruct_image,
    render_ascii_art,
    video_ocr_timeline,
    transcribe_speech,
    see_media
)
from pathlib import Path

# 1. Extract text and UI layout
ocr_data = ocr_image(Path("screenshot.png"))
print("Extracted Text:", ocr_data["extracted_text"])
print("Top-level buttons/headers:", ocr_data["spatial_layout"]["top"])

# 2. Get full visual brief (theme, palette, layout)
visual_brief = deconstruct_image(Path("mockup.png"))
print(visual_brief["agent_visual_summary"])

# 3. Analyze screencast video timeline
video_data = video_ocr_timeline(Path("screencast.mp4"), sample_count=6)
for event in video_data["timeline"]:
    print(f"[{event['timestamp_human']}] {event['newly_appeared_text']}")
```
