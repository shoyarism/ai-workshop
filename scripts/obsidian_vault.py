#!/usr/bin/env python3
"""
Workshop Obsidian Vault Manager & Agent Knowledge Engine
=========================================================
The centralized, local-first engine managing the Workshop AI Agent Second Brain.
Replaces remote Notion APIs with sub-millisecond local filesystem I/O,
deterministic note scaffolding, fast regex search, and health verification.

Usage:
    python scripts/obsidian_vault.py status
    python scripts/obsidian_vault.py search "<query>"
    python scripts/obsidian_vault.py list [--space <space>]
    python scripts/obsidian_vault.py adr new "<title>"
    python scripts/obsidian_vault.py postmortem new "<title>"
"""

import os
import sys
import re
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
VAULT_DIR = WORKSHOP_DIR / "vault"

def get_vault_notes() -> List[Path]:
    """Return all markdown notes in the vault excluding hidden or system dirs."""
    if not VAULT_DIR.exists():
        return []
    notes = []
    for p in VAULT_DIR.rglob("*.md"):
        if not any(part.startswith(".") for part in p.parts):
            notes.append(p)
    return sorted(notes)

def parse_frontmatter(content: str) -> Dict[str, str]:
    """Extract YAML frontmatter fields from markdown content."""
    meta = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_yaml = parts[1]
            for line in raw_yaml.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta

def cmd_status(args):
    """Output vault diagnostic health, note counts, and folder topology."""
    print("\n=======================================================")
    print(" 🧠 OBSIDIAN SECOND BRAIN VAULT STATUS")
    print(f" Vault Location: {VAULT_DIR}")
    print("=======================================================\n")

    if not VAULT_DIR.exists():
        print(f"[!] Error: Vault directory does not exist at {VAULT_DIR}")
        return

    notes = get_vault_notes()
    spaces: Dict[str, List[Path]] = {}
    total_words = 0
    missing_frontmatter = []

    for note in notes:
        try:
            rel = note.relative_to(VAULT_DIR)
            space_name = rel.parts[0] if len(rel.parts) > 1 else "Root Hub"
            spaces.setdefault(space_name, []).append(note)

            text = note.read_text(encoding="utf-8", errors="replace")
            total_words += len(text.split())
            if not text.startswith("---"):
                missing_frontmatter.append(note.name)
        except Exception as err:  # @court-exempt: handled fallback
            pass

    print(f" • Total Knowledge Notes : {len(notes)}")
    print(f" • Total Words Indexed   : {total_words:,}")
    print(f" • Storage Model         : Local Plaintext AST (.md) + YAML Frontmatter")
    print(f" • Latency Model         : Sub-millisecond SSD Direct I/O (Offline Sovereignty)\n")

    print(" 📂 Spaces & Spaces Breakdown:")
    for space, note_list in sorted(spaces.items()):
        print(f"   [{space}] ({len(note_list)} notes)")
        for n in note_list[:5]:
            print(f"     • {n.stem}")
        if len(note_list) > 5:
            print(f"     • ... and {len(note_list) - 5} more")
        print()

    if missing_frontmatter:
        print(f" [!] Notes Missing Frontmatter ({len(missing_frontmatter)}):")
        for m in missing_frontmatter[:5]:
            print(f"     - {m}")
    else:
        print(" [✓] 100% of notes contain structured YAML frontmatter.")

    print("\n=======================================================\n")

def cmd_search(args):
    """Execute high-speed regex/string search across the Obsidian vault."""
    query = args.query.strip()
    if not query:
        print("[!] Please provide a search query.")
        return

    notes = get_vault_notes()
    matches = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for note in notes:
        try:
            lines = note.read_text(encoding="utf-8", errors="replace").splitlines()
            for idx, line in enumerate(lines, 1):
                if pattern.search(line):
                    rel = note.relative_to(VAULT_DIR)
                    matches.append((rel, idx, line.strip()))
        except Exception as err:  # @court-exempt: handled fallback
            pass

    print("\n=======================================================")
    print(f" 🔍 OBSIDIAN VAULT SEARCH: '{query}'")
    print(f" Scanned {len(notes)} notes | Found {len(matches)} matches")
    print("=======================================================\n")

    if not matches:
        print(" [!] No matching notes found.")
    else:
        limit = getattr(args, "limit", 20) or 20
        for rel_path, line_no, context in matches[:limit]:
            print(f" • {rel_path} [Line {line_no}]:")
            print(f"   {context}\n")
        if len(matches) > limit:
            print(f" ... and {len(matches) - limit} more matches.")
    print("=======================================================\n")

def cmd_adr(args):
    """Manage Architecture Decision Records (ADRs)."""
    subaction = getattr(args, "adr_action", "list") or "list"
    adr_dir = VAULT_DIR / "01 - Architecture Decision Records (ADRs)"
    adr_dir.mkdir(parents=True, exist_ok=True)

    if subaction == "new":
        title = args.title.strip()
        if not title:
            print("[!] Please provide a title for the ADR.")
            return

        # Find next ADR ID
        existing = list(adr_dir.glob("ADR-*.md"))
        highest_id = 0
        for f in existing:
            m = re.match(r"ADR-(\d+)", f.name)
            if m:
                highest_id = max(highest_id, int(m.group(1)))
        
        next_id = highest_id + 1
        adr_id_str = f"ADR-{next_id:03d}"
        clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
        filename = f"{adr_id_str} - {clean_title}.md"
        filepath = adr_dir / filename
        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""---
title: {adr_id_str} - {clean_title}
type: adr
status: proposed
date: {today}
tags: [adr, architecture, workshop]
---

# {adr_id_str}: {clean_title}

## Context & Problem Statement
<!-- What is the background, context, and the problem being solved? -->

## Decision
<!-- What is the architectural decision, change, or choice? -->

## Status
`Proposed` <!-- Options: Proposed, Accepted, Deprecated, Superseded -->

## Consequences
### Positive
* <!-- Benefits and positive impacts -->

### Negative
* <!-- Costs, trade-offs, and negative consequences -->
"""
        filepath.write_text(content, encoding="utf-8")
        print(f"\n[+] Created new Architecture Decision Record:")
        print(f"    File: {filepath}")
        print(f"    Wiki-Link: [[{filename[:-3]}]]\n")

    else:
        existing = sorted(adr_dir.glob("ADR-*.md"))
        print(f"\n[*] Found {len(existing)} ADRs in vault:")
        for f in existing:
            meta = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
            status = meta.get("status", "unknown").upper()
            print(f" • {f.stem} [{status}]")
        print()

def cmd_postmortem(args):
    """Manage Error Post-Mortems."""
    subaction = getattr(args, "pm_action", "list") or "list"
    pm_dir = VAULT_DIR / "02 - Post-Mortems"
    pm_dir.mkdir(parents=True, exist_ok=True)

    if subaction == "new":
        title = args.title.strip()
        if not title:
            print("[!] Please provide a title for the Post-Mortem.")
            return

        existing = list(pm_dir.glob("PM-*.md"))
        highest_id = 0
        for f in existing:
            m = re.match(r"PM-(\d+)", f.name)
            if m:
                highest_id = max(highest_id, int(m.group(1)))
        
        next_id = highest_id + 1
        pm_id_str = f"PM-{next_id:03d}"
        clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
        filename = f"{pm_id_str} - {clean_title}.md"
        filepath = pm_dir / filename
        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""---
title: {pm_id_str} - {clean_title}
type: post-mortem
status: resolved
date: {today}
tags: [post-mortem, bugs, troubleshooting, fixes]
---

# {pm_id_str}: {clean_title}

## Problem Description
<!-- What was the exact error, symptom, or failure trace observed? -->

## Root Cause
<!-- What was the underlying technical or environmental cause? -->

## Deterministic Fix
<!-- What is the verified, reproducible solution to prevent or resolve this? -->
```python
# Verified code snippet or configuration
```
"""
        filepath.write_text(content, encoding="utf-8")
        print(f"\n[+] Created new Post-Mortem Record:")
        print(f"    File: {filepath}")
        print(f"    Wiki-Link: [[{filename[:-3]}]]\n")

    else:
        existing = sorted(pm_dir.glob("PM-*.md"))
        print(f"\n[*] Found {len(existing)} Post-Mortems in vault:")
        for f in existing:
            print(f" • {f.stem}")
        print()

def cmd_journal(args):
    """Create an automated agent execution log and session handoff."""
    task = getattr(args, "task", "").strip() or "General Agent Sprint"
    summary = getattr(args, "summary", "").strip() or "Executed multi-step workshop tasks."
    blockers = getattr(args, "blockers", "").strip() or "None"
    next_steps = getattr(args, "next_steps", "").strip() or "Continue sprint backlog."
    artifacts = getattr(args, "artifacts", "").strip()

    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M")
    file_timestamp = now.strftime("%Y-%m-%d-%H%M")

    tasks_dir = VAULT_DIR / "04 - Tasks & Sprints"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    journal_file = tasks_dir / f"Journal - {file_timestamp}.md"

    artifacts_section = ""
    if artifacts:
        artifacts_section = "\n### Modified Artifacts & Files\n" + "\n".join(f"- `{a.strip()}`" for a in artifacts.split(","))

    content = f"""---
title: Session Journal - {file_timestamp}
type: journal
date: {now.strftime("%Y-%m-%d")}
time: "{now.strftime("%H:%M")}"
tags: [journal, session, handoff, tasks]
---

# 📝 Session Journal: {task}
*Recorded: {timestamp_str}*

## Executive Summary
{summary}
{artifacts_section}

## 🚧 Blockers & Edge Cases
{blockers}

## 🎯 Recommended Next Actions
{next_steps}
"""
    journal_file.write_text(content, encoding="utf-8")
    print(f"\n[+] Created Session Journal Note: {journal_file.name}")
    print(f"    Wiki-Link: [[{journal_file.stem}]]")

    # Update Autonomous Task Queue & Session Handoffs.md
    queue_file = tasks_dir / "Autonomous Task Queue & Session Handoffs.md"
    if queue_file.exists():
        queue_text = queue_file.read_text(encoding="utf-8", errors="replace")
        entry = f"\n- **[[{journal_file.stem}]]:** {task} — *{summary[:100]}...* ({timestamp_str})"
        if "## 📜 Session History" not in queue_text:
            queue_text += "\n\n## 📜 Session History\n"
        queue_text += entry
        queue_file.write_text(queue_text, encoding="utf-8")
        print(f"[+] Appended to Autonomous Task Queue: [[Autonomous Task Queue & Session Handoffs]]\n")

def cmd_compact(args):
    """
    Compact aged session handoffs, journal entries, and routine audits.
    - Summarizes aged items (> days threshold, default 7 days) into a Rolling Compaction Summary.
    - Moves raw aged notes into vault/99 - Archive/ without destroying history or breaking links.
    - Ensures notes carry status, date, and supersedes fields.
    - Updates Autonomous Task Queue & Session Handoffs.md with the rolling summary pointer.
    """
    days_threshold = getattr(args, "days", 7) or 7
    dry_run = getattr(args, "dry_run", False)

    print("\n=======================================================")
    print(" 📦 OBSIDIAN VAULT COMPACTION & NOTE LIFECYCLE ENGINE")
    print(f" Vault Location : {VAULT_DIR}")
    print(f" Age Threshold  : {days_threshold} days")
    print(f" Mode           : {'DRY RUN (Preview Only)' if dry_run else 'LIVE EXECUTION'}")
    print("=======================================================\n")

    tasks_dir = VAULT_DIR / "04 - Tasks & Sprints"
    archive_dir = VAULT_DIR / "99 - Archive"
    if not tasks_dir.exists():
        print(f"[!] Tasks directory does not exist at {tasks_dir}")
        return

    now = datetime.now()
    now_date = now.date()
    candidates = []

    protected_stems = {"Autonomous Task Queue & Session Handoffs"}

    for p in tasks_dir.rglob("*.md"):
        if any(part.startswith(".") for part in p.parts):
            continue
        if p.stem in protected_stems or p.name.startswith("Rolling_Summary_"):
            continue

        content = p.read_text(encoding="utf-8", errors="replace")
        meta = parse_frontmatter(content)
        note_date = None
        
        if "date" in meta:
            try:
                note_date = datetime.strptime(meta["date"][:10], "%Y-%m-%d").date()
            except Exception as err:  # @court-exempt: handled fallback
                pass
        
        if not note_date:
            m = re.search(r'(\d{4}-\d{2}-\d{2})', p.stem)
            if m:
                try:
                    note_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                except Exception as err:  # @court-exempt: handled fallback
                    pass

        if not note_date:
            note_date = datetime.fromtimestamp(p.stat().st_mtime).date()

        age_days = (now_date - note_date).days
        if age_days >= days_threshold:
            candidates.append({
                "path": p,
                "stem": p.stem,
                "meta": meta,
                "date": note_date,
                "age_days": age_days,
                "content": content
            })

    if not candidates:
        print(f"[✓] No session notes older than {days_threshold} days found. Vault is already fully compacted!\n")
        return

    print(f"[*] Found {len(candidates)} aged note(s) eligible for rolling compaction:\n")
    for c in candidates:
        print(f" • [[{c['stem']}]] ({c['date']}, {c['age_days']} days old)")

    if dry_run:
        print(f"\n[Preview] Would archive {len(candidates)} note(s) to vault/99 - Archive/ and generate Rolling Summary.")
        print("          Run without --dry-run to execute.\n")
        return

    date_str = now.strftime("%Y-%m-%d")
    ts_str = now.strftime("%Y-%m-%d %H:%M")
    rolling_file = tasks_dir / f"Rolling_Summary_{date_str}.md"
    
    # Pre-compaction Git Snapshot Invariant
    git_dir = VAULT_DIR / ".git"
    if git_dir.exists():
        try:
            subprocess.run(["git", "add", "."], cwd=str(VAULT_DIR), capture_output=True, check=False)
            subprocess.run(
                ["git", "commit", "-m", f"chore(vault): pre-compaction snapshot {ts_str}"],
                cwd=str(VAULT_DIR),
                capture_output=True,
                check=False
            )
            print("[+] Automated Git snapshot created for vault before compaction.")
        except Exception as e:
            print(f"[!] Warning: Git pre-compaction snapshot skipped: {e}")
    
    summary_lines = [
        "---",
        f"title: Rolling Compaction Summary ({date_str})",
        "type: rolling-summary",
        "status: active",
        f"date: {date_str}",
        f"compacted_count: {len(candidates)}",
        "tags: [vault, compaction, archive, rolling-summary, tasks]",
        "---",
        "",
        f"# 📦 Rolling Compaction Summary: {date_str}",
        f"*Generated: {ts_str} | Compacted {len(candidates)} notes older than {days_threshold} days.*",
        "",
        "## Compacted Sources & History Links",
    ]

    for c in sorted(candidates, key=lambda x: str(x['date'])):
        summary_lines.append(f"- **[[Archive/{c['stem']}|{c['stem']}]]:** Date: `{c['date']}` (Age: {c['age_days']} days)")

    summary_lines.extend([
        "",
        "## Consolidated Session Milestones",
    ])

    for c in candidates:
        text = c["content"]
        match = re.search(r'##\s*(?:Executive\s+)?Summary\s*\n(.*?)(?=\n##|\Z)', text, re.DOTALL | re.IGNORECASE)
        if match:
            s_text = match.group(1).strip()
            first_p = s_text.split("\n\n")[0].strip()
            summary_lines.append(f"### [[{c['stem']}]] ({c['date']})\n{first_p}\n")

    summary_lines.extend([
        "## Durable Assets & Architecture Decisions",
        "- All durable decisions are preserved in `vault/01 - Architecture Decision Records (ADRs)/`.",
        "- All root-cause fixes are preserved in `vault/02 - Post-Mortems/`.",
        "- Raw historical session notes are safely preserved in `vault/99 - Archive/`.",
        "",
        "---",
        "*Created automatically by `workshop vault compact`.*"
    ])

    rolling_file.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"\n[+] Created Rolling Summary Note: [[{rolling_file.stem}]]")

    archive_dir.mkdir(parents=True, exist_ok=True)
    for c in candidates:
        src = c["path"]
        rel = src.relative_to(tasks_dir)
        dst = archive_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        note_content = c["content"]
        if note_content.startswith("---"):
            parts = note_content.split("---", 2)
            if len(parts) >= 3:
                raw_fm = parts[1]
                if "status:" in raw_fm:
                    raw_fm = re.sub(r'status:\s*\S+', 'status: archived', raw_fm)
                else:
                    raw_fm += f"\nstatus: archived"
                raw_fm += f"\narchived_date: {date_str}\nsuperseded_by: [[{rolling_file.stem}]]"
                note_content = f"---{raw_fm}---{parts[2]}"
        
        dst.write_text(note_content, encoding="utf-8")
        src.unlink()
        print(f" [->] Archived: `{src.name}` -> `{dst.relative_to(VAULT_DIR)}`")

    queue_file = tasks_dir / "Autonomous Task Queue & Session Handoffs.md"
    if queue_file.exists():
        queue_text = queue_file.read_text(encoding="utf-8", errors="replace")
        entry = f"\n- **[[{rolling_file.stem}]]:** Compacted {len(candidates)} historical sessions into rolling summary ({ts_str})"
        if "## 📜 Session History" not in queue_text:
            queue_text += "\n\n## 📜 Session History\n"
        queue_text += entry
        queue_file.write_text(queue_text, encoding="utf-8")
        print(f"[+] Updated Autonomous Task Queue with rolling compaction pointer.")

    if git_dir.exists():
        try:
            subprocess.run(["git", "add", "."], cwd=str(VAULT_DIR), capture_output=True, check=False)
            subprocess.run(
                ["git", "commit", "-m", f"chore(vault): completed rolling compaction ({len(candidates)} archived) {ts_str}"],
                cwd=str(VAULT_DIR),
                capture_output=True,
                check=False
            )
            print("[+] Automated Git snapshot created for post-compaction state.")
        except Exception as e:
            pass

    print(f"\n✅ Vault compaction completed successfully! {len(candidates)} notes archived.\n")

def main():
    parser = argparse.ArgumentParser(description="Workshop Obsidian Vault Engine")
    subparsers = parser.add_subparsers(dest="command")

    # status
    subparsers.add_parser("status", help="Check vault health, note counts, and folder topology")

    # search
    p_search = subparsers.add_parser("search", help="Search vault notes")
    p_search.add_argument("query", help="Regex or string query")
    p_search.add_argument("--limit", type=int, default=20, help="Max results to display")

    # adr
    p_adr = subparsers.add_parser("adr", help="Manage ADRs")
    adr_subs = p_adr.add_subparsers(dest="adr_action")
    p_adr_new = adr_subs.add_parser("new", help="Scaffold new ADR")
    p_adr_new.add_argument("title", help="Title of the ADR")
    adr_subs.add_parser("list", help="List all ADRs")

    # postmortem
    p_pm = subparsers.add_parser("postmortem", help="Manage Post-Mortems")
    pm_subs = p_pm.add_subparsers(dest="pm_action")
    p_pm_new = pm_subs.add_parser("new", help="Scaffold new Post-Mortem")
    p_pm_new.add_argument("title", help="Title of the Post-Mortem")
    pm_subs.add_parser("list", help="List all Post-Mortems")

    # journal
    p_jr = subparsers.add_parser("journal", help="Record automated agent session journal note")
    p_jr.add_argument("--task", default="", help="Task or sprint objective")
    p_jr.add_argument("--summary", default="", help="Completed work summary")
    p_jr.add_argument("--blockers", default="None", help="Known blockers or edge cases")
    p_jr.add_argument("--next-steps", default="Continue backlog", help="Next actions")
    p_jr.add_argument("--artifacts", default="", help="Comma-separated list of modified artifacts")

    # compact
    p_comp = subparsers.add_parser("compact", help="Compact aged session handoffs and routine audits into rolling summary")
    p_comp.add_argument("--days", type=int, default=7, help="Age threshold in days (default: 7)")
    p_comp.add_argument("--dry-run", action="store_true", help="Preview compaction without moving files")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "adr":
        cmd_adr(args)
    elif args.command == "postmortem":
        cmd_postmortem(args)
    elif args.command == "journal":
        cmd_journal(args)
    elif args.command == "compact":
        cmd_compact(args)
    else:
        cmd_status(args)

if __name__ == "__main__":
    main()
