# Prompts — AI Agent Prompt Library

Curated system prompts, operational specs, and reusable prompt templates for AI coding agents and multi-agent workflows.

## Contents

| Path | Purpose |
|---|---|
| [`SYSTEM_PROMPT.md`](./SYSTEM_PROMPT.md) | Autonomous website reconnaissance & reverse-engineering system prompt (6-phase pipeline). |
| [`OPERATIONAL_SPEC.md`](./OPERATIONAL_SPEC.md) | Technical execution protocols: headless browser/CDP, AST parsing, network telemetry, auth/JWT decoding, error recovery. |
| [`OUTPUT_SCHEMAS.md`](./OUTPUT_SCHEMAS.md) | JSON Schema (Draft-07) + Markdown templates for endpoint catalogs, component graphs, state machines, data models. |
| [`VERIFICATION_MATRIX.md`](./VERIFICATION_MATRIX.md) | Weighted scoring rubrics, benchmark scenarios, and release gates for agent execution. |
| [`library/`](./library/) | Reusable, general-purpose prompt templates (system-prompt framework, code review, architecture planning, prompt-engineering guide). |

## Usage

1. Load the applicable system prompt (top-level docs or `library/`) as the agent's system prompt.
2. For web reconnaissance tasks, use `SYSTEM_PROMPT.md` + `OPERATIONAL_SPEC.md` + `OUTPUT_SCHEMAS.md` as a single suite, and score results with `VERIFICATION_MATRIX.md`.
3. Combine with skills from [`skills/`](../skills/SKILLS_INDEX.md) and the master agent rules in [`ai agents handbook/`](../ai%20agents%20handbook/AI-AGENT-MASTER-PROMPT.md).

## Archive

`_archive/` holds the original multi-agent build-run artifacts (Gemini Antigravity `.agents/` sessions, BRIEFING/handoff/ORIGINAL_REQUEST records) from when this suite was produced. Kept for provenance; not part of the active prompt set.
