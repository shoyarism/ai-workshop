---
name: workshop-arsenal
description: "How to use the Workshop OS centralized arsenal: MCP server tools (skill_search, memory_recall, verify, critique) and Master CLI."
---

# Workshop OS Centralized Arsenal

Workshop OS centralizes tools so any AI agent harness (Antigravity, Claude Code, OpenCode, Cursor, Codex) can access skills, persistent memory, vision, and verification.

## 1. Native MCP Tools (Direct Function Calling)

| Tool | Purpose | Example |
| :--- | :--- | :--- |
| `skill_search(query)` | Hybrid semantic + BM25 search across 920+ skills | `skill_search("ffmpeg audio")` |
| `skill_load(name)` | Retrieve full SKILL.md and assets on demand | `skill_load("agent-reach")` |
| `memory_recall(query)` | Query Obsidian vault ADRs and Post-Mortems | `memory_recall("pipe decoding")` |
| `memory_write(kind, title, content)` | Save ADR, post-mortem, or task handoff | `memory_write("postmortem", "Fix X", "...")` |
| `verify(cmd)` | Deterministic test runner | `verify("npm test")` |
| `critique(code)` | Escalate plan or diff to critic model for review | `critique(plan_text)` |
| `antislop_audit(path)` | Check code for AI clichés and lazy comments | `antislop_audit(".")` |
| `graphify_query(q)` | Query codebase AST knowledge graph | `graphify_query("entrypoints")` |

## 2. Universal CLI Commands (Shell Execution)

Execute via `uv run python scripts/workshop.py <subcommand>`:

```powershell
# 1. Search catalog
uv run python scripts/workshop.py search "<keyword>"

# 2. Workspace diagnostics
uv run python scripts/workshop.py doctor

# 3. Multimodal vision and OCR
uv run python scripts/workshop.py see "<file_or_dir>"

# 4. Anti-slop quality gates
uv run python scripts/workshop.py antislop gate

# 5. Obsidian Vault memory
uv run python scripts/workshop.py vault status
uv run python scripts/workshop.py vault search "<query>"
```
