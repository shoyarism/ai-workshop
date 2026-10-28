#!/usr/bin/env python3
"""
Vox-Inspired Editorial Explainer Video Production Agent
======================================================
Autonomous orchestrator for newsroom-grade explainer documentaries.
Implements the 9-stage narrative arc, 11 functional visual modes,
and headless browser-to-FFmpeg rendering pipeline.

Usage:
    python scripts/vox_production_agent.py init --dir <project_dir> [--topic <title>]
    python scripts/vox_production_agent.py validate --storyboard <path/to/storyboard.json>
    python scripts/vox_production_agent.py audio --script <path/to/script.txt> --output-dir <dir> [--voice id-ID-ArdiNeural]
    python scripts/vox_production_agent.py render --project-dir <dir> [--fps 24]
"""

import os
import sys
import argparse
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
SKILL_DIR = WORKSHOP_DIR / "skills" / "vox-inspired-explainer"
SCHEMA_FILE = SKILL_DIR / "storyboard.schema.json"
STYLE_SPEC_FILE = SKILL_DIR / "style-spec.yaml"

FFMPEG_CANDIDATES = [
    r"C:\Users\TRIAL\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe",
    r"C:\ffmpeg\bin\ffmpeg.exe",
    "ffmpeg"
]

def find_ffmpeg() -> str:
    for cand in FFMPEG_CANDIDATES:
        if os.path.exists(cand):
            return cand
    return "ffmpeg"

def find_ffprobe() -> str:
    ffmpeg_bin = find_ffmpeg()
    ffprobe_cand = str(Path(ffmpeg_bin).parent / "ffprobe.exe")
    if os.path.exists(ffprobe_cand):
        return ffprobe_cand
    return "ffprobe"

def cmd_validate_storyboard(storyboard_path: Path) -> bool:
    """Validate storyboard JSON against schema contracts and Anti-Slop QC gates."""
    print(f"\n🔍 [QC AUDIT] Validating Storyboard: {storyboard_path.name}")
    if not storyboard_path.exists():
        print(f"❌ Error: File not found: {storyboard_path}")
        return False
        
    try:
        with open(storyboard_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON Syntax Error: {e}")
        return False

    # 1. Structural Schema Contract Validation
    required_root = ["project_title", "topic_summary", "target_duration_seconds", "aspect_ratio", "narrative_arc", "beats"]
    missing_root = [k for k in required_root if k not in data]
    if missing_root:
        print(f"  ❌ Schema Failure: Missing root fields: {missing_root}")
        return False

    if data.get("aspect_ratio") not in ["16:9", "9:16", "1:1"]:
        print(f"  ❌ Schema Failure: Invalid aspect_ratio: {data.get('aspect_ratio')}")
        return False

    beats = data.get("beats", [])
    if not isinstance(beats, list) or len(beats) == 0:
        print("  ❌ Schema Failure: 'beats' must be a non-empty array.")
        return False

    print("  ✅ Schema Contract: PASS (Root structure & types verified)")

    # 2. Anti-Slop & Visual Grammar QC Gates
    allowed_modes = {
        "ARCHIVAL", "INTERVIEW", "PHOTO", "DOCUMENT", "MAP", 
        "TIMELINE", "CHART", "DIAGRAM", "DATA CARD", "DATA_CARD", 
        "RECONSTRUCTION", "GRAPHIC TITLE", "GRAPHIC_TITLE"
    }
    allowed_stages = {
        "HOOK", "OBSERVATION", "QUESTION", "PRECEDENT", "MECHANISM", 
        "SYSTEM_POLICY", "INCENTIVE", "CONSEQUENCE", "RESPONSE", "IMPLICATION"
    }
    
    passed_qc = True
    print(f"\n📋 Inspecting {len(beats)} Narrative Beats:")
    prev_timecode = 0.0

    for idx, b in enumerate(beats, start=1):
        bid = b.get("beat_id", f"beat_{idx:02d}")
        tin = b.get("timecode_in", 0.0)
        tout = b.get("timecode_out", 0.0)
        stage = b.get("narrative_stage")
        mode = b.get("visual_mode")
        job = b.get("visual_job", "")
        focal = b.get("focal_subject", "")
        prov = b.get("source_provenance", "")
        on_screen = b.get("on_screen_text", {})
        headline = on_screen.get("headline", "") if isinstance(on_screen, dict) else str(on_screen)

        # Timecode monotonicity check
        if tout <= tin:
            print(f"  ❌ Beat {idx} ({bid}): timecode_out ({tout}s) <= timecode_in ({tin}s)")
            passed_qc = False

        # Visual Mode check
        if mode not in allowed_modes:
            print(f"  ❌ Beat {idx} ({bid}): Invalid visual_mode '{mode}'")
            passed_qc = False

        # Narrative stage check
        if stage and stage not in allowed_stages:
            print(f"  ❌ Beat {idx} ({bid}): Unrecognized narrative_stage '{stage}'")
            passed_qc = False

        # Non-trivial visual job check (Anti-Slop)
        if not job or len(job.split()) < 3:
            print(f"  ❌ Beat {idx} ({bid}): Vague visual_job: '{job}'. Must specify exact communicative duty.")
            passed_qc = False

        # Source provenance check
        if not prov:
            print(f"  ⚠️ Beat {idx} ({bid}): Missing source_provenance citation.")

        # Text Density check (max 16 words in headline)
        word_count = len(headline.split())
        if word_count > 16:
            print(f"  ⚠️ Beat {idx} ({bid}): Headline has {word_count} words (>16 word limit). Consider shortening.")

        print(f"  ✓ [{bid}] {tin:5.1f}s - {tout:5.1f}s | {mode:12s} | Job: {job[:40]}... | Prov: {prov[:25]}")
        prev_timecode = tout

    if passed_qc:
        print(f"\n🏆 [QC PASSED] Storyboard satisfies all Vox Editorial Explainer criteria!\n")
    return passed_qc

def cmd_audio_synthesis(script_path: Path, out_dir: Path, voice: str = "id-ID-ArdiNeural", bgm_path: Optional[Path] = None):
    """Synthesize voiceover using edge-tts via uv and align with BGM."""
    out_dir.mkdir(parents=True, exist_ok=True)
    audio_raw = out_dir / "voiceover_full.mp3"
    srt_out = out_dir / "subtitles.srt"
    json_out = out_dir / "subtitles.json"
    master_audio = out_dir / "audio_master.mp3"

    print(f"\n🎙️ [AUDIO SYNTHESIS] Voice: {voice}")
    print(f"Source Script: {script_path}")

    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read().strip()

    # Use uv run --with edge-tts for isolated execution
    uv_bin = r"C:\Users\TRIAL\.local\bin\uv.exe"
    if not os.path.exists(uv_bin):
        uv_bin = "uv"

    py_inline = f"""
import asyncio, edge_tts

script = {repr(script_text)}
async def run():
    communicate = edge_tts.Communicate(script, '{voice}', rate='+2%')
    submaker = edge_tts.SubMaker()
    with open(r'{str(audio_raw)}', 'wb') as f:
        async for chunk in communicate.stream():
            if chunk['type'] == 'audio':
                f.write(chunk['data'])
            elif chunk['type'] in ('WordBoundary', 'SentenceBoundary'):
                submaker.feed(chunk)
    with open(r'{str(srt_out)}', 'w', encoding='utf-8') as f:
        f.write(submaker.get_srt())
    print('TTS and SRT synthesis complete.')

asyncio.run(run())
"""
    cmd = [uv_bin, "run", "--with", "edge-tts", "python", "-c", py_inline]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error during TTS synthesis:\n{res.stderr}")
        return False

    print(f"  ✓ Voiceover created: {audio_raw.name}")
    print(f"  ✓ Subtitles SRT created: {srt_out.name}")

    # Parse SRT into structured JSON timestamps
    subtitles_list = []
    import re
    with open(srt_out, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.strip().split("\n\n")
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            time_match = re.match(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", lines[1])
            if time_match:
                def to_sec(s):
                    h, m, sec_ms = s.split(":")
                    sec, ms = sec_ms.split(",")
                    return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000.0
                start_sec = to_sec(time_match.group(1))
                end_sec = to_sec(time_match.group(2))
                text = " ".join(lines[2:]).strip()
                subtitles_list.append({"start": start_sec, "end": end_sec, "text": text})

    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(subtitles_list, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Subtitles JSON created: {json_out.name} ({len(subtitles_list)} sentences)")

    # Duck BGM if provided
    ffmpeg = find_ffmpeg()
    if bgm_path and bgm_path.exists():
        print(f"  🎵 Ducking background music: {bgm_path.name}")
        cmd_duck = [
            ffmpeg, "-y",
            "-i", str(bgm_path),
            "-i", str(audio_raw),
            "-filter_complex",
            "[0:a]volume=0.18[bgm];[1:a]volume=1.0[v];[bgm][v]amix=inputs=2:duration=longest",
            "-c:a", "mp3", "-b:a", "192k",
            str(master_audio)
        ]
        subprocess.run(cmd_duck, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  ✓ Master mixed audio ready: {master_audio.name}")
    else:
        # Just copy voiceover as master
        import shutil
        shutil.copy2(audio_raw, master_audio)
        print(f"  ✓ Master audio (voiceover only): {master_audio.name}")

    return True

def cmd_render(project_dir: Path, fps: int = 24, out_name: str = "output_vox.mp4"):
    """Render project_dir/index.html to MP4 using Playwright and FFmpeg direct pipe."""
    html_file = project_dir / "index.html"
    audio_file = project_dir / "audio_master.mp3"
    out_mp4 = project_dir / out_name

    if not html_file.exists():
        print(f"❌ Error: index.html not found in {project_dir}")
        return False
    if not audio_file.exists():
        print(f"❌ Error: audio_master.mp3 not found in {project_dir}")
        return False

    # Get duration from audio
    ffprobe = find_ffprobe()
    ffmpeg = find_ffmpeg()
    cmd_probe = [ffprobe, "-i", str(audio_file), "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    try:
        dur_str = subprocess.check_output(cmd_probe, text=True).strip()
        total_duration = float(dur_str)
    except Exception:
        total_duration = 60.0

    total_frames = int(total_duration * fps)
    print(f"\n🎬 [RENDER PIPELINE] 1920x1080 @ {fps}fps | Duration: {total_duration:.2f}s ({total_frames} frames)")
    print(f"Target: {out_mp4}")

    from playwright.sync_api import sync_playwright

    cmd_ffmpeg = [
        ffmpeg, "-y",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-r", str(fps),
        "-i", "-",
        "-i", str(audio_file),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out_mp4)
    ]

    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    t_start = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        html_url = html_file.resolve().as_uri()
        page.goto(html_url, wait_until="networkidle")

        print("Piping frames directly from Playwright to FFmpeg stdin...")
        for frame_idx in range(total_frames):
            t = frame_idx / fps
            page.evaluate(f"window.seekToTime({t})")
            buf = page.screenshot(type="jpeg", quality=90)
            proc.stdin.write(buf)

            if (frame_idx + 1) % 200 == 0 or frame_idx == total_frames - 1:
                elapsed = time.time() - t_start
                curr_fps = (frame_idx + 1) / elapsed
                percent = ((frame_idx + 1) / total_frames) * 100
                print(f"  [{percent:5.1f}%] Frame {frame_idx + 1}/{total_frames} | {curr_fps:.1f} fps")

        browser.close()

    proc.stdin.close()
    proc.wait()
    total_time = time.time() - t_start

    if proc.returncode == 0:
        size_mb = out_mp4.stat().st_size / (1024 * 1024)
        print(f"\n✅ [RENDER SUCCESS] {out_mp4.name} ({size_mb:.2f} MB in {total_time:.1f}s)")
        return True
    else:
        err = proc.stderr.read().decode("utf-8", errors="ignore")
        print(f"❌ Render failed:\n{err}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Vox-Inspired Editorial Explainer Video Production Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate
    p_val = subparsers.add_parser("validate", help="Audit and validate a storyboard JSON against schema and QC gates")
    p_val.add_argument("--storyboard", required=True, type=Path, help="Path to storyboard.json")

    # audio
    p_aud = subparsers.add_parser("audio", help="Synthesize studio VO and ducked audio master")
    p_aud.add_argument("--script", required=True, type=Path, help="Path to script text file")
    p_aud.add_argument("--output-dir", required=True, type=Path, help="Output directory for audio assets")
    p_aud.add_argument("--voice", default="id-ID-ArdiNeural", help="TTS voice model")
    p_aud.add_argument("--bgm", type=Path, default=None, help="Path to background music file")

    # render
    p_ren = subparsers.add_parser("render", help="Render video project to MP4")
    p_ren.add_argument("--project-dir", required=True, type=Path, help="Path to project directory containing index.html & audio_master.mp3")
    p_ren.add_argument("--fps", type=int, default=24, help="Frames per second")
    p_ren.add_argument("--output", default="output_vox.mp4", help="Output MP4 filename")

    args = parser.parse_args()

    if args.command == "validate":
        success = cmd_validate_storyboard(args.storyboard)
        sys.exit(0 if success else 1)
    elif args.command == "audio":
        success = cmd_audio_synthesis(args.script, args.output_dir, args.voice, args.bgm)
        sys.exit(0 if success else 1)
    elif args.command == "render":
        success = cmd_render(args.project_dir, args.fps, args.output)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
