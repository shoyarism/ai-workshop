# Workshop Master Arsenal â€” Unified Centralized Reference

**Workspace Root**: `E:/AI/Workshop`  
**Universal Master CLI**: `python scripts/workshop.py`  
**Live Browser Hub**: `http://localhost:7860`  
**Stealth Browser**: `camofox` (Port `9377`)

---

## 1. Quick Master Commands

```bash
# ðŸ‘ï¸ Visual & Multimodal Media Inspection (Images, Videos, Audio, Dirs)
python scripts/workshop.py see "<file_or_dir>" [--prompt "<question>"]
python scripts/workshop.py vision inspect "<image_path>"
python scripts/workshop.py vision storyboard "<video_path>" [--cols 3 --rows 3]
python scripts/workshop.py vision frames "<video_path>" --count 8
python scripts/workshop.py vision ocr "<image_path>"
python scripts/workshop.py vision transcribe "<audio_or_video_path>"

# ðŸŽ¯ Search across 820+ skills, MCPs, 1,500+ Public APIs, and cloud tiers
python scripts/workshop.py search "<keyword>"
python scripts/workshop.py search "browser" --limit 10
python scripts/workshop.py search "crypto" --category apis

# ðŸ©º Environment health check
python scripts/workshop.py doctor

# ðŸŒ Launch Live Browser Hub (Web Dashboard at http://localhost:7860)
python scripts/workshop.py hub --port 7860

# ðŸ¤– Execute browser task with real-time live watching
python scripts/workshop.py browser --url "https://news.ycombinator.com" --task "Inspect top stories" --live

# ðŸ› ï¸ MCP server inspection and management
python scripts/workshop.py mcp list
python scripts/workshop.py mcp test playwright
python scripts/workshop.py mcp test memory

# ðŸ“Š Check full repository matrix status
python scripts/workshop.py status
```

---

## 2. Integrated Skills Catalog (827+ Skills Across 12 Paths)

1. `skills/` *(816+ curated domain skills including `hospital-live-api-connector`, `heroui-v3-design-system`, `hospital-color-coding`, `multimodal-vision-and-media-inspector`, `live-browser-agent`, `modern-ui-ux-architect`, `mcp-ecosystem-master`, `fullstack-system-builder`, `cli-anything`, `deep-tutor`, `stop-slop`, `witr`, `heretic`, `ai-toolkit`, `ecosystem`, `notion-second-brain`, `pinchtab`, `hackingtool`, `cua`, `ecc`)*
2. `hyperframes/skills/` *(20 motion & video generation skills)*
3. `browser-use/skills/` *(6 browser automation skills)*
4. `ai agents handbook/packs/ponytail/skills/` *(Architecture debt auditor skills)*
5. `ai agents handbook/packs/styleseed/skills/` *(UI design system skills)*
6. `ai agents handbook/packs/garden-skills/skills/` *(Garden web component skills)*
7. `ai agents handbook/packs/baoyu-design/skills/` *(Visual illustration & design skills)*
8. `ai agents handbook/packs/huashu-design/skills/` *(Aesthetics & layout skills)*
9. `ai agents handbook/packs/karpathy/skills/` *(Deep learning & training skills)*
10. `ui-ux-arsenal/` *(Master design system, Tailwind v4 design tokens, UI recipes)*
11. Antigravity & science plugins (`~/.gemini/config/plugins/science/skills`)
12. Claude and Hermes global skills (`~/.agents/skills`, `~/.claude/skills`)

---

## 3. Connected Model Context Protocol (MCP) Servers

| Server | Category | Launch Command |
| :--- | :--- | :--- |
| **`playwright`** | Browser Automation | `npx -y @playwright/mcp` |
| **`puppeteer`** | Headless Scraping & PDF | `npx -y @modelcontextprotocol/server-puppeteer` |
| **`chrome-devtools`** | Runtime & Network Profiling | `npx -y chrome-devtools-mcp@latest` |
| **`memory`** | Persistent Graph Memory | `npx -y @modelcontextprotocol/server-memory` |
| **`sequential-thinking`** | Multi-Branch Reasoning | `npx -y @modelcontextprotocol/server-sequential-thinking` |
| **`fetch`** | HTML/Web Fetching | `npx -y @modelcontextprotocol/server-fetch` |
| **`github`** | GitHub PRs, Repos & Issues | `npx -y @modelcontextprotocol/server-github` |
| **`git`** | Local Git Repository Tool | `npx -y @modelcontextprotocol/server-git` |
| **`filesystem`** | Direct Workspace Filesystem | `npx -y @modelcontextprotocol/server-filesystem .` |
| **`camofox-browser`** | Stealth Anti-Detect Engine | `node camofox-browser/server.js` |
| **`sqlite`** | SQLite Relational DB | `npx -y @modelcontextprotocol/server-sqlite` |
| **`postgres`** | Production PostgreSQL DB | `npx -y @modelcontextprotocol/server-postgres` |
| **`docker`** | Docker Container Mgmt | `npx -y @modelcontextprotocol/server-docker` |
| **`firebase`** | Firebase Cloud & Data Connect | `npx -y firebase-tools@latest mcp` |
| **`terraform`** | Terraform Infrastructure-as-Code | `npx -y mcp-terraform` |
| **`brave-search`** | Real-Time Web Search Engine | `npx -y @modelcontextprotocol/server-brave-search` |
| **`time`** | Temporal & Timezone Tools | `npx -y @modelcontextprotocol/server-time` |
| **`sentry`** | Sentry Error & Crash Triage | `npx -y @modelcontextprotocol/server-sentry` |
| **`linear`** | Linear Issue & Project Mgmt | `npx -y @modelcontextprotocol/server-linear` |
| **`exa-search`** | Neural Search Engine | `npx -y exa-mcp-server` |
| **`notion`** | Second Brain / Knowledge Base | `npx -y @notionhq/notion-mcp-server` (set NOTION_TOKEN) |
| **`notion`** | Second Brain / Knowledge Base | `npx -y @modelcontextprotocol/server-notion` (configure) |

---

## 4. UI/UX Design System Arsenal

- **Master Blueprint**: [`ui-ux-arsenal/DESIGN_SYSTEM_MASTER.md`](file:///E:/AI/Workshop/ui-ux-arsenal/DESIGN_SYSTEM_MASTER.md)
- **Master Tokens**: [`ui-ux-arsenal/tokens/design_tokens.json`](file:///E:/AI/Workshop/ui-ux-arsenal/tokens/design_tokens.json)
- **Archetypes**: Modern Clean SaaS, Dark Glassmorphism, Industrial Brutalism, Spring Motion Physics.



