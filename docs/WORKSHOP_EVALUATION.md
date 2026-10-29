# Workshop Arsenal Evaluation vs External Landscape
**Source**: `D:\Workshop` — 1,005 skills, 18 MCP servers  
**Date**: Sun Oct 18 2026  
**Purpose**: Gap analysis against trending agent skills, MCP servers, and tooling

---

## 1. Workshop Arsenal Inventory (from `D:\Workshop/opencode.json`)

### MCP Servers configured (18)
| Server | Type | Purpose |
|--------|------|---------|
| context7 | remote | Framework/docs lookup |
| ai-dev-jobs | remote | AI/ML job board |
| sentry | remote | Error monitoring |
| linear | remote | Project management |
| omniroute | remote | Local model router (localhost:20128) |
| playwright | local | Browser automation |
| puppeteer | local | Headless scraping/PDF |
| chrome-devtools | local | Runtime & network profiling |
| memory | local | Persistent graph memory |
| sequential-thinking | local | Multi-branch reasoning |
| fetch | local | HTML/web fetching |
| github | local | PRs, repos, issues |
| git | local | Local git operations |
| sqlite | local | SQLite DB |
| postgres | local | PostgreSQL |
| docker | local | Container management |
| firebase | local | Firebase tools |
| terraform | local | Terraform IaC |
| filesystem | local | Direct workspace access |
| camofox | local | Stealth anti-detect browser |
| workshop | local | Master MCP (skill_search, memory_recall, verify, critique, doctor, vision, antislop, graphify) |

### Skills catalog
- 1,005 skills discovered across 5 roots
- 949 in `skills/`, 2 in `hyperframes/skills`, 6 in `browser-use/skills`, 48 in agent-pack universal skills
- 36 Tier-0 core skills mounted in `.workshop_state/skills-core`

---

## 2. External Landscape (research findings)

### Agent Skills standards & marketplaces
- **Anthropic Agent Skills** (agentskills.io, Dec 2025): SKILL.md format, progressive disclosure, token-efficient. Skills ship alongside MCP servers.
- **skills.sh / Vercel**: 600,000 OSS skills, GA June 2026, `npx skills add` CLI, cross-host (Claude Code, Codex, Cursor, OpenClaw).
- **agentskills.io**: ~40 compatible products including OpenAI Codex, GitHub Copilot, Cursor, Gemini CLI, VS Code, Goose, OpenCode.
- **MCP marketplaces**: Smithery, MCP Marketplace, LobeHub, SkillsMP, Glama.
- **Key repos**: anthropics/skills (172K stars), addyosmani/agent-skills, DietrichGebert/ponytail, mattpocock/skills (277K stars).

### Key MCP servers trending (Oct 2026)
- GitHub MCP, Sequential Thinking, Context7, Supabase, Playwright, Filesystem, Postgres
- REA (Reverse Engineer Anything) — MCP server for binary/app decompilation
- code-review-graph — local-first code intelligence graph via MCP
- Various security-scanning MCPs (credential leak, prompt injection detection)

### OpenAI Agents SDK (April 2026)
- Tool use via MCP, progressive disclosure via skills, AGENTS.md, shell/exec, apply_patch
- Sandboxed code execution, long-horizon tasks

### Key pattern emerging
MCP = external connectivity (tools, data, auth). Agent Skills = token-efficient domain knowledge. They are **complementary**, not competing. Best practice: ship a Skill alongside each MCP server.

---

## 3. Gap Analysis: What's Missing vs Trending

### Critical gaps (high priority)

| Gap | External reference | Impact |
|-----|-------------------|--------|
| **Reverse engineering / binary analysis MCP** | REA (mattpocock/skills), code-review-graph | No ability to decompile/analyze binaries, JS/Electron, .NET assemblies |
| **Web search / neural search MCP** | Exa, Brave Search, Perplexity | Only context7 (docs) — no general web research MCP |
| **Security scanning MCP** | Glama top-20 lists credential-leak/prompt-injection scanners | No dedicated security MCP |
| **Notion MCP** | Notion MCP server (notionhq/notion-mcp-server) | Only listed as option, not configured |
| **Linear MCP** | Already configured ✅ |
| **Slack MCP** | Common in Reddit MCP lists | Not configured |
| **Discord MCP** | Common | Not configured |
| **Resend MCP server (custom)** | We built `mcp-resend-email` skill but no server deployed | Skill exists, server not running |

### Skill gaps (medium priority)

| Gap | External reference |
|-----|-------------------|
| **MCP server authoring skill** | `mcp-builder` exists ✅, but no `mcp-server-dev` reference set |
| **Code execution sandbox** | OpenAI Agents SDK shell tool — not present |
| **Vector DB / pgvector skill** | RAG pipeline builder covers theory, no dedicated pgvector skill |
| **Home Assistant / IoT skill** | Reddit claude-skills collection includes it |
| **Financial / accounting skill** | Not present |
| **Legal / compliance skill** | Not present |
| **Biomedical / life sciences skill** | biopython exists ✅ |

### Already covered well
- Multi-agent frameworks: LangGraph, CrewAI ✅ (added)
- Local LLM: Ollama ✅ (added)
- TTS/Audio: ElevenLabs, Kokoro, Edge, Azure, Piper ✅ (added)
- Image gen: Flux, Nano Banana, GPT Image 2 ✅ (added)
- Video perception: watch-skill, video-vision-mcp ✅ (added)
- RAG pipeline + evaluation ✅ (added)
- Obsidian vault automation ✅ (added)
- E-commerce scraping (Amazon, eBay, Etsy, Taobao, Walmart) ✅ extensive
- Social media scraping (X, TikTok, Instagram, YouTube, Threads, Xiaohongshu) ✅ extensive
- Cloud: Azure, GCP, AWS ✅ extensive
- Design/UI: StyleSeed, UI/UX Pro Max, shadcn ✅ extensive

---

## 4. Recommendations (ranked)

### Tier 1 — Deploy now (highest impact)
1. **Deploy `mcp-resend-email` server** — skill written, server not running. `pip install mcp resend python-dotenv`, configure RESEND_API_KEY.
2. **Add Exa/Brave web search MCP** — only context7 covers docs; no general web research MCP configured.
3. **Configure Notion MCP** — `npx @notionhq/notion-mcp-server` (NOTION_TOKEN needed). Workshop has `notion-second-brain` skill but no server.

### Tier 2 — Author next (medium impact)
4. **MCP server authoring reference set** — `mcp-server-dev` composing skills (remote Streamable HTTP default, Cloudflare Workers scaffold, Express/FastMCP).
5. **pgvector / vector DB skill** — complement `rag-pipeline-builder`.
6. **Security scanning MCP** — credential leak, prompt injection, tool description poisoning (per Glama top-20).

### Tier 3 — Monitor (low impact)
7. REA reverse-engineering MCP — niche but powerful for binary analysis.
8. Home Assistant / IoT skill.
9. Code execution sandbox integration.

---

## 5. Strategic position

Workshop at `D:\Workshop` is **ahead of the curve** in:
- Local-first, zero-cloud media perception (watch-skill, video-vision-mcp — no API key/GPU required)
- Multi-agent frameworks (LangGraph + CrewAI — both covered)
- E-commerce and social-media scraping (one of the most extensive skill sets)
- Obsidian vault integration as agent memory (`obsidian-vault-automation` + MCP memory)

Workshop is **behind** in:
- General web search MCP (context7 is docs-only)
- Deployed MCP servers for email (skill written, server not running)
- Notion/Slack/Discord MCP servers
- Code execution sandbox
- Vector DB dedicated skill

Next step: pick a Tier 1 item to deploy.
