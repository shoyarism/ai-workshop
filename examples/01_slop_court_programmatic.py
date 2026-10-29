"""
Programmatic usage of Workshop OS Slop Court quality tribunal.
Run this script to inspect files against the 38 Penal Statutes.
"""

from pathlib import Path
import sys

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.workshop_court import Prosecutor, SlopCourtMagistrate, render_trial_report

def main() -> None:
    court = SlopCourtMagistrate()
    prosecutor = Prosecutor(root_dir=REPO_ROOT)

    # 1. Audit a single target file
    target = REPO_ROOT / "scripts" / "workshop.py"
    print(f"[*] Convening Slop Court on: {target.name}")

    indictment = prosecutor.indict(target)
    verdict = court.trial(indictment)

    # 2. Render official judicial report
    print(render_trial_report(verdict))

    print(f"Ruling     : {verdict.ruling}")
    print(f"Slop Index : {indictment.slop_index:.1f}%")
    print(f"Total Hits : {len(indictment.charges)}")

    if verdict.ruling in ("ACQUITTED", "ACQUITTED_HONORS"):
        print("[✓] Target acquitted with honors. Codebase meets zero-slop invariants.")
    else:
        print("[✗] Target convicted. Remediation required.")

if __name__ == "__main__":
    main()
