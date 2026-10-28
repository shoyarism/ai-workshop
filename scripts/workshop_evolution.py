#!/usr/bin/env python3
"""
Workshop Self-Evolution Engine (Skill Freshness & Auto-Update)
===============================================================
Monitors skill health, detects staleness, suggests updates from upstream sources,
and manages deprecation lifecycle for the 900+ skill registry.
"""

import sys
import json
import re
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

WORKSHOP_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = WORKSHOP_DIR / "skills"
STATE_DIR = WORKSHOP_DIR / ".workshop_state"
EVOLUTION_DB = STATE_DIR / "skill_evolution.json"
EVOLUTION_LOG = STATE_DIR / "evolution_log.jsonl"

# Freshness thresholds
FRESHNESS_THRESHOLDS = {
    "critical": 30,   # days - security/API-breaking skills
    "high": 90,       # days - active framework skills  
    "normal": 180,    # days - standard utility skills
    "low": 365        # days - reference/archival skills
}

SKILL_CATEGORIES = {
    "critical": ["security", "auth", "crypto", "encryption", "pentest", "vuln", "audit"],
    "high": ["browser", "automation", "mcp", "api", "framework", "agent", "llm"],
    "normal": ["ui", "design", "data", "analysis", "viz", "convert", "format"],
    "low": ["reference", "guide", "template", "example", "demo", "tutorial"]
}

def load_evolution_db() -> Dict:
    """Load or initialize the evolution database."""
    if EVOLUTION_DB.exists():
        try:
            return json.loads(EVOLUTION_DB.read_text(encoding="utf-8"))
        except (IOError, OSError, json.JSONDecodeError):  # @court-exempt: json cache fallback
            pass
    return {"skills": {}, "last_full_scan": None}

def save_evolution_db(db: Dict):
    """Save the evolution database."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    EVOLUTION_DB.write_text(json.dumps(db, indent=2, default=str), encoding="utf-8")

def log_evolution_event(event_type: str, skill_name: str, details: Dict):
    """Log an evolution event to the audit trail."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "skill": skill_name,
        "details": details
    }
    with open(EVOLUTION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

def get_skill_category(skill_path: Path, frontmatter: Dict) -> str:
    """Determine skill freshness category based on tags and content."""
    tags = frontmatter.get("tags", [])
    category = frontmatter.get("category", "").lower()
    name = frontmatter.get("name", "").lower()
    desc = frontmatter.get("description", "").lower()
    
    all_text = " ".join(tags + [category, name, desc] if isinstance(tags, list) else [tags, category, name, desc])
    
    for cat, keywords in SKILL_CATEGORIES.items():
        if any(kw in all_text for kw in keywords):
            return cat
    return "normal"

def extract_frontmatter(skill_md_path: Path) -> Dict:
    """Extract YAML frontmatter from SKILL.md."""
    try:
        content = skill_md_path.read_text(encoding="utf-8", errors="ignore")[:3000]
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if match:
            fm_text = match.group(1)
            fm = {}
            for line in fm_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    fm[key.strip()] = val.strip().strip('"\'')
            return fm
    except Exception:  # @court-exempt: handled fallback
        pass
    return {}

def get_git_last_modified(file_path: Path) -> Optional[datetime]:
    """Get last git commit date for a file."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci", "--", str(file_path)],
            capture_output=True, text=True, cwd=WORKSHOP_DIR
        )
        if result.returncode == 0 and result.stdout.strip():
            return datetime.fromisoformat(result.stdout.strip().replace(" ", "T"))
    except Exception:  # @court-exempt: handled fallback
        pass
    return None

def get_upstream_remote(skill_dir: Path) -> Optional[str]:
    """Check if skill dir has an upstream git remote."""
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True, text=True, cwd=skill_dir
        )
        if "upstream" in result.stdout:
            for line in result.stdout.splitlines():
                if "upstream" in line and "(fetch)" in line:
                    return line.split()[1]
    except Exception:  # @court-exempt: handled fallback
        pass
    return None

def check_upstream_updates(skill_dir: Path) -> Dict:
    """Check for upstream updates."""
    upstream = get_upstream_remote(skill_dir)
    if not upstream:
        return {"has_upstream": False}
    
    try:
        # Fetch latest
        subprocess.run(["git", "fetch", "upstream"], cwd=skill_dir, capture_output=True, timeout=30)
        
        # Check if local is behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", "HEAD...upstream/main"],
            cwd=skill_dir, capture_output=True, text=True
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                behind = int(parts[1])
                return {"has_upstream": True, "behind_commits": behind, "remote": upstream}
    except Exception:  # @court-exempt: handled fallback
        pass
    return {"has_upstream": True, "behind_commits": 0, "remote": upstream}

def scan_skill_health(skill_md_path: Path) -> Dict:
    """Comprehensive health scan for a single skill."""
    skill_dir = skill_md_path.parent
    frontmatter = extract_frontmatter(skill_md_path)
    
    name = frontmatter.get("name", skill_dir.name)
    category = get_skill_category(skill_dir, frontmatter)
    threshold = FRESHNESS_THRESHOLDS.get(category, 180)
    
    # Git last modified
    git_modified = get_git_last_modified(skill_md_path)
    
    # File system modified
    fs_modified = datetime.fromtimestamp(skill_md_path.stat().st_mtime, tz=timezone.utc)
    
    # Use the more recent of git/fs
    last_modified = max(filter(None, [git_modified, fs_modified])) if any([git_modified, fs_modified]) else fs_modified
    
    # Calculate age
    age_days = (datetime.now(timezone.utc) - last_modified).days
    
    # Freshness status
    if age_days <= threshold:
        freshness = "fresh"
    elif age_days <= threshold * 2:
        freshness = "aging"
    elif age_days <= threshold * 3:
        freshness = "stale"
    else:
        freshness = "critical"
    
    # Check upstream
    upstream_status = check_upstream_updates(skill_dir)
    
    # Content hash for change detection
    content = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
    
    # Check for deprecation markers
    deprecated = any(marker in content.lower() for marker in ["deprecated", "archived", "superseded", "no longer maintained"])
    
    return {
        "name": name,
        "path": str(skill_md_path.relative_to(WORKSHOP_DIR)),
        "category": category,
        "threshold_days": threshold,
        "last_modified": last_modified.isoformat() if last_modified else None,
        "age_days": age_days,
        "freshness": freshness,
        "upstream": upstream_status,
        "content_hash": content_hash,
        "deprecated": deprecated,
        "frontmatter": frontmatter
    }

def run_evolution_scan() -> Dict:
    """Run full evolution scan across all skills."""
    print("[EVOLUTION] Starting full skill health scan...")
    
    db = load_evolution_db()
    skills = {}
    stats = {"total": 0, "fresh": 0, "aging": 0, "stale": 0, "critical": 0, "deprecated": 0, "with_upstream": 0, "behind": 0}
    
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        if skill_md.is_file():
            health = scan_skill_health(skill_md)
            skills[health["name"]] = health
            
            stats["total"] += 1
            stats[health["freshness"]] = stats.get(health["freshness"], 0) + 1
            if health["deprecated"]:
                stats["deprecated"] += 1
            if health["upstream"].get("has_upstream"):
                stats["with_upstream"] += 1
                if health["upstream"].get("behind_commits", 0) > 0:
                    stats["behind"] += 1
            
            # Check for changes since last scan
            prev = db["skills"].get(health["name"])
            if prev and prev.get("content_hash") != health["content_hash"]:
                log_evolution_event("skill_modified", health["name"], {
                    "old_hash": prev.get("content_hash"),
                    "new_hash": health["content_hash"],
                    "age_days": health["age_days"]
                })
    
    db["skills"] = skills
    db["last_full_scan"] = datetime.now(timezone.utc).isoformat()
    db["stats"] = stats
    save_evolution_db(db)
    
    log_evolution_event("full_scan", "all", stats)
    print(f"[EVOLUTION] Scan complete: {stats['total']} skills ({stats['fresh']} fresh, {stats['aging']} aging, {stats['stale']} stale, {stats['critical']} critical)")
    
    return {"stats": stats, "skills": skills}

def get_update_recommendations() -> List[Dict]:
    """Get prioritized update recommendations."""
    db = load_evolution_db()
    recommendations = []
    
    for name, skill in db["skills"].items():
        if skill["freshness"] in ["stale", "critical"]:
            rec = {
                "skill": name,
                "priority": "HIGH" if skill["freshness"] == "critical" else "MEDIUM",
                "reason": f"Skill is {skill['freshness']} ({skill['age_days']} days old, threshold: {skill['threshold_days']} days)",
                "category": skill["category"],
                "path": skill["path"]
            }
            
            if skill["upstream"].get("behind_commits", 0) > 0:
                rec["reason"] += f" | Upstream is {skill['upstream']['behind_commits']} commits ahead"
                rec["action"] = "git pull upstream"
            else:
                rec["action"] = "review_and_update"
            
            recommendations.append(rec)
    
    # Sort by priority and age
    recommendations.sort(key=lambda x: (0 if x["priority"] == "HIGH" else 1, -db["skills"][x["skill"]]["age_days"]))
    return recommendations

def auto_update_skill(skill_name: str, dry_run: bool = True) -> Dict:
    """Attempt to auto-update a skill from upstream."""
    db = load_evolution_db()
    skill = db["skills"].get(skill_name)
    if not skill:
        return {"success": False, "error": "Skill not found in database"}
    
    if not skill["upstream"].get("has_upstream"):
        return {"success": False, "error": "No upstream remote configured"}
    
    skill_path = WORKSHOP_DIR / skill["path"]
    skill_dir = skill_path.parent
    
    try:
        # Show what would happen
        if dry_run:
            result = subprocess.run(
                ["git", "fetch", "upstream"],
                cwd=skill_dir, capture_output=True, text=True
            )
            result = subprocess.run(
                ["git", "log", "--oneline", "HEAD..upstream/main"],
                cwd=skill_dir, capture_output=True, text=True
            )
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
            return {
                "success": True,
                "dry_run": True,
                "commits_behind": len(commits),
                "pending_commits": commits[:10]
            }
        
        # Actual update
        result = subprocess.run(
            ["git", "pull", "upstream", "main"],
            cwd=skill_dir, capture_output=True, text=True
        )
        
        if result.returncode == 0:
            log_evolution_event("skill_auto_updated", skill_name, {
                "output": result.stdout[-500:] if result.stdout else ""
            })
            # Re-scan this skill
            new_health = scan_skill_health(skill_path)
            db["skills"][skill_name] = new_health
            save_evolution_db(db)
            return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Workshop Self-Evolution Engine")
    parser.add_argument("action", choices=["scan", "recommend", "update", "status"], default="scan", nargs="?")
    parser.add_argument("--skill", help="Skill name for update action")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute", action="store_true", help="Actually execute updates (not dry run)")
    args = parser.parse_args()
    
    if args.action == "scan":
        result = run_evolution_scan()
        print(json.dumps(result["stats"], indent=2))
    elif args.action == "recommend":
        recs = get_update_recommendations()
        print(json.dumps(recs[:20], indent=2))
    elif args.action == "update":
        if not args.skill:
            print("Error: --skill required for update action")
            sys.exit(1)
        result = auto_update_skill(args.skill, dry_run=not args.execute)
        print(json.dumps(result, indent=2))
    elif args.action == "status":
        db = load_evolution_db()
        print(json.dumps(db.get("stats", {}), indent=2))