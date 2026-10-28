#!/usr/bin/env python3
"""
Workshop Harness & Agent Capability Evaluation Suite
===================================================
Runs deterministic benchmarks to verify harness integration, MCP tools,
safety guards, and reasoning support across Antigravity and OpenCode.

Usage:
    uv run python scripts/workshop_eval.py [--json]
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict

# UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workshop_paths import (
    ROOT,
    SCRIPTS,
    python_executable,
)
import workshop_mcp
import workshop_skills

def run_eval_paths() -> Dict[str, Any]:
    """Test 1: Path portability and resolver."""
    t0 = time.perf_counter()
    passed = ROOT.is_dir() and (ROOT / "WORKSHOP_PROTOCOL.md").is_file() and python_executable().is_file()
    dur = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "id": "EVAL-01-PATHS",
        "name": "Path Resolution & Environment Portability",
        "passed": passed,
        "latency_ms": dur,
        "details": f"Root: {ROOT}, Python: {python_executable()}"
    }

def run_eval_skills_tier0() -> Dict[str, Any]:
    """Test 2: Tier 0 Core Skills footprint and integrity."""
    t0 = time.perf_counter()
    core_dir = ROOT / ".workshop_state" / "skills-core"
    skills = []
    if core_dir.is_dir():
        for d in core_dir.iterdir():
            if d.is_dir() and (d / "SKILL.md").is_file():
                s = workshop_skills.load_skill(d / "SKILL.md", core_dir)
                skills.append(s)
    
    tokens = workshop_skills.metadata_tokens(skills)
    passed = len(skills) >= 25 and tokens < 5000
    dur = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "id": "EVAL-02-SKILLS-TIER0",
        "name": "Tier 0 Core Skills Footprint & Frontmatter",
        "passed": passed,
        "latency_ms": dur,
        "details": f"{len(skills)} core skills mounted (~{tokens:,} tokens budget)"
    }

def run_eval_mcp_tools() -> Dict[str, Any]:
    """Test 3: Master MCP Tool Server functionality."""
    t0 = time.perf_counter()
    
    # 1. Search
    search_out = workshop_mcp.skill_search("react", limit=2)
    search_ok = "Found" in search_out and "react" in search_out.lower()
    
    # 2. Load
    load_out = workshop_mcp.skill_load("antislop")
    load_ok = "Domain Skill: antislop" in load_out
    
    # 3. Memory recall
    recall_out = workshop_mcp.memory_recall("registry", limit=1)
    recall_ok = "Retrieved" in recall_out or "Local Service" in recall_out
    
    passed = search_ok and load_ok and recall_ok
    dur = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "id": "EVAL-03-MCP-TOOLS",
        "name": "Workshop Master MCP Tools (Search/Load/Memory)",
        "passed": passed,
        "latency_ms": dur,
        "details": f"Search: {'OK' if search_ok else 'FAIL'}, Load: {'OK' if load_ok else 'FAIL'}, Memory: {'OK' if recall_ok else 'FAIL'}"
    }

def run_eval_safety_hooks() -> Dict[str, Any]:
    """Test 4: Pre-tool safety hook blocking destructive actions."""
    t0 = time.perf_counter()
    py = str(python_executable())
    hook_script = str(SCRIPTS / "workshop_hooks.py")
    
    # Destructive command should be blocked (return code 1)
    proc_blocked = subprocess.run([py, hook_script, "pre-tool", "rm", "-rf", "/"], capture_output=True, stdin=subprocess.DEVNULL)
    blocked_ok = proc_blocked.returncode == 1
    
    # Benign command should pass (return code 0)
    proc_allowed = subprocess.run([py, hook_script, "pre-tool", "python", "--version"], capture_output=True, stdin=subprocess.DEVNULL)
    allowed_ok = proc_allowed.returncode == 0
    
    passed = blocked_ok and allowed_ok
    dur = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "id": "EVAL-04-SAFETY-HOOKS",
        "name": "Safety Guard & Pre-Tool Execution Hook",
        "passed": passed,
        "latency_ms": dur,
        "details": f"Blocked destructive: {'PASS' if blocked_ok else 'FAIL'}, Allowed safe: {'PASS' if allowed_ok else 'FAIL'}"
    }

def run_eval_harness_configs() -> Dict[str, Any]:
    """Test 5: Live configuration integrity across harnesses."""
    t0 = time.perf_counter()
    
    # Antigravity config
    g_cfg = Path.home() / ".gemini" / "config" / "mcp_config.json"
    g_ok = False
    if g_cfg.is_file():
        g_text = g_cfg.read_text(encoding="utf-8")
        g_ok = '"workshop":' in g_text
        
    # OpenCode / Kilo clean paths
    op_clean = True
    for f in ("opencode.json", "kilo.jsonc"):
        p = ROOT / f
        if p.is_file():
            txt = p.read_text(encoding="utf-8")
            stale_paths = ["E:/Personal", "E:\\Personal", "~", "C:\\Users\\USER", "C:/Users/Ideapad", "C:\\Users\\Ideapad"]
            if any(stale in txt for stale in stale_paths):
                op_clean = False
                
    passed = g_ok and op_clean
    dur = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "id": "EVAL-05-HARNESS-CONFIGS",
        "name": "Multi-Harness Live Configuration State",
        "passed": passed,
        "latency_ms": dur,
        "details": f"Antigravity: {'OK' if g_ok else 'FAIL'}, OpenCode: {'OK' if op_clean else 'FAIL'}"
    }

def main():
    evals = [
        run_eval_paths(),
        run_eval_skills_tier0(),
        run_eval_mcp_tools(),
        run_eval_safety_hooks(),
        run_eval_harness_configs(),
    ]
    
    if "--reasoning" in sys.argv:
        import workshop_reasoning_eval
        workshop_reasoning_eval.main()
        return

    all_passed = all(e["passed"] for e in evals)
    
    if "--json" in sys.argv and "--all" not in sys.argv:
        print(json.dumps({"success": all_passed, "evals": evals}, indent=2))
        sys.exit(0 if all_passed else 1)
        
    print("\n" + "=" * 70)
    print(" 🧪 WORKSHOP OS HARNESS INTEGRATION & PLUMBING VERIFICATION REPORT")
    print("=" * 70 + "\n")
    
    for e in evals:
        mark = "✅ PASS" if e["passed"] else "❌ FAIL"
        print(f"{mark} | {e['id']} | {e['name']} ({e['latency_ms']} ms)")
        print(f"       └─ {e['details']}\n")
        
    print("=" * 70)
    if all_passed:
        print("🎉 100% PLUMBING VERIFIED: All harness communication, tools, and paths are operational!")
    else:
        print("⚠️ SOME INTEGRATION CHECKS FAILED. Review details above.")
    print("=" * 70 + "\n")

    if "--all" in sys.argv:
        import workshop_reasoning_eval
        workshop_reasoning_eval.main()
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
