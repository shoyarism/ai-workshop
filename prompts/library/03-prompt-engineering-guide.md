# Prompt Engineering Field Guide

A condensed, agent-oriented distillation of current best practices. Use this as a reference when writing or debugging prompts.

## 1. Anatomy of a strong prompt

| Element | What it does |
|---|---|
| Role / identity | Sets perspective and domain knowledge. |
| Mission | One-sentence objective; prevents scope drift. |
| Rules | Concrete behavioral contracts (not vibes). |
| Workflow | Ordered phases with explicit inputs/outputs. |
| Tools | What is available, when to use it. |
| Output contract | Exact schema/format to return. |
| Constraints | Anti-patterns, boundaries, failure behavior. |
| Verification | How "done" is measured. |

## 2. Clarity techniques

- **Be explicit about format**: "Return a JSON object with fields X, Y, Z" beats "summarize".
- **Show, don't tell**: give 1–2 few-shot examples of the *output shape* you want.
- **Define the audience**: "for a non-technical stakeholder" changes tone/length more reliably than "be concise".
- **Prevent ambiguity**: ask the agent to restate the task before doing it when stakes are high.
- **One instruction per sentence**; number multi-part instructions.

## 3. Control techniques

- **Chain of thought / structured reasoning**: require "steps: ... then conclusion" for multi-step logic.
- **Self-verification**: ask the agent to check its own output against the source (for code/claims).
- **Confidence flags**: `"inferred": true` on anything not directly observed — kills hallucination politely.
- **Scoring rubrics**: numeric or checkbox gates make "done" objective and auditable.
- **Tool routing**: load a skill only when its trigger matches; prevents context bloat.

## 4. Common failure modes & fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Verbose / rambling | No output contract | Specify format + max length |
| Hallucinated details | Inference treated as fact | Mandate evidence + `inferred` flags |
| Scope creep | Vague mission | State non-goals explicitly |
| Wrong stack/assumptions | Prompt implies a default | "Adapt to the project; justify choices" |
| Shallow work | No verification loop | Add quality gates before "done" |
| Ignored instructions | Rules buried at the end | Put critical rules first; number them |

## 5. Iteration loop

1. Run once with a minimal prompt.
2. Read the output *against the source* (never assume).
3. Identify the single worst behavior.
4. Patch the prompt with one targeted instruction.
5. Re-run the same input; compare.
6. Promote stable prompts to the library / system prompt.

## 6. References

- Anthropic prompt engineering guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- Anthropic prompt engineering cookbook (GitHub): https://github.com/anthropics/prompt-eng-interactive-tutorial
- OpenAI prompt engineering guide: https://platform.openai.com/docs/guides/prompt-engineering
- Vercel skills.sh directory: https://skills.sh
