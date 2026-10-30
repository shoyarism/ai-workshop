#!/usr/bin/env python3
"""
Workshop Gateway & Background Services Supervisor
=================================================
Manages persistent local services and gateways for AI agents:
  - Live Browser Hub (Port 7860) -> http://127.0.0.1:7860/health
  - Camofox Stealth Browser (Port 9377) -> http://127.0.0.1:9377/health

Usage:
    python scripts/workshop_services.py status
    python scripts/workshop_services.py start [service_name|all]
    python scripts/workshop_services.py stop [service_name|all]
    python scripts/workshop_services.py restart [service_name|all]
"""

import os
import sys
import time
import json
import signal
import shutil
import urllib.request
import urllib.error
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
STATE_FILE = SCRIPTS_DIR / ".services_state.json"

SERVICES = {
    "browser_hub": {
        "name": "Live Browser Hub",
        "port": 7860,
        "health_url": "http://127.0.0.1:7860/health",
        "cwd": str(WORKSHOP_DIR),
        "command": [sys.executable, str(SCRIPTS_DIR / "live_browser_hub.py"), "--port", "7860"],
        "description": "Real-time browser streaming dashboard and viewport",
    },
    "camofox": {
        "name": "Camofox Anti-Detect Browser",
        "port": 9377,
        "health_url": "http://127.0.0.1:9377/health",
        "cwd": str(WORKSHOP_DIR / "camofox-browser"),
        "command": ["node", "server.js"],
        "description": "Stealth anti-detection headless browser engine",
    },
    "agent_runtime": {
        "name": "Agent Runtime Daemon",
        "port": 7861,
        "health_url": "http://127.0.0.1:7861/health",
        "cwd": str(WORKSHOP_DIR),
        "command": [sys.executable, str(SCRIPTS_DIR / "agent_runtime.py")],
        "description": "Persistent autonomous agent with task queue and memory",
    },
    "watchdog": {
        "name": "Agent Watchdog (24/7 Supervisor)",
        "port": 7862,
        "health_url": "http://127.0.0.1:7862/health",
        "cwd": str(WORKSHOP_DIR),
        "command": [sys.executable, str(SCRIPTS_DIR / "agent_watchdog.py")],
        "description": "Auto-restart supervisor for agent services",
    },
}


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state: dict):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:  # @court-exempt: handled fallback
        pass


def probe_health(url: str, timeout: float = 1.5) -> tuple[bool, float, str]:
    """Check if an HTTP health endpoint responds with 200 OK. Returns (is_healthy, latency_ms, detail)."""
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WorkshopSupervisor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            latency = (time.perf_counter() - t0) * 1000.0
            if resp.status == 200:
                body = resp.read(256).decode("utf-8", errors="replace")
                return True, latency, body.strip()
            return False, latency, f"Status {resp.status}"
    except urllib.error.URLError as e:
        latency = (time.perf_counter() - t0) * 1000.0
        return False, latency, str(e.reason)
    except Exception as e:
        latency = (time.perf_counter() - t0) * 1000.0
        return False, latency, str(e)


def is_pid_alive(pid: int) -> bool:
    """Check if process with PID exists."""
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
    """Safely terminate a process by PID."""
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


def get_service_status(key: str) -> dict:
    svc = SERVICES.get(key)
    if not svc:
        return {"error": f"Unknown service '{key}'"}

    state = load_state()
    pid = state.get(key, {}).get("pid", 0)
    pid_active = is_pid_alive(pid)
    is_healthy, latency, detail = probe_health(svc["health_url"])

    return {
        "key": key,
        "name": svc["name"],
        "port": svc["port"],
        "health_url": svc["health_url"],
        "description": svc["description"],
        "pid": pid if pid_active else None,
        "online": is_healthy,
        "latency_ms": round(latency, 2) if is_healthy else None,
        "detail": detail,
    }


def start_service(key: str) -> dict:
    svc = SERVICES.get(key)
    if not svc:
        print(f"[!] Unknown service: {key}")
        return {"success": False, "error": "unknown service"}

    status = get_service_status(key)
    if status["online"]:
        print(f"[*] {svc['name']} is ALREADY RUNNING on Port {svc['port']} (PID: {status['pid']}, {status['latency_ms']}ms).")
        return {"success": True, "already_running": True}

    print(f"[*] Starting {svc['name']} (Port {svc['port']})...")

    # Verify binary exists (e.g. node for camofox)
    bin_name = svc["command"][0]
    if not shutil.which(bin_name) and not Path(bin_name).exists():
        print(f"[!] Required binary '{bin_name}' not found on PATH.")
        return {"success": False, "error": f"missing binary {bin_name}"}

    cwd_path = Path(svc["cwd"])
    if not cwd_path.exists():
        print(f"[!] Working directory does not exist: {cwd_path}")
        return {"success": False, "error": "cwd missing"}

    # Launch detached process
    creationflags = 0
    if os.name == "nt":
        # DETACHED_PROCESS (0x8) | CREATE_NEW_PROCESS_GROUP (0x200) | CREATE_BREAKAWAY_FROM_JOB (0x01000000)
        creationflags = 0x00000008 | 0x00000200 | 0x01000000

    log_file = SCRIPTS_DIR / f".{key}.log"
    out = open(log_file, "a", encoding="utf-8")
    out.write(f"\n--- Service Started at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    out.flush()
    proc = subprocess.Popen(
        svc["command"],
        cwd=str(cwd_path),
        stdout=out,
        stderr=subprocess.STDOUT,
        creationflags=creationflags,
        close_fds=True if os.name != "nt" else False,
    )

    state = load_state()
    state[key] = {
        "pid": proc.pid,
        "started_at": time.time(),
        "log": str(log_file),
    }
    save_state(state)

    # Wait for health check with polling (up to 8 seconds)
    print(f"[*] Waiting for {svc['name']} health probe on {svc['health_url']}...")
    for _ in range(16):
        time.sleep(0.5)
        healthy, latency, detail = probe_health(svc["health_url"])
        if healthy:
            print(f"[OK] {svc['name']} is ONLINE (PID: {proc.pid}, Latency: {round(latency, 1)}ms)")
            return {"success": True, "pid": proc.pid, "latency": latency}

    print(f"[!] {svc['name']} spawned (PID: {proc.pid}) but health probe timed out. Check log: {log_file}")
    return {"success": False, "pid": proc.pid, "warning": "probe_timeout"}


def stop_service(key: str) -> bool:
    svc = SERVICES.get(key)
    if not svc:
        print(f"[!] Unknown service: {key}")
        return False

    state = load_state()
    pid = state.get(key, {}).get("pid", 0)

    print(f"[*] Stopping {svc['name']} (PID: {pid})...")
    if pid:
        kill_pid(pid)
    
    # Also check if anything else is listening on that port
    time.sleep(0.5)
    healthy, _, _ = probe_health(svc["health_url"], timeout=0.5)
    if not healthy:
        print(f"[OK] {svc['name']} stopped cleanly.")
        state.pop(key, None)
        save_state(state)
        return True
    else:
        print(f"[!] Warning: Port {svc['port']} still responding after process termination.")
        return False


def cmd_status():
    print("\n=======================================================")
    print(" 🌐 WORKSHOP PERSISTENT SERVICES & GATEWAYS STATUS")
    print("=======================================================\n")
    print(f"{'Service':<30} {'Port':<8} {'Status':<12} {'PID':<8} {'Latency'}")
    print("-" * 68)

    for key in SERVICES:
        st = get_service_status(key)
        status_label = "[ONLINE]" if st["online"] else "[OFFLINE]"
        pid_label = str(st["pid"]) if st["pid"] else "-"
        lat_label = f"{st['latency_ms']} ms" if st["latency_ms"] is not None else "-"
        print(f"{st['name']:<30} {st['port']:<8} {status_label:<12} {pid_label:<8} {lat_label}")

    print("\nUse 'python scripts/workshop.py services start <service|all>' to start.")
    print("=======================================================\n")


def cmd_start(targets: list[str]):
    if not targets or "all" in targets:
        targets = list(SERVICES.keys())
    for t in targets:
        start_service(t)


def cmd_stop(targets: list[str]):
    if not targets or "all" in targets:
        targets = list(SERVICES.keys())
    for t in targets:
        stop_service(t)


def cmd_restart(targets: list[str]):
    cmd_stop(targets)
    time.sleep(1)
    cmd_start(targets)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Workshop Services & Gateways Supervisor")
    sub = parser.add_subparsers(dest="action", help="Service command")

    sub.add_parser("status", help="Show live status of all services")
    p_start = sub.add_parser("start", help="Start service(s)")
    p_start.add_argument("services", nargs="*", default=["all"], help="Service name or 'all'")

    p_stop = sub.add_parser("stop", help="Stop service(s)")
    p_stop.add_argument("services", nargs="*", default=["all"], help="Service name or 'all'")

    p_restart = sub.add_parser("restart", help="Restart service(s)")
    p_restart.add_argument("services", nargs="*", default=["all"], help="Service name or 'all'")

    args = parser.parse_args()

    if args.action == "status" or not args.action:
        cmd_status()
    elif args.action == "start":
        cmd_start(args.services)
    elif args.action == "stop":
        cmd_stop(args.services)
    elif args.action == "restart":
        cmd_restart(args.services)


if __name__ == "__main__":
    main()
