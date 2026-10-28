#!/usr/bin/env python3
"""
Workshop Unified Event Bus & Telemetry Ledger (The Agent Nervous System)
========================================================================
Provides local asynchronous event publishing and logging across workshop subsystems 
(OpenHands, Browser-Use, Strix, Langflow, Skill Compounding, and Verification).
"""

import json
from pathlib import Path
from datetime import datetime, timezone

WORKSHOP_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = WORKSHOP_DIR / ".workshop_state"
LEDGER_FILE = LEDGER_DIR / "event_ledger.jsonl"

def ensure_ledger():
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if not LEDGER_FILE.exists():
        LEDGER_FILE.write_text("", encoding="utf-8")

def publish_event(event_type: str, source: str, payload: dict):
    ensure_ledger()
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "source": source,
        "payload": payload
    }
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    return event

def read_recent_events(limit: int = 50):
    ensure_ledger()
    if not LEDGER_FILE.exists():
        return []
    lines = LEDGER_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    events = []
    for line in lines[-limit:]:
        try:
            events.append(json.loads(line))
        except (IOError, OSError, json.JSONDecodeError):  # @court-exempt: json cache fallback
            pass
    return events

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Workshop Agent Nervous System Event Bus")
    parser.add_argument("action", choices=["publish", "read"], default="read", nargs="?")
    parser.add_argument("--type", default="GENERIC_EVENT")
    parser.add_argument("--source", default="workshop-cli")
    parser.add_argument("--data", default="{}")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if args.action == "publish":
        try:
            payload = json.loads(args.data)
        except Exception:
            payload = {"raw_data": args.data}
        ev = publish_event(args.type, args.source, payload)
        print(json.dumps(ev, indent=2))
    elif args.action == "read":
        events = read_recent_events(args.limit)
        print(json.dumps(events, indent=2))
