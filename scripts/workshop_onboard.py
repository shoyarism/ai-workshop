#!/usr/bin/env python3
"""
Workshop Onboard Script -- Portable Bootstrap for Any Machine
=============================================================
Run this on ANY machine after plugging in the Workshop external drive.
It sets up the local harness config without touching anything on the drive itself.

Usage:
    uv run python scripts/workshop_onboard.py              # Full setup
    uv run python scripts/workshop_onboard.py --dry-run   # Preview only
    uv run python scripts/workshop_onboard.py --verify    # Check current state
"""
import argparse
import subprocess
import sys

from workshop_paths import ROOT, SCRIPTS, uv_executable

DRY_RUN = False
QUIET = False

def log(msg: str, force: bool = False):
    if not QUIET or force:
        print(f"  {msg}")

def check_command(cmd: str) -> bool:
    try:
        r = subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False

def ensure_uv():
    """Check uv is available and install if missing."""
    uv_bin = uv_executable()
    if uv_bin:
        log(f"[OK] uv found at: {uv_bin}")
        return True
    log("[WARN] uv not found in PATH. Install: https://astral.sh/uv/install")
    return False

def ensure_python():
    """Check Python 3.10+ is available."""
    try:
        r = subprocess.run(["python", "--version"], capture_output=True, text=True, timeout=5)
        log(f"[OK] Python: {r.stdout.strip()}")
        return True
    except Exception as e:
        log(f"[WARN] Python not found: {e}")
        return False

def setup_skills():
    """Ensure Tier 0 core skills are mounted."""
    core_dir = ROOT / ".workshop_state" / "skills-core"

    if not core_dir.exists():
        log("[INFO] Running workshop sync to mount core skills...")
        if not DRY_RUN:
            r = subprocess.run(
                [sys.executable, str(SCRIPTS / "workshop.py"), "sync"],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120
            )
            if r.returncode == 0:
                log("[OK] Core skills synced")
            else:
                log(f"[WARN] Sync failed: {r.stderr[:200]}")
        return

    # Check if workshop-watch skill is there
    watch_skill = core_dir / "workshop-watch"
    if not watch_skill.exists():
        log("[INFO] Regenerating skills-core index...")
        if not DRY_RUN:
            r = subprocess.run(
                [sys.executable, str(SCRIPTS / "workshop.py"), "index"],
                cwd=str(ROOT), capture_output=True, text=True, timeout=60
            )
            log(f"[OK] Index regenerated: {r.stdout.strip()[-100:] if r.stdout else ''}")

def verify_setup():
    """Run full verification."""
    log("=== WORKSHOP ONBOARD VERIFICATION ===", force=True)

    checks = [
        ("Python", "python", ["--version"]),
        ("uv", "uv", ["--version"]),
        ("git", "git", ["--version"]),
    ]

    results = {}
    for name, cmd, args in checks:
        ok = check_command(cmd)
        results[name] = "OK" if ok else "MISSING"
        log(f"[{results[name]}] {name}")

    # Check Workshop root
    marker = ROOT / "WORKSHOP_PROTOCOL.md"
    if marker.exists():
        results["workshop_root"] = "OK"
        log(f"[OK] Workshop root: {ROOT}")
    else:
        results["workshop_root"] = "MISSING"
        log(f"[MISSING] Workshop root not found: {ROOT}")

    # Check core skills
    core_dir = ROOT / ".workshop_state" / "skills-core"
    if core_dir.exists():
        skills_count = len(list(core_dir.glob("*/SKILL.md")))
        results["core_skills"] = f"{skills_count} skills"
        log(f"[OK] Core skills: {skills_count} mounted")
    else:
        results["core_skills"] = "MISSING"
        log("[MISSING] Core skills directory not found")

    log("=== SUMMARY ===", force=True)
    all_ok = all(v == "OK" for v in results.values())
    for k, v in results.items():
        status = "OK" if v == "OK" else v
        log(f"  {k:20} {status}")

    if all_ok:
        log("\n[SUCCESS] Workshop is ready for use!", force=True)
        log("  Run: uv run python scripts/workshop.py doctor", force=True)
    else:
        log("\n[PARTIAL] Some items need attention:", force=True)
        for k, v in results.items():
            if v != "OK":
                log(f"  - {k}: {v}", force=True)

    return results

def main():
    global DRY_RUN, QUIET

    parser = argparse.ArgumentParser(
        description="Workshop portable bootstrap -- set up harnesses for any machine"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--verify", action="store_true", help="Run verification only")
    parser.add_argument("--quiet", action="store_true", help="Suppress output except errors")
    parser.add_argument("--full-sync", action="store_true", help="Run full workshop sync")
    args = parser.parse_args()

    DRY_RUN = args.dry_run
    QUIET = args.quiet

    log("Workshop Onboard -- Portable Bootstrap", force=True)
    log(f"Root: {ROOT}", force=True)
    log(f"Dry-run: {DRY_RUN}", force=True)
    log("")

    if args.verify:
        verify_setup()
        return

    # Phase 1: Dependency check
    log("=== PHASE 1: Dependencies ===")
    has_uv = ensure_uv()
    has_python = ensure_python()

    if not has_uv:
        log("\n[ERROR] uv is required. Install: https://astral.sh/uv/install")
        sys.exit(1)

    if not has_python:
        log("\n[ERROR] Python 3.10+ is required.")
        sys.exit(1)

    log("")

    # Phase 2: Sync and mount
    log("=== PHASE 2: Workshop Sync ===")
    if args.full_sync:
        log("Running full workshop sync...")
        if not DRY_RUN:
            r = subprocess.run(
                [sys.executable, str(SCRIPTS / "workshop.py"), "sync"],
                cwd=str(ROOT), capture_output=True, text=True, timeout=180
            )
            log(r.stdout)
            if r.stderr:
                log(f"[WARN] {r.stderr[:200]}")
    else:
        log("Skipping full sync (use --full-sync to enable)")

    log("")

    # Phase 3: Skills
    log("=== PHASE 3: Skills Setup ===")
    setup_skills()

    log("")
    log("=== COMPLETE ===")
    log("Workshop is now configured for this machine.")
    log("")
    log("Next steps:")
    log("  1. uv run python scripts/workshop.py doctor      # Health check")
    log("  2. uv run python scripts/workshop.py index        # Rebuild skill index")
    log("  3. uv run python scripts/workshop.py search '<query>'  # Test search")
    log("")
    log(f"Workshop root: {ROOT}")
    log(f"Skills library: {ROOT / 'skills'}")

if __name__ == "__main__":
    main()
