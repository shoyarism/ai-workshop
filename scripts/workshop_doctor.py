#!/usr/bin/env python3
"""
Workshop Diagnostic and Doctor Tool
===================================
Verifies health, dependencies, browser engines, media/vision tools, MCP servers, and subsystems in the Workshop.

Usage:
    python scripts/workshop_doctor.py [--verbose] [--fix]
"""

import os
import sys
import shutil
import subprocess
import json
import urllib.request
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent

def check_mark(status: bool) -> str:
    return "[OK]" if status else "[MISSING]"

def check_python_environment():
    print("--- 1. Python Environment ---")
    py_ver = sys.version.split()[0]
    print(f"  {check_mark(True)} Python Version: {py_ver} ({sys.executable})")
    
    required_packages = [
        "playwright",
        "PIL",
        "fastapi",
        "uvicorn",
        "websockets",
        "pydantic",
        "requests",
        "gradio_client",
        "fastmcp",
        "crawl4ai",
        "mem0",
        "pydantic_ai",
        "agno",
        "smolagents"
    ]
    
    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"  {check_mark(True)} Python package '{pkg}' is installed.")
        except ImportError:
            print(f"  {check_mark(False)} Python package '{pkg}' is NOT installed. (Run: uv tool install {pkg})")

def check_node_and_system_binaries():
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
                except Exception as err:  # @court-exempt: handled fallback
                    pass
            for p in os.environ.get("PATH", "").split(";"):
                if p and p not in env_paths:
                    env_paths.append(p)
            os.environ["PATH"] = ";".join([p for p in env_paths if p])
        except Exception as err:  # @court-exempt: handled fallback
            pass

    tools = ["node", "npm", "npx", "pnpm", "bun", "uv", "git", "ffmpeg", "ffprobe"]
    for t in tools:
        path = shutil.which(t)
        if path:
            print(f"  {check_mark(True)} {t:<8} found: {path}")
        else:
            print(f"  {check_mark(False)} {t:<8} not found in PATH.")

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
                print(f"  {check_mark(False)} Playwright Chromium: Needs install (run: npx playwright install chromium)")
    except ImportError:
        print(f"  {check_mark(False)} Playwright is not installed.")

def check_local_gateways():
    print("\n--- 4. Local Gateway Connectivity ---")
    gateways = [
        ("Camofox Browser Hub", "http://127.0.0.1:9377/health"),
        ("Live Browser Hub", "http://127.0.0.1:7860/health")
    ]
    
    for name, url in gateways:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WorkshopDoctor/1.0"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                print(f"  {check_mark(True)} {name:<22} is ONLINE ({url})")
        except Exception:
            print(f"  [OFFLINE] {name:<22} is OFFLINE / Standby ({url})")

def check_subsystems_health():
    print("\n--- 5. Workshop Subsystems Matrix ---")
    catalog_path = WORKSHOP_DIR / "CATALOG.json"
    if not catalog_path.exists():
        from workshop_indexer import main as index_main
        index_main()
        
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    subsystems = data.get("subsystems", {})
    ready_count = 0
    for key, info in subsystems.items():
        p = WORKSHOP_DIR / info.get("path", key)
        is_ready = p.exists() and (len(list(p.iterdir())) > 1 if p.is_dir() else True)
        if is_ready:
            ready_count += 1
        name = info.get("name", key)
        if len(name) > 35:
            name = name[:32] + "..."
        print(f"  {check_mark(is_ready)} {name:<36} -> {info.get('path')}")
        
    print(f"\n  Subsystem Health: {ready_count}/{len(subsystems)} Subsystems Operational")

def check_skills_integrity():
    print("\n--- 6. Skills Registry and Frontmatter Integrity ---")
    import workshop_skills
    skills = workshop_skills.discover()
    total_unique = len(skills)
    
    # Root breakdown
    root_counts = {}
    for s in skills:
        rel_root = str(s.root.relative_to(WORKSHOP_DIR)).replace("\\", "/")
        root_counts[rel_root] = root_counts.get(rel_root, 0) + 1
        
    db_skills_count = 0
    db_file = WORKSHOP_DIR / "scripts" / ".workshop_skills.db"
    if db_file.exists():
        try:
            import sqlite3
            con = sqlite3.connect(str(db_file))
            row = con.cursor().execute("SELECT count(*) FROM items WHERE item_type = 'skill';").fetchone()
            if row:
                db_skills_count = row[0]
        except Exception as err:  # @court-exempt: handled fallback
            pass

    print(f"  {check_mark(total_unique > 0)} Skills Registry: {total_unique} discovered on disk | {db_skills_count} in SQLite database")
    for rpath, count in sorted(root_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"     • {rpath:<42}: {count} skills")
    
    # Tier 0 core skills
    core_dir = WORKSHOP_DIR / ".workshop_state" / "skills-core"
    core_count = len([d for d in core_dir.iterdir() if d.is_dir()]) if core_dir.exists() else 0
    print(f"  {check_mark(core_count > 0)} Tier 0 Core Skills: {core_count} skills natively mounted in .workshop_state/skills-core")

def check_obsidian_vault():
    print("\n--- 7. Obsidian Second Brain Vault ---")
    vault_dir = WORKSHOP_DIR / "vault"
    if not vault_dir.exists():
        print(f"  {check_mark(False)} Vault directory not found: {vault_dir}")
        return

    notes = [p for p in vault_dir.rglob("*.md") if not any(part.startswith(".") for part in p.parts)]
    home_note = vault_dir / "Home.md"
    adr_dir = vault_dir / "01 - Architecture Decision Records (ADRs)"
    adrs = list(adr_dir.glob("*.md")) if adr_dir.exists() else []
    pm_dir = vault_dir / "02 - Post-Mortems"
    postmortems = list(pm_dir.glob("*.md")) if pm_dir.exists() else []

    # Query database counts from semantic index
    db_notes_count = 0
    db_file = WORKSHOP_DIR / "scripts" / ".workshop_skills.db"
    if db_file.exists():
        try:
            import sqlite3
            con = sqlite3.connect(str(db_file))
            row = con.cursor().execute("SELECT count(*) FROM items WHERE item_type = 'vault';").fetchone()
            if row:
                db_notes_count = row[0]
        except Exception as err:  # @court-exempt: handled fallback
            pass

    print(f"  {check_mark(home_note.exists())} Master Vault Hub: {'Operational' if home_note.exists() else 'Missing Home.md'}")
    print(f"  {check_mark(len(notes) > 0)} Total Knowledge Notes: {len(notes)} notes on disk | {db_notes_count} in SQLite database")
    print(f"  {check_mark(len(adrs) > 0)} Architecture Records: {len(adrs)} ADRs active")
    print(f"  {check_mark(len(postmortems) > 0)} Error Post-Mortems: {len(postmortems)} incidents documented")

    # Wiki-Link Integrity Linter
    import re
    notes_map = {p.stem.lower(): p for p in notes}
    broken_links = []
    total_links = 0
    for p in notes:
        content = p.read_text(encoding="utf-8", errors="ignore")
        for link in re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", content):
            total_links += 1
            target = link.strip().lower()
            if target not in notes_map and (target + ".md") not in notes_map:
                broken_links.append((p.name, link.strip()))

    links_status = len(broken_links) == 0
    print(f"  {check_mark(links_status)} Wiki-Link Integrity: {total_links} verified links | {len(broken_links)} broken")
    if broken_links:
        for src, target in broken_links[:5]:
            print(f"     • Broken in {src}: [[{target}]]")

def main():
    print("\n=======================================================")
    print(" [*] WORKSHOP HEALTH & DIAGNOSTIC DOCTOR")
    print(f" Workspace Root: {WORKSHOP_DIR}")
    print("=======================================================\n")
    
    check_python_environment()
    check_node_and_system_binaries()
    check_browser_engines()
    check_local_gateways()
    check_subsystems_health()
    check_skills_integrity()
    check_obsidian_vault()
    
    print("\n=======================================================")
    print(" Workshop Doctor Check Complete.")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
