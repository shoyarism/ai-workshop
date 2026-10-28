# Workshop Documentation

> **Workspace Root:** `D:\Workshop`  or drive E
> **Universal Master CLI:** `python scripts/workshop.py`  
> **Skills Count:** 963 (across all sources)  
> **MCP Servers:** 20+  
> **Public APIs Index:** 1,500+  

---

## Table of Contents

1. [Overview](#1-overview)
2. [Workspace Structure](#2-workspace-structure)
3. [Master CLI](#3-master-cli)
4. [Skills Library](#4-skills-library)
5. [Scripts & Tooling](#5-scripts--tooling)
6. [AI Agents Handbook](#6-ai-agents-handbook)
7. [MCP Servers](#7-mcp-servers)
8. [Design Arsenal](#8-design-arsenal)
9. [Reference Repositories](#9-reference-repositories)
10. [Prompts Library](#10-prompts-library)
11. [Operating Standards](#11-operating-standards)
12. [Quick Reference Cheat Sheet](#12-quick-reference-cheat-sheet)

---

## 1. Overview

The Workshop is a centralized AI operating system and engineering arsenal. It serves as a universal workspace for AI agents (Hermes, Claude Code, Codex, Gemini CLI, OpenCode, etc.) containing:

- **963 agent skills** across 12+ category paths
- **20+ MCP servers** for browser automation, databases, search, and more
- **Master CLI** (`workshop.py`) for search, vision, diagnostics, and browser tasks
- **UI/UX design system** with tokens and architecture guidelines
- **Reference repositories** for public APIs, free tiers, and self-hosted software
- **Prompt library** for code review, architecture planning, and prompt engineering
- **Motion/video generation** toolkit (Hyperframes)
- **Stealth browser** engine (Camofox) for anti-detect automation

---

## 2. Workspace Structure

```
D:\Workshop\
â”‚
â”œâ”€â”€ AGENTS.md                    # Universal agent standards & protocols
â”œâ”€â”€ CLAUDE.md                    # Claude Code specific guidelines
â”œâ”€â”€ WORKSHOP.md                  # Centralized startup & arsenal activation
â”œâ”€â”€ WORKSHOP_ARSENAL.md          # Unified arsenal reference (Hermes-focused)
â”œâ”€â”€ HERMES_ARSENAL.md            # Hermes-specific arsenal quick reference
â”œâ”€â”€ OPENCODE.md                  # OpenCode agent guidelines
â”œâ”€â”€ OPENCODE_ARSENAL.md
â”œâ”€â”€ OPENCODE_GUIDE.md
â”œâ”€â”€ kilo.jsonc                   # Kilo Code configuration
â”œâ”€â”€ opencode.json                # OpenCode configuration
â”‚
â”œâ”€â”€ skills/                      # Primary skills library (854+ skills)
â”‚   â”œâ”€â”€ _archive/               # Archived/deprecated skills (3)
â”‚   â”œâ”€â”€ aion-ui/                # AI agent cowork app (iOfficeAI/AionUi)
â”‚   â”œâ”€â”€ officecli/              # Office document automation CLI
â”‚   â”œâ”€â”€ officecli-docx/         # Word document specialist
â”‚   â”œâ”€â”€ officecli-xlsx/         # Excel spreadsheet specialist
â”‚   â”œâ”€â”€ officecli-pptx/         # PowerPoint specialist
â”‚   â”œâ”€â”€ officecli-pitch-deck/   # Fundraising deck specialist
â”‚   â”œâ”€â”€ officecli-financial-model/
â”‚   â”œâ”€â”€ officecli-academic-paper/
â”‚   â”œâ”€â”€ officecli-data-dashboard/
â”‚   â”œâ”€â”€ officecli-word-form/
â”‚   â”œâ”€â”€ googleworkspace-cli/    # Google Workspace CLI (gws)
â”‚   â”œâ”€â”€ larksuite-cli/          # Lark/Feishu CLI
â”‚   â”œâ”€â”€ mineru-skill/           # PDF/Office â†’ Markdown parser
â”‚   â”œâ”€â”€ officekit/              # Python Office automation library
â”‚   â”œâ”€â”€ office2pdf/             # DOCX/XLSX/PPTX â†’ PDF converter
â”‚   â”œâ”€â”€ deckprobe/              # Document metadata probe
â”‚   â”œâ”€â”€ harness-anything/       # WPS/MS Office/Zotero/Illustrator automation
â”‚   â”œâ”€â”€ pretty-mermaid-skills/  # Mermaid diagram rendering
â”‚   â”œâ”€â”€ ...                     # 830+ more skills
â”‚
â”œâ”€â”€ scripts/                     # Workshop tooling
â”‚   â”œâ”€â”€ workshop.py             # Master CLI entrypoint
â”‚   â”œâ”€â”€ workshop_search.py      # Skills/APIs search engine
â”‚   â”œâ”€â”€ workshop_vision.py      # Multimodal vision inspector
â”‚   â”œâ”€â”€ workshop_doctor.py      # Health & diagnostics
â”‚   â”œâ”€â”€ live_browser_hub.py     # Browser automation dashboard (:7860)
â”‚   â”œâ”€â”€ run_browser_agent.py    # Autonomous browser task runner
â”‚   â”œâ”€â”€ mcp_launcher.py         # MCP server launcher
â”‚   â”œâ”€â”€ mcp_configs/            # MCP configuration files
â”‚   â”œâ”€â”€ configure_context_and_combos.py
â”‚   â”œâ”€â”€ fix_all_workshop_issues.py
â”‚   â”œâ”€â”€ fix_claude_omniroute.py
â”‚   â”œâ”€â”€ generate_office_layout.py
â”‚   â”œâ”€â”€ inspect_combos.py
â”‚   â”œâ”€â”€ notion_sync.py
â”‚   â”œâ”€â”€ optimize_omniroute.py
â”‚
â”œâ”€â”€ camofox-browser/            # Stealth anti-detect browser (Port 9377)
â”‚   â”œâ”€â”€ server.js               # REST API server
â”‚   â”œâ”€â”€ camofox.config.json     # Browser configuration
â”‚   â”œâ”€â”€ mcp/                    # MCP server integration
â”‚   â”œâ”€â”€ docs/                   # Documentation
â”‚   â””â”€â”€ ...
â”‚
â”œâ”€â”€ browser-use/                 # Vision-based web automation framework
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ pyproject.toml
â”‚   â”œâ”€â”€ skills/                 # 6 browser automation skills
â”‚   â””â”€â”€ ...
â”‚
â”œâ”€â”€ hyperframes/                 # Motion & generative video toolkit
â”‚   â”œâ”€â”€ skills/                 # 20 motion/video generation skills
â”‚   â”œâ”€â”€ CLAUDE.md
â”‚   â””â”€â”€ ...
â”‚
â”œâ”€â”€ ui-ux-arsenal/               # UI/UX design system
â”‚   â”œâ”€â”€ DESIGN_SYSTEM_MASTER.md # Design architecture & guidelines
â”‚   â””â”€â”€ tokens/
â”‚       â””â”€â”€ design_tokens.json  # Master design tokens (colors, typography, spacing)
â”‚
â”œâ”€â”€ prompts/                     # Prompt library
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ library/                # 5 operational prompts
â”‚   â”‚   â”œâ”€â”€ 00-system-prompt-framework.md
â”‚   â”‚   â”œâ”€â”€ 01-code-review-prompt.md
â”‚   â”‚   â”œâ”€â”€ 02-architecture-planning-prompt.md
â”‚   â”‚   â””â”€â”€ 03-prompt-engineering-guide.md
â”‚   â””â”€â”€ _archive/               # Archived prompts
â”‚       â””â”€â”€ agents-run-artifacts/
â”‚
â”œâ”€â”€ ai agents handbook/          # AI agent playbook & packs
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ AI-AGENT-MASTER-PROMPT.md
â”‚   â”œâ”€â”€ ai-agent-suite/
â”‚   â”œâ”€â”€ references/
â”‚   â””â”€â”€ packs/
â”‚       â”œâ”€â”€ garden-skills/      # Garden web component skills
â”‚       â”œâ”€â”€ ponytail/           # Architecture debt auditor skills
â”‚       â”œâ”€â”€ styleseed/          # UI design system skills
â”‚       â”œâ”€â”€ baoyu-design/       # Visual illustration & design
â”‚       â”œâ”€â”€ huashu-design/      # Aesthetics & layout
â”‚       â”œâ”€â”€ karpathy/           # Deep learning & training
â”‚       â””â”€â”€ ecc/
â”‚
â”œâ”€â”€ public-apis/                 # Public APIs index (1,500+ APIs)
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ CONTRIBUTING.md
â”‚   â”œâ”€â”€ LICENSE
â”‚   â””â”€â”€ scripts/
â”‚
â”œâ”€â”€ free-for-dev/                # Free developer tiers index
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ CONTRIBUTING.md
â”‚   â””â”€â”€ LICENSE
â”‚
â”œâ”€â”€ awesome-selfhosted/          # Self-hosted software directory
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ CONTRIBUTING.md
â”‚   â”œâ”€â”€ LICENSE
â”‚   â””â”€â”€ non-free.md
â”‚
â”œâ”€â”€ awesome-mcp-servers/         # MCP server directory
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ CONTRIBUTING.md
â”‚   â””â”€â”€ LICENSE
â”‚
â”œâ”€â”€ mcp-servers-official/        # Official MCP servers
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ CONTRIBUTING.md
â”‚   â””â”€â”€ LICENSE
â”‚
â”œâ”€â”€ eliza/                       # Eliza framework
â”‚   â””â”€â”€ ...
â”‚
â”œâ”€â”€ openclaw/                    # OpenClaw agent platform
â”‚   â””â”€â”€ ...
â”‚
â”œâ”€â”€ opencode/                    # OpenCode agent platform
â”‚   â””â”€â”€ ...
â”‚
â””â”€â”€ open-generative-ai/          # Open generative AI resources
    â””â”€â”€ ...
```

---

## 3. Master CLI

### Entry Point

```bash
python scripts/workshop.py <command> [options]
```

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `see` | Multimodal vision inspector (images, videos, audio, directories) | `python scripts/workshop.py see "report.pdf" --prompt "Summarize"}` |
| `vision` | Vision subcommands (inspect, storyboard, frames, ocr, transcribe) | `python scripts/workshop.py vision ocr "screenshot.png"` |
| `search` | Search 820+ skills, 20+ MCPs, 1,500+ APIs | `python scripts/workshop.py search "browser automation"` |
| `doctor` | Environment health & diagnostics | `python scripts/workshop.py doctor` |
| `hub` | Launch live browser dashboard | `python scripts/workshop.py hub --port 7860` |
| `browser` | Autonomous browser task execution | `python scripts/workshop.py browser --url "https://example.com" --task "Scrape titles" --live` |
| `mcp` | MCP server management (list, test, start) | `python scripts/workshop.py mcp list` |
| `status` | Workspace repository matrix status | `python scripts/workshop.py status` |

### Vision Commands

```bash
# Smart media inspection (auto-detects type)
python scripts/workshop.py see "<file_or_dir>" [--prompt "<question>"]

# Image inspection
python scripts/workshop.py vision inspect "<image_path>"

# Video storyboarding
python scripts/workshop.py vision storyboard "<video_path>" [--cols 3 --rows 3]

# Extract video frames
python scripts/workshop.py vision frames "<video_path>" --count 8

# OCR from screenshots
python scripts/workshop.py vision ocr "<image_path>"

# Audio transcription
python scripts/workshop.py vision transcribe "<audio_or_video_path>"
```

### Search Commands

```bash
# Search skills
python scripts/workshop.py search "browser automation"

# Search with limit
python scripts/workshop.py search "office" --limit 10

# Search by category
python scripts/workshop.py search "crypto" --category apis
```

---

## 4. Skills Library

### Overview

The Workshop contains **963 agent skills** distributed across multiple sources:

| Source | Count | Description |
|--------|-------|-------------|
| `skills/` | 854 | Primary curated skills library |
| `hyperframes/skills/` | 20 | Motion & video generation |
| `browser-use/skills/` | 6 | Browser automation |
| `ai agents handbook/packs/*/skills/` | ~70 | Specialized pack skills |
| **Total** | **~963** | |

### Skill Categories (Top by Count)

| Prefix | Count | Category |
|--------|-------|----------|
| `google*` | 44 | Google Cloud, Workspace, Ads |
| `convex*` | 33 | Convex platform |
| `gke*` | 29 | Google Kubernetes Engine |
| `lark*` | 28 | Lark/Feishu integration |
| `agent*` | 26 | Agent orchestration & tools |
| `azure*` | 24 | Microsoft Azure |
| `ss*` | 22 | Stream Skateboard (SS) design system |
| `ai*` | 22 | AI/ML tools |
| `remotion*` | 13 | Video generation |
| `youtube*` | 12 | YouTube automation |
| `amazon*` | 12 | Amazon/e-commerce |
| `hugging*` | 10 | Hugging Face |
| `firebase*` | 10 | Firebase |
| `prisma*` | 9 | Prisma ORM |
| `officecli*` | 9 | Office document automation |
| `higgsfield*` | 9 | AI image/video generation |
| `x*` | 8 | X/Twitter |
| `video*` | 8 | Video tools |
| `writing*` | 7 | Content writing |
| `hyperframes*` | 7 | Motion/video |

### Skill Format

Each skill is a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: "When to use this skill..."
source: "https://github.com/owner/repo"
risk: unknown
---
```

### Office Suite Skills (Recently Added)

| Skill | Source | Stars | Purpose |
|-------|--------|-------|---------|
| `officecli` | `iOfficeAI/OfficeCLI` | â­29.6K | Create/analyze/modify .docx, .xlsx, .pptx |
| `aion-ui` | `iOfficeAI/AionUi` | â­32.5K | AI agent cowork desktop app |
| `harness-anything` | `yb2460/harness-anything` | â­1.6K | WPS/MS Office/Zotero/Illustrator automation |
| `officekit` | `dream-zjk/officekit` | â­110 | Python Office library with MCP server |
| `mineru-skill` | `Nebutra/MinerU-Skill` | â­108 | PDF/Office â†’ Markdown parser |
| `pretty-mermaid-skills` | `imxv/Pretty-mermaid-skills` | â­1.2K | Mermaid diagram rendering |
| `googleworkspace-cli` | `googleworkspace/cli` | â­30.7K | Google Workspace CLI |
| `larksuite-cli` | `larksuite/cli` | â­16.9K | Lark/Feishu CLI |
| `office2pdf` | `developer0hye/office2pdf` | â­108 | DOCX/XLSX/PPTX â†’ PDF converter |
| `deckprobe` | `deckflow/deckprobe` | â­92 | Document metadata probe |

---

## 5. Scripts & Tooling

### Core Scripts

| Script | Purpose |
|--------|---------|
| `workshop.py` | Master CLI entrypoint (all commands) |
| `workshop_search.py` | Skills/APIs search engine |
| `workshop_vision.py` | Multimodal vision inspection engine |
| `workshop_doctor.py` | Health & diagnostics checker |
| `live_browser_hub.py` | Browser automation dashboard server |
| `run_browser_agent.py` | Autonomous browser task runner |
| `mcp_launcher.py` | MCP server launcher/manager |
| `notion_sync.py` | Notion synchronization utility |
| `configure_context_and_combos.py` | Context configuration |
| `fix_all_workshop_issues.py` | Automated workshop repair |
| `fix_claude_omniroute.py` | Claude omniroute fixer |
| `generate_office_layout.py` | Office layout generator |
| `inspect_combos.py` | Skill combo inspector |
| `optimize_omniroute.py` | Omniroute optimizer |

### MCP Configs

Located in `scripts/mcp_configs/` â€” configuration files for all MCP servers.

---

## 6. AI Agents Handbook

### Structure

```
ai agents handbook/
â”œâ”€â”€ README.md
â”œâ”€â”€ AI-AGENT-MASTER-PROMPT.md
â”œâ”€â”€ ai-agent-suite/
â”œâ”€â”€ references/
â””â”€â”€ packs/
    â”œâ”€â”€ garden-skills/      # Garden web components
    â”œâ”€â”€ ponytail/           # Architecture debt auditing
    â”œâ”€â”€ styleseed/          # UI design systems
    â”œâ”€â”€ baoyu-design/       # Visual illustration
    â”œâ”€â”€ huashu-design/      # Aesthetics & layout
    â”œâ”€â”€ karpathy/           # Deep learning
    â””â”€â”€ ecc/
```

### Packs

| Pack | Purpose |
|------|---------|
| `garden-skills` | Web component design system |
| `ponytail` | Architecture debt auditor |
| `styleseed` | UI design system generator |
| `baoyu-design` | Visual illustration & design |
| `huashu-design` | Aesthetics & layout patterns |
| `karpathy` | Deep learning & training workflows |
| `ecc` | Edge computing & communication |

---

## 7. MCP Servers

### Built-in MCP Servers

| Server | Category | Launch |
|--------|----------|--------|
| `playwright` | Browser Automation | `npx -y @playwright/mcp` |
| `puppeteer` | Headless Scraping & PDF | `npx -y @modelcontextprotocol/server-puppeteer` |
| `chrome-devtools` | Runtime & Network Profiling | `npx -y chrome-devtools-mcp@latest` |
| `memory` | Persistent Graph Memory | `npx -y @modelcontextprotocol/server-memory` |
| `sequential-thinking` | Multi-Branch Reasoning | `npx -y @modelcontextprotocol/server-sequential-thinking` |
| `fetch` | HTML/Web Fetching | `npx -y @modelcontextprotocol/server-fetch` |
| `github` | GitHub PRs, Repos & Issues | `npx -y @modelcontextprotocol/server-github` |
| `git` | Local Git Repository Tool | `npx -y @modelcontextprotocol/server-git` |
| `filesystem` | Direct Workspace Access | `npx -y @modelcontextprotocol/server-filesystem .` |
| `camofox-browser` | Stealth Anti-Detect Browser | `node camofox-browser/server.js` (Port 9377) |
| `sqlite` | SQLite Database | `npx -y @modelcontextprotocol/server-sqlite` |
| `postgres` | Production PostgreSQL | `npx -y @modelcontextprotocol/server-postgres` |
| `docker` | Docker Container Management | `npx -y @modelcontextprotocol/server-docker` |
| `firebase` | Firebase Cloud & Data Connect | `npx -y firebase-tools@latest mcp` |
| `terraform` | Infrastructure as Code | `npx -y mcp-terraform` |
| `brave-search` | Real-Time Web Search | `npx -y @modelcontextprotocol/server-brave-search` |
| `time` | Temporal & Timezone Tools | `npx -y @modelcontextprotocol/server-time` |
| `sentry` | Error & Crash Triage | `npx -y @modelcontextprotocol/server-sentry` |
| `linear` | Issue & Project Management | `npx -y @modelcontextprotocol/server-linear` |
| `exa-search` | Neural Search Engine | `npx -y exa-mcp-server` |
| `notion` | Knowledge Base | `npx -y @notionhq/notion-mcp-server` |

---

## 8. Design Arsenal

### Location

`ui-ux-arsenal/`

### Contents

| File | Purpose |
|------|---------|
| `DESIGN_SYSTEM_MASTER.md` | Master design architecture & guidelines |
| `tokens/design_tokens.json` | Machine-readable design tokens |

### Design Tokens Schema

```json
{
  "$schema": "https://design-tokens.org/schema.json",
  "name": "Workshop Design System",
  "version": "1.0.0",
  "colors": { ... },
  "typography": { ... },
  "spacing": { ... },
  "radii": { ... },
  "shadows": { ... },
  "animation": { ... }
}
```

### Design Archetypes

1. **Clean Modern SaaS** â€” Linear/Raycast style, deep neutrals, neon accents
2. **Dark Glassmorphism** â€” Backdrop blur, radial glows, multi-layer shadows
3. **Industrial/Neu-Brutalism** â€” Sharp borders, hard shadows, high saturation
4. **Spring Motion Physics** â€” Bouncy, elastic animations

### Grid System

All layouts use the **4pt/8pt grid**:

| Token | Pixels | Tailwind | Usage |
|-------|--------|----------|-------|
| `space-1` | 4px | `p-1` | Badge padding |
| `space-2` | 8px | `p-2` | Icon button |
| `space-3` | 12px | `p-3` | Compact card |
| `space-4` | 16px | `p-4` | Standard padding |
| `space-6` | 24px | `p-6` | Section padding |
| `space-8` | 32px | `p-8` | Modal padding |
| `space-12` | 48px | `p-12` | Hero spacing |

---

## 9. Reference Repositories

### public-apis/

Curated index of **1,500+ public REST APIs** across 50+ categories.

```bash
# Search APIs
python scripts/workshop.py search "crypto" --category apis
```

### free-for-dev/

Curated list of **free developer tiers** for SaaS, PaaS, and IaaS products.

### awesome-selfhosted/

Directory of **self-hostable open-source software** alternatives to commercial products.

### awesome-mcp-servers/

Curated list of **MCP servers** for AI agents.

---

## 10. Prompts Library

### Location

`prompts/library/`

### Available Prompts

| File | Purpose |
|------|---------|
| `00-system-prompt-framework.md` | System prompt architecture |
| `01-code-review-prompt.md` | Code review workflow |
| `02-architecture-planning-prompt.md` | Architecture design planning |
| `03-prompt-engineering-guide.md` | Prompt engineering best practices |
| `README.md` | Prompt library index |

---

## 11. Operating Standards

### Core Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Universal agent standards & 5-stage protocol |
| `CLAUDE.md` | Claude Code specific guidelines |
| `WORKSHOP.md` | Centralized startup & arsenal activation |
| `WORKSHOP_ARSENAL.md` | Hermes-focused arsenal reference |
| `HERMES_ARSENAL.md` | Quick Hermes commands |

### 5-Stage Problem Solving Protocol

```
[1. RECON & SKILL ACTIVATION]
       â”‚  Scan 820+ skills via 'python scripts/workshop.py search'
       â–¼
[2. ARCHITECTURAL PLANNING]
       â”‚  Design schemas, data contracts, component trees
       â–¼
[3. CLEAN IMPLEMENTATION]
       â”‚  Implement modular, type-safe, complete code
       â–¼
[4. REVIEW & SECURITY AUDIT]
       â”‚  Audit performance, edge cases, vulnerabilities
       â–¼
[5. DETERMINISTIC VERIFICATION]
       â”‚  Verify with tests, CLI commands, or browser tests
```

### Anti-Dumbass Rules

1. **Zero Sycophancy & Zero Boilerplate** â€” No filler phrases
2. **Never Cut Corners** â€” No `// TODO` or incomplete code
3. **Evidence-Based Recon** â€” Inspect before modifying
4. **Autonomous Root-Cause Resolution** â€” Fix the source, not the symptom
5. **Deterministic Verification** â€” Every deliverable must be verified

---

## 12. Quick Reference Cheat Sheet

### Essential Commands

```bash
# Search for a skill
python scripts/workshop.py search "browser automation"

# Inspect an image or document
python scripts/workshop.py see "report.pdf"

# OCR a screenshot
python scripts/workshop.py vision ocr "screenshot.png"

# Create a video storyboard
python scripts/workshop.py vision storyboard "video.mp4"

# Check workshop health
python scripts/workshop.py doctor

# Launch browser dashboard
python scripts/workshop.py hub --port 7860

# Run browser task
python scripts/workshop.py browser --url "https://example.com" --task "Scrape" --live

# List MCP servers
python scripts/workshop.py mcp list

# Check workspace status
python scripts/workshop.py status
```

### Office CLI Commands

```bash
# OfficeCLI (iOfficeAI)
officecli create deck.pptx
officecli add deck.pptx / --type slide --prop title="Q4 Report"
officecli view deck.pptx outline
officecli watch deck.pptx          # Live preview at :26315

# Office2PDF
office2pdf input.docx output.pdf
office2pdf --pdf-a report.docx archival.pdf

# MinerU (PDF â†’ Markdown)
python scripts/mineru.py document.pdf --stdout
python scripts/mineru.py docs/ --obsidian /path/to/vault

# DeckProbe (Document metadata)
deckprobe --pretty -t slide_count deck.pptx
deckprobe --pretty -t page_count report.pdf

# Pretty Mermaid
pretty-mermaid 'flowchart TD\n  A --> B' --theme tokyo-night --output diagram.svg
```

### Google Workspace CLI

```bash
# Auth
gws auth login

# Drive
gws drive files list --query "trashed=false"
gws drive files upload --name "report.pdf" --path ./report.pdf

# Gmail
gws gmail messages list --labelId INBOX --max-results 10
gws gmail messages send --to user@example.com --subject "Hello" --body "Body"

# Calendar
gws calendar events create --summary "Meeting" --start "2026-09-01T10:00:00" --end "2026-09-01T11:00:00"

# Sheets
gws sheets values get --spreadsheet-id <id> --range "Sheet1!A1:D10"
```

### Lark/Feishu CLI

```bash
# Auth
lark auth login

# Docs
lark docs create --title "Report"
lark docs get --doc-token <token>

# Sheets
lark sheets create --title "Q3 Data"
lark sheets values update --spreadsheet-id <id> --range "Sheet1!A1" --values '[["Name","Score"]]'

# Messenger
lark messenger send --to <user_id> --text "Hello"
```

---

## Appendix: Skill Count by Top-Level Category

| Category | Approx. Skills |
|----------|---------------|
| Google Cloud / Workspace | 44+ |
| Convex | 33+ |
| GKE (Kubernetes) | 29+ |
| Lark/Feishu | 28+ |
| Agent Tools | 26+ |
| Azure | 24+ |
| SS Design System | 22+ |
| AI/ML | 22+ |
| Video/Motion | 20+ |
| YouTube | 12+ |
| Amazon/E-commerce | 12+ |
| Hugging Face | 10+ |
| Firebase | 10+ |
| Prisma | 9+ |
| Office Suite | 9+ |
| Higgsfield | 9+ |
| X/Twitter | 8+ |
| Writing/Content | 7+ |
| Hyperframes | 7+ |
| **Total** | **~963** |

