# Workshop OS — Quick Start Guide

## 1. Zero-Friction Setup

### Step 1: Install Dependencies
```bash
# Clone the repository
git clone https://github.com/shoyarism/ai-workshop.git
cd ai-workshop

# Sync Python environment (requires uv or standard Python 3.11+)
uv sync
```

### Step 2: Arm the Slop Court Bailiff Hook
```bash
# Installs git pre-commit and pre-push interception hooks
python scripts/workshop.py court bailiff install
```

### Step 3: Verify Subsystems
```bash
# Comprehensive diagnostics across all modules
python scripts/workshop.py doctor
```

---

## 2. Connecting Your AI Agent Harness

Workshop OS works across all major AI harnesses without vendor lock-in. Copy the master instructions from [`WORKSHOP_DEFAULT_SYSTEM_PROMPT.md`](WORKSHOP_DEFAULT_SYSTEM_PROMPT.md):

| Harness | Configuration File | Behavior |
| :--- | :--- | :--- |
| **Claude Code** | `CLAUDE.md` or `~/.claude/CLAUDE.md` | Auto-binds FastMCP tools & pre-commit Bailiff |
| **Cursor** | `.cursorrules` or `.cursor/rules/` | Local Foundry or Zero-Clone via GitHub API |
| **Gemini Antigravity** | `~/.gemini/config/AGENTS.md` | Master Soul hooks (`court_trial`, `court_council`) |
| **Windsurf** | `.windsurfrules` or `AGENTS.md` | Cascading Context & Tool Forge |
| **OpenCode / Hermes** | `opencode.json` & `SOUL.md` | Local Foundry execution |

---

## 3. Daily Command Palette

```bash
# 1. Search 2,140+ domain skills in milliseconds
python scripts/workshop.py search "<keyword>"

# 2. Convene Slop Court quality review on staged code
python scripts/workshop.py court trial --staged

# 3. Convene Supreme Council dialectic debate on any decision
python scripts/workshop.py court council "<topic>" --domain <general|architecture|business|creative>

# 4. Enumerate available FastMCP tools
python scripts/workshop.py mcp list
```

---

## 4. The Zero-Clone Cloud Protocol

Operating in an ephemeral container, GitHub Codespace, or remote VM? You do not need to clone 600+ MB of assets. Stream any skill runbook directly into your agent context using raw curl:

```bash
# Fetch any skill directly into context
curl -fsSL https://raw.githubusercontent.com/shoyarism/ai-workshop/main/skills/systematic-debugging/SKILL.md
```
