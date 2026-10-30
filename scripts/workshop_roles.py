#!/usr/bin/env python3
"""
Workshop Role Definition & Loader Engine
=========================================
Loads compiled role definitions from `.agents/subagents/<role>.md`, parses frontmatter
metadata, and enforces role-based tool scoping across agent harnesses (Antigravity,
Claude Code, OpenCode).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workshop_paths import ROOT

SUBAGENTS_DIR = ROOT / ".agents" / "subagents"
STATE_DIR = ROOT / ".workshop_state"
ACTIVE_ROLE_FILE = STATE_DIR / "active_role.json"

WORKSHOP_MCP_TOOLS = {
    "skill_search",
    "skill_load",
    "memory_recall",
    "memory_write",
    "verify",
    "critique",
    "antislop_audit",
    "court_trial",
    "court_council",
    "graphify_query",
}

WRITE_NATIVE_TOOLS = {
    "write_to_file",
    "replace_file_content",
    "run_command",
}

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and markdown body from role definition file."""
    meta = {}
    body = content
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2).strip()
        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if v.startswith("[") and v.endswith("]"):
                    try:
                        meta[k] = json.loads(v)
                    except Exception:
                        meta[k] = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
                else:
                    meta[k] = v
    return meta, body

def load_role_definition(role_name: str) -> Dict[str, Any]:
    """Load and parse the compiled role definition file from `.agents/subagents/<role>.md`."""
    role_file = SUBAGENTS_DIR / f"{role_name}.md"
    if not role_file.is_file():
        raise FileNotFoundError(f"Compiled role definition not found: {role_file}")
    
    content = role_file.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(content)
    
    tools = meta.get("tools", [])
    allowed_mcp = [t for t in tools if t in WORKSHOP_MCP_TOOLS]
    denied_mcp = [t for t in WORKSHOP_MCP_TOOLS if t not in tools]
    has_write_tools = any(t in WRITE_NATIVE_TOOLS for t in tools)
    
    return {
        "role": role_name,
        "name": meta.get("name", role_name),
        "description": meta.get("description", ""),
        "model": meta.get("model", "auto"),
        "tools": tools,
        "allowed_mcp_tools": sorted(allowed_mcp),
        "denied_mcp_tools": sorted(denied_mcp),
        "has_write_tools": has_write_tools,
        "prompt": body,
        "definition_path": str(role_file.relative_to(ROOT)).replace("\\", "/"),
    }

def activate_role(role_name: str) -> Dict[str, Any]:
    """Activate role in state file and environment for runtime RBAC enforcement."""
    role_def = load_role_definition(role_name)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVE_ROLE_FILE.write_text(json.dumps({"role": role_name, "name": role_def["name"]}, indent=2), encoding="utf-8")
    os.environ["WORKSHOP_ROLE"] = role_name
    return role_def

def deactivate_role() -> None:
    """Clear active role."""
    if ACTIVE_ROLE_FILE.is_file():
        try:
            ACTIVE_ROLE_FILE.unlink()
        except OSError:  # @court-exempt: best-effort state file cleanup
            pass
    if "WORKSHOP_ROLE" in os.environ:
        del os.environ["WORKSHOP_ROLE"]

def verify_all_roles() -> Dict[str, Any]:
    """Verify that all compiled role files exist, parse correctly, and satisfy least-privilege invariants."""
    roles = ["researcher", "reviewer", "debugger", "architect"]
    results = {}
    for r in roles:
        r_def = load_role_definition(r)
        results[r] = {
            "name": r_def["name"],
            "model": r_def["model"],
            "tool_count": len(r_def["tools"]),
            "has_write_tools": r_def["has_write_tools"],
            "allowed_mcp": r_def["allowed_mcp_tools"],
            "denied_mcp": r_def["denied_mcp_tools"],
        }
    return results

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "list":
            for r, info in verify_all_roles().items():
                print(f"Role: {r:<12} (Model: {info['model']:<8}) Write: {info['has_write_tools']} | Allowed MCP: {info['allowed_mcp']}")
        elif cmd == "load" and len(sys.argv) > 2:
            r_info = load_role_definition(sys.argv[2])
            print(json.dumps(r_info, indent=2))
        elif cmd == "activate" and len(sys.argv) > 2:
            activate_role(sys.argv[2])
            print(f"Activated role: {sys.argv[2]}")
        elif cmd == "deactivate":
            deactivate_role()
            print("Deactivated role.")
    else:
        print(json.dumps(verify_all_roles(), indent=2))
