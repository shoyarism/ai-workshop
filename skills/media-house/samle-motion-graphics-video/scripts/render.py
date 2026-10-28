#!/usr/bin/env python3
"""
render.py — Headless browser to FFmpeg motion graphic renderer.

Usage:
  python render.py --html sample/composition.html --audio audio.mp3 --output video.mp4
  python render.py --html sample/composition.html --output video.mp4  # no audio

Pipeline:
  1. Open HTML in headless Chromium via Playwright
  2. Call seekToTime(t) at each frame
  3. Capture screenshot → pipe to FFmpeg image2pipe
  4. Mux with audio → final MP4
"""

import asyncio
import json
import subprocess
import sys
import argparse
import os
import tempfile
import shutil
from pathlib import Path

# Frame settings
WIDTH = 1920
HEIGHT = 1080
FPS = 24
CRF = 20
PRESET = "veryfast"

async def render_frame(page, t, frame_dir, frame_num):
    """Seek to time t and capture a screenshot."""
    await page.evaluate(f"window.seekToTime({t})")
    await page.wait_for_timeout(50)  # let GSAP settle
    screenshot = await page.screenshot(full_page=False)
    # Write PNG frame to temp directory
    frame_path = os.path.join(frame_dir, f"frame_{frame_num:04d}.png")
    with open(frame_path, "wb") as f:
        f.write(screenshot)
    return frame_path

async def render_video(html_path, audio_path, output_path, duration=None):
    """Render HTML composition to MP4 via Playwright + FFmpeg."""
    from playwright.async_api import async_playwright

    # Calculate duration from audio if not provided
    if duration is None and audio_path and os.path.exists(audio_path):
        duration = get_audio_duration(audio_path)
    if duration is None:
        duration = 26  # default: 26 seconds

    total_frames = int(duration * FPS)

    # Create temp dir for PNG frames
    frame_dir = tempfile.mkdtemp(prefix="motion_frames_")
    total_frames = int(duration * FPS)

    print(f"Rendering {total_frames} frames ({duration}s @ {FPS}fps)...")
    print(f"Frames dir: {frame_dir}")
    print(f"Output: {output_path}")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        await page.goto(f"file://{os.path.abspath(html_path)}")
        await page.wait_for_timeout(1000)  # wait for DOM + GSAP init

        for frame_num in range(total_frames):
            t = frame_num / FPS
            await render_frame(page, t, frame_dir, frame_num)

            if frame_num % 24 == 0:
                print(f"  Frame {frame_num}/{total_frames} ({t:.1f}s)")

        await browser.close()

    # Combine PNG frames into video using FFmpeg
    print("Encoding video...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frame_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", PRESET,
        "-crf", str(CRF),
        "-r", str(FPS),
        "-movflags", "+faststart",
        output_path
    ]

    # Add audio if provided
    if audio_path and os.path.exists(audio_path):
        ffmpeg_cmd += ["-i", audio_path, "-c:a", "aac", "-b:a", "192k", "-shortest"]

    proc = await asyncio.create_subprocess_exec(
        *ffmpeg_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    # Cleanup frames
    shutil.rmtree(frame_dir, ignore_errors=True)

    if proc.returncode != 0:
        print(f"FFmpeg error: {stderr.decode()}")
        sys.exit(1)

    print(f"✓ Done: {output_path}")
    print(f"  Size: {os.path.getsize(output_path):,} bytes")

def get_audio_duration(audio_path):
    """Get audio duration using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True
        )
        return float(result.stdout.strip())
    except Exception:
        return None

def generate_subtitles(script_path):
    """Parse script.md and generate subtitles.json with timestamps."""
    with open(script_path) as f:
        lines = f.readlines()

    scenes = []
    current_scene = None
    current_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith("## SCENE"):
            if current_scene:
                current_scene["lines"] = current_lines
                scenes.append(current_scene)
            parts = line.replace("##", "").strip().split(" - ")
            current_scene = {"id": len(scenes), "label": parts[0].strip()}
            if len(parts) > 1:
                current_scene["time"] = parts[1].strip()
            current_lines = []
        elif line and not line.startswith("#"):
            current_lines.append(line)

    if current_scene:
        current_scene["lines"] = current_lines
        scenes.append(current_scene)

    # Assign timestamps (simplified: 4s per scene)
    subtitles = []
    t = 0
    for scene in scenes:
        for line in scene["lines"]:
            if line.startswith("SCENE"):
                continue
            duration = max(1.5, len(line.split()) * 0.3)
            subtitles.append({
                "start": round(t, 3),
                "end": round(t + duration, 3),
                "text": line
            })
            t += duration + 0.2

    return subtitles

def main():
    parser = argparse.ArgumentParser(description="Motion Graphic Video Renderer")
    parser.add_argument("--html", required=True, help="Path to composition HTML")
    parser.add_argument("--audio", default=None, help="Path to audio MP3")
    parser.add_argument("--output", default="output.mp4", help="Output video path")
    parser.add_argument("--duration", type=float, default=None, help="Override duration (seconds)")
    parser.add_argument("--script", default=None, help="Script MD for subtitle generation")
    args = parser.parse_args()

    # Generate subtitles if script provided
    if args.script and os.path.exists(args.script):
        subs = generate_subtitles(args.script)
        sub_path = args.output.replace(".mp4", "_subtitles.json")
        with open(sub_path, "w") as f:
            json.dump(subs, f, indent=2)
        print(f"Subtitles: {sub_path}")

    # Run render
    asyncio.run(render_video(args.html, args.audio, args.output, args.duration))

if __name__ == "__main__":
    main()
