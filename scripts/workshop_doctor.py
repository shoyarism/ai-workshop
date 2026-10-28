#!/usr/bin/env python3
"""
Workshop Diagnostic and Doctor Tool
===================================
Verifies health, dependencies, browser engines, media/vision tools, MCP servers, and subsystems in the Workshop.

Usage:
    python scripts/workshop_doctor.py [--strict] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import List, Tuple

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent


def check_mark(status: bool) -> str:
    return "[OK]" if status else "[MISSING]"


def check_python_environment(critical_failures: List[str]):
    print("--- 1. Python Environment ---")
    py_ver = sys.version.split()[0]
    major, minor = sys.version_info[:2]
    py_ok = (major == 3 and minor >= 11)
    if not py_ok:
        critical_failures.append(f"Python >= 3.11 required, found {py_ver}")
    print(f"  {check_mark(py_ok)} Python Version: {py_ver} ({sys.executable})")

    # Core required dependencies for Workshop OS CLI, Court, and Scanners
    core_packages = [
        ("yaml", "pyyaml"),
        ("pydantic", "pydantic"),
        ("requests", "requests"),
    ]

    print("\n  [Core Dependencies - Required]")
    for mod_name, pkg_name in core_packages:
        try:
            __import__(mod_name)
            print(f"  {check_mark(True)} Python package '{pkg_name}' is installed.")
        except ImportError:
            critical_failures.append(f"Missing core package: {pkg_name}")
            print(f"  {check_mark(False)} Python package '{pkg_name}' is NOT installed. (Run: uv pip install {pkg_name})")

    # Optional extension packages for specific agent capabilities
    optional_packages = [
        ("fastmcp", "fastmcp", "FastMCP server protocol"),
        ("fastapi", "fastapi", "Local HTTP gateway / services"),
        ("uvicorn", "uvicorn", "ASGI server for local gateways"),
        ("websockets", "websockets", "WebSocket stream transport"),
        ("PIL", "pillow", "Visual asset inspection"),
        ("playwright", "playwright", "Headless browser automation"),
        ("gradio_client", "gradio-client", "FLUX & Image model inference"),
        ("pydantic_ai", "pydantic-ai", "PydanticAI agent runner"),
        ("smolagents", "smolagents", "HuggingFace smolagents"),
        ("agno", "agno", "Agno multi-agent runner"),
        ("mem0", "mem0ai", "Mem0 long-term memory"),
        ("crawl4ai", "crawl4ai", "Autonomous crawler"),
    ]

    print("\n  [Feature Extensions - Optional / Standby]")
    for mod_name, pkg_name, feat_desc in optional_packages:
        try:
            __import__(mod_name)
            print(f"  [OK] Optional '{pkg_name}' ({feat_desc}): Ready")
        except ImportError:
            print(f"  [STANDBY] Optional '{pkg_name}' ({feat_desc}): Not installed")


def check_node_and_system_binaries(critical_failures: List[str]):
    print("\n--- 2. Node.js, Media and System Binaries ---")
    if sys.platform == "win32":
        try:
            import winreg
            env_paths = []
            for root, subkey in [
                (winreg.HKEY_CURRENT_USER, r"Environment"),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
            ]:
                try:
                    with winreg.OpenKey(root, subkey) as k:
                        val, _ = winreg.QueryValueEx(k, "Path")
                        env_paths.extend(val.split(";"))
                except (AttributeError, ValueError, OSError):
                    pass
            for p in os.environ.get("PATH", "").split(";"):
                if p and p not in env_paths:
                    env_paths.append(p)
            os.environ["PATH"] = ";".join([p for p in env_paths if p])
        except (AttributeError, ValueError, OSError):
            pass

    # Git is strictly required
    git_path = shutil.which("git")
    if git_path:
        print(f"  {check_mark(True)} {'git':<8} found: {git_path}")
    else:
        critical_failures.append("Missing required binary: git")
        print(f"  {check_mark(False)} {'git':<8} not found in PATH.")

    optional_tools = ["uv", "node", "npm", "npx", "pnpm", "bun", "ffmpeg", "ffprobe"]
    for t in optional_tools:
        path = shutil.which(t)
        if path:
            print(f"  [OK] {t:<8} found: {path}")
        else:
            print(f"  [STANDBY] {t:<8} not found in PATH (optional feature).")


def check_browser_engines():
    print("\n--- 3. Browser Automation and Engines ---")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print(f"  {check_mark(True)} Playwright Chromium: Available and functional")
            except Exception as e:
                print(f"  [STANDBY] Playwright Chromium: Installed but not initialized ({e})")
    except ImportError:
        print("  [STANDBY] Playwright: Not installed (optional feature).")


def check_local_gateways():
    print("\n--- 4. Local Gateway Connectivity ---")
    gateways = [
        ("Camofox Browser Hub", "http://127.0.0.1:9377/health"),
        ("Live Browser Hub", "http://127.0.0.1:7860/health")
    ]
    for name, url in gateways:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WorkshopDoctor/1.0"})
            with urllib.request.urlopen(req, timeout=1.0):
                print(f"  {check_mark(True)} {name:<22} is ONLINE ({url})")
        except Exception:
            print(f"  [STANDBY] {name:<22} is OFFLINE / Standby ({url})")


CORE_SUBSYSTEMS = {"skills", "scripts", "prompts"}


def check_subsystems_health(critical_failures: List[str], require_all: bool = False):
    print("\n--- 5. Workshop Subsystems Matrix ---")
    catalog_path = WORKSHOP_DIR / "CATALOG.json"
    if not catalog_path.exists():
        from workshop_indexer import main as index_main
        index_main()

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    subsystems = data.get("subsystems", {})
    ready_core = 0
    total_core = len(CORE_SUBSYSTEMS)
    ready_ext = 0
    total_ext = 0

    for key, info in subsystems.items():
        p = WORKSHOP_DIR / info.get("path", key)
        is_ready = p.exists() and (len(list(p.iterdir())) > 1 if p.is_dir() else True)
        name = info.get("name", key)
        if len(name) > 35:
            name = name[:32] + "..."

        is_core = key in CORE_SUBSYSTEMS
        if is_core:
            if is_ready:
                ready_core += 1
                status_label = "[ACTIVE]"
            else:
                status_label = "[MISSING]"
                critical_failures.append(f"Core repository subsystem '{key}' is missing or empty on disk")
        else:
            total_ext += 1
            if is_ready:
                ready_ext += 1
                status_label = "[ACTIVE]"
            else:
                status_label = "[STANDBY]"
                if require_all:
                    critical_failures.append(f"Subsystem '{key}' is on standby")
        print(f"  {status_label:<9} {name:<36} -> {info.get('path')}")

    print(f"\n  Core Repository Subsystems : {ready_core}/{total_core} Active (Required)")
    print(f"  Ecosystem Companions       : {ready_ext}/{total_ext} Active (Standby on-demand)")



def check_skills_integrity(critical_failures: List[str]):
    print("\n--- 6. Skills Registry and Frontmatter Integrity ---")
    import workshop_skills
    skills = workshop_skills.discover()
    total_unique = len(skills)

    if total_unique == 0:
        critical_failures.append("No skills discovered in skills directory")

    print(f"  {check_mark(total_unique > 0)} Skills Registry: {total_unique} discovered on disk")

    # Frontmatter & BOM checks across skills
    bom_files: List[str] = []
    for s in skills:
        if s.path.exists():
            try:
                with open(s.path, "rb") as bf:
                    raw_header = bf.read(4)
                    if raw_header.startswith(b"\xef\xbb\xbf"):
                        bom_files.append(str(s.path.relative_to(WORKSHOP_DIR)))
            except OSError:
                pass

    if bom_files:
        print(f"  [WARN] Found {len(bom_files)} skills with UTF-8 BOM headers (will be normalized)")
        for bf in bom_files[:3]:
            print(f"     • {bf}")
    else:
        print(f"  {check_mark(True)} UTF-8 Encoding: Zero BOM headers detected across skills")


def check_obsidian_vault(critical_failures: List[str]):
    print("\n--- 7. Obsidian Second Brain Vault ---")
    vault_dir = WORKSHOP_DIR / "vault"
    if not vault_dir.exists():
        critical_failures.append("Missing vault directory")
        print(f"  {check_mark(False)} Vault directory not found: {vault_dir}")
        return

    notes = [p for p in vault_dir.rglob("*.md") if not any(part.startswith(".") for part in p.parts)]
    home_note = vault_dir / "Home.md"
    if not home_note.exists():
        critical_failures.append("Missing vault/Home.md")

    print(f"  {check_mark(home_note.exists())} Master Vault Hub: {'Operational' if home_note.exists() else 'Missing Home.md'}")
    print(f"  {check_mark(len(notes) > 0)} Total Knowledge Notes: {len(notes)} notes on disk")

    # Wiki-Link Integrity Linter
    notes_map = {p.stem.lower(): p for p in notes}
    broken_links: List[Tuple[str, str]] = []
    total_links = 0

    for p in notes:
        content = p.read_text(encoding="utf-8", errors="ignore")
        for link in re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", content):
            total_links += 1
            t_clean = link.strip()
            t_path = vault_dir / t_clean
            t_stem = Path(t_clean).stem.lower()
            resolved = (
                t_clean.lower() in notes_map
                or t_stem in notes_map
                or t_path.exists()
                or (vault_dir / (t_clean + ".md")).exists()
            )
            if not resolved:
                broken_links.append((p.name, t_clean))

    links_status = (len(broken_links) == 0)
    if not links_status:
        critical_failures.append(f"Found {len(broken_links)} broken wiki-links in vault")

    print(f"  {check_mark(links_status)} Wiki-Link Integrity: {total_links} verified links | {len(broken_links)} broken")
    if broken_links:
        for src, target in broken_links[:5]:
            print(f"     • Broken in {src}: [[{target}]]")


def main(strict: bool = False):
    parser = argparse.ArgumentParser(description="Workshop OS Health & Doctor")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 on any critical failure")
    parser.add_argument("--require-all-subsystems", action="store_true", help="Fail strict mode if any ecosystem subsystem is on standby")
    args, _ = parser.parse_known_args()

    is_strict = strict or args.strict
    require_all = args.require_all_subsystems

    print("\n=======================================================")
    print(" [*] WORKSHOP HEALTH & DIAGNOSTIC DOCTOR")
    print(f" Workspace Root: {WORKSHOP_DIR}")
    print(f" Mode          : {'STRICT (Zero Tolerance)' if is_strict else 'STANDARD (Diagnostic)'}")
    print("=======================================================\n")

    critical_failures: List[str] = []

    check_python_environment(critical_failures)
    check_node_and_system_binaries(critical_failures)
    check_browser_engines()
    check_local_gateways()
    check_subsystems_health(critical_failures, require_all=require_all)
    check_skills_integrity(critical_failures)
    check_obsidian_vault(critical_failures)

    print("\n=======================================================")
    if critical_failures:
        print(f" [FAIL] Doctor found {len(critical_failures)} critical issue(s):")
        for cf in critical_failures:
            print(f"   ✗ {cf}")
        print("=======================================================\n")
        if is_strict:
            sys.exit(1)
        sys.exit(0)
    else:
        print(" [PASS] All core subsystems and invariants verified clean.")
        print("=======================================================\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
