#!/usr/bin/env python3
"""
Workshop Agent Watchdog — 24/7 Supervisor
==========================================
Monitors and auto-restarts the Agent Runtime daemon and Live Browser Hub.
Survives reboots via Windows Task Scheduler or systemd on Linux.
"""

import os
import sys
import time
import json
import subprocess
import signal
import threading
import traceback
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = WORKSHOP_DIR / "scripts"
DATA_DIR = WORKSHOP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

STATE_FILE = DATA_DIR / "watchdog_state.json"
LOG_FILE = SCRIPTS_DIR / ".watchdog.log"
WATCHDOG_HEALTH_PORT = 7862

SERVICES = {
    "agent_runtime": {
        "name": "Agent Runtime Daemon",
        "command": [sys.executable, str(SCRIPTS_DIR / "agent_runtime.py")],
        "health_check": lambda: check_http_health("http://127.0.0.1:7861/health"),
        "restart_delay": 5,
        "max_restarts": 10,
        "restart_window": 300,  # 5 minutes
    },
    "browser_hub": {
        "name": "Live Browser Hub",
        "command": [sys.executable, str(SCRIPTS_DIR / "live_browser_hub.py"), "--port", "7860"],
        "health_check": lambda: check_http_health("http://127.0.0.1:7860/health"),
        "restart_delay": 3,
        "max_restarts": 5,
        "restart_window": 300,
    },
    "watchdog": {
        "name": "Agent Watchdog (Self-check)",
        "command": [sys.executable, str(SCRIPTS_DIR / "agent_watchdog.py")],
        "health_check": lambda: check_http_health("http://127.0.0.1:7862/health"),
        "restart_delay": 3,
        "max_restarts": 3,
        "restart_window": 300,
    },
}

def check_http_health(url: str, timeout: float = 1.5) -> bool:
    """Check if an HTTP health endpoint responds with 200 OK."""
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WorkshopWatchdog/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False

def write_log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:  # @court-exempt: handled fallback
        pass
    print(line.strip())

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, OSError, json.JSONDecodeError):  # @court-exempt: json cache fallback
            pass
    return {}

def save_state(state: dict):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:  # @court-exempt: handled fallback
        pass

def start_health_server():
    """Start a simple HTTP health endpoint for the watchdog itself."""
    class HealthHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):  # @court-exempt: suppress noisy HTTP server logging
            pass
        
        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                status = {
                    "status": "ok",
                    "service": "watchdog",
                    "uptime": time.time() - self.server.start_time,
                    "monitored_services": list(SERVICES.keys())
                }
                self.wfile.write(json.dumps(status).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
    
    server = HTTPServer(('127.0.0.1', WATCHDOG_HEALTH_PORT), HealthHandler)
    server.start_time = time.time()
    
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    write_log(f"[*] Watchdog health server started on port {WATCHDOG_HEALTH_PORT}")

def is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            output = subprocess.check_output(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            return str(pid) in output
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

def kill_pid(pid: int) -> bool:
    if pid <= 0 or not is_pid_alive(pid):
        return True
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.5)
            if is_pid_alive(pid):
                os.kill(pid, signal.SIGKILL)
        return True
    except Exception:
        return False

def start_service(key: str) -> dict:
    svc = SERVICES[key]
    write_log(f"[*] Starting {svc['name']}...")
    
    creationflags = 0
    if os.name == "nt":
        creationflags = 0x00000008 | 0x00000200 | 0x01000000
    
    log_file = SCRIPTS_DIR / f".{key}.log"
    out = open(log_file, "a", encoding="utf-8")
    out.write(f"\n--- Service Started at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    out.flush()
    
    proc = subprocess.Popen(
        svc["command"],
        cwd=str(WORKSHOP_DIR),
        stdout=out,
        stderr=subprocess.STDOUT,
        creationflags=creationflags,
        close_fds=True if os.name != "nt" else False,
    )
    
    state = load_state()
    state[key] = {
        "pid": proc.pid,
        "started_at": time.time(),
        "restart_count": state.get(key, {}).get("restart_count", 0),
        "last_restart": state.get(key, {}).get("last_restart", 0),
    }
    save_state(state)
    
    write_log(f"[OK] {svc['name']} started (PID: {proc.pid})")
    return {"success": True, "pid": proc.pid}

def check_restart_limit(key: str) -> bool:
    state = load_state()
    svc = SERVICES[key]
    info = state.get(key, {})
    restart_count = info.get("restart_count", 0)
    last_restart = info.get("last_restart", 0)
    
    if time.time() - last_restart > svc["restart_window"]:
        # Reset counter if outside window
        return True
    
    return restart_count < svc["max_restarts"]

def increment_restart(key: str):
    state = load_state()
    if key not in state:
        state[key] = {}
    state[key]["restart_count"] = state[key].get("restart_count", 0) + 1
    state[key]["last_restart"] = time.time()
    save_state(state)

def monitor_services():
    write_log("[*] Watchdog started - monitoring services 24/7")
    start_health_server()
    
    # Initial start
    for key in SERVICES:
        start_service(key)
    
    while True:
        for key in SERVICES:
            svc = SERVICES[key]
            state = load_state()
            info = state.get(key, {})
            pid = info.get("pid", 0)
            
            # Check if process is alive
            process_alive = is_pid_alive(pid)
            health_ok = True
            
            try:
                health_ok = svc["health_check"]()
            except Exception:
                health_ok = False
            
            if not process_alive or not health_ok:
                write_log(f"[!] {svc['name']} unhealthy (pid_alive={process_alive}, health={health_ok})")
                
                if check_restart_limit(key):
                    write_log(f"[*] Restarting {svc['name']}...")
                    if pid:
                        kill_pid(pid)
                    time.sleep(svc["restart_delay"])
                    increment_restart(key)
                    start_service(key)
                else:
                    write_log(f"[!] {svc['name']} exceeded restart limit. Manual intervention required.")
            else:
                # Process healthy
                pass
        
        time.sleep(10)

def install_windows_task():
    """Install watchdog as a Windows Scheduled Task for auto-start on boot."""
    script_path = str(SCRIPTS_DIR / "agent_watchdog.py").replace("/", "\\")
    python_exe = sys.executable.replace("/", "\\")
    
    # PowerShell command to create scheduled task
    ps_cmd = f"""
$action = New-ScheduledTaskAction -Execute '{python_exe}' -Argument '{script_path}'
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
Register-ScheduledTask -TaskName 'WorkshopAgentWatchdog' -Action $action -Trigger $trigger -Settings $settings -Force -RunLevel Highest
"""
    try:
        subprocess.run(["powershell", "-Command", ps_cmd], check=True)
        write_log("[OK] Windows Scheduled Task 'WorkshopAgentWatchdog' installed for auto-start on boot.")
    except Exception as e:
        write_log(f"[!] Failed to install Windows task: {e}")

def install_linux_systemd():
    """Generate systemd service file for Linux auto-start."""
    service_content = f"""[Unit]
Description=Workshop Agent Watchdog
After=network.target

[Service]
Type=simple
WorkingDirectory={WORKSHOP_DIR}
ExecStart={sys.executable} {SCRIPTS_DIR / "agent_watchdog.py"}
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
    service_path = Path("/etc/systemd/system/workshop-agent-watchdog.service")
    try:
        service_path.write_text(service_content)
        write_log(f"[OK] systemd service written to {service_path}. Run: sudo systemctl enable --now workshop-agent-watchdog")
    except Exception as e:
        write_log(f"[!] Failed to write systemd service: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Workshop Agent Watchdog — 24/7 Supervisor")
    parser.add_argument("--install", action="store_true", help="Install auto-start on boot (Windows Task Scheduler or systemd)")
    parser.add_argument("--run", action="store_true", help="Run watchdog loop (default)")
    args = parser.parse_args()
    
    if args.install:
        if os.name == "nt":
            install_windows_task()
        else:
            install_linux_systemd()
        return
    
    # Run monitor loop
    try:
        monitor_services()
    except KeyboardInterrupt:
        write_log("[*] Watchdog stopped by user.")
    except Exception as e:
        write_log(f"[!] Watchdog crashed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()