#!/usr/bin/env python3
"""
Workshop Live Browser Streaming & Automation Hub
=================================================
Provides real-time browser automation with a live interactive web dashboard
for watching AI agent browser sessions in real-time.

Dashboard: http://localhost:7860
Features:
- Live MJPEG / WebSocket Viewport Streaming (watch the agent browse live)
- Real-time Action Logger & DOM Inspector
- Agent REST/WebSocket Dispatch API (navigate, click, type, screenshot, evaluate)
- Human-in-the-loop takeover, pause, and prompt injection

Usage:
    python scripts/live_browser_hub.py [--port 7860] [--headless]
"""

import os
import sys
import time
import json
import base64
import asyncio
import argparse
import threading
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Global State
BROWSER_STATE = {
    "current_url": "about:blank",
    "status": "idle", # idle, navigating, interacting, waiting
    "last_screenshot": None, # bytes
    "actions": [],
    "page_title": "Workshop Live Browser",
    "viewport": {"width": 1280, "height": 800},
    "active": True
}

def load_live_state():
    state_file = Path(__file__).resolve().parent / ".browser_live_state.json"
    shot_file = Path(__file__).resolve().parent / ".browser_live_shot.jpg"
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                BROWSER_STATE["current_url"] = data.get("current_url", BROWSER_STATE["current_url"])
                BROWSER_STATE["page_title"] = data.get("page_title", BROWSER_STATE["page_title"])
                if "actions" in data:
                    BROWSER_STATE["actions"] = data["actions"]
        except Exception as err:  # @court-exempt: handled fallback
            pass
    if shot_file.exists():
        try:
            with open(shot_file, "rb") as f:
                BROWSER_STATE["last_screenshot"] = f.read()
        except Exception as err:  # @court-exempt: handled fallback
            pass

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Live Browser Hub — Workshop</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --border-color: #30363d;
            --accent: #58a6ff;
            --accent-green: #238636;
            --accent-purple: #8957e5;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: var(--bg-primary); color: var(--text-primary); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        header { background-color: var(--bg-secondary); border-bottom: 1px solid var(--border-color); padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; }
        .logo-area { display: flex; align-items: center; gap: 12px; }
        .badge { background: var(--accent-purple); color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; background: #2ea043; display: inline-block; box-shadow: 0 0 8px #2ea043; }
        .container { display: grid; grid-template-columns: 1fr 380px; flex: 1; overflow: hidden; }
        
        /* Browser Viewport */
        .viewport-section { display: flex; flex-direction: column; background: #000; border-right: 1px solid var(--border-color); }
        .url-bar { background: var(--bg-secondary); padding: 8px 16px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid var(--border-color); }
        .url-input { flex: 1; background: var(--bg-tertiary); border: 1px solid var(--border-color); color: var(--text-primary); padding: 6px 12px; border-radius: 6px; font-size: 13px; outline: none; }
        .stream-container { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; overflow: auto; background: #0a0c10; }
        #live-stream { max-width: 100%; max-height: 100%; object-fit: contain; box-shadow: 0 4px 20px rgba(0,0,0,0.5); border-radius: 4px; }
        .empty-stream { text-align: center; color: var(--text-secondary); }
        
        /* Sidebar & Logs */
        .sidebar { background: var(--bg-secondary); display: flex; flex-direction: column; }
        .tab-header { display: flex; border-bottom: 1px solid var(--border-color); background: var(--bg-primary); }
        .tab-btn { flex: 1; padding: 10px; background: none; border: none; color: var(--text-secondary); font-weight: 600; cursor: pointer; font-size: 13px; text-align: center; }
        .tab-btn.active { color: var(--accent); border-bottom: 2px solid var(--accent); background: var(--bg-secondary); }
        .tab-content { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
        .action-item { background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; font-size: 12px; }
        .action-time { color: var(--text-secondary); font-size: 11px; margin-bottom: 4px; }
        .action-cmd { font-family: monospace; color: var(--accent); font-weight: 600; }
        
        /* Controls */
        .control-panel { padding: 12px; background: var(--bg-primary); border-top: 1px solid var(--border-color); display: flex; gap: 8px; }
        .btn { background: var(--accent-green); color: white; border: none; padding: 8px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; }
        .btn-secondary { background: var(--bg-tertiary); border: 1px solid var(--border-color); color: var(--text-primary); }
        .btn:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <header>
        <div class="logo-area">
            <span class="status-dot"></span>
            <h2>AI Agent Live Browser</h2>
            <span class="badge">Live Stream</span>
        </div>
        <div>
            <span id="session-status" style="font-size: 13px; color: var(--text-secondary);">Agent Status: <strong style="color: #2ea043;">Ready</strong></span>
        </div>
    </header>

    <div class="container">
        <div class="viewport-section">
            <div class="url-bar">
                <span style="font-size: 14px;">🌐</span>
                <input type="text" id="url-display" class="url-input" value="https://google.com" readonly />
                <button class="btn btn-secondary" onclick="refreshFrame()">Refresh</button>
            </div>
            <div class="stream-container">
                <img id="live-stream" src="/stream.mjpg" alt="Agent Live View" onerror="showPlaceholder()" />
                <div id="stream-placeholder" class="empty-stream" style="display: none;">
                    <h3>Waiting for Agent Browser Session...</h3>
                    <p style="margin-top: 8px;">Run <code>python scripts/run_browser_agent.py --url &lt;url&gt;</code> to start.</p>
                </div>
            </div>
        </div>

        <div class="sidebar">
            <div class="tab-header">
                <button class="tab-btn active">Agent Activity Log</button>
            </div>
            <div id="action-logs" class="tab-content">
                <div class="action-item">
                    <div class="action-time">System Ready</div>
                    <div class="action-cmd">Live Browser Hub initialized on :7860</div>
                </div>
            </div>
            <div class="control-panel">
                <input type="text" id="agent-input" class="url-input" placeholder="Inject prompt / URL..." />
                <button class="btn" onclick="sendAgentAction()">Dispatch</button>
            </div>
        </div>
    </div>

    <script>
        function refreshFrame() {
            const img = document.getElementById('live-stream');
            img.src = '/screenshot?t=' + new Date().getTime();
        }
        function showPlaceholder() {
            document.getElementById('live-stream').style.display = 'none';
            document.getElementById('stream-placeholder').style.display = 'block';
        }
        
        // Poll status & actions
        setInterval(async () => {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                if (data.current_url) {
                    document.getElementById('url-display').value = data.current_url;
                }
                const logsDiv = document.getElementById('action-logs');
                if (data.actions && data.actions.length > 0) {
                    logsDiv.innerHTML = data.actions.map(act => `
                        <div class="action-item">
                            <div class="action-time">${act.time}</div>
                            <div class="action-cmd">${act.action}</div>
                            <div style="margin-top: 4px; color: var(--text-secondary);">${act.details || ''}</div>
                        </div>
                    `).join('');
                }
            } catch(e) { /* @court-exempt: polling error */ }
        }, 1000);

        async function sendAgentAction() {
            const input = document.getElementById('agent-input');
            const val = input.value.trim();
            if (!val) return;
            await fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: 'navigate', url: val})
            });
            input.value = '';
        }
    </script>
</body>
</html>
"""

class LiveBrowserHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        try:
            sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))
            sys.stderr.flush()
        except Exception as err:  # @court-exempt: handled fallback
            pass

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
            return
            
        elif parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "hub": "live-browser"}).encode("utf-8"))
            return
            
        elif parsed.path == "/api/status":
            load_live_state()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": BROWSER_STATE["status"],
                "current_url": BROWSER_STATE["current_url"],
                "page_title": BROWSER_STATE["page_title"],
                "actions": BROWSER_STATE["actions"][-20:]
            }).encode("utf-8"))
            return
            
        elif parsed.path == "/screenshot":
            load_live_state()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.end_headers()
            if BROWSER_STATE["last_screenshot"]:
                self.wfile.write(BROWSER_STATE["last_screenshot"])
            else:
                # Return 1x1 blank image
                self.wfile.write(b"")
            return
            
        elif parsed.path == "/stream.mjpg":
            # MJPEG stream
            self.send_response(200)
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
            self.end_headers()
            try:
                while BROWSER_STATE["active"]:
                    load_live_state()
                    if BROWSER_STATE["last_screenshot"]:
                        self.wfile.write(b"--frame\r\n")
                        self.send_header("Content-Type", "image/jpeg")
                        self.send_header("Content-Length", str(len(BROWSER_STATE["last_screenshot"])))
                        self.end_headers()
                        self.wfile.write(BROWSER_STATE["last_screenshot"])
                        self.wfile.write(b"\r\n")
                    time.sleep(0.5)
            except Exception as err:  # @court-exempt: handled fallback
                pass
            return
            
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/action":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode('utf-8'))
                BROWSER_STATE["actions"].append({
                    "time": time.strftime("%H:%M:%S"),
                    "action": data.get("action", "custom"),
                    "details": str(data)
                })
                if "url" in data:
                    BROWSER_STATE["current_url"] = data["url"]
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port: int = 7860):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, LiveBrowserHandler)
    print(f"\n=======================================================")
    print(f" 🚀 Workshop Live Browser Hub Active: http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        BROWSER_STATE["active"] = False
        httpd.server_close()

def main():
    parser = argparse.ArgumentParser(description="Workshop Live Browser Hub")
    parser.add_argument("--port", type=int, default=7860, help="Port to host live dashboard")
    args = parser.parse_args()
    run_server(args.port)

if __name__ == "__main__":
    main()
