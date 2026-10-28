#!/usr/bin/env python3
"""
Workshop OS Native Desktop Automation Engine
============================================
Enables autonomous AI agents to perform full OS desktop operations on Windows:
- High-speed multi-monitor screenshots via MSS
- Mouse control (click, double-click, right-click, drag)
- Keyboard input and hotkeys (type, hotkey, press)
- Window management (list, focus, minimize, maximize)
- Detached application launching

Usage:
    python scripts/workshop_desktop.py screenshot [output.png]
    python scripts/workshop_desktop.py click <x> <y> [--button left|right] [--clicks 1|2]
    python scripts/workshop_desktop.py type "<text>" [--press enter]
    python scripts/workshop_desktop.py hotkey ctrl c
    python scripts/workshop_desktop.py windows [--json]
    python scripts/workshop_desktop.py focus "<title>"
    python scripts/workshop_desktop.py launch "<command>"
"""

import os
import sys
import time
import json
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
DEFAULT_SCREENSHOT_PATH = SCRIPTS_DIR / ".desktop_screenshot.png"


def take_screenshot(output_path: str = None, monitor_idx: int = 1) -> dict:
    out = Path(output_path) if output_path else DEFAULT_SCREENSHOT_PATH
    out.parent.mkdir(parents=True, exist_ok=True)

    # Strategy 1: MSS (Sub-millisecond multi-monitor)
    try:
        from mss import MSS
        with MSS() as sct:
            monitors = sct.monitors
            if monitor_idx >= len(monitors):
                monitor_idx = 0
            target_mon = monitors[monitor_idx]
            sct_img = sct.grab(target_mon)
            from mss.tools import to_png
            to_png(sct_img.rgb, sct_img.size, output=str(out))
            res = {
                "status": "success",
                "path": str(out),
                "width": target_mon["width"],
                "height": target_mon["height"],
                "engine": "mss",
            }
            print(f"[OK] Screenshot captured: {out} ({target_mon['width']}x{target_mon['height']}) [Engine: mss]")
            return res
    except Exception as e_mss:
        # Strategy 2: Pillow ImageGrab fallback
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            img.save(str(out))
            res = {
                "status": "success",
                "path": str(out),
                "width": img.width,
                "height": img.height,
                "engine": "pillow",
            }
            print(f"[OK] Screenshot captured: {out} ({img.width}x{img.height}) [Engine: pillow]")
            return res
        except Exception as e_pil:
            print(f"[!] Desktop display surface not accessible in current execution context ({e_mss}).")
            print("    [NOTE] Desktop screenshots require an interactive desktop session (WinSta0\\Default).")
            return {
                "status": "unavailable",
                "error": str(e_mss),
                "detail": "Non-interactive desktop session or display surface not attached.",
            }


def click_coords(x: int, y: int, button: str = "left", clicks: int = 1) -> dict:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.click(x=x, y=y, clicks=clicks, button=button)
    print(f"[OK] Clicked {button} at ({x}, {y}) [clicks={clicks}]")
    return {"status": "success", "x": x, "y": y, "button": button, "clicks": clicks}


def type_input(text: str, press_key: str = None, interval: float = 0.01) -> dict:
    import pyautogui
    import pyperclip
    pyautogui.FAILSAFE = False
    
    # For large blocks of text, paste via clipboard for speed and unicode safety
    if len(text) > 25 or any(ord(c) > 127 for c in text):
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.typewrite(text, interval=interval)
        
    if press_key:
        time.sleep(0.1)
        pyautogui.press(press_key)
        
    print(f"[OK] Typed text ({len(text)} chars)" + (f" and pressed {press_key}" if press_key else ""))
    return {"status": "success", "length": len(text), "pressed": press_key}


def press_hotkey(*keys) -> dict:
    import pyautogui
    pyautogui.FAILSAFE = False
    clean_keys = [k.lower().strip() for k in keys]
    pyautogui.hotkey(*clean_keys)
    print(f"[OK] Pressed hotkey: {' + '.join(clean_keys)}")
    return {"status": "success", "hotkey": clean_keys}


def list_open_windows() -> list[dict]:
    import pygetwindow as gw
    windows = gw.getAllWindows()
    results = []
    for w in windows:
        title = w.title.strip()
        if title and w.visible and w.width > 50 and w.height > 50:
            results.append({
                "title": title,
                "x": w.left,
                "y": w.top,
                "width": w.width,
                "height": w.height,
                "is_active": w.isActive,
            })
    return results


def focus_window(title_query: str) -> dict:
    import pygetwindow as gw
    windows = gw.getWindowsWithTitle(title_query)
    if not windows:
        print(f"[!] No visible window found matching '{title_query}'")
        return {"status": "error", "message": f"Window not found: {title_query}"}
    
    win = windows[0]
    try:
        if win.isMinimized:
            win.restore()
        win.activate()
        print(f"[OK] Focused window: '{win.title}' ({win.width}x{win.height})")
        return {"status": "success", "title": win.title, "x": win.left, "y": win.top}
    except Exception as e:
        print(f"[!] Could not activate window: {e}")
        return {"status": "error", "message": str(e)}


def launch_application(command_str: str) -> dict:
    creationflags = 0
    if os.name == "nt":
        creationflags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        
    proc = subprocess.Popen(
        command_str,
        shell=True,
        creationflags=creationflags,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"[OK] Launched application detached: '{command_str}' (PID: {proc.pid})")
    return {"status": "success", "command": command_str, "pid": proc.pid}


def main():
    parser = argparse.ArgumentParser(description="Workshop OS Native Desktop Automation Engine")
    sub = parser.add_subparsers(dest="action", help="Desktop action")

    p_shot = sub.add_parser("screenshot", help="Capture screen image")
    p_shot.add_argument("output", nargs="?", default=None, help="Output image path (default: .desktop_screenshot.png)")
    p_shot.add_argument("--monitor", "-m", type=int, default=1, help="Monitor index (1=primary, 0=all)")
    p_shot.add_argument("--json", action="store_true")

    p_click = sub.add_parser("click", help="Click at screen coordinates")
    p_click.add_argument("x", type=int, help="X pixel coordinate")
    p_click.add_argument("y", type=int, help="Y pixel coordinate")
    p_click.add_argument("--button", "-b", choices=["left", "right", "middle"], default="left")
    p_click.add_argument("--clicks", "-c", type=int, default=1)

    p_type = sub.add_parser("type", help="Type text into current active window")
    p_type.add_argument("text", help="Text string to type")
    p_type.add_argument("--press", "-p", default=None, help="Key to press after typing (e.g. enter, tab)")

    p_hotkey = sub.add_parser("hotkey", help="Press keyboard combination")
    p_hotkey.add_argument("keys", nargs="+", help="Keys (e.g. ctrl c, alt tab, win r)")

    p_win = sub.add_parser("windows", help="List active visible desktop windows")
    p_win.add_argument("--json", action="store_true")

    p_focus = sub.add_parser("focus", help="Bring window to front")
    p_focus.add_argument("title", help="Substring of window title to focus")

    p_launch = sub.add_parser("launch", help="Launch desktop app or command detached")
    p_launch.add_argument("command", help="Executable or command to run (e.g. notepad.exe, calc)")

    args = parser.parse_args()

    if args.action == "screenshot":
        res = take_screenshot(args.output, args.monitor)
        if args.json:
            print(json.dumps(res))
    elif args.action == "click":
        click_coords(args.x, args.y, args.button, args.clicks)
    elif args.action == "type":
        type_input(args.text, args.press)
    elif args.action == "hotkey":
        press_hotkey(*args.keys)
    elif args.action == "windows":
        wins = list_open_windows()
        if args.json:
            print(json.dumps(wins, indent=2))
        else:
            print(f"\nVisible Desktop Windows ({len(wins)}):")
            print("-" * 65)
            for i, w in enumerate(wins, 1):
                active_mark = "[ACTIVE] " if w["is_active"] else "         "
                print(f"{i:2d}. {active_mark}{w['title'][:45]:<45} ({w['width']}x{w['height']})")
            print()
    elif args.action == "focus":
        focus_window(args.title)
    elif args.action == "launch":
        launch_application(args.command)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
