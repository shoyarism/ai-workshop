#!/usr/bin/env python3
"""
Workshop path resolution.

Every script and generated config must derive locations from here instead of
hardcoding drive letters or user names, so the Workshop works from E:, G:, a
clone on another machine, or a different Windows account.

Resolution order for the Workshop root:
    1. WORKSHOP_ROOT environment variable (if it contains the marker file)
    2. Walk up from this file until WORKSHOP_PROTOCOL.md is found
    3. Known fallbacks: E:/AI/Workshop, E:/Workshop, D:/Workshop
"""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path

MARKER = "WORKSHOP_PROTOCOL.md"
FALLBACK_ROOTS = (
    Path("."),
    Path(".."),
)


def _is_root(p: Path) -> bool:
    return (p / MARKER).is_file()


@lru_cache(maxsize=1)
def workshop_root() -> Path:
    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        if _is_root(parent):
            return parent
    env = os.environ.get("WORKSHOP_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if _is_root(p):
            return p
    for p in FALLBACK_ROOTS:
        if _is_root(p):
            return p
    raise RuntimeError(
        f"Workshop root not found. Set WORKSHOP_ROOT to the directory containing {MARKER}."
    )


def home() -> Path:
    return Path.home()


def uv_executable() -> str:
    """Absolute uv path when known, so MCP clients with a minimal PATH can still launch servers."""
    candidates = [
        home() / ".local" / "bin" / ("uv.exe" if sys.platform == "win32" else "uv")
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    return "uv"


def posix(p: Path | str) -> str:
    """Forward-slash path string; accepted by every harness config format on Windows."""
    return str(p).replace("\\", "/")


def python_executable() -> Path:
    """Workshop venv interpreter; falls back to the running interpreter."""
    venv = workshop_root() / ".venv"
    exe = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    return exe if exe.is_file() else Path(sys.executable)


ROOT = workshop_root()
SCRIPTS = ROOT / "scripts"
SKILLS = ROOT / "skills"
VAULT = ROOT / "vault"
STATE = ROOT / ".workshop_state"
BACKUPS = STATE / "backups"


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for k, v in {
        "workshop_root": ROOT,
        "uv": uv_executable(),
    }.items():
        print(f"{k:15} {v}")
