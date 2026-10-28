---
name: samle-motion-graphics-video
description: "End-to-end motion graphic video production pipeline using HTML5/CSS3/GSAP, Web Audio API TTS sync, and headless browser-to-FFmpeg rendering. Produces broadcast-ready 1080p@24fps videos with deterministic timeline seeking."
allowed-tools: Read Write Edit Glob Grep run_command
---

# Sample Motion Graphics Video Pipeline

A deterministic, production-grade pipeline for generating motion graphic videos using web-native technologies (HTML5/CSS3/GSAP), Neural TTS with sentence-level timestamps, and headless browser-to-FFmpeg direct piping.

## 1. Core Visual Architecture

### Mode A: Clean Corporate (product launch, promo)
1. **White/Cream Canvas** (`#FFFFFF` - `#F8F9FA`) with subtle gradient
2. **Bold Sans-Serif Typography** (Inter, Helvetica Now, or Barlow Black)
3. **GSAP ScrollTrigger/Pin animations** for section reveals
4. **Particle/Shape animations** as background texture
5. **Lower Third overlays** with brand colors

### Mode B: Dark Editorial (documentary, tech)
1. **Dark Slate Ground** (`#0F1117` - `#1A1D23`)
2. **Accent color highlights** (cyan #00D4FF, orange #FF6B35)
3. **Motion lines, geometric reveals**
4. **Counter animations** for statistics

## 2. Production Workflow

### Step 1: Script → Audio Sync
1. Write script with sentence timestamps
2. Synthesize TTS (edge-tts or ElevenLabs)
3. Export `subtitles.json` with start/end times per sentence
4. Mix voiceover + BGM with dynamic ducking

### Step 2: HTML Composition
1. Fixed 1920×1080 stage
2. GSAP timeline with `paused: true`
3. `window.seekToTime(t)` function for deterministic playback
4. Anchor all animations to audio timestamps

### Step 3: Render
1. Headless Chromium → FFmpeg image2pipe
2. 1080p@24fps, H.264, CRF 20

## 3. Quick Start

```bash
# Generate audio from script
node scripts/tts.js --script script.md --output audio.mp3

# Render video
python render.py --html composition.html --audio audio.mp3 --output video.mp4
```

## 4. Key Files
- `composition.html` — Main animation canvas
- `scripts/tts.js` — TTS synthesis with timestamps
- `render.py` — FFmpeg pipe renderer
- `subtitles.json` — Sentence-level timing data
