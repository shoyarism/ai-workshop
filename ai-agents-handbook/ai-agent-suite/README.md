# AI ENGINEERING AGENT — DOCUMENT SUITE

Modular companion documents for the **AI Engineering Agent — Master Workflow & Architecture Rules** prompt (`AI-AGENT-MASTER-PROMPT.md`).

## Documents

| File | Purpose |
|---|---|
| [`00-MASTER-PROMPT.md`](./00-MASTER-PROMPT.md) | Canonical single-file master prompt (entry point). |
| [`01-OPERATIONAL-SPEC.md`](./01-OPERATIONAL-SPEC.md) | Detailed technical execution protocols: codebase fingerprinting, website reconnaissance pipeline (headless browser/CDP, DOM & Shadow DOM piercing, hydration extraction, JS AST analysis, network telemetry, auth/JWT tracing), and error recovery. |
| [`02-OUTPUT-SCHEMAS.md`](./02-OUTPUT-SCHEMAS.md) | Formal JSON Schema (Draft-07) definitions and AI-optimized Markdown templates for all output artifacts. |
| [`03-VERIFICATION-MATRIX.md`](./03-VERIFICATION-MATRIX.md) | Weighted scoring model, performance rubrics, benchmark scenarios, validation commands, and release gates. |
| [`04-SKILLS-CATALOG.md`](./04-SKILLS-CATALOG.md) | Full managed skill catalog (796 skills) organized by domain with routing guidance. |

## Relationship to source material

- **`AI-AGENT-MASTER-PROMPT.md`** — original Senior Full-Stack Engineer workflow prompt; developed and expanded into the master prompt.
- **`prompts/`** — website reconnaissance suite (`SYSTEM_PROMPT.md`, `OPERATIONAL_SPEC.md`, `OUTPUT_SCHEMAS.md`, `VERIFICATION_MATRIX.md`); its methodology is embedded and generalized throughout this suite.
- **`skills/`** — managed agent skill library (796 skills from 30+ official + community repositories and agent packs); indexed in `SKILLS_INDEX.md`, provenance in `SOURCES.md`, and routed via `04-SKILLS-CATALOG.md`.
- **`ai-agents-handbook/packs/`** — agent persona & config packs (ponytail, karpathy, ECC, huashu-design, baoyu-design, garden-skills, styleseed); skills are extracted into `skills/`.
- **`ai-agents-handbook/references/`** — awesome-lists and directories for skills, MCP servers, system prompts, and plugins.

## How to use

1. Load `00-MASTER-PROMPT.md` (or `AI-AGENT-MASTER-PROMPT.md`) as the agent system prompt.
2. Consult `01-OPERATIONAL-SPEC.md` when executing the analysis/reconnaissance phases or hitting an edge-case protocol.
3. Use `02-OUTPUT-SCHEMAS.md` as the authoritative schema reference for generated artifacts.
4. Gate acceptance using `03-VERIFICATION-MATRIX.md`.
5. Route task types to skills using `04-SKILLS-CATALOG.md`.
