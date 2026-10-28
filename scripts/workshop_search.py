#!/usr/bin/env python3
"""
Workshop Arsenal Search Engine (Sub-Millisecond Direct Indexing)
================================================================
Scans 2,150+ skills across 7 Sovereign Houses, MCP servers, Public APIs, Free developer tiers, tools, and repositories in the Workshop.

Usage:
    python scripts/workshop_search.py "<query>" [--category <cat>] [--json] [--limit <n>]
    python scripts/workshop_search.py "browser"
    python scripts/workshop_search.py "ui ux" --limit 10
    python scripts/workshop_search.py "crypto" --category apis
    python scripts/workshop_search.py "pentest" --category repos
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent
CACHE_FILE = WORKSHOP_DIR / "scripts" / ".skills_cache.json"

SKILL_PATHS = [
    WORKSHOP_DIR / "skills",
    WORKSHOP_DIR / "open-design",
    WORKSHOP_DIR / "ai agents handbook",
    WORKSHOP_DIR / "agent-skills" / "skills",
    WORKSHOP_DIR / "claude-plugins-official",
    WORKSHOP_DIR / "claude-mem",
    WORKSHOP_DIR / "openclaw" / "skills",
    WORKSHOP_DIR / "open-seo",
    WORKSHOP_DIR / "strix" / "skills",
    WORKSHOP_DIR / "ponytail",
    WORKSHOP_DIR / "graphify" / "graphify",
    WORKSHOP_DIR / "hyperframes" / "skills",
    WORKSHOP_DIR / "browser-use" / "skills",
]

SKIP_DIRS = {".git", ".venv", ".venv_old", "node_modules", "__pycache__", ".workshop_state", ".ruff_cache", "dist", "build"}

def extract_skill_metadata(skill_md_path: Path):
    """Parse YAML frontmatter or title/description from SKILL.md."""
    try:
        content = skill_md_path.read_text(encoding="utf-8", errors="ignore")[:1500]
        name = skill_md_path.parent.name
        desc = ""
        
        # Check YAML frontmatter (--- ... ---)
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if frontmatter_match:
            fm_text = frontmatter_match.group(1)
            name_m = re.search(r"^name:\s*['\"]?(.*?)['\"]?\s*$", fm_text, re.MULTILINE)
            desc_m = re.search(r"^description:\s*['\"]?(.*?)['\"]?\s*$", fm_text, re.MULTILINE)
            if name_m:
                name = name_m.group(1).strip()
            if desc_m:
                desc = desc_m.group(1).strip()
        
        if not desc:
            lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]
            desc = lines[0] if lines else "No description available."
            
        return {
            "type": "skill",
            "name": name,
            "description": desc,
            "path": str(skill_md_path.relative_to(WORKSHOP_DIR)).replace("\\", "/"),
            "full_path": str(skill_md_path).replace("\\", "/")
        }
    except Exception:
        return None

def scan_all_skills(force_refresh: bool = False):
    """Fast recursive scan of all skills (including nested skill packs) with disk caching."""
    if not force_refresh and CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, OSError, json.JSONDecodeError):  # @court-exempt: json cache fallback
            pass

    skills = []
    seen = set()
    for base_dir in SKILL_PATHS:
        if not base_dir.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base_dir):
            dirnames[:] = sorted(
                d for d in dirnames
                if not d.startswith((".", "_")) and d not in SKIP_DIRS
            )
            if "SKILL.md" in filenames:
                skill_md = Path(dirpath) / "SKILL.md"
                if skill_md not in seen:
                    seen.add(skill_md)
                    meta = extract_skill_metadata(skill_md)
                    if meta:
                        skills.append(meta)

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(skills, f)
    except Exception:  # @court-exempt: handled fallback
        pass

    return skills

def scan_subsystems():
    """Scan subsystems and repositories registered in CATALOG.json."""
    catalog_path = WORKSHOP_DIR / "CATALOG.json"
    subsystems = []
    if catalog_path.exists():
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, item in data.get("subsystems", {}).items():
                subsystems.append({
                    "type": "subsystem",
                    "name": item.get("name", k),
                    "slug": k,
                    "category": item.get("category_label", item.get("category", "")),
                    "description": item.get("description", ""),
                    "capabilities": ", ".join(item.get("capabilities", [])),
                    "tags": " ".join(item.get("tags", [])),
                    "path": str(item.get("path", k)).replace("\\", "/"),
                    "status": item.get("status", "READY")
                })
        except Exception:  # @court-exempt: handled fallback
            pass
    return subsystems

def _parse_mcp_readme_desc(readme_path: Path, fallback: str) -> str:
    """Extract first non-heading paragraph from readme."""
    if not readme_path.exists():
        return fallback
    try:
        paras = [l.strip() for l in readme_path.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip() and not l.startswith("#")]
        return paras[0] if paras else fallback
    except Exception:  # @court-exempt: handled fallback
        return fallback

def scan_mcp_servers():
    """Scan configured and available MCP servers."""
    mcps = []
    official_dir = WORKSHOP_DIR / "mcp-servers-official" / "src"
    if official_dir.exists():
        try:
            for d in official_dir.iterdir():
                if not d.is_dir() or d.name.startswith("."):
                    continue
                desc = _parse_mcp_readme_desc(d / "README.md", f"Official MCP server for {d.name}")
                mcps.append({
                    "type": "mcp-server",
                    "name": f"mcp-{d.name}",
                    "description": desc,
                    "path": str(d.relative_to(WORKSHOP_DIR)).replace("\\", "/")
                })
        except Exception:  # @court-exempt: handled fallback
            pass
    
    mcps.extend([
        {
            "type": "mcp-server",
            "name": "camofox-browser",
            "description": "Stealth Anti-Detect Browser Automation MCP server with fingerprint masking",
            "path": "camofox-browser"
        },
        {
            "type": "mcp-server",
            "name": "browser-use-mcp",
            "description": "Autonomous vision & DOM web-agent MCP server",
            "path": "browser-use/browser_use/mcp"
        },
        {
            "type": "mcp-server",
            "name": "mcp-inspector",
            "description": "Official MCP Inspector and developer test harness UI",
            "path": "mcp-inspector"
        }
    ])
    return mcps

def scan_public_apis():
    """Scan public APIs index if present."""
    apis = []
    api_dir = WORKSHOP_DIR / "public-apis"
    readme = api_dir / "README.md"
    if readme.exists():
        try:
            content = readme.read_text(encoding="utf-8", errors="ignore")
            for line in content.splitlines()[:500]:
                if line.startswith("|") and not line.startswith("|---") and not line.startswith("| API"):
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 2:
                        name_match = re.search(r"\[(.*?)\]\((.*?)\)", parts[0])
                        api_name = name_match.group(1) if name_match else parts[0]
                        api_url = name_match.group(2) if name_match else ""
                        api_desc = parts[1] if len(parts) > 1 else ""
                        apis.append({
                            "type": "public-api",
                            "name": api_name,
                            "description": api_desc,
                            "url": api_url,
                            "auth": parts[2] if len(parts) > 2 else "unknown"
                        })
        except Exception:  # @court-exempt: handled fallback
            pass
    return apis

def normalize_text(text: str) -> str:
    """Normalize text by removing hyphens, underscores, and whitespace."""
    return re.sub(r"[\s\-_]+", "", text.lower())

def search_arsenal(query: str, category: str = "all", limit: int = 15):
    """Search skills, subsystems, MCPs, and APIs with query string matching and normalized tokens."""
    q_raw = query.lower().strip()
    q_tokens = [tok.lower() for tok in re.split(r"[\s\-_]+", query) if tok.strip()]
    q_norm = normalize_text(query)
    results = []
    
    # Search Subsystems / Repositories
    if category in ["all", "repos", "subsystems", "repo"]:
        for sub in scan_subsystems():
            searchable = f"{sub['name']} {sub['slug']} {sub['description']} {sub.get('capabilities', '')} {sub.get('tags', '')}".lower()
            norm_searchable = normalize_text(searchable)
            score = sum(3 for tok in q_tokens if tok in searchable)
            if q_norm and q_norm in norm_searchable:
                score += 10
            if score > 0 or not query.strip():
                if q_raw in sub['slug'].lower() or q_raw in sub['name'].lower() or (q_norm and q_norm in normalize_text(sub['slug'])):
                    score += 15
                results.append((score, sub))

    # Search skills
    if category in ["all", "skills", "skill"]:
        for skill in scan_all_skills():
            searchable = f"{skill['name']} {skill['description']}".lower()
            norm_searchable = normalize_text(searchable)
            score = sum(1 for tok in q_tokens if tok in searchable)
            if q_norm and q_norm in norm_searchable:
                score += 8
            if score > 0 or not query.strip():
                if q_raw in skill['name'].lower() or (q_norm and q_norm in normalize_text(skill['name'])):
                    score += 12
                results.append((score, skill))
                
    # Search MCPs
    if category in ["all", "mcps", "mcp"]:
        for mcp in scan_mcp_servers():
            searchable = f"{mcp['name']} {mcp['description']}".lower()
            norm_searchable = normalize_text(searchable)
            score = sum(1 for tok in q_tokens if tok in searchable)
            if q_norm and q_norm in norm_searchable:
                score += 8
            if score > 0 or not query.strip():
                if q_raw in mcp['name'].lower() or (q_norm and q_norm in normalize_text(mcp['name'])):
                    score += 12
                results.append((score, mcp))
                
    # Search Public APIs
    if category in ["all", "apis", "api"]:
        for api in scan_public_apis():
            searchable = f"{api['name']} {api['description']}".lower()
            norm_searchable = normalize_text(searchable)
            score = sum(1 for tok in q_tokens if tok in searchable)
            if q_norm and q_norm in norm_searchable:
                score += 6
            if score > 0:
                results.append((score, api))
                
    results.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in results[:limit]]

def main():
    parser = argparse.ArgumentParser(description="Search the Workshop Arsenal (865+ skills, Subsystems, MCPs, APIs)")
    parser.add_argument("query", nargs="?", default="", help="Search query (e.g. 'browser', 'ui ux', 'pentest', 'scrapling')")
    parser.add_argument("--category", "-c", choices=["all", "skills", "repos", "mcps", "apis"], default="all", help="Filter category")
    parser.add_argument("--limit", "-l", type=int, default=15, help="Result limit")
    parser.add_argument("--refresh", action="store_true", help="Force refresh skills cache")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    if args.refresh:
        scan_all_skills(force_refresh=True)
        
    results = search_arsenal(args.query, category=args.category, limit=args.limit)
    
    if args.json:
        print(json.dumps(results, indent=2))
        return
        
    print("\n=======================================================")
    print(f" [*] Workshop Arsenal Search: '{args.query}' (Found: {len(results)})")
    print("=======================================================")
    
    if not results:
        print("  No matching arsenal items found. Try a broader search term.\n")
        return
        
    for idx, item in enumerate(results, 1):
        item_type = item.get("type", "unknown").upper()
        name = item.get("name", "Unnamed")
        desc = item.get("description", "No description")
        if len(desc) > 95:
            desc = desc[:92] + "..."
        path = item.get("path") or item.get("url", "")
        
        print(f"[{idx:2d}] [{item_type:<10}] {name}")
        print(f"     Desc: {desc}")
        if path:
            print(f"     Path: {path}")
        print()

if __name__ == "__main__":
    main()
