# ⚡ OpenCode Master User Guide — Maximizing Skills, Tools, MCPs & Subagent Swarms

Welcome to your fully supercharged OpenCode environment! This guide details how to leverage all **800+ skills**, **20+ MCP servers**, **7 specialized subagent teams**, **LSP code intelligence**, and **custom slash commands**.

---

## 1. Quick Command Reference

OpenCode supports customized slash commands for instant 1-click execution:

| Slash Command | Role & Workflow | What Happens Behind the Scenes |
|---|---|---|
| `/team <task>` | **Full Multi-Agent Swarm** | Launches the complete workflow: `@researcher` (finds docs) -> `@plan` (architects specs) -> `@build` (writes code) -> `@designer` (styles UI) -> `@reviewer` (audits code) -> `@qa` (runs tests). |
| `/plan <feature>` | **Architectural Blueprint** | Dispatches `@plan` to generate detailed component diagrams, API specs, and implementation steps before coding. |
| `/research <topic>` | **Deep Intelligence & Docs** | Dispatches `@researcher` to query `exa-search`, `context7`, and local skill indices for up-to-date documentation. |
| `/design <component>` | **UI/UX & Aesthetics** | Dispatches `@designer` to build beautiful interfaces using `styleseed`, `react-bits`, `motion` animations, and modern typography. |
| `/review` | **Security & Code Review** | Dispatches `@reviewer` to audit diffs, detect architectural debt using `ponytail`, and check for security vulnerabilities. |
| `/test` | **Automated Testing & QA** | Dispatches `@qa` to write and execute unit tests, end-to-end tests, and browser tests via `playwright` and `puppeteer`. |
| `/skill <query>` | **Skill Search & Load** | Searches the 800+ skill index and pulls in relevant `SKILL.md` instructions for the task. |

---

## 2. The 7 Specialized Agent Roles

You can also target specific subagents directly using `@<agent>`:

```
                  ┌────────────────────────────────────────┐
                  │       @orchestrator (Coordinator)      │
                  │   Model: omniroute/auto-best-reasoning │
                  └───────────────────┬────────────────────┘
                                      │
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
 ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
 │    @plan    │ │ @researcher │ │   @build    │ │  @designer  │ │  @reviewer  │
 │ (Architect) │ │  (Doc Scout)│ │  (Engineer) │ │  (UI / UX)  │ │ (Code Audit)│
 └─────────────┘ └─────────────┘ └──────┬──────┘ └─────────────┘ └─────────────┘
                                        │
                                        ▼
                                 ┌─────────────┐
                                 │     @qa     │
                                 │(Test Runner)│
                                 └─────────────┘
```

1. **`@orchestrator`** (Primary Coordinator): High-level task planning and subagent swarm management.
2. **`@plan`** (Software Architect): System specifications, database schemas, and structured blueprints.
3. **`@build`** (Full-Stack Engineer): Production-ready TypeScript, Python, Go, Rust, or C++ implementation.
4. **`@researcher`** (Intelligence Scout): Queries `exa-search`, `context7`, and 800+ skills library.
5. **`@designer`** (UI/UX Craftsman): Master of layout, typography, animations (`motion`), and design tokens.
6. **`@reviewer`** (Security & Debt Auditor): Code quality, vulnerability audits, and `ponytail` debt analysis.
7. **`@qa`** (Testing & Verification Engineer): End-to-end browser automation (`playwright`/`puppeteer`) and unit tests.

---

## 3. Active MCP Server Capabilities

OpenCode is wired to **20+ active MCP tools**:

- **Web Intelligence**:
  - `exa-search`: Neural semantic search engine for up-to-date documentation and code samples.
  - `context7`: Real-time documentation context for popular libraries and frameworks.
- **Browser Automation & Inspection**:
  - `playwright`: High-fidelity browser testing, clicking, form submission, and visual screenshots.
  - `puppeteer`: Headless scraping and PDF/snapshot generation.
  - `chrome-devtools`: Chrome DevTools protocol inspection for console logs and network profiling.
- **Cognition & Memory**:
  - `sequential-thinking`: Dynamic thought tree reasoning for solving difficult bugs.
  - `memory`: Knowledge graph for storing persistent project facts and preferences across sessions.
- **Engineering & Operations**:
  - `github`: Inspect pull requests, issues, commits, and remote repositories.
  - `filesystem`: Direct workshop filesystem access.
  - `motion`: Programmatic UI animation and spring curves.
  - `ponytail`: Codebase architecture and technical debt auditing.
  - `firebase`: Firebase tools and emulator management.
  - `sqlite`: SQLite querying and introspection.

---

## 4. How Skill Resolution Works (800+ Skills)

OpenCode automatically searches across registered skill directories:
1. `./skills` (primary skills)
2. `ai agents handbook/packs/ponytail/skills` (Debt & refactor skills)
3. `ai agents handbook/packs/styleseed/skills` (Design system skills)
4. `ai agents handbook/packs/garden-skills/skills` (Web engineering skills)

### Example Skill Workflows:
- To build a modern SaaS UI: OpenCode invokes `tailwind-design-system`, `shadcn`, `react-bits`, and `motion-ai`.
- To optimize PostgreSQL queries: OpenCode invokes `sql-optimization` and `supabase-postgres-best-practices`.
- To write reliable test suites: OpenCode invokes `tdd-workflow`, `e2e-testing`, and `webapp-testing`.
- To audit security rules: OpenCode invokes `firebase-security-rules-auditor` and `security-review`.

---

## 5. OmniRoute Full-Auto Routing

All requests route through OmniRoute (`http://localhost:20128/v1`), which dynamically selects the highest-scoring model:
- `auto/best-coding` -> Top coding model (Claude Opus 5, Qwen 3.8 Max, Kimi K3, GPT 5.6 Sol)
- `auto/best-reasoning` -> Deepest reasoning model (Claude Fable 5, Opus 4.8 Thinking, Grok 4.6)
- `auto/best-fast` -> Fast model for subagents and rapid queries (DeepSeek V4 Flash)
- `auto/best-free` -> Zero-cost auto failover across free provider tiers.
