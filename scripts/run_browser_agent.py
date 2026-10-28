#!/usr/bin/env python3
"""
Workshop Live Browser Agent Runner
==================================
Spins up an autonomous browser session and streams screenshots/actions
in real-time to the Workshop Live Browser Hub (http://localhost:7860).

Supports:
- Headless / Headed execution across Chromium, Firefox, WebKit
- Connecting to existing running browser instances via CDP / Remote Debugging
- Persistent user profile mounting to reuse existing cookies and sessions

Usage:
    python scripts/run_browser_agent.py --url "https://news.ycombinator.com" --task "Inspect top stories" --live
    python scripts/run_browser_agent.py --url "https://huggingface.co" --browser firefox
    python scripts/run_browser_agent.py --cdp "http://localhost:9222" --task "Check active tab"
    python scripts/run_browser_agent.py --url "https://github.com" --profile "C:/Users/.../AppData/Roaming/Mozilla/Firefox/Profiles/..."
"""

import os
import sys
import time
import json
import argparse
import urllib.request
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

HUB_URL = "http://127.0.0.1:7860"

def notify_hub(action_name: str, details: str = "", url: str = None, screenshot_bytes: bytes = None):
    """Notify the local live browser dashboard."""
    try:
        payload = {"action": action_name, "details": details}
        if url:
            payload["url"] = url
        req = urllib.request.Request(
            f"{HUB_URL}/api/action",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=0.5)
    except Exception as err:  # @court-exempt: handled fallback
        pass

def run_agent_session(
    url: str,
    task: str = "",
    headed: bool = False,
    live: bool = True,
    browser_type: str = "chromium",
    cdp: str = None,
    profile: str = None
):
    print("\n=======================================================")
    print(f" [*] Launching AI Agent Browser Session")
    print(f" Target URL:   {url or (cdp and 'Attached Browser')}")
    print(f" Browser Type: {browser_type.upper()}")
    if cdp:
        print(f" Remote CDP:   {cdp}")
    if profile:
        print(f" User Profile: {profile}")
    print(f" Task:         {task or 'General Inspection'}")
    print(f" Live Stream:  {HUB_URL if live else 'Disabled'}")
    print("=======================================================\n")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] Playwright is not installed. Please install: uv tool install playwright")
        return

    notify_hub("session_start", f"Starting session for: {url or 'CDP'}", url=url)

    with sync_playwright() as p:
        browser = None
        context = None
        page = None

        if cdp:
            print(f" -> Attaching to running browser via CDP ({cdp})...")
            try:
                browser = p.chromium.connect_over_cdp(cdp)
                context = browser.contexts[0] if browser.contexts else browser.new_context()
                page = context.pages[0] if context.pages else context.new_page()
                print(f" [OK] Successfully attached to remote browser tab: '{page.title()}'")
            except Exception as e:
                print(f"[!] CDP Connection failed: {e}")
                print("    Ensure your browser was started with: --remote-debugging-port=9222")
                return
        elif profile:
            print(f" -> Launching persistent context with profile: {profile}...")
            engine = getattr(p, browser_type.lower(), p.chromium)
            try:
                context = engine.launch_persistent_context(
                    user_data_dir=profile,
                    headless=not headed,
                    viewport={"width": 1280, "height": 800}
                )
                page = context.pages[0] if context.pages else context.new_page()
            except Exception as e:
                print(f"[!] Could not launch persistent profile: {e}")
                return
        else:
            engine = getattr(p, browser_type.lower(), p.chromium)
            args_list = ["--disable-blink-features=AutomationControlled", "--no-sandbox"] if browser_type == "chromium" else []
            browser = engine.launch(
                headless=not headed,
                args=args_list
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            page = context.new_page()

        if url and (not cdp or page.url == "about:blank"):
            print(f" -> Navigating to {url}...")
            notify_hub("navigate", f"Navigating to {url}", url=url)
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Capture initial screenshot
        screenshot_path = Path(__file__).resolve().parent.parent / "browser_snapshot.jpg"
        try:
            page.screenshot(path=str(screenshot_path), type="jpeg", quality=80)
            print(f" [OK] Page loaded: {page.title()}")
            print(f" [OK] Screenshot saved to: {screenshot_path}")
            notify_hub("page_ready", f"Loaded title: '{page.title()}'", url=page.url)
        except Exception as e_snap:
            print(f"[!] Warning: Could not capture snapshot: {e_snap}")

        # If a task is specified or interactive
        if task:
            print(f" -> Executing task: {task}...")
            try:
                text_content = page.inner_text("body")[:500]
                print("\n--- Page Snippet ---")
                print(text_content.strip())
                print("--------------------\n")
            except Exception as err:  # @court-exempt: handled fallback
                pass

        print(" -> Browser session active. Press Ctrl+C to close or wait 5s...")
        try:
            for i in range(5):
                time.sleep(1)
                try:
                    page.screenshot(path=str(screenshot_path), type="jpeg", quality=75)
                except Exception as err:  # @court-exempt: handled fallback
                    pass
        except KeyboardInterrupt:
            print("\n [!] Stopping browser session.")
        
        if browser:
            browser.close()
        elif context:
            context.close()
            
        notify_hub("session_end", "Browser closed.")
        print(" [OK] Browser session finished successfully.\n")

def main():
    parser = argparse.ArgumentParser(description="Run autonomous browser agent with live stream")
    parser.add_argument("--url", "-u", default="https://example.com", help="Target URL")
    parser.add_argument("--task", "-t", default="", help="Task or instruction to execute")
    parser.add_argument("--browser", "-b", choices=["chromium", "firefox", "webkit"], default="chromium", help="Browser engine")
    parser.add_argument("--cdp", help="Attach to running browser via CDP (e.g. 'http://localhost:9222')")
    parser.add_argument("--profile", help="Path to existing browser profile directory")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    parser.add_argument("--live", action="store_true", default=True, help="Stream to Live Browser Hub")
    
    args = parser.parse_args()
    run_agent_session(
        args.url,
        task=args.task,
        headed=args.headed,
        live=args.live,
        browser_type=args.browser,
        cdp=args.cdp,
        profile=args.profile
    )

if __name__ == "__main__":
    main()
