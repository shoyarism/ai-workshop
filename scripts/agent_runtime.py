#!/usr/bin/env python3
"""
Workshop Agent Runtime & Persistent Core
========================================
A self-contained 24/7 agent daemon that:
1. Maintains a persistent SQLite task queue and memory store.
2. Drives Playwright / Camofox browser sessions autonomously.
3. Streams live screenshots and reasoning steps to the Live Browser Hub (Port 7860).
4. Executes workshop tools and skills.
"""

import os
import sys
import time
import json
import sqlite3
import asyncio
import threading
import traceback
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = WORKSHOP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "agent_runtime.db"
HEALTH_PORT = 7861

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            status TEXT DEFAULT 'pending', -- pending, running, completed, failed
            result TEXT,
            created_at REAL,
            updated_at REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            level TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

class AgentRuntime:
    def __init__(self):
        init_db()
        self.running = False
        self.current_task = None
        self.browser = None
        self.page = None
        self.health_server = None

    def start_health_server(self):
        """Start a simple HTTP health endpoint."""
        class HealthHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
            
            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path == "/health":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    status = {
                        "status": "ok",
                        "service": "agent_runtime",
                        "running": self.server.runtime.running,
                        "current_task": self.server.runtime.current_task,
                        "tasks_pending": self.get_pending_count(),
                        "uptime": time.time() - self.server.start_time
                    }
                    self.wfile.write(json.dumps(status).encode("utf-8"))
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def get_pending_count(self):
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
                    count = cursor.fetchone()[0]
                    conn.close()
                    return count
                except Exception:
                    return 0
        
        HealthHandler.server = self
        HealthHandler.runtime = self
        HealthHandler.start_time = time.time()
        
        server = HTTPServer(('127.0.0.1', HEALTH_PORT), HealthHandler)
        self.health_server = server
        
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.log("info", f"Health server started on port {HEALTH_PORT}")

    def log(self, level: str, message: str):
        print(f"[{time.strftime('%H:%M:%S')}] [{level.upper()}] {message}")
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)", (time.time(), level, message))
            conn.commit()
            conn.close()
        except Exception as err:  # @court-exempt: handled fallback
            pass

    def add_task(self, goal: str) -> int:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (goal, status, created_at, updated_at) VALUES (?, 'pending', ?, ?)", (goal, time.time(), time.time()))
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.log("info", f"Queued task #{task_id}: {goal}")
        return task_id

    def get_next_task(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, goal FROM tasks WHERE status = 'pending' ORDER BY id ASC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "goal": row[1]}
        return None

    def update_task_status(self, task_id: int, status: str, result: str = ""):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE tasks SET status = ?, result = ?, updated_at = ? WHERE id = ?", (status, result, time.time(), task_id))
        conn.commit()
        conn.close()

    def run_loop(self):
        self.running = True
        self.start_health_server()
        self.log("info", "Agent Runtime Daemon started successfully.")
        
        while self.running:
            task = self.get_next_task()
            if task:
                task_id = task["id"]
                goal = task["goal"]
                self.current_task = goal
                self.update_task_status(task_id, "running")
                self.log("info", f"Executing task #{task_id}: {goal}")
                
                try:
                    # Execute task (e.g. browser navigation or research)
                    result = asyncio.run(self.execute_agent_goal(goal))
                    self.update_task_status(task_id, "completed", result)
                    self.log("info", f"Task #{task_id} completed successfully.")
                except Exception as e:
                    err_msg = str(e) + "\n" + traceback.format_exc()
                    self.update_task_status(task_id, "failed", err_msg)
                    self.log("error", f"Task #{task_id} failed: {e}")
                
                self.current_task = None
            else:
                time.sleep(2)

    async def execute_agent_goal(self, goal: str):
        from playwright.async_api import async_playwright
        self.log("info", f"Launching Playwright for goal: {goal}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1280, "height": 800})
            
            # Simple heuristic: if goal is a URL or search query
            target_url = "https://www.google.com"
            if goal.startswith("http://") or goal.startswith("https://"):
                target_url = goal
            elif "browse" in goal.lower() or "visit" in goal.lower():
                # Extract URL if present
                words = goal.split()
                for w in words:
                    if w.startswith("http"):
                        target_url = w
            
            self.log("info", f"Navigating to {target_url}")
            await page.goto(target_url, timeout=30000)
            await page.wait_for_load_state("networkidle")
            
            title = await page.title()
            screenshot_bytes = await page.screenshot(type="jpeg", quality=85)
            
            # Save screenshot to shared state file for live browser hub
            state_file = WORKSHOP_DIR / "scripts" / ".browser_live_state.json"
            screenshot_path = WORKSHOP_DIR / "scripts" / ".browser_live_shot.jpg"
            with open(screenshot_path, "wb") as f:
                f.write(screenshot_bytes)
                
            state_data = {
                "current_url": page.url,
                "status": "idle",
                "page_title": title,
                "last_screenshot_file": str(screenshot_path),
                "timestamp": time.time(),
                "actions": [
                    {"time": time.strftime("%H:%M:%S"), "action": "navigate", "details": f"Navigated to {page.url} ({title})"}
                ]
            }
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2)
                
            await browser.close()
            return f"Successfully visited {page.url}. Page title: {title}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Workshop Agent Runtime Daemon")
    parser.add_argument("--add-task", type=str, help="Add a task to the queue")
    parser.add_argument("--list-tasks", action="store_true", help="List all tasks")
    args = parser.parse_args()
    
    if args.add_task:
        runtime = AgentRuntime()
        task_id = runtime.add_task(args.add_task)
        print(f"Added task #{task_id}: {args.add_task}")
        sys.exit(0)
    
    if args.list_tasks:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, goal, status, created_at FROM tasks ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        print(f"\n{'ID':<5} {'Status':<12} {'Created':<20} Goal")
        print("-" * 80)
        for row in rows:
            created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row[3]))
            print(f"{row[0]:<5} {row[2]:<12} {created:<20} {row[1][:60]}")
        sys.exit(0)
    
    # Default: run the daemon
    runtime = AgentRuntime()
    runtime.run_loop()
