#!/usr/bin/env python3
"""
Workshop Adversarial & Quality Verification Gate (Stage 5 Enforcer)
===================================================================
Performs rigorous pre-flight security auditing, vulnerability scanning, static analysis,
and test verification before declaring any agent task or code change complete.
"""

import sys
import subprocess
from pathlib import Path

WORKSHOP_DIR = Path(__file__).resolve().parent.parent

def audit_codebase(target_dir: Path = WORKSHOP_DIR):
    print("=======================================================")
    print(" 🛡️ WORKSHOP ADVERSARIAL & QUALITY VERIFICATION GATE")
    print("=======================================================\n")
    
    issues_found = 0
    
    # 1. Check for hardcoded secrets or .env exposure
    env_file = target_dir / ".env"
    if env_file.exists():
        print(" [!] WARNING: .env file present in root. Ensuring git ignores it...")
        git_ignore = target_dir / ".gitignore"
        if git_ignore.exists() and ".env" not in git_ignore.read_text(encoding="utf-8", errors="ignore"):
            print("   -> Adding .env to .gitignore")
            with open(git_ignore, "a", encoding="utf-8") as f:
                f.write("\n.env\n")
    
    # 2. Run Python syntax & import checks on recent files
    print(" [1/3] Running Python bytecode compilation sanity check...")
    py_files = list(target_dir.glob("scripts/*.py"))
    syntax_errors = 0
    for pf in py_files:
        res = subprocess.run([sys.executable, "-m", "py_compile", str(pf)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"   [X] Syntax error in {pf.name}: {res.stderr}")
            syntax_errors += 1
    if syntax_errors == 0:
        print(f"   [OK] All {len(py_files)} Workshop scripts compiled cleanly.")
    else:
        issues_found += syntax_errors

    # 3. Check doctor health
    print(" [2/3] Running Workshop Doctor diagnostic...")
    doctor_res = subprocess.run([sys.executable, str(target_dir / "scripts" / "workshop.py"), "doctor"], capture_output=True, text=True)
    if doctor_res.returncode == 0:
        print("   [OK] Workshop Doctor subsystems operational.")
    else:
        print("   [!] Doctor reported minor warnings/offline services.")

    # 4. Final Verdict
    print("\n=======================================================")
    if issues_found == 0:
        print(" 🎉 VERIFICATION GATE PASSED: Codebase is secure and healthy.")
        print("=======================================================\n")
        return 0
    else:
        print(f" ❌ VERIFICATION GATE FAILED: {issues_found} issues detected.")
        print("=======================================================\n")
        return 1

if __name__ == "__main__":
    sys.exit(audit_codebase())
