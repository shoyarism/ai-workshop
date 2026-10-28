# OPENCODE.md — Centralized Workshop Protocol & Master Arsenal Guide

## 0. MANDATORY: Anti-Dumbass Engineering Directives

Before writing code or executing any task, every OpenCode intelligence MUST:
1. **First-Principles Thinking:** Deconstruct problems to irreducible axioms, physical/logical invariants, and state machines. Derive solutions from the bottom up.
2. **Multi-Source Grounded Research:** Ground all decisions across the 6-tier research hierarchy: peer-reviewed journals (Voyager, Reflexion, DSPy), RFCs/standards (IETF/W3C), upstream ASTs/docs, production post-mortems, and empirical benchmarks.
3. **Anti-Slop AI Quality Filter:** Strictly enforce 38 anti-slop rules (R-01..R-38), Purpose-Gates, Liveliness dials (1-5), and 4-block Delivery Gate verification.
4. **Never Cut Corners or Truncate Output:** Deliver 100% complete, fully implemented code. Zero placeholders, zero `// TODO: implement later`, zero lazy shortcuts.
5. **Reconnaissance First:** Scan the centralized Workshop arsenal via `uv run python scripts/workshop.py search "<keyword>"` (878+ skills, 32 subsystems, 23 MCP tools, 1,500+ APIs).
6. **Multimodal Media Analysis:** When inspecting images, videos, audio, or UI layouts, always use `uv run python scripts/workshop.py see "<file>"` or `uv run python scripts/workshop.py vision storyboard "<video>"`.
7. **Announce Selected Arsenal:** State chosen skills, tools, and MCP servers (e.g. `🎯 Workshop Arsenal Selected: [Skills: ... | MCPs: ... | Reference: ...]`).
8. **Deterministic Verification:** Verify every solution before handing off (smoke tests, WCAG contrast 4.5:1, test suites).

---

## 1. Unified Master CLI (`scripts/workshop.py`)

All operations are centralized through the master CLI:
- **Search**: `uv run python scripts/workshop.py search "<query>"`
- **Anti-Slop Quality Gate**: `uv run python scripts/workshop.py antislop [rules|gate|skills|contrast|audit]`
- **See / Media Vision**: `uv run python scripts/workshop.py see "<file_or_dir>" [--prompt "<question>"]`
- **Vision Suite**: `uv run python scripts/workshop.py vision [inspect|frames|storyboard|ocr|transcribe]`
- **Doctor**: `uv run python scripts/workshop.py doctor`
- **Live Browser Hub**: `uv run python scripts/workshop.py hub --port 7860`
- **Browser Execution**: `uv run python scripts/workshop.py browser --url "<url>" --task "<task>" --live`
- **MCP Manager**: `uv run python scripts/workshop.py mcp list`
- **Matrix Status**: `uv run python scripts/workshop.py status`

---

## 2. Universal 5-Stage Problem Solving Protocol

```
[ STAGE 1: RECON & MULTI-SOURCE RESEARCH ]
       │  Scan 878+ skills catalog & documentation via 'uv run python scripts/workshop.py search'
       │  Ground in literature: Peer-reviewed journals, RFCs, upstream specs & benchmarks
       ▼
[ STAGE 2: FIRST-PRINCIPLES ARCHITECTURAL PLANNING ]
       │  Deconstruct problem to irreducible axioms, physical/logical invariants & state machines
       │  Blueprint system specifications, schemas, UI wireframes & API contracts
       ▼
[ STAGE 3: CLEAN BUILD & ANTI-SLOP CRAFT ]
       │  Implement type-safe, modular code using 'ui-ux-arsenal/tokens/design_tokens.json'
       │  Enforce 38 Anti-Slop rules: Pass Purpose-Gates & calibrate Liveliness Dials (1-5)
       ▼
[ STAGE 4: REVIEW & SECURITY AUDIT ]
       │  Audit code quality, debt, vulnerabilities, and edge cases
       ▼
[ STAGE 5: DETERMINISTIC VERIFICATION & DELIVERY GATE ]
       │  Verify via unit tests, runtime execution, and live browser streaming (:7860)
       │  Execute 4-Block Delivery Gate: R-35 smoke test, WCAG contrast (4.5:1), responsive layout
```

---

## 3. Universal Model Context Protocol (MCP) Matrix

| Need | Active MCP Server | Invocation Protocol |
|---|---|---|
| **Live Web & Neural Search** | `exa-search` | Use for cutting-edge documentation, latest release notes, and real-time facts. |
| **Framework Docs & Context** | `context7` | Use for fast, authoritative context on standard libraries and frameworks. |
| **Interactive Browser Testing** | `playwright` | Use for clicking, typing, navigating, taking screenshots, and verifying web UIs. |
| **Headless Scraping & PDF** | `puppeteer` | Use for background page scraping, DOM extraction, and rendering PDF documents. |
| **Chrome DevTools Inspection** | `chrome-devtools` | Use for console log capture, network timing inspection, and runtime profiling. |
| **Long-Term Knowledge Graph** | `memory` | Use for storing persistent facts, user preferences, and project context across sessions. |
| **Deep Cognition & Reasoning** | `sequential-thinking` | Use for complex multi-step algorithm design and root-cause debugging. |
| **GitHub PRs, Issues & Code** | `github` | Use for reviewing pull requests, inspecting issues, and querying remote repos. |
| **Local Git Operations** | `git` | Local Git repository inspection, branches, and diff analysis. |
| **Direct Workspace Operations** | `filesystem` | Direct filesystem access for reading and writing files in the workshop. |
| **Stealth Anti-Detect** | `camofox-browser` | Stealth headless browser with fingerprint protection. |
| **SQLite Database** | `sqlite` | Relational SQLite database inspection and SQL execution. |
| **PostgreSQL Database** | `postgres` | Production PostgreSQL management and schema inspection. |
| **Docker Containers** | `docker` | Containerized app inspection, logs, and process management. |
| **Firebase Cloud** | `firebase` | Firebase database, Auth, Data Connect, and Cloud management. |
| **Terraform IaC** | `terraform` | Infrastructure-as-Code automation, validation, and planning. |
| **Brave Search** | `brave-search` | Real-time web querying and multi-source search engine. |
| **Time & Temporal** | `time` | Timezone management, conversions, and temporal calculations. |
| **Sentry Monitoring** | `sentry` | Error tracking, stack trace inspection, and issue triage. |
| **Linear Workflows** | `linear` | Project management, issue tracking, and task orchestration. |

---

## 4. Live Browser Hub & Visual Streaming

When performing browser automation or visual UI verification:
- **Live Stream Dashboard**: `http://localhost:7860`
- **Runner**: `uv run python scripts/workshop.py browser --url "<url>" --task "<task>" --live`
- Allows real-time live video/canvas stream of the browser session, DOM inspection, and manual takeover.

---

## 5. UI/UX Design System Arsenal
- **Master Blueprint**: [`ui-ux-arsenal/DESIGN_SYSTEM_MASTER.md`](file:///ui-ux-arsenal/DESIGN_SYSTEM_MASTER.md)
- **Master Tokens**: [`ui-ux-arsenal/tokens/design_tokens.json`](file:///ui-ux-arsenal/tokens/design_tokens.json)
- **Aesthetic Archetypes**: Modern Clean SaaS, Dark Glassmorphism, Industrial Brutalism, and Framer Motion spring physics.

<!-- antislop:start -->
## antislop
For UI, copy, people, mobile layout, or code comments work, read `anti-slop/antislop.md` (core) and then the skill for the task:
- Core filter: `skills/antislop/SKILL.md`
- UI / visual: `skills/antislop-ui/SKILL.md`
- Copy & text: `skills/antislop-copywriting/SKILL.md`
- People / accessibility: `skills/antislop-human/SKILL.md`
- Mobile / responsive: `skills/antislop-layoutmobile/SKILL.md`
- Code comments: `skills/antislop-code/SKILL.md`
Before starting, ask the user when antislop applies: during the work, or after it is done.
<!-- antislop:end -->

---

## 6. OpenCode Native Harness Integration

OpenCode is fully configured to operate natively inside Workshop OS:

### 🛠️ Built-in Tools & Permissions:
- `apply_patch`: High-speed multi-file unified diff application.
- `edit` / `read`: Targeted file modifications and AST inspections.
- `glob` / `grep` / `list`: Filesystem exploration and regex searching.
- `bash`: Non-interactive execution of Workshop CLI and testing suites.
- `task`: Subagent orchestration and parallel delegation.
- `skill`: Instant on-demand loading of 920+ parameterized agent skills.
- `todowrite` / `todoread`: Monotonic task progress checklist.
- `webfetch` / `websearch`: Grounded web research and documentation scraping.
- `lsp`: Language server protocol queries (symbols, definitions, diagnostics).
- `question`: Interactive clarification for genuine architectural trade-offs.

### 🤖 Specialized Agents:
- **`build`** (`mode: primary`): Default engineering agent with full tool permissions.
- **`plan`** (`mode: primary`): Architectural planning agent with read-only permissions (`edit: deny`, `bash: deny`).
- **`reviewer`** (`mode: subagent`): Code review, security auditing, and anti-slop compliance.
- **`debugger`** (`mode: subagent`): Root-cause error deconstruction and minimal surgical fixes.
- **`researcher`** (`mode: subagent`): Deep codebase reconnaissance and external documentation querying.
- **`architect`** (`mode: subagent`): High-level system design, schema migrations, and ADR authoring.
- **`security-auditor`** (`mode: subagent`): Vulnerability identification, auth verification, and boundary checks.
- **`docs-writer`** (`mode: subagent`): Clear, non-truncated technical documentation and guides.

### ⚡ Custom Slash Commands:
- `/doctor`: Run full Workshop OS health diagnostics (`scripts/workshop.py doctor`).
- `/search <query>`: Search Workshop catalog for skills, tools, and subsystems.
- `/review`: Review recent changes against 38 Anti-Slop rules and type safety.
- `/debug <issue>`: Deconstruct and debug errors with episodic post-mortem checks.
- `/audit <path>`: Run anti-slop audit and security scan on target files.
- `/plan <task>`: Formulate a first-principles architectural plan before modifying code.
- `/verify`: Run the deterministic verification and test suite (`scripts/workshop_eval.py`).

### 🧩 Custom TypeScript Tools (`.opencode/tools/` & `~/.config/opencode/tools/`):
- `workshop_search`: Invokes Workshop search via Python subprocess.
- `workshop_doctor`: Runs system diagnostics.
- `workshop_antislop`: Audits rules or gates.
- `workshop_see`: Inspects multimodal media files.

---

## 7. Model Provider Catalog (16 Configured Providers)

OpenCode is wired to utilize all providers and authentication tokens from our backup ecosystem:

| Provider | Type | Endpoint / Base URL | Key Models |
|---|---|---|---|
| **omniroute** | Local Engine | `http://localhost:20128/v1` | `auto/best-coding`, `auto/best-fast`, `auto/best-reasoning`, `auto/best-coding-fast` |
| **freellmapi**| Local Gateway | `http://localhost:31415/v1` | `auto` (Smart multi-platform fallback across 92 keys & 616 models) |
| **9router**   | Local Fallback | `http://localhost:20128/v1` | `best-coding`, `best-fast`, `best-reasoning`, `claude-3-7-sonnet` |
| **openrouter**| Direct Cloud | `https://openrouter.ai/api/v1` | `nvidia/nemotron-3.5-lightning:free`, `cohere/north-mini-code:free` |
| **groq**      | Direct Cloud | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile`, `qwen-2.5-coder-32b`, `llama-3.1-8b-instant` |
| **mistral**   | Direct Cloud | `https://api.mistral.ai/v1` | `codestral-latest`, `mistral-large-latest`, `mistral-small-latest` |
| **cerebras**  | Direct Cloud | `https://api.cerebras.ai/v1` | `llama-3.3-70b` (2000 tok/s), `llama3.1-8b` |
| **siliconflow**| Direct Cloud| `https://api.siliconflow.cn/v1` | `deepseek-ai/DeepSeek-V3`, `Qwen/Qwen2.5-72B-Instruct` |
| **deepseek**  | Direct Cloud | `https://api.deepseek.com/v1` | `deepseek-chat` (V3), `deepseek-reasoner` (R1) |
| **cohere**    | Direct Cloud | `https://api.cohere.com/v2` | `command-r-plus-08-2024`, `command-r-08-2024` |
| **nvidia**    | Direct Cloud | `https://integrate.api.nvidia.com/v1` | `meta/llama-3.3-70b-instruct`, `nvidia/llama-3.1-nemotron-70b-instruct` |
| **together**  | Direct Cloud | `https://api.together.xyz/v1` | `meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| **hyperbolic**| Direct Cloud | `https://api.hyperbolic.xyz/v1` | `deepseek-ai/DeepSeek-V3` |
| **venice**    | Direct Cloud | `https://api.venice.ai/api/v1` | `llama-3.3-70b` (Zero-log privacy) |
| **chutes**    | Direct Cloud | `https://chutes.ai/v1` | `deepseek-ai/DeepSeek-V3` |
| **tokenrouter**| Direct Cloud| `https://api.tokenrouter.io/v1` | `tokenrouter/deepseek-v4-pro` |

### Quick Switching in OpenCode CLI:
```bash
# SOTA Coding via OmniRoute Auto-Combo (default):
opencode -m omniroute/best-coding

# 2000 tok/s Wafer Inference via Cerebras:
opencode -m cerebras/llama-3.3-70b

# 500 tok/s LPU Inference via Groq:
opencode -m groq/llama-3.3-70b

# Deep Code Reasoning via Mistral Codestral:
opencode -m mistral/codestral

# Direct Official DeepSeek V3 / R1:
opencode -m deepseek/deepseek-chat
opencode -m deepseek/deepseek-reasoner

# Zero-Cost Free Cloud Tier via OpenRouter:
opencode -m openrouter/nemotron-free
```


