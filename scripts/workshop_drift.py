#!/usr/bin/env python3
"""
Workshop Subsystem Drift & Upstream Sync Engine
===============================================
Audits all 33 integrated subsystems against upstream GitHub remotes.
Detects commit divergence, uncommitted changes, and provides automated
fast-forward synchronization to prevent bit rot across the Workshop.

Usage:
    python scripts/workshop_drift.py [--fetch] [--sync] [--json]
    python scripts/workshop.py drift [--fetch] [--sync]
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
CATALOG_PATH = WORKSHOP_DIR / "CATALOG.json"


def _run_git(cwd: Path, args: list, timeout: int = 15) -> tuple[int, str, str]:
    """Run git command in subsystem directory with timeout."""
    try:
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes"
        res = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            env=env
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def audit_subsystem(sub_key: str, sub_info: dict, do_fetch: bool = False) -> dict:
    """Audit a single subsystem for git remote status and commit drift."""
    sub_path = WORKSHOP_DIR / sub_info.get("path", sub_key)
    result = {
        "key": sub_key,
        "name": sub_info.get("name", sub_key),
        "path": str(sub_path.relative_to(WORKSHOP_DIR)).replace("\\", "/"),
        "is_git": False,
        "branch": "unknown",
        "behind": 0,
        "ahead": 0,
        "dirty": False,
        "status": "NOT_GIT",
        "remote_url": sub_info.get("git_remote", ""),
        "detail": ""
    }

    if not sub_path.exists():
        result["status"] = "DIR_MISSING"
        return result

    git_dir = sub_path / ".git"
    if not git_dir.exists():
        result["status"] = "LOCAL_NO_GIT"
        return result

    result["is_git"] = True

    # 1. Get current branch
    code, out, _ = _run_git(sub_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    if code == 0 and out:
        result["branch"] = out

    # 2. Check for uncommitted changes
    code, out, _ = _run_git(sub_path, ["status", "--porcelain"])
    if code == 0 and out:
        result["dirty"] = True

    # 3. Optional fetch remote
    if do_fetch:
        _run_git(sub_path, ["fetch", "origin", "--quiet"], timeout=20)

    # 4. Check upstream tracking
    code, upstream, _ = _run_git(sub_path, ["rev-parse", "--abbrev-ref", "@{u}"])
    if code != 0:
        result["status"] = "NO_UPSTREAM"
        result["detail"] = "No upstream tracking branch configured"
        return result

    # 5. Check ahead/behind counts
    code, counts, _ = _run_git(sub_path, ["rev-list", "--left-right", "--count", "HEAD...@{u}"])
    if code == 0 and counts:
        parts = counts.split()
        if len(parts) >= 2:
            try:
                result["ahead"] = int(parts[0])
                result["behind"] = int(parts[1])
            except ValueError:
                pass

    if result["behind"] > 0 and result["ahead"] > 0:
        result["status"] = "DIVERGED"
    elif result["behind"] > 0:
        result["status"] = "BEHIND"
    elif result["ahead"] > 0:
        result["status"] = "AHEAD"
    else:
        result["status"] = "UP_TO_DATE"

    return result


def sync_subsystem(sub_key: str, sub_info: dict) -> dict:
    """Execute safe fast-forward pull for a subsystem."""
    sub_path = WORKSHOP_DIR / sub_info.get("path", sub_key)
    res_status = {"key": sub_key, "action": "skipped", "message": ""}

    if not (sub_path / ".git").exists():
        res_status["message"] = "Not a git repository"
        return res_status

    # Check dirty
    code, out, _ = _run_git(sub_path, ["status", "--porcelain"])
    if out:
        res_status["message"] = "Skipped: local uncommitted changes exist"
        return res_status

    code, out, err = _run_git(sub_path, ["pull", "--ff-only"], timeout=30)
    if code == 0:
        res_status["action"] = "updated"
        res_status["message"] = out or "Fast-forward update successful"
    else:
        res_status["action"] = "failed"
        res_status["message"] = err or out or "Pull failed"

    return res_status


def run_drift_audit(do_fetch: bool = True, do_sync: bool = False, as_json: bool = False):
    if not CATALOG_PATH.exists():
        print("[!] CATALOG.json missing. Run: python scripts/workshop.py index")
        return

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    subsystems = data.get("subsystems", {})

    print("\n=======================================================")
    print(" 🛰️ WORKSHOP DRIFT & UPSTREAM HEALTH AUDITOR")
    print(f" Auditing {len(subsystems)} Integrated Subsystems against Upstream...")
    if do_fetch:
        print(" [Action: Fetching latest git remote metadata in parallel]")
    print("=======================================================\n")

    # Parallel audit with ThreadPool
    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(audit_subsystem, k, v, do_fetch): k
            for k, v in subsystems.items()
        }
        for fut in futures:
            try:
                results.append(fut.result())
            except Exception as e:
                k = futures[fut]
                results.append({"key": k, "status": "ERROR", "detail": str(e)})

    # Sort results
    results.sort(key=lambda x: (x.get("status") != "BEHIND", x.get("key", "")))

    if as_json:
        print(json.dumps(results, indent=2))
        return

    # Display Table
    status_icons = {
        "UP_TO_DATE": "🟢 UP-TO-DATE",
        "BEHIND": "🟡 BEHIND",
        "AHEAD": "🔵 AHEAD",
        "DIVERGED": "🔴 DIVERGED",
        "NO_UPSTREAM": "⚪ LOCAL-ONLY",
        "LOCAL_NO_GIT": "⚪ NO-GIT",
        "DIR_MISSING": "❌ MISSING",
        "ERROR": "⚠️ ERROR"
    }

    print(f"{'Subsystem':<26} | {'Branch':<12} | {'Status':<14} | {'Behind':<6} | {'Ahead':<5} | {'Worktree'}")
    print("-" * 84)

    behind_count = 0
    uptodate_count = 0

    for r in results:
        key = r.get("key", "")[:24]
        branch = r.get("branch", "-")[:12]
        st = status_icons.get(r.get("status"), r.get("status", "UNKNOWN"))
        behind = str(r.get("behind", 0))
        ahead = str(r.get("ahead", 0))
        dirty = "⚠️ DIRTY" if r.get("dirty") else "CLEAN"

        if r.get("status") == "BEHIND":
            behind_count += 1
        elif r.get("status") == "UP_TO_DATE":
            uptodate_count += 1

        print(f"{key:<26} | {branch:<12} | {st:<14} | {behind:<6} | {ahead:<5} | {dirty}")

    print("-" * 84)
    print(f" Summary: {uptodate_count} Up-to-Date | {behind_count} Outdated (Behind Upstream) | {len(results)} Total Subsystems")
    print("=======================================================\n")

    if do_sync and behind_count > 0:
        print(" [*] Initiating Automated Safe Fast-Forward Sync for Outdated Subsystems...\n")
        for r in results:
            if r.get("status") == "BEHIND" and not r.get("dirty"):
                sub_key = r["key"]
                print(f" -> Syncing {sub_key}...")
                sync_res = sync_subsystem(sub_key, subsystems.get(sub_key, {}))
                print(f"    [{sync_res['action'].upper()}] {sync_res['message']}")
        print("\n=======================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Audit subsystem drift against upstream git remotes")
    parser.add_argument("--fetch", "-f", action="store_true", default=True, help="Fetch remotes before checking")
    parser.add_argument("--no-fetch", action="store_false", dest="fetch", help="Skip remote fetch")
    parser.add_argument("--sync", "-s", action="store_true", help="Automatically pull fast-forward updates for behind repos")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    run_drift_audit(do_fetch=args.fetch, do_sync=args.sync, as_json=args.json)


if __name__ == "__main__":
    main()
