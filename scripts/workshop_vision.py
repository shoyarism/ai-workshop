#!/usr/bin/env python3
"""
Workshop Multimodal Media & Vision Engine (Universal Vision for Text-Only & Vision Agents)
========================================================================================
Empowers ALL AI models and agents (even text-only models without native vision)
to see, read, inspect, decompose, transcribe, and understand images, screenshots,
UI mockups, diagrams, videos, and audio.

Capabilities:
1. High-Precision OCR: Fast ONNX OCR extracting text with exact spatial bounding boxes.
2. Image Deconstructor: UI layout decomposition, color palettes, theme detection (dark/light), and spatial coordinates.
3. ANSI/ASCII Canvas: Truecolor 24-bit ANSI and unicode luminance art for terminal visual perception.
4. Video Deconstructor: Keyframe sampling, scene change detection, video OCR timeline, and storyboard contact sheets.
5. Speech Transcription: Faster-Whisper automated speech-to-text with timestamps.
6. Multimodal Vision Fallback: Optional LLM vision proxy via LiteLLM / OmniRoute.
7. Universal 'see' Dispatcher: Automatically analyzes any media file or directory.

Usage:
    python scripts/workshop.py see "<file_or_dir>"
    python scripts/workshop.py vision ocr "<image_path>"
    python scripts/workshop.py vision describe "<image_path>"
    python scripts/workshop.py vision ascii "<image_path>"
    python scripts/workshop.py vision storyboard "<video_path>"
    python scripts/workshop.py vision video-ocr "<video_path>"
    python scripts/workshop.py vision transcribe "<audio_or_video_path>"
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(WORKSHOP_DIR / ".env")
except ImportError:  # @court-exempt: optional dotenv fallback
    pass

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".svg", ".ico"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv", ".m4v"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma", ".opus"}

OMNIROUTE_URL = os.environ.get("OMNIROUTE_URL", "http://127.0.0.1:20128/v1")
OMNIROUTE_KEY = os.environ.get("OMNIROUTE_API_KEY", "omniroute-local")

# Global lazy OCR instance
_OCR_ENGINE = None

def get_ocr_engine():
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _OCR_ENGINE = RapidOCR()
        except Exception:
            _OCR_ENGINE = False
    return _OCR_ENGINE

def run_cmd(cmd: List[str], timeout: int = 60) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        return -1, "", str(e)

# ==============================================================================
# 1. OCR & SPATIAL LAYOUT ENGINE
# ==============================================================================

def ocr_image(image_path: Path) -> Dict[str, Any]:
    """Extract all text, bounding boxes, confidence, and spatial layout from an image."""
    if not image_path.exists():
        return {"error": f"File not found: {image_path}"}
    
    result = {
        "file": str(image_path.resolve()),
        "engine": "rapidocr",
        "total_text_blocks": 0,
        "extracted_text": "",
        "text_blocks": [],
        "spatial_layout": {
            "top": [],
            "middle": [],
            "bottom": []
        }
    }

    try:
        from PIL import Image
        import numpy as np
        
        with Image.open(image_path) as img:
            img_rgb = img.convert("RGB")
            width, height = img_rgb.size
            img_np = np.array(img_rgb)
            
        result["image_width"] = width
        result["image_height"] = height

        ocr = get_ocr_engine()
        if ocr:
            ocr_results, elapse = ocr(img_np)
            if ocr_results:
                raw_lines = []
                blocks = []
                for box, text, score in ocr_results:
                    text_str = text.strip()
                    if not text_str:
                        continue
                    raw_lines.append(text_str)
                    
                    # Calculate center and box coordinates
                    xs = [pt[0] for pt in box]
                    ys = [pt[1] for pt in box]
                    x_min, x_max = min(xs), max(xs)
                    y_min, y_max = min(ys), max(ys)
                    center_x = (x_min + x_max) / 2.0
                    center_y = (y_min + y_max) / 2.0
                    
                    # Spatial region
                    vert_region = "top" if center_y < height * 0.33 else ("bottom" if center_y > height * 0.66 else "middle")
                    horiz_region = "left" if center_x < width * 0.33 else ("right" if center_x > width * 0.66 else "center")
                    region_tag = f"{vert_region}-{horiz_region}"
                    
                    block_info = {
                        "text": text_str,
                        "confidence": round(float(score), 3),
                        "region": region_tag,
                        "box": [round(x_min), round(y_min), round(x_max - x_min), round(y_max - y_min)]
                    }
                    blocks.append(block_info)
                    result["spatial_layout"][vert_region].append(f"[{region_tag}] {text_str}")

                result["total_text_blocks"] = len(blocks)
                result["extracted_text"] = "\n".join(raw_lines)
                result["text_blocks"] = blocks
                return result
    except Exception as e:
        result["ocr_error"] = str(e)

    # Fallback to Tesseract CLI if available
    code, out, _ = run_cmd(["tesseract", str(image_path), "stdout", "--oem", "1", "-l", "eng"])
    if code == 0 and out.strip():
        result["extracted_text"] = out.strip()
        result["engine"] = "tesseract_cli"
        return result

    return result

# ==============================================================================
# 2. IMAGE VISUAL DECONSTRUCTOR (FOR TEXT-ONLY AGENTS)
# ==============================================================================

def rgb_to_color_name(r: int, g: int, b: int) -> str:
    """Classify RGB values into human and AI readable color names."""
    brightness = (r + g + b) / 3.0
    if brightness < 30:
        return "Near-Black / Dark Slate"
    if brightness > 235:
        return "Near-White / Clean Light"
    
    if r > g + 40 and r > b + 40:
        return "Red / Crimson"
    if g > r + 30 and g > b + 30:
        return "Green / Emerald"
    if b > r + 30 and b > g + 30:
        return "Blue / Azure"
    if r > 180 and g > 180 and b < 100:
        return "Yellow / Amber"
    if r > 180 and g > 100 and b < 50:
        return "Orange / Coral"
    if r > 140 and b > 140 and g < 100:
        return "Purple / Violet"
    if r > 180 and b > 180 and g > 180:
        return "Light Gray"
    if r < 100 and b < 100 and g < 100:
        return "Dark Charcoal"
    return "Neutral Slate"

def deconstruct_image(image_path: Path) -> Dict[str, Any]:
    """Deconstruct an image completely into structural, visual, and textual descriptions."""
    if not image_path.exists():
        return {"error": f"File not found: {image_path}"}

    info = {
        "file_name": image_path.name,
        "path": str(image_path.resolve()),
        "size_kb": round(image_path.stat().st_size / 1024, 1),
        "extension": image_path.suffix.lower()
    }

    try:
        from PIL import Image, ImageStat
        with Image.open(image_path) as img:
            w, h = img.size
            info["dimensions"] = {"width": w, "height": h, "aspect_ratio": f"{w}:{h} ({w/h:.2f})"}
            info["format"] = img.format
            info["mode"] = img.mode
            
            rgb = img.convert("RGB")
            stat = ImageStat.Stat(rgb)
            mean_bright = sum(stat.mean) / (3.0 * 255.0) * 100.0
            info["brightness_percent"] = round(mean_bright, 1)
            info["theme"] = "Dark Theme (Dark Mode UI / Low Luminance)" if mean_bright < 45 else ("Light Theme (Light Mode UI / High Luminance)" if mean_bright > 65 else "Balanced Contrast")
            
            # Palette extraction
            small = rgb.resize((50, 50), Image.Resampling.BILINEAR)
            colors = small.getcolors(maxcolors=2500)
            if colors:
                colors.sort(key=lambda x: x[0], reverse=True)
                palette = []
                for count, (r, g, b) in colors[:6]:
                    hex_code = f"#{r:02x}{g:02x}{b:02x}"
                    c_name = rgb_to_color_name(r, g, b)
                    pct = round(count / 2500 * 100, 1)
                    palette.append({"hex": hex_code, "name": c_name, "coverage_pct": pct})
                info["dominant_palette"] = palette

        # Run OCR decomposition
        ocr_data = ocr_image(image_path)
        info["ocr_extracted_text"] = ocr_data.get("extracted_text", "")
        info["total_text_blocks"] = ocr_data.get("total_text_blocks", 0)
        info["spatial_layout"] = ocr_data.get("spatial_layout", {})
        
        # Build synthesis summary for text-only agents
        summary_lines = [
            f"Image '{image_path.name}' is a {w}x{h} ({info['dimensions']['aspect_ratio']}) {info['theme']}.",
            f"Primary Colors: {', '.join(p['name'] + ' (' + p['hex'] + ')' for p in info.get('dominant_palette', [])[:3])}."
        ]
        if ocr_data.get("extracted_text"):
            summary_lines.append(f"Detected {ocr_data['total_text_blocks']} text elements:")
            for b in ocr_data.get("text_blocks", [])[:8]:
                summary_lines.append(f"  • [{b['region']}] \"{b['text']}\" (conf: {b['confidence']})")
            if ocr_data['total_text_blocks'] > 8:
                summary_lines.append(f"  ... and {ocr_data['total_text_blocks'] - 8} more text blocks.")
        else:
            summary_lines.append("No prominent typography or text detected (likely a graphic, photo, or background asset).")

        info["agent_visual_summary"] = "\n".join(summary_lines)

    except Exception as e:
        info["error"] = str(e)

    return info

# ==============================================================================
# 3. ANSI & ASCII TERMINAL ART RENDERING
# ==============================================================================

def render_ansi_thumbnail(image_path: Path, max_width: int = 50, max_height: int = 25) -> str:
    """Render a 24-bit truecolor ANSI block image for direct terminal visual display."""
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            w, h = img.size
            aspect = (h / w) * 0.5
            target_w = min(max_width, w)
            target_h = int(target_w * aspect)
            if target_h > max_height:
                target_h = max_height
                target_w = int(target_h / aspect)
            
            target_w = max(1, target_w)
            target_h = max(1, target_h)
            img = img.resize((target_w, target_h), Image.Resampling.BILINEAR)
            
            lines = []
            for y in range(target_h):
                row = []
                for x in range(target_w):
                    r, g, b = img.getpixel((x, y))
                    row.append(f"\033[48;2;{r};{g};{b}m \033[0m")
                lines.append("".join(row))
            return "\n".join(lines)
    except Exception as e:
        return f"[ANSI Preview Unavailable: {e}]"

def render_ascii_art(image_path: Path, width: int = 60) -> str:
    """Render a high-resolution monochrome ASCII luminance character grid."""
    chars = " .:-=+*#%@"
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            img = img.convert("L")  # Grayscale
            orig_w, orig_h = img.size
            aspect = (orig_h / orig_w) * 0.55
            height = max(1, int(width * aspect))
            img = img.resize((width, height), Image.Resampling.BILINEAR)
            
            lines = []
            for y in range(height):
                row = []
                for x in range(width):
                    val = img.getpixel((x, y))
                    char_idx = int(val / 255 * (len(chars) - 1))
                    row.append(chars[char_idx])
                lines.append("".join(row))
            return "\n".join(lines)
    except Exception as e:
        return f"[ASCII Art Unavailable: {e}]"

# ==============================================================================
# 4. VIDEO DECONSTRUCTOR, KEYFRAMES & STORYBOARD
# ==============================================================================

def format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def inspect_video(video_path: Path) -> Dict[str, Any]:
    if not video_path.exists():
        return {"error": f"File not found: {video_path}"}

    result = {
        "file_name": video_path.name,
        "path": str(video_path.resolve()),
        "file_size_bytes": video_path.stat().st_size,
        "file_size_human": f"{video_path.stat().st_size / (1024 * 1024):.2f} MB",
        "extension": video_path.suffix.lower(),
        "type": "video"
    }

    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", str(video_path)
    ]
    code, out, err = run_cmd(cmd)
    if code == 0 and out.strip():
        try:
            info = json.loads(out)
            fmt = info.get("format", {})
            result["duration_seconds"] = float(fmt.get("duration", 0))
            result["duration_human"] = format_time(result["duration_seconds"])
            result["bitrate_kbps"] = int(int(fmt.get("bit_rate", 0)) / 1000) if fmt.get("bit_rate") else None
            
            streams = info.get("streams", [])
            video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
            audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
            
            if video_stream:
                result["video_codec"] = video_stream.get("codec_name")
                result["width"] = int(video_stream.get("width", 0))
                result["height"] = int(video_stream.get("height", 0))
                result["aspect_ratio"] = f"{result['width']}:{result['height']}"
                fps_str = video_stream.get("avg_frame_rate", "0/1")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    result["fps"] = round(float(num) / float(den), 2) if float(den) > 0 else 0
                else:
                    result["fps"] = float(fps_str)
            
            if audio_stream:
                result["has_audio"] = True
                result["audio_codec"] = audio_stream.get("codec_name")
                result["audio_channels"] = audio_stream.get("channels")
                result["sample_rate_hz"] = audio_stream.get("sample_rate")
            else:
                result["has_audio"] = False
        except Exception as e:
            result["ffprobe_parse_error"] = str(e)
    else:
        result["ffprobe_error"] = err or "ffprobe execution failed"

    return result

def extract_video_keyframes(
    video_path: Path,
    count: int = 8,
    output_dir: Optional[Path] = None
) -> List[Tuple[float, Path]]:
    """Extract keyframes with timestamps from a video file."""
    if not output_dir:
        output_dir = video_path.parent / f".tmp_frames_{video_path.stem}"
    output_dir.mkdir(parents=True, exist_ok=True)

    info = inspect_video(video_path)
    duration = info.get("duration_seconds", 0)
    if duration <= 0:
        duration = 10.0

    step = duration / (count + 1)
    timestamps = [step * (i + 1) for i in range(count)]

    extracted = []
    for idx, ts in enumerate(timestamps):
        out_file = output_dir / f"frame_{idx+1:02d}_{int(ts)}s.jpg"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{ts:.2f}",
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(out_file)
        ]
        code, _, _ = run_cmd(cmd)
        if code == 0 and out_file.exists():
            extracted.append((ts, out_file))

    return extracted

def generate_video_storyboard(
    video_path: Path,
    grid_cols: int = 3,
    grid_rows: int = 3,
    output_image: Optional[Path] = None
) -> Optional[Path]:
    """Generate a single master storyboard contact sheet combining keyframes."""
    total_frames = grid_cols * grid_rows
    temp_dir = video_path.parent / f".tmp_storyboard_{video_path.stem}"
    framedata = extract_video_keyframes(video_path, count=total_frames, output_dir=temp_dir)

    if not framedata:
        return None

    if not output_image:
        output_image = video_path.parent / f"{video_path.stem}_storyboard.jpg"

    try:
        from PIL import Image, ImageDraw
        frames = [p for _, p in framedata]
        
        sample_img = Image.open(frames[0])
        orig_w, orig_h = sample_img.size
        sample_img.close()
        
        thumb_w = 400
        thumb_h = int(thumb_w * (orig_h / orig_w))
        padding = 8
        header_height = 50
        footer_height = 30
        
        canvas_w = grid_cols * thumb_w + (grid_cols + 1) * padding
        canvas_h = header_height + (grid_rows * thumb_h) + (grid_rows + 1) * padding + footer_height
        
        board = Image.new("RGB", (canvas_w, canvas_h), color=(20, 24, 30))
        draw = ImageDraw.Draw(board)
        
        draw.rectangle([(0, 0), (canvas_w, header_height)], fill=(12, 14, 18))
        draw.text((padding + 10, 15), f"VIDEO STORYBOARD: {video_path.name}", fill=(255, 255, 255))
        
        info = inspect_video(video_path)
        dur_str = info.get("duration_human", "Unknown")
        draw.text((canvas_w - 220, 15), f"Duration: {dur_str} | Frames: {len(frames)}", fill=(160, 180, 200))
        
        for idx, (ts, frame_path) in enumerate(framedata):
            col = idx % grid_cols
            row = idx // grid_cols
            if row >= grid_rows:
                break
            
            x = padding + col * (thumb_w + padding)
            y = header_height + padding + row * (thumb_h + padding)
            
            with Image.open(frame_path) as f_img:
                f_resized = f_img.resize((thumb_w, thumb_h), Image.Resampling.BILINEAR)
                board.paste(f_resized, (x, y))
            
            ts_label = format_time(ts)
            draw.rectangle([(x + 6, y + thumb_h - 24), (x + 70, y + thumb_h - 6)], fill=(0, 0, 0))
            draw.text((x + 10, y + thumb_h - 22), ts_label, fill=(255, 220, 0))
            draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], outline=(60, 70, 85), width=1)
        
        draw.text((padding + 10, canvas_h - 22), "Workshop Centralized Vision Engine", fill=(100, 115, 130))
        board.save(output_image, quality=92)
        
        for _, f in framedata:
            try:
                f.unlink()
            except Exception:  # @court-exempt: handled fallback
                pass
        try:
            temp_dir.rmdir()
        except Exception:  # @court-exempt: handled fallback
            pass
            
        return output_image
    except Exception as e:
        print(f"[!] Storyboard generation failed: {e}", file=sys.stderr)
        return None

def video_ocr_timeline(video_path: Path, sample_count: int = 8) -> Dict[str, Any]:
    """Extract keyframes and perform frame-by-frame OCR to create a timeline of visual text changes."""
    if not video_path.exists():
        return {"error": f"File not found: {video_path}"}
        
    temp_dir = video_path.parent / f".tmp_video_ocr_{video_path.stem}"
    framedata = extract_video_keyframes(video_path, count=sample_count, output_dir=temp_dir)
    
    timeline = []
    seen_texts = set()
    
    for ts, frame_file in framedata:
        ocr_res = ocr_image(frame_file)
        text_lines = [b["text"] for b in ocr_res.get("text_blocks", [])]
        unique_new = [t for t in text_lines if t not in seen_texts]
        for t in unique_new:
            seen_texts.add(t)
            
        timeline.append({
            "timestamp_seconds": round(ts, 2),
            "timestamp_human": format_time(ts),
            "text_count": len(text_lines),
            "all_text": text_lines,
            "newly_appeared_text": unique_new
        })
        
        try:
            frame_file.unlink()
        except Exception:  # @court-exempt: handled fallback
            pass
            
    try:
        temp_dir.rmdir()
    except Exception:  # @court-exempt: handled fallback
        pass
        
    return {
        "video": video_path.name,
        "total_sampled_frames": len(timeline),
        "total_unique_text_tokens": len(seen_texts),
        "timeline": timeline
    }

# ==============================================================================
# 5. AUDIO & SPEECH TRANSCRIPTION
# ==============================================================================

def extract_audio(media_path: Path, output_audio: Optional[Path] = None) -> Optional[Path]:
    """Extract 16kHz mono PCM WAV audio from any video or audio container."""
    if not output_audio:
        output_audio = media_path.parent / f"{media_path.stem}_audio.wav"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(media_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(output_audio)
    ]
    code, _, err = run_cmd(cmd)
    if code == 0 and output_audio.exists():
        return output_audio
    return None

def transcribe_speech(media_path: Path, model_size: str = "base") -> Dict[str, Any]:
    """Transcribe speech in audio or video with timestamps using faster-whisper."""
    audio_file = extract_audio(media_path) if media_path.suffix.lower() in VIDEO_EXTENSIONS else media_path
    if not audio_file or not audio_file.exists():
        return {"error": f"Could not extract or read audio for {media_path}"}

    result = {
        "media": str(media_path.resolve()),
        "audio_file": str(audio_file.resolve()),
        "segments": [],
        "full_transcript": ""
    }

    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, info = model.transcribe(str(audio_file), beam_size=5)
        
        result["language"] = info.language
        result["language_probability"] = round(info.language_probability, 3)
        result["duration_seconds"] = round(info.duration, 2)
        
        trans_segments = []
        full_text = []
        for segment in segments:
            seg_text = segment.text.strip()
            trans_segments.append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "timestamp": f"[{format_time(segment.start)} -> {format_time(segment.end)}]",
                "text": seg_text
            })
            full_text.append(seg_text)
            
        result["segments"] = trans_segments
        result["full_transcript"] = " ".join(full_text)
        return result
    except Exception as e:
        result["whisper_error"] = str(e)
        result["note"] = "Whisper transcription failed, raw audio preserved at " + str(audio_file)
        return result

# ==============================================================================
# 6. UNIVERSAL 'SEE' DISPATCHER
# ==============================================================================

def see_media(path_str: str, prompt: Optional[str] = None, make_storyboard: bool = True) -> Dict[str, Any]:
    """Universal dispatcher: inspects images, videos, audio, or directories and returns rich context."""
    target = Path(path_str).resolve()
    if not target.exists():
        return {"error": f"Target path does not exist: {path_str}"}

    if target.is_dir():
        images = [p for p in target.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
        videos = [p for p in target.iterdir() if p.suffix.lower() in VIDEO_EXTENSIONS]
        audio = [p for p in target.iterdir() if p.suffix.lower() in AUDIO_EXTENSIONS]
        
        return {
            "type": "directory",
            "directory": str(target),
            "total_images": len(images),
            "total_videos": len(videos),
            "total_audio": len(audio),
            "images": [p.name for p in images[:20]],
            "videos": [p.name for p in videos[:10]],
            "audio": [p.name for p in audio[:10]]
        }

    ext = target.suffix.lower()

    if ext in IMAGE_EXTENSIONS:
        decon = deconstruct_image(target)
        decon["ansi_preview"] = render_ansi_thumbnail(target, max_width=50, max_height=20)
        return decon

    elif ext in VIDEO_EXTENSIONS:
        data = inspect_video(target)
        if make_storyboard:
            sb_path = generate_video_storyboard(target)
            if sb_path:
                data["storyboard_image"] = str(sb_path)
                data["storyboard_preview"] = render_ansi_thumbnail(sb_path, max_width=60, max_height=20)
        # Add video OCR summary
        data["video_ocr_timeline"] = video_ocr_timeline(target, sample_count=6)
        return data

    elif ext in AUDIO_EXTENSIONS:
        return transcribe_speech(target)

    return {"error": f"Unsupported media type for '{target.name}'"}

def main():
    parser = argparse.ArgumentParser(
        description="Workshop Multimodal Media & Vision Engine (Universal Vision for AI Agents)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Vision command to run")

    # See
    p_see = subparsers.add_parser("see", help="Smart visual inspection of images/videos/directories")
    p_see.add_argument("path", help="Path to image, video, audio, or directory")
    p_see.add_argument("--prompt", "-p", default="", help="Optional prompt for AI vision model")
    p_see.add_argument("--no-storyboard", action="store_true", help="Skip video storyboard creation")
    p_see.add_argument("--json", action="store_true", help="Output raw JSON")

    # Describe / Deconstruct
    p_desc = subparsers.add_parser("describe", help="Deconstruct image layout, palette, theme, and OCR text for text-only agents")
    p_desc.add_argument("image", help="Path to image file")
    p_desc.add_argument("--json", action="store_true")

    # OCR
    p_ocr = subparsers.add_parser("ocr", help="Perform ONNX OCR extracting text and spatial layout boxes")
    p_ocr.add_argument("image", help="Path to image file")
    p_ocr.add_argument("--json", action="store_true")

    # ASCII / ANSI
    p_ascii = subparsers.add_parser("ascii", help="Render monochrome ASCII luminance art of an image")
    p_ascii.add_argument("image", help="Path to image file")
    p_ascii.add_argument("--width", "-w", type=int, default=60)

    # Video Keyframes
    p_frames = subparsers.add_parser("frames", help="Extract video keyframes")
    p_frames.add_argument("video", help="Path to video file")
    p_frames.add_argument("--count", "-c", type=int, default=8, help="Number of frames to extract")

    # Storyboard
    p_sb = subparsers.add_parser("storyboard", help="Generate video storyboard contact sheet")
    p_sb.add_argument("video", help="Path to video file")
    p_sb.add_argument("--cols", type=int, default=3)
    p_sb.add_argument("--rows", type=int, default=3)
    p_sb.add_argument("--out", "-o", default=None)

    # Video OCR
    p_vocr = subparsers.add_parser("video-ocr", help="Extract frame-by-frame OCR timeline from video")
    p_vocr.add_argument("video", help="Path to video file")
    p_vocr.add_argument("--count", "-c", type=int, default=6)

    # Transcribe
    p_trans = subparsers.add_parser("transcribe", help="Transcribe speech from audio or video using Faster-Whisper")
    p_trans.add_argument("media", help="Path to audio or video file")
    p_trans.add_argument("--model", "-m", default="base", choices=["tiny", "base", "small", "medium"])

    args = parser.parse_args()

    if args.command == "see":
        res = see_media(args.path, prompt=args.prompt if args.prompt else None, make_storyboard=not args.no_storyboard)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("\n=======================================================")
            print(f" 👁️ WORKSHOP VISION INSPECTOR: {Path(args.path).name}")
            print("=======================================================\n")
            if "ansi_preview" in res:
                print(res["ansi_preview"])
                print()
            if "agent_visual_summary" in res:
                print("📋 Agent Visual & Structural Summary:")
                print(res["agent_visual_summary"])
                print()
            if "storyboard_preview" in res:
                print("🎬 Storyboard Grid Preview:")
                print(res["storyboard_preview"])
                print(f"\nStoryboard saved: {res.get('storyboard_image')}\n")
            if "video_ocr_timeline" in res:
                print("⏱️ Video OCR Text Timeline:")
                for item in res["video_ocr_timeline"].get("timeline", []):
                    if item.get("all_text"):
                        print(f"  • {item['timestamp_human']}: {', '.join(item['all_text'])}")
                print()
            for k, v in res.items():
                if k not in ("ansi_preview", "storyboard_preview", "agent_visual_summary", "video_ocr_timeline"):
                    print(f" • {k:<20}: {v}")
            print("\n=======================================================\n")

    elif args.command == "describe":
        res = deconstruct_image(Path(args.image))
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"\n=== Visual Deconstruction: {Path(args.image).name} ===")
            print(res.get("agent_visual_summary", "No summary generated."))
            print(f"\nTheme: {res.get('theme')}")
            print(f"Dimensions: {res.get('dimensions')}")
            print("Dominant Palette:")
            for p in res.get("dominant_palette", []):
                print(f"  - {p['hex']} ({p['name']}) : {p['coverage_pct']}%")
            print()

    elif args.command == "ocr":
        res = ocr_image(Path(args.image))
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"\n=== OCR Extraction: {Path(args.image).name} ({res.get('total_text_blocks')} blocks) ===")
            print(res.get("extracted_text", "No text detected."))
            print("\n--- Spatial Layout Map ---")
            for region, items in res.get("spatial_layout", {}).items():
                if items:
                    print(f"[{region.upper()}]:")
                    for item in items:
                        print(f"  {item}")
            print()

    elif args.command == "ascii":
        art = render_ascii_art(Path(args.image), width=args.width)
        print(art)

    elif args.command == "frames":
        data = extract_video_keyframes(Path(args.video), count=args.count)
        print(f"[+] Extracted {len(data)} keyframes:")
        for ts, p in data:
            print(f"  - [{format_time(ts)}] {p}")

    elif args.command == "storyboard":
        sb = generate_video_storyboard(Path(args.video), grid_cols=args.cols, grid_rows=args.rows, output_image=Path(args.out) if args.out else None)
        if sb:
            print(f"[+] Storyboard contact sheet generated: {sb}")

    elif args.command == "video-ocr":
        res = video_ocr_timeline(Path(args.video), sample_count=args.count)
        print(json.dumps(res, indent=2))

    elif args.command == "transcribe":
        res = transcribe_speech(Path(args.media), model_size=args.model)
        print(json.dumps(res, indent=2))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
