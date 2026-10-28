---
name: obsidian-vault-automation
description: Programmatically read, write, search, and organize an Obsidian vault — markdown notes, frontmatter, tags, wiki links, ADRs, post-mortems, and task queues. Use when the user wants AI agents to maintain their second brain, create records, query vault content, or sync knowledge programmatically. Triggers on: obsidian, vault, markdown notes, frontmatter, wiki links, tags, adr, postmortem, task queue, second brain, knowledge base, vault automation.
---

# Obsidian Vault Automation

Programmatically read, write, search, and organize an Obsidian vault. AI agents can create ADRs, post-mortems, task handoffs, search existing notes, update frontmatter, and maintain the second brain as a structured knowledge base.

## When to trigger

- User wants AI agents to write to their Obsidian vault (ADRs, post-mortems, notes)
- User needs to search vault content programmatically (find past decisions, post-mortems)
- User wants vault maintenance (frontmatter updates, tag organization, link fixing)
- User is building a knowledge base that agents read from and write to

## Vault structure (Workshop convention)

```
vault/
  Home.md                          # Master hub
  00 - Meta/                       # User DNA, environment profile
  01 - Architecture Decision Records (ADRs)/
  02 - Post-Mortems/               # PM-001, PM-002, ...
  03 - Subsystems/
  04 - Tasks & Sprints/            # Autonomous task queue, handoffs
  05 - Skills Library/
  99 - Archive/
```

## Reading vault notes

```python
from pathlib import Path
import yaml
import re

VAULT = Path("D:/Workshop/vault")

def read_note(rel_path: str) -> str:
    return (VAULT / rel_path).read_text(encoding="utf-8")

def parse_frontmatter(content: str) -> dict:
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}

def search_vault(query: str, limit: int = 10) -> list[tuple[Path, str]]:
    """Simple text search across vault markdown files."""
    query_lower = query.lower()
    results = []
    for md_file in VAULT.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="replace")
        if query_lower in content.lower():
            results.append((md_file, content[:200]))
            if len(results) >= limit:
                break
    return results

def get_frontmatter(rel_path: str) -> dict:
    content = read_note(rel_path)
    return parse_frontmatter(content)
```

## Writing vault notes

### Create an ADR

```python
from datetime import datetime

def create_adr(title: str, content: str, tags: list[str] | None = None):
    adr_dir = VAULT / "01 - Architecture Decision Records (ADRs)"
    adr_dir.mkdir(parents=True, exist_ok=True)
    
    existing = list(adr_dir.glob("ADR-*.md"))
    count = len(existing) + 1
    filename = f"ADR-{count:03d} - {title}.md"
    
    now = datetime.now().strftime("%Y-%m-%d")
    tags_str = ", ".join(tags or ["adr", "architecture"])
    
    fm = f"""---
title: {title}
type: adr
status: Proposed
date: {now}
tags: [{tags_str}]
---

# ADR-{count:03d}: {title}

## Context & Problem Statement

{content}
"""
    (adr_dir / filename).write_text(fm, encoding="utf-8")
    return filename

def create_postmortem(title: str, content: str, severity: str = "Medium"):
    pm_dir = VAULT / "02 - Post-Mortems"
    pm_dir.mkdir(parents=True, exist_ok=True)
    
    existing = list(pm_dir.glob("PM-*.md"))
    count = len(existing) + 1
    filename = f"PM-{count:03d} - {title}.md"
    
    now = datetime.now().strftime("%Y-%m-%d")
    
    fm = f"""---
title: {title}
type: post-mortem
status: Resolved
date: {now}
tags: ["post-mortem", "bugfix"]
severity: {severity}
---

# PM-{count:03d}: {title}

{content}
"""
    (pm_dir / filename).write_text(fm, encoding="utf-8")
    return filename

def create_handoff(title: str, content: str, tags: list[str] | None = None):
    task_dir = VAULT / "04 - Tasks & Sprints"
    task_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"Handoff - {now} - {title}.md"
    
    tags_str = ", ".join(tags or ["handoff", "session"])
    
    fm = f"""---
title: {title}
type: handoff
date: {now}
tags: [{tags_str}]
---

# Session Handoff: {title}

{content}
"""
    (task_dir / filename).write_text(fm, encoding="utf-8")
    return filename
```

## Updating frontmatter

```python
def update_frontmatter(rel_path: str, updates: dict):
    """Update frontmatter fields while preserving body content."""
    path = VAULT / rel_path
    content = path.read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not m:
        return False
    
    fm = yaml.safe_load(m.group(1)) or {}
    fm.update(updates)
    
    new_fm = yaml.dump(fm, default_flow_style=False)
    new_content = f"---\n{new_fm}---\n{m.group(2)}"
    path.write_text(new_content, encoding="utf-8")
    return True
```

## Wiki link management

```python
def find_wiki_links(content: str) -> list[str]:
    """Find all [[Wiki Links]] in a note."""
    return re.findall(r"\[\[([^\]]+)\]\]", content)

def fix_broken_links(rel_path: str):
    """Report broken wiki links in a note."""
    content = read_note(rel_path)
    links = find_wiki_links(content)
    broken = []
    for link in links:
        # Handle [[link|alias]] syntax
        target = link.split("|")[0].strip()
        if not (VAULT / f"{target}.md").exists() and not (VAULT / target).exists():
            broken.append(target)
    return broken
```

## Example workflows

**Record an architecture decision:**
```python
create_adr(
    "Use LangGraph for multi-agent workflows",
    "Selected LangGraph over CrewAI for stateful cyclic workflows with checkpointers.",
    tags=["adr", "architecture", "langgraph", "agents"]
)
```

**Record a post-mortem after an incident:**
```python
create_postmortem(
    "Workshop copy path remapping failure",
    "Initial robocopy missed .mcp.json path remapping; fixed on second pass.",
    severity="Low"
)
```

**Create a session handoff:**
```python
create_handoff(
    "Workshop enrichment session",
    "Added langgraph-agent-builder, crewai-orchestrator, mcp-stripe-server, mcp-resend-email, rag-eval-observability skills.",
    tags=["handoff", "enrichment", "skills"]
)
```

## Decision checklist

- [ ] Vault root path identified (D:/Workshop/vault)
- [ ] Note types mapped to vault folders (ADR → 01, post-mortem → 02, handoff → 04)
- [ ] Frontmatter schema defined per note type
- [ ] Search function implemented for querying existing notes
- [ ] Link validation included for wiki-style links
- [ ] Backup strategy considered before bulk writes

## Related Workshop skills

- `workshop-scout` — discover Workshop skills and subsystems
- `memory-recall` / `memory-write` — MCP tools for vault memory (read-only/write)
- `documentation-and-adrs` — ADR writing standards
- `documentation-lookup` — read documentation from vault and external sources
