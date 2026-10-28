# Workshop Master Arsenal — Unified Centralized Reference

**Universal Master CLI**: `uv run python scripts/workshop.py`  
**Master Catalog Index**: [`INDEX.md`](file:///INDEX.md) & [`CATALOG.json`](file:///CATALOG.json)  
**Live Browser Hub**: `http://localhost:7860`  
**Stealth Browser**: `camofox` (Port `9377`)

---

## 1. Quick Master Commands

```bash
# 🔍 Search across 865+ skills, 30 Subsystems, MCPs, 1,500+ Public APIs, and cloud tiers
python scripts/workshop.py search "<keyword>"
python scripts/workshop.py search "browser" --limit 10
python scripts/workshop.py search "crypto" --category apis
python scripts/workshop.py search "pentest" --category repos

# 📋 Subsystem Briefing & Architecture Context
python scripts/workshop.py info <subsystem_name>  # e.g., python scripts/workshop.py info scrapling

# 🔄 Regenerate Machine Catalog & Master Index
python scripts/workshop.py index

# 🩺 Environment health check
python scripts/workshop.py doctor

# 👁️ Visual & Multimodal Media Inspection (Images, Videos, Audio, Dirs)
python scripts/workshop.py see "<file_or_dir>" [--prompt "<question>"]
python scripts/workshop.py vision inspect "<image_path>"
python scripts/workshop.py vision storyboard "<video_path>" [--cols 3 --rows 3]
python scripts/workshop.py vision frames "<video_path>" --count 8
python scripts/workshop.py vision ocr "<image_path>"
python scripts/workshop.py vision transcribe "<audio_or_video_path>"

# 🌐 Launch Live Browser Hub (Web Dashboard at http://localhost:7860)
python scripts/workshop.py hub --port 7860

# 🤖 Execute browser task with real-time live watching
python scripts/workshop.py browser --url "https://news.ycombinator.com" --task "Inspect top stories" --live

# 🛠️ MCP server inspection and management
python scripts/workshop.py mcp list
python scripts/workshop.py mcp test playwright
python scripts/workshop.py mcp test memory
python scripts/workshop.py mcp test mcp-inspector

# 📊 Check full repository matrix status (30 Subsystems)
python scripts/workshop.py status

# 🛡️ Digital Forensics & Data Recovery (TSK 4.15, TestDisk 7.3, Dissect, Volatility 3)
python scripts/workshop.py forensic status
python scripts/workshop.py forensic hash "<evidence_file>"
python scripts/workshop.py forensic partitions "<disk_image>"
python scripts/workshop.py forensic list-deleted "<disk_image>" --offset 2048
python scripts/workshop.py forensic recover "<disk_image>" <inode> "<output>"
python scripts/workshop.py forensic carve "<disk_image>" "<output_dir>"

# 🌐 OSINT & Auspex Intelligence Suite (75+ Modules, Identity, Telecom, Recon)
python scripts/workshop.py osint status
python scripts/workshop.py osint username "<target>"
python scripts/workshop.py osint email "<email>"
python scripts/workshop.py osint phone "+14155552671"
python scripts/workshop.py osint domain "<domain>"
python scripts/workshop.py osint ip "<ip>"
python scripts/workshop.py osint metadata "<file>"
```

---

## 2. Integrated Skills Catalog (865+ Skills Across 14 Paths)

1. `skills/` *(865+ curated domain skills including `scrapling-fast-scraper`, `strix-security-pentester`, `graphify-codebase-graph`, `open-seo-audit`, `open-notebook-ai`, `book-to-skill-converter`, `awesome-llm-apps-catalog`, `open-design-tokens`, `langflow-pipeline-builder`, `openhands-agent-developer`, `litellm-proxy-gateway`, `stagehand-browser-automator`, `mcp-inspector-debugger`, `adhd-focus-assistant`, `hospital-live-api-connector`, `heroui-v3-design-system`, `modern-ui-ux-architect`, `mcp-ecosystem-master`, `fullstack-system-builder`)*
2. `hyperframes/skills/` *(20 motion & video generation skills)*
3. `browser-use/skills/` *(6 browser automation skills)*
4. `ai agents handbook/packs/ponytail/skills/` *(Architecture debt auditor skills)*
5. `ai agents handbook/packs/styleseed/skills/` *(UI design system skills)*
6. `ai agents handbook/packs/garden-skills/skills/` *(Garden web component skills)*
7. `ai agents handbook/packs/baoyu-design/skills/` *(Visual illustration & design skills)*
8. `ai agents handbook/packs/karpathy/skills/` *(Deep learning & training skills)*
9. `ui-ux-arsenal/` *(Master design system, Tailwind v4 design tokens, UI recipes)*
10. `open-design/` *(OpenDesign token specifications & component blueprints)*
11. `book-to-skill/` *(Automated book and documentation skill distillation compiler)*

---

## 3. Connected Model Context Protocol (MCP) Servers

| Server | Category | Launch Command |
| :--- | :--- | :--- |
| **`playwright`** | Browser Automation | `npx -y @playwright/mcp` |
| **`puppeteer`** | Headless Scraping & PDF | `npx -y @modelcontextprotocol/server-puppeteer` |
| **`camofox-browser`** | Stealth Anti-Detect Engine | `node camofox-browser/server.js` |
| **`stagehand`** | Natural Language AI Browser | `npx -y @browserbasehq/stagehand` |
| **`mcp-inspector`** | MCP Debugging Test Harness | `npx -y @modelcontextprotocol/inspector` |
| **`chrome-devtools`** | Runtime & Network Profiling | `npx -y chrome-devtools-mcp@latest` |
| **`memory`** | Persistent Graph Memory | `npx -y @modelcontextprotocol/server-memory` |
| **`sequential-thinking`** | Multi-Branch Reasoning | `npx -y @modelcontextprotocol/server-sequential-thinking` |
| **`fetch`** | HTML/Web Fetching | `npx -y @modelcontextprotocol/server-fetch` |
| **`github`** | GitHub PRs, Repos & Issues | `npx -y @modelcontextprotocol/server-github` |
| **`git`** | Local Git Repository Tool | `npx -y @modelcontextprotocol/server-git` |
| **`filesystem`** | Direct Workspace Filesystem | `npx -y @modelcontextprotocol/server-filesystem .` |
| **`sqlite`** | SQLite Relational DB | `npx -y @modelcontextprotocol/server-sqlite` |
| **`postgres`** | Production PostgreSQL DB | `npx -y @modelcontextprotocol/server-postgres` |
| **`supabase`** | Supabase Cloud Database | `npx -y @supabase/mcp` |
| **`docker`** | Docker Container Mgmt | `npx -y @modelcontextprotocol/server-docker` |
| **`firebase`** | Firebase Cloud & Data Connect | `npx -y firebase-tools@latest mcp` |
| **`terraform`** | Terraform Infrastructure-as-Code | `npx -y mcp-terraform` |
| **`brave-search`** | Real-Time Web Search Engine | `npx -y @modelcontextprotocol/server-brave-search` |
| **`time`** | Temporal & Timezone Tools | `npx -y @modelcontextprotocol/server-time` |
| **`sentry`** | Sentry Error & Crash Triage | `npx -y @modelcontextprotocol/server-sentry` |
| **`linear`** | Linear Issue & Project Mgmt | `npx -y @modelcontextprotocol/server-linear` |
| **`exa-search`** | Neural Search Engine | `npx -y exa-mcp-server` |
| **`notion`** | Second Brain / Knowledge Base | `npx -y @notionhq/notion-mcp-server` |

---

## 4. UI/UX Design System Arsenal

- **Master Blueprint**: [`ui-ux-arsenal/DESIGN_SYSTEM_MASTER.md`](file:///ui-ux-arsenal/DESIGN_SYSTEM_MASTER.md)
- **Master Tokens**: [`ui-ux-arsenal/tokens/design_tokens.json`](file:///ui-ux-arsenal/tokens/design_tokens.json)
- **OpenDesign Toolkit**: [`open-design/`](file:///open-design/)
- **Archetypes**: Modern Clean SaaS, Dark Glassmorphism, Industrial Brutalism, Spring Motion Physics.
