#!/usr/bin/env python3
"""
Local CI Pipeline Runner
Executes the full automated CI test suite locally.
"""

import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("Unit Test Suite", [sys.executable, "-m", "unittest", "discover", "tests"]),
    ("Ruff Linter Check", ["uvx", "ruff", "check", "--select", "F", "scripts"]),
    ("Slop Court Trial (scripts)", [sys.executable, "scripts/workshop_court.py", "trial", "scripts"]),
    ("Secrets & Privacy Gate", [sys.executable, "scripts/scan_secrets.py"]),
    ("Workshop Doctor Diagnostics (--strict)", [sys.executable, "scripts/workshop.py", "doctor", "--strict"]),
    ("Agent Instruction Drift Gate", [sys.executable, "scripts/workshop_sync.py", "--check"]),
]

def main():
    print("=" * 65)
    print(" 🚀 WORKSHOP OS LOCAL CI PIPELINE")
    print(f" Workspace Root: {ROOT}")
    print("=" * 65)
    
    passed = 0
    for name, cmd in STEPS:
        print(f"\n[*] Running: {name}...")
        res = subprocess.run(cmd, cwd=str(ROOT))
        if res.returncode != 0:
            print(f"\n❌ FAILED: {name} (exit code {res.returncode})")
            sys.exit(res.returncode)
        print(f"✓ PASSED: {name}")
        passed += 1

    print("\n" + "=" * 65)
    print(f" 🎉 ALL {passed}/{len(STEPS)} CI SUITE GATES PASSED CLEANLY!")
    print("=" * 65)
    sys.exit(0)

if __name__ == "__main__":
    main()
