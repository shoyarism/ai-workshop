# Workshop Documentation

> **Workspace Root:** `.`  or drive E
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
.\
│
├── AGENTS.md                    # Universal agent standards & protocols
├── CLAUDE.md                    # Claude Code specific guidelines
├── WORKSHOP.md                  # Centralized startup & arsenal activation
├── WORKSHOP_ARSENAL.md          # Unified arsenal reference (Hermes-focused)
├── HERMES_ARSENAL.md            # Hermes-specific arsenal quick reference
├── OPENCODE.md                  # OpenCode agent guidelines
├── OPENCODE_ARSENAL.md
├── OPENCODE_GUIDE.md
├── kilo.jsonc                   # Kilo Code configuration
├── opencode.json                # OpenCode configuration
│
├── skills/                      # Primary skills library (854+ skills)
│   ├── _archive/               # Archived/deprecated skills (3)
│   ├── aion-ui/                # AI agent cowork app (iOfficeAI/AionUi)
│   ├── officecli/              # Office document automation CLI
│   ├── officecli-docx/         # Word document specialist
│   ├── officecli-xlsx/         # Excel spreadsheet specialist
│   ├── officecli-pptx/         # PowerPoint specialist
│   ├── officecli-pitch-deck/   # Fundraising deck specialist
│   ├── officecli-financial-model/
│   ├── officecli-academic-paper/
│   ├── officecli-data-dashboard/
│   ├── officecli-word-form/
│   ├── googleworkspace-cli/    # Google Workspace CLI (gws)
│   ├── larksuite-cli/          # Lark/Feishu CLI
│   ├── mineru-skill/           # PDF/Office → Markdown parser
│   ├── officekit/              # Python Office automation library
│   ├── office2pdf/             # DOCX/XLSX/PPTX → PDF converter
│   ├── deckprobe/              # Document metadata probe
│   ├── harness-anything/       # WPS/MS Office/Zotero/Illustrator automation
│   ├── pretty-mermaid-skills/  # Mermaid diagram rendering
│   ├── ...                     # 830+ more skills
│
├── scripts/                     # Workshop tooling
│   ├── workshop.py             # Master CLI entrypoint
│   ├── workshop_search.py      # Skills/APIs search engine
│   ├── workshop_vision.py      # Multimodal vision inspector
│   ├── workshop_doctor.py      # Health & diagnostics
│   ├── live_browser_hub.py     # Browser automation dashboard (:7860)
│   ├── run_browser_agent.py    # Autonomous browser task runner
│   ├── mcp_launcher.py         # MCP server launcher
│   ├── mcp_configs/            # MCP configuration files
│   ├── configure_context_and_combos.py
│   ├── fix_all_workshop_issues.py
│   ├── fix_claude_omniroute.py
│   ├── generate_office_layout.py
│   ├── inspect_combos.py
│   ├── notion_sync.py
│   ├── optimize_omniroute.py
│
├── camofox-browser/            # Stealth anti-detect browser (Port 9377)
│   ├── server.js               # REST API server
│   ├── camofox.config.json     # Browser configuration
│   ├── mcp/                    # MCP server integration
│   ├── docs/                   # Documentation
│   └── ...
│
├── browser-use/                 # Vision-based web automation framework
│   ├── README.md
│   ├── pyproject.toml
│   ├── skills/                 # 6 browser automation skills
│   └── ...
│
├── hyperframes/                 # Motion & generative video toolkit
│   ├── skills/                 # 20 motion/video generation skills
│   ├── CLAUDE.md
│   └── ...
│
├── ui-ux-arsenal/               # UI/UX design system
│   ├── DESIGN_SYSTEM_MASTER.md # Design architecture & guidelines
│   └── tokens/
│       └── design_tokens.json  # Master design tokens (colors, typography, spacing)
│
├── prompts/                     # Prompt library
│   ├── README.md
│   ├── library/                # 5 operational prompts
│   │   ├── 00-system-prompt-framework.md
│   │   ├── 01-code-review-prompt.md
│   │   ├── 02-architecture-planning-prompt.md
│   │   └── 03-prompt-engineering-guide.md
│   └── _archive/               # Archived prompts
│       └── agents-run-artifacts/
│
├── ai agents handbook/          # AI agent playbook & packs
│   ├── README.md
│   ├── AI-AGENT-MASTER-PROMPT.md
│   ├── ai-agent-suite/
│   ├── references/
│   └── packs/
│       ├── garden-skills/      # Garden web component skills
│       ├── ponytail/           # Architecture debt auditor skills
│       ├── styleseed/          # UI design system skills
│       ├── baoyu-design/       # Visual illustration & design
│       ├── huashu-design/      # Aesthetics & layout
│       ├── karpathy/           # Deep learning & training
│       └── ecc/
│
├── public-apis/                 # Public APIs index (1,500+ APIs)
│   ├── README.md
│   ├── CONTRIBUTING.md
│   ├── LICENSE
│   └── scripts/
│
├── free-for-dev/                # Free developer tiers index
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── LICENSE
│
├── awesome-selfhosted/          # Self-hosted software directory
│   ├── README.md
│   ├── CONTRIBUTING.md
│   ├── LICENSE
│   └── non-free.md
│
├── awesome-mcp-servers/         # MCP server directory
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── LICENSE
│
├── mcp-servers-official/        # Official MCP servers
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── LICENSE
│
├── eliza/                       # Eliza framework
│   └── ...
│
├── openclaw/                    # OpenClaw agent platform
│   └── ...
│
├── opencode/                    # OpenCode agent platform
│   └── ...
│
└── open-generative-ai/          # Open generative AI resources
    └── ...
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
| `officecli` | `iOfficeAI/OfficeCLI` | ⭐29.6K | Create/analyze/modify .docx, .xlsx, .pptx |
| `aion-ui` | `iOfficeAI/AionUi` | ⭐32.5K | AI agent cowork desktop app |
| `harness-anything` | `yb2460/harness-anything` | ⭐1.6K | WPS/MS Office/Zotero/Illustrator automation |
| `officekit` | `dream-zjk/officekit` | ⭐110 | Python Office library with MCP server |
| `mineru-skill` | `Nebutra/MinerU-Skill` | ⭐108 | PDF/Office → Markdown parser |
| `pretty-mermaid-skills` | `imxv/Pretty-mermaid-skills` | ⭐1.2K | Mermaid diagram rendering |
| `googleworkspace-cli` | `googleworkspace/cli` | ⭐30.7K | Google Workspace CLI |
| `larksuite-cli` | `larksuite/cli` | ⭐16.9K | Lark/Feishu CLI |
| `office2pdf` | `developer0hye/office2pdf` | ⭐108 | DOCX/XLSX/PPTX → PDF converter |
| `deckprobe` | `deckflow/deckprobe` | ⭐92 | Document metadata probe |

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

Located in `scripts/mcp_configs/` — configuration files for all MCP servers.

---

## 6. AI Agents Handbook

### Structure

```
ai agents handbook/
├── README.md
├── AI-AGENT-MASTER-PROMPT.md
├── ai-agent-suite/
├── references/
└── packs/
    ├── garden-skills/      # Garden web components
    ├── ponytail/           # Architecture debt auditing
    ├── styleseed/          # UI design systems
    ├── baoyu-design/       # Visual illustration
    ├── huashu-design/      # Aesthetics & layout
    ├── karpathy/           # Deep learning
    └── ecc/
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

1. **Clean Modern SaaS** — Linear/Raycast style, deep neutrals, neon accents
2. **Dark Glassmorphism** — Backdrop blur, radial glows, multi-layer shadows
3. **Industrial/Neu-Brutalism** — Sharp borders, hard shadows, high saturation
4. **Spring Motion Physics** — Bouncy, elastic animations

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
       │  Scan 820+ skills via 'python scripts/workshop.py search'
       ▼
[2. ARCHITECTURAL PLANNING]
       │  Design schemas, data contracts, component trees
       ▼
[3. CLEAN IMPLEMENTATION]
       │  Implement modular, type-safe, complete code
       ▼
[4. REVIEW & SECURITY AUDIT]
       │  Audit performance, edge cases, vulnerabilities
       ▼
[5. DETERMINISTIC VERIFICATION]
       │  Verify with tests, CLI commands, or browser tests
```

### Anti-Dumbass Rules

1. **Zero Sycophancy & Zero Boilerplate** — No filler phrases
2. **Never Cut Corners** — No `// TODO` or incomplete code
3. **Evidence-Based Recon** — Inspect before modifying
4. **Autonomous Root-Cause Resolution** — Fix the source, not the symptom
5. **Deterministic Verification** — Every deliverable must be verified

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

# MinerU (PDF → Markdown)
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
