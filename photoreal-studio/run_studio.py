# -*- coding: utf-8 -*-
"""
One-Click Launcher for Photoreal Studio.
Starts the local server and opens the browser.
"""

import os
import sys
import webbrowser
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn


def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\n=======================================================")
    print(f"  PHOTOREAL STUDIO - ULTRA-REALISTIC AI GENERATION")
    print(f"  Studio Web UI: {url}")
    print(f"=======================================================\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")


if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("backend.server:app", host="127.0.0.1", port=8000, reload=False, log_level="info")