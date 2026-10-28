# Prompt Library

Reusable, general-purpose prompt templates and guides for AI coding agents.

| File | Purpose |
|---|---|
| [`00-system-prompt-framework.md`](./00-system-prompt-framework.md) | Skeleton + best practices for authoring any system prompt. |
| [`01-code-review-prompt.md`](./01-code-review-prompt.md) | Review agent prompt with severity tiers, passes, and report format. |
| [`02-architecture-planning-prompt.md`](./02-architecture-planning-prompt.md) | Turns a vague request into a phased, verifiable implementation plan. |
| [`03-prompt-engineering-guide.md`](./03-prompt-engineering-guide.md) | Field guide: anatomy, clarity/control techniques, failure modes, iteration loop. |

## How to use

- Copy the relevant template into a new file, fill in the bracketed sections, and load it as a system prompt.
- Pair prompts with skills: `code-review` / `code-quality`, `writing-plans`, `brainstorming`, `acceptance-orchestrator` (see [`skills/SKILLS_INDEX.md`](../../skills/SKILLS_INDEX.md)).
- For the website-recon system prompt suite, see the top-level [`prompts/`](../README.md).
