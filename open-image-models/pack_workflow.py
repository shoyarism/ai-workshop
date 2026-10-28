#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comfy-Pack Automation Helper:
Package ComfyUI workflows into .cpack.zip and serve them as scalable APIs (BentoML integration).
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
COMFY_DIR = ROOT_DIR / "ComfyUI"


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pack_workflow.py pack <path_to_workflow.json> [output_file.cpack.zip]")
        print("  python pack_workflow.py serve <path_to_workflow.cpack.zip>")
        print("  python pack_workflow.py --help")
        sys.exit(0)

    cmd = sys.argv[1]
    
    if cmd == "pack":
        workflow_path = sys.argv[2]
        out = sys.argv[3] if len(sys.argv) > 3 else "workflow.cpack.zip"
        print(f"[comfy-pack] Packaging workflow {workflow_path} into {out}...")
        subprocess.run(["comfy-pack", "pack", workflow_path, "--output", out], check=True)
    elif cmd == "serve":
        package_path = sys.argv[2]
        print(f"[comfy-pack] Serving packaged workflow {package_path} as BentoML API...")
        subprocess.run(["comfy-pack", "serve", package_path], check=True)
    else:
        subprocess.run(["comfy-pack"] + sys.argv[1:], check=True)


if __name__ == "__main__":
    main()
