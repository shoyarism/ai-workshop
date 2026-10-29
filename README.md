<div align="center">
  <img src="assets/logo.svg" alt="Workshop OS Logo" width="440">
  <p><strong>The Irreducible Operating Foundation &amp; Code Quality Gate for AI Agents</strong></p>

[![CI](https://github.com/shoyarism/ai-workshop/actions/workflows/ci.yml/badge.svg)](https://github.com/shoyarism/ai-workshop/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11 | 3.12](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)
[![Quality Gate](https://img.shields.io/badge/Slop_Court-v3.5_Armed-eb5e28.svg)](scripts/workshop_court.py)
[![Code Style: Ruff](https://img.shields.io/badge/linter-ruff-black.svg)](pyproject.toml)

<br>

[English](README.md) • [简体中文](docs/i18n/README.zh-CN.md) • [日本語](docs/i18n/README.ja.md) • [Español](docs/i18n/README.es.md)

</div>

<br>

<div align="center">
  <img src="assets/hero-banner.svg?v=3.5.0" alt="Workshop OS Manifesto Graphic" width="100%">
</div>

<br>

<p align="center">
  <code>SPEC: WORKSHOP-OS-3.5</code> &nbsp;•&nbsp;
  <code>LICENSE: APACHE-2.0</code> &nbsp;•&nbsp;
  <code>7 SOVEREIGN HOUSES</code> &nbsp;•&nbsp;
  <code>2,147 VERIFIED SKILLS</code> &nbsp;•&nbsp;
  <code>SLOP COURT: v3.5 ARMED</code>
</p>

---

## 📑 TABLE OF CONTENTS

- [01 // Quick Start (60 Seconds)](#01--quick-start-60-seconds)
- [02 // The Manifesto: Why AI Agents Erode Codebases](#02--the-manifesto-why-ai-agents-erode-codebases)
- [03 // Architectural Topology](#03--architectural-topology)
- [04 // The 7 Sovereign Houses](#04--the-7-sovereign-houses)
- [05 // Slop Court v3.5: The Code Quality Tribunal](#05--slop-court-v35-the-code-quality-tribunal)
- [06 // The Universal Supreme Council](#06--the-universal-supreme-council)
- [07 // Architectural Capability & Invariant Matrix](#07--architectural-capability--invariant-matrix)
- [08 // Master CLI Command Palette](#08--master-cli-command-palette)
- [09 // Harness Configuration Matrix](#09--harness-configuration-matrix)
- [10 // Project Documentation & Examples](#10--project-documentation--examples)
- [11 // Synthetic Team, Authors & Contributors](#11--the-synthetic-team-authors--contributors)
- [12 // Open Source Governance & Licensing](#12--open-source-governance--licensing)

---

## 01 // QUICK START (60 SECONDS)

For extended setup details and troubleshooting, see [QUICKSTART.md](QUICKSTART.md).

### Option A: Local Workstation Setup (Recommended)

Choose either `uv` (fastest) or standard `pip`:

```bash
# 1. Clone the repository
git clone https://github.com/shoyarism/ai-workshop.git
cd ai-workshop

# 2. Install dependencies (choose ONE)
uv sync                 # If using uv
pip install -e .        # If using standard pip

# 3. Arm the Slop Court Bailiff pre-commit and pre-push interceptors
workshop court bailiff install

# 4. Verify environment and run test suite
workshop doctor --strict
pytest
```

### Option B: Sandboxed Docker Container

Isolate all subprocess executions and file operations in a non-root container sandbox:

```bash
# Run strict health diagnostics inside an isolated container
docker compose run --rm runtime

# Start sandboxed local browser hubs and background services
docker compose up -d hub
```

### Option C: The Zero-Clone Cloud Protocol

Operating inside an ephemeral container, GitHub Codespace, or remote cloud instance? Stream any skill runbook directly into your agent context using raw `curl`:

```bash
# Stream any skill directly into agent context (cross-platform curl)
curl -fsSL https://raw.githubusercontent.com/shoyarism/ai-workshop/main/skills/dev-house/using-superpowers/SKILL.md
```

> **Windows PowerShell Note:** In Windows PowerShell, run `curl.exe` to ensure the native binary executes rather than the `Invoke-WebRequest` alias.

---

## 02 // THE MANIFESTO: WHY AI AGENTS ERODE CODEBASES

Every developer using AI coding agents eventually hits the **degradation wall**:

* **The Omission Fraud:** When the task gets difficult or context runs long, models quietly omit core logic with lazy placeholders, leaving you with broken files.
* **The Error Blackhole:** To make a script run without failing, agents wrap dangerous operations in empty `except:` or `catch (e) {}` blocks. Bugs become silent landmines.
* **The Yes-Man Echo Chamber:** LLMs are trained to please. Ask an AI if a fragile architecture or flawed business model will work, and it invariably compliments you. Single-model feedback is an echo chamber.
* **Context Amnesia:** Every session starts from scratch. Past architectural decisions and post-mortems vanish.

**Workshop OS establishes enforceable boundaries:** a 3-juror quality tribunal combining native Python AST parsing and polyglot lexical heuristics that halts commits at the Git level, an adversarial 4-persona council that stress-tests decisions, and **2,147 verified execution runbooks**.

---

## 03 // ARCHITECTURAL TOPOLOGY

<br>

<div align="center">
  <img src="assets/architecture.svg" alt="Workshop OS Architectural Schematic" width="100%">
</div>

<br>

### The 4 Execution Zones

```
[ ZONE A: HARNESSES ]         [ ZONE B: THE COURT ]       [ ZONE C: THE COUNCIL ]     [ ZONE D: THE FOUNDRY ]
Claude Code / Codex    -->    Static AST Analysis   -->   Skeptical Inquisitor   -->   2,147 Domain Skills
Cursor & Windsurf             3-Juror Deliberation        Radical Minimalist         7 Sovereign Houses
Gemini Antigravity            Git Bailiff Hooks           UI/UX Craft Architect      Obsidian 2nd Brain
OpenCode & Kilo               Pre-Commit & Pre-Push       Zero-Trust SRE             Zero-Clone HTTP Stream
CLI (`workshop`)              SHA-256 Content Hash        Adversarial Dialectics     Docker Sandbox
```

---

## 04 // THE 7 SOVEREIGN HOUSES

<br>

<div align="center">
  <img src="assets/houses-topology.svg" alt="Workshop OS 7 Sovereign Houses Topology" width="100%">
</div>

<br>

To prevent **context window rot** and cognitive clutter, Workshop OS categorizes its **2,147 verified skills** into **7 Sovereign Houses**. Rather than dumping hundreds of tools into the LLM context, operators and agents load modular profiles tailored for the current mission:

| Sovereign House | Jurisdiction & Focus | Lead Arsenal Tools | Verified Capacity |
| :--- | :--- | :--- | :---: |
| **🛡️ 01 The Security House**| Defensive monitoring, incident response, AST arrest, forensic recovery, and penetration testing. | `slop-court` v3.5, `git-bailiff`, `strix-pentest`, `digital-forensics` | **835 Skills** |
| **⚡ 02 The Dev House** | Senior dev invariants, TDD, strict TypeScript, AST refactoring, and dead code pruning. | `superpowers`, `matt-pocock`, `karpathy-skills`, `ponytail`, `ast-grep` | **357 Skills** |
| **🎬 03 The Media House** | Programmatic video code, autonomous studio pipelines, FLUX optics, and Remotion/HyperFrames. | `hyperframes`, `OpenMontage`, `photoreal-studio`, `remotion`, `youtube` | **178 Skills** |
| **🏎️ 04 Ops & Tokens** | Spec-Driven Dev (SDD), token diet, context compression, and YC startup team simulation. | `caveman` (-70% tokens), `headroom`, `gsd`, `bmad-method`, `gstack` | **166 Skills** |
| **🎨 05 The Design House** | Typography, aesthetic anti-slop, layout grids, visual tokens, and presentation decks. | `ui-ux-pro-max`, `design-taste`, `impeccable`, `archify`, `ppt-master` | **132 Skills** |
| **🔬 06 The Intel House** | AST knowledge graphs, zero-cost scrapers, 30-day recency intel, and reverse engineering. | `graphify`, `agent-reach`, `last-30-days`, `understand-anything`, `rea` | **90 Skills** |
| **📢 07 The Growth House** | Authentic human tone, conversion copywriting, value props, SEO, and product launches. | `humanizer`, `marketing-skills`, `brand-voice`, `product-hunt-launch` | **79 Skills** |

*Auxiliary Infrastructure:* `skills/cloud-and-apis/` houses **320 specialized connectors** (AWS, Azure, GCP, BigQuery, Stripe, Resend) kept neatly isolated from core Houses.

<details>
<summary><b>🔍 Expand Directory Mapping & House Inspection Commands</b></summary>
<br>

Each Sovereign House is versioned as a modular directory tree under `skills/`:
* `skills/security-house/` — Defensive monitors, Slop Court tribunal rules, forensic collectors.
* `skills/dev-house/` — TDD frameworks, strict typing runbooks, AST refactoring guides.
* `skills/media-house/` — Programmatic motion graphics, video pipelines, photoreal studio.
* `skills/ops-tokens-house/` — Token diet protocols, SDD execution templates, context compressors.
* `skills/design-house/` — Design tokens, visual anti-slop rules, typography scales.
* `skills/intel-house/` — AST knowledge graph parsers, OSINT scrapers, recency intelligence.
* `skills/growth-house/` — Authentic human voice guides, product launch checklists, technical SEO.
* `skills/cloud-and-apis/` — Isolated cloud service and external API runbooks.

```bash
# Explore and inspect any house from the terminal
workshop house list
workshop house inspect design-house
workshop house inspect dev-house
```
</details>

---

## 05 // SLOP COURT v3.5: THE CODE QUALITY TRIBUNAL

<br>

<div align="center">
  <img src="assets/court-tribunal.svg" alt="Slop Court Judicial Deliberation Pipeline" width="100%">
</div>

<br>

Rather than relying on vague subjective prompts, the **Slop Court** evaluates staged code as an automated judicial review before a 3-juror bench:

1. **Juror Craft & Tone (40% Weight):** Flags marketing fluff, unearned purple-indigo gradients, tautological comments (`// returns response`), fabricated stats (`10M+ users`, `99.9% uptime` without telemetry tags), and lazy omission stubs.
2. **Juror Architecture & AST (30% Weight):**
   * *Python:* Full deterministic Python AST parsing via the standard `ast` module. Flags extreme control flow nesting (> 5 levels) or monolithic functions (> 150 statements).
   * *Non-Python (TS, JS, Go, Rust):* Pattern and regex heuristics for control nesting, token count, and structural metrics.
3. **Juror Security & Invariants (30% Weight):** Intercepts silent error swallowers (`except: pass`), unlogged exception catches, and hardcoded secrets.

> **Suppression Pragmas:** Legitimate exceptions (e.g. platform encoding fallbacks) can be explicitly annotated with `# @court-exempt: <reason>`, providing a documented, auditable paper trail similar to `# noqa` or `eslint-disable`.

### The Git Bailiff Gate

The Bailiff installs into `.git/hooks/pre-commit` and `.git/hooks/pre-push`. When code contains a sustained felony, **the Bailiff aborts the commit immediately** with exit code 1:

```shell
$ git commit -m "feat: user pipeline"
⚖️  Slop Court Bailiff: Convening Pre-Flight Judicial Review...
======================================================================
 ⚖️  SLOP COURT v3.5: SUPREME JUDICIAL TRIBUNAL TRIAL REPORT
======================================================================
 Case Docket : CR-20261028-FADA
 Target      : Staged Git Diffs (1 files | 237 lines)
 Slop Index  : 0.0% | Penalties: 0 pts | Felonies: 0 | Misdemeanors: 0
 SHA-256 Sig : 46342aca9f37c404...a76d509f
----------------------------------------------------------------------
 [3-JUROR BENCH DELIBERATION]
  ✓ [ACQUIT] Juror Craft & Tone           : 0 aesthetic violations. Tone clean.
  ✓ [ACQUIT] Juror Architecture & AST     : 0 architectural smells. Invariants clean.
  ✓ [ACQUIT] Juror Security & Invariants  : 0 security/error invariant breaches.
----------------------------------------------------------------------
 [FINAL JUDICIAL RULING]
  🎉 VERDICT: ACQUITTED WITH HONORS (UNANIMOUS)
  Certificate of Cleanliness granted for commit and push.
======================================================================
[main 4a4825c2] feat: user pipeline
```

---

## 06 // THE UNIVERSAL SUPREME COUNCIL

> *"A board that agrees on everything is redundant. Value is forged through intellectual collision and exposing unstated blind spots."*

Single-agent reasoning is prone to confirmation bias. The **Supreme Council** forces 4 distinct cognitive postures into adversarial debate before you commit to critical paths:

* **The Skeptical Inquisitor:** Red-teams assumptions, hunts tail risks, and maps cascading failure modes.
* **The Radical Minimalist:** Ruthlessly enforces YAGNI. Prunes bloated dependencies, unnecessary microservices, and premature abstraction.
* **The UI/UX Craft Architect:** Defends typographic hierarchy, spacing rhythm, and WCAG AA accessibility standards.
* **The Zero-Trust SRE:** Assumes services will crash at 3 AM. Demands backpressure, idempotency, and explicit telemetry.

```bash
# Deliberate an architectural choice
workshop court council "Should we rewrite the ingestion pipeline in Rust?" --domain architecture

# Deliberate a product strategy
workshop court council "Launching an API with a $99/mo minimum and zero free tier" --domain business

# Deliberate any technical question
workshop court council "Mandating 100% test coverage before release" --domain general
```

---

## 07 // ARCHITECTURAL CAPABILITY & INVARIANT MATRIX

Workshop OS establishes deterministic guarantees that convert open-ended LLM non-determinism into verifiable, repeatable engineering invariants:

| Engineering Dimension | Workshop OS Architecture | Conventional AI Tools & Assistants | Deterministic Invariant Guaranteed |
| :--- | :--- | :--- | :--- |
| **Code Quality Gate** | **Slop Court (Deterministic Python AST + Polyglot Lexical Heuristics)** | Ad-hoc system prompt hints & external linters | Zero lazy stubs, zero truncated lines, zero unlogged exceptions (Deterministic AST parsing for Python; lexical regex heuristics across polyglot assets) |
| **Pre-Commit Enforcement** | **Turnkey Git Bailiff Interceptor (`court bailiff`)** | Manual pre-commit hooks or manual bash scripts | Commits blocked automatically on AST/Penal Code breach |
| **Cognitive Bias Defense** | **Universal Supreme Council (4 Adversarial Personas)** | Single-model echo chamber / unverified synthesis | Multi-perspective blindspot exposure prior to critical commits |
| **Execution Runbooks** | **7 Sovereign Houses with 2,147 Verified Skills** | Empty workspace or generic unversioned prompts | Standardized YAML frontmatter contracts & executable runbooks |
| **Epistemic Memory** | **Obsidian Markdown Vault + ADRs + Post-Mortems** | Ephemeral context window lost upon session termination | Grounded organizational learning with immutable post-mortems |
| **Deployment Footprint** | **Dual-Mode: Local Foundry or Zero-Clone Cloud Protocol** | Heavy full-clone dependencies or cloud SaaS lock-in | Instant zero-clone raw GitHub streaming or isolated Docker sandbox |
| **Multi-Harness Portability** | **Native Unified Config: Antigravity, Claude, Cursor, Windsurf** | Vendor-specific extension silos | Single source of truth system prompt & skills across all agents |
| **Open Governance** | **Apache 2.0 Open Source Core** | Proprietary walled gardens | Auditable codebase with transparent synthetic swarm lineage |

---

## 08 // MASTER CLI COMMAND PALETTE

Workshop OS provides a centralized console entrypoint (`workshop` or `python scripts/workshop.py`):

```bash
# === 1. System Health & Diagnostics ===
workshop doctor --strict               # Comprehensive diagnostic across 41+ subsystems
workshop status                        # Live operational state and background services

# === 2. Sovereign Houses & Skill Arsenal ===
workshop house list                    # Enumerate all 7 Sovereign Houses and capacities
workshop house inspect <house-name>    # Deep-dive into lead tools and runbook inventory
workshop search "<keyword>"            # Fuzzy search across 2,147 verified skills and tools

# === 3. Slop Court Judicial Tribunal ===
workshop court trial --staged          # Prosecute staged Git diffs before 3-juror bench
workshop court jury --staged           # View detailed juror-by-juror voting breakdown
workshop court reform <file>           # Auto-purge tautological comments and slop markers
workshop court bailiff install         # Install Git pre-commit and pre-push hooks

# === 4. Supreme Council Dialectics ===
workshop court council "<topic>" --domain <general|architecture|business|creative>

# === 5. Multimodal & MCP Extensions ===
workshop see path/to/asset.png         # Inspect visual assets using multimodal vision
workshop mcp list                      # Enumerate active FastMCP tools and servers
workshop hub                           # Launch real-time live browser automation hub
```

---

## 09 // HARNESS CONFIGURATION MATRIX

Connect Workshop OS to your preferred AI agent environment using the master instructions in [`docs/WORKSHOP_DEFAULT_SYSTEM_PROMPT.md`](docs/WORKSHOP_DEFAULT_SYSTEM_PROMPT.md):

| Harness | Configuration File | Integration Mode |
| :--- | :--- | :--- |
| **Claude Code** | `CLAUDE.md` or `~/.claude/CLAUDE.md` | Native FastMCP + Slop Court pre-commit hook |
| **Cursor** | `.cursorrules` or Project Rules | Local Foundry or Zero-Clone via GitHub API |
| **Gemini Antigravity** | `~/.gemini/config/AGENTS.md` | Master Soul hook (`court_trial`, `court_council`) |
| **Windsurf** | `.windsurfrules` or `AGENTS.md` | Cascading Context & Tool Forge |
| **OpenCode / Hermes** | `opencode.json` & `SOUL.md` | Local Foundry execution |
| **Kilo** | `kilo.jsonc` | Multi-directory workspace indexing |
| **Docker Sandbox** | `Dockerfile` & `docker-compose.yml` | Non-root isolated execution boundary |

---

## 10 // PROJECT DOCUMENTATION & EXAMPLES

* **[GLOSSARY.md](GLOSSARY.md):** Complete architectural glossary defining Slop Court, Git Bailiff, the 7 Sovereign Houses, and codified penal statutes (FEL-01..08, MIS-01..06).
* **[QUICKSTART.md](QUICKSTART.md):** Comprehensive onboarding guide with step-by-step instructions for `uv`, `pip`, Docker, and Zero-Clone mode.
* **[BENCHMARKS.md](BENCHMARKS.md):** Empirical latency, memory footprint, and SLA metrics across CLI commands and Git pre-commit interceptors.
* **[ROADMAP.md](ROADMAP.md):** Architectural roadmap across Phases 1, 2, and 3.
* **[docs/COUNCIL_AND_SYNC_POLICY.md](docs/COUNCIL_AND_SYNC_POLICY.md):** Model routing, token costs, zero-cost offline fallbacks, and vendored skill maintenance policy.
* **[examples/](examples/):**
  * [`examples/01_slop_court_programmatic.py`](examples/01_slop_court_programmatic.py): Programmatic Python API usage for Slop Court.
  * [`examples/02_skill_template/SKILL.md`](examples/02_skill_template/SKILL.md): Standard YAML frontmatter contract template for creating new skills.
  * [`examples/03_supreme_council_debate.py`](examples/03_supreme_council_debate.py): Programmatic invocation of the 4-persona Supreme Council dialectic panel.
  * [`examples/04_pre_commit_pipeline_integration.md`](examples/04_pre_commit_pipeline_integration.md): Recipe for integrating Slop Court with native Bailiff, `.pre-commit-config.yaml`, and GitHub Actions.

---

## 11 // THE SYNTHETIC TEAM, AUTHORS & CONTRIBUTORS

Workshop OS is built through a human-synthetic collaborative engineering swarm and an open-source lineage. See [AUTHORS.md](AUTHORS.md) for full attribution:

* **Human Founder, Lead Architect & Designer:** **shoyarism** ([@shoyarism](https://github.com/shoyarism))
* **The Synthetic Engineering Swarm:**
  * **Antigravity (Google DeepMind)** — Master Systems Architect & Integrator
  * **Slop Court Magistrate** — Chief Judicial Arbiter & AST Invariant Auditor
  * **Skeptical Inquisitor** — Adversarial Red-Team Lead & Failure Invariant Hunter
  * **Radical Minimalist** — Anti-Bloat, KISS Principle & YAGNI Champion
  * **UI/UX Craft Architect** — Typography, Spacing Rhythm & Visual Discipline
  * **Zero-Trust SRE** — Zero-Trust Reliability & Fault-Tolerance Engineer
  * **Knowledge Synthesizer** — Task-to-Skill Compiler & Obsidian Vault Curator
* **Community Contributors & Pioneers:** Andrej Karpathy (*llm-council, karpathy-skills*), Garry Tan (*gstack*), Jesse Vincent (*superpowers*), Matt Pocock (*matt-pocock-skills*), Brian Madison (*bmad-method*), Leon Lin (*design-taste-frontend*), Matt Van Horn (*last-30-days*), Hugo He (*ppt-master*), Mor Luto (*rea*), Addy Osmani (*agent-skills*), Dietrich Gebert (*ponytail*), Daniel Miessler (*fabric / PAI*), and Anthropic (*Claude Code & MCP*).

---

## 12 // OPEN SOURCE GOVERNANCE & LICENSING

* **Core License:** The Workshop OS orchestration framework, CLI scripts, and Slop Court tribunal are licensed under the [Apache License, Version 2.0](LICENSE).
* **Vendored Skills & Third-Party Runbooks:** Community skill packs and external tools retained within the Sovereign Houses preserve their respective upstream open-source licenses (MIT, Apache-2.0, BSD-3-Clause) as noted in their respective directories. See [VENDORED_LICENSES.md](VENDORED_LICENSES.md) for license declarations.
* **Contributing:** Review the [CONTRIBUTING.md](CONTRIBUTING.md) guide and zero-slop pre-flight checklist.
* **Code of Conduct:** Community expectations documented in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
* **Security Policy & Threat Model:** Detailed operational boundaries and responsible disclosure protocols are in [SECURITY.md](SECURITY.md).
* **Episodic Memory Vault:** Architecture Decision Records (ADRs) and Post-Mortems live in [`vault/`](vault/).
