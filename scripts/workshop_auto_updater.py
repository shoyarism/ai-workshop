#!/usr/bin/env python3
"""
Workshop Auto-Updater (Subsystem Drift Sync & Skill Refresh)
============================================================
Automatically syncs subsystems from upstream git remotes, refreshes skill indexes,
and manages the complete update lifecycle for the Workshop ecosystem.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone

WORKSHOP_DIR = Path(__file__).resolve().parent.parent
CATALOG_PATH = WORKSHOP_DIR / "CATALOG.json"

def load_catalog() -> dict:
    """Load the workshop catalog."""
    if CATALOG_PATH.exists():
        return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {"subsystems": {}}

def check_subsystem_drift(subsystem_name: str, subsystem_info: dict) -> dict:
    """Check if a subsystem has drifted from its upstream remote."""
    path = WORKSHOP_DIR / subsystem_info.get("path", subsystem_name)
    remote = subsystem_info.get("git_remote", "")
    
    if not remote:
        return {"subsystem": subsystem_name, "has_remote": False}
    
    try:
        # Check if directory is a git repo
        git_dir = path / ".git"
        if not git_dir.exists():
            return {"subsystem": subsystem_name, "has_remote": False, "is_git": False}
        
        # Fetch latest
        fetch_result = subprocess.run(
            ["git", "fetch", "origin"],
            cwd=path, capture_output=True, text=True, timeout=60
        )
        
        # Check if behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"],
            cwd=path, capture_output=True, text=True
        )
        
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                ahead, behind = int(parts[0]), int(parts[1])
                return {
                    "subsystem": subsystem_name,
                    "has_remote": True,
                    "is_git": True,
                    "ahead": ahead,
                    "behind": behind,
                    "needs_update": behind > 0
                }
    except Exception as e:
        return {"subsystem": subsystem_name, "error": str(e)}
    
    return {"subsystem": subsystem_name, "has_remote": True, "is_git": True, "ahead": 0, "behind": 0}

def sync_subsystem(subsystem_name: str, subsystem_info: dict, dry_run: bool = True) -> dict:
    """Sync a subsystem from upstream."""
    path = WORKSHOP_DIR / subsystem_info.get("path", subsystem_name)
    
    if dry_run:
        drift = check_subsystem_drift(subsystem_name, subsystem_info)
        return {"subsystem": subsystem_name, "dry_run": True, "drift": drift}
    
    try:
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=path, capture_output=True, text=True
        )
        return {
            "subsystem": subsystem_name,
            "success": result.returncode == 0,
            "output": result.stdout[-500:] if result.stdout else "",
            "error": result.stderr[-500:] if result.stderr else ""
        }
    except Exception as e:
        return {"subsystem": subsystem_name, "success": False, "error": str(e)}

def refresh_skill_index() -> dict:
    """Refresh the semantic skill index after updates."""
    try:
        result = subprocess.run(
            [sys.executable, str(WORKSHOP_DIR / "scripts" / "workshop_semantic_indexer.py"), "--action", "index"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {"status": "error", "error": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def run_auto_update_cycle(dry_run: bool = True) -> dict:
    """Run a complete auto-update cycle."""
    catalog = load_catalog()
    subsystems = catalog.get("subsystems", {})
    
    print(f"[AUTO-UPDATE] Checking {len(subsystems)} subsystems...")
    
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "subsystems_checked": 0,
        "subsystems_behind": 0,
        "subsystems_updated": 0,
        "details": []
    }
    
    for name, info in subsystems.items():
        drift = check_subsystem_drift(name, info)
        results["subsystems_checked"] += 1
        
        if drift.get("behind", 0) > 0:
            results["subsystems_behind"] += 1
            print(f"  [!] {name}: {drift['behind']} commits behind")
            
            if not dry_run:
                sync_result = sync_subsystem(name, info, dry_run=False)
                results["subsystems_updated"] += 1
                results["details"].append(sync_result)
            else:
                results["details"].append({"subsystem": name, "would_update": True, "drift": drift})
    
    # Refresh skill index
    if not dry_run and results["subsystems_updated"] > 0:
        print("[AUTO-UPDATE] Refreshing skill index...")
        refresh_result = refresh_skill_index()
        results["skill_refresh"] = refresh_result
    
    print(f"[AUTO-UPDATE] Complete: {results['subsystems_behind']} behind, {results['subsystems_updated']} updated")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workshop Auto-Updater")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Check only, don't pull")
    parser.add_argument("--execute", action="store_true", help="Actually execute updates")
    parser.add_argument("--refresh-index", action="store_true", help="Only refresh skill index")
    args = parser.parse_args()
    
    if args.refresh_index:
        result = refresh_skill_index()
        print(json.dumps(result, indent=2))
    else:
        result = run_auto_update_cycle(dry_run=not args.execute)
        print(json.dumps(result, indent=2, default=str))