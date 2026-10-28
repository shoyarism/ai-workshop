#!/usr/bin/env python3
"""
Workshop Backup Synchronization Module
======================================
Coordinates ecosystem backups between Workshop and Backup repository.
Dispatches to backup.ps1 or modular synchronization routines.
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
BACKUP_DIR = WORKSHOP_DIR.parent / "Backup"

def get_backup_script():
    """Locate backup.ps1 in the Backup workspace."""
    candidate = BACKUP_DIR / "backup.ps1"
    if candidate.exists():
        return candidate
    # Fallback to current drive alternative
    for drive in ["E:", "G:"]:
        alt = Path(f"{drive}/Backup/backup.ps1")
        if alt.exists():
            return alt
    return None

def run_backup(args=None):
    """Execute ecosystem backup via PowerShell backup.ps1."""
    ps_script = get_backup_script()
    if not ps_script:
        print(f"[!] Error: backup.ps1 not found in Backup workspace ({BACKUP_DIR})")
        return 1

    print("\n=======================================================")
    print(" 🛡️ WORKSHOP ECOSYSTEM BACKUP SYNCHRONIZATION")
    print(f" Target Backup Base: {ps_script.parent}")
    print("=======================================================\n")

    cmd = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", str(ps_script)
    ]
    if args:
        cmd.extend(args)

    result = subprocess.run(cmd)
    return result.returncode

def main():
    sub_args = sys.argv[1:] if len(sys.argv) > 1 else []
    sys.exit(run_backup(sub_args))

if __name__ == "__main__":
    main()
