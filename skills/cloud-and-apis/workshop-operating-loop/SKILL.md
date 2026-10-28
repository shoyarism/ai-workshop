---
name: workshop-operating-loop
description: "Master 5-stage engineering problem-solving loop (RECON -> PLAN -> CRAFT -> AUDIT -> VERIFY) for AI agents in Workshop OS."
---

# Workshop Operating Loop

Execute this deterministic cycle on every non-trivial engineering task:

```
[ STAGE 1: RECON ] ──▶ [ STAGE 2: PLAN ] ──▶ [ STAGE 3: CRAFT ] ──▶ [ STAGE 4: AUDIT ] ──▶ [ STAGE 5: VERIFY ]
```

## Stage 1: Reconnaissance (RECON)
- Inspect project AST, file directory, and existing conventions before making edits.
- Query AST graph: `graphify query "<feature>"` or direct code search.
- Search relevant domain skills via `skill_search("<topic>")` or `workshop search "<topic>"`.
- Check known errors: `memory_recall("<topic>")` to review previous post-mortems (PM-xxx).
- Ground all facts in code and telemetry—never guess paths or APIs.

## Stage 2: Planning (PLAN)
- Deconstruct the challenge into first principles: computational complexity, memory layout, invariants.
- Define type-safe interfaces, function signatures, and error boundaries.
- For non-trivial features, draft a plan artifact and call `critique` to detect architectural flaws.

## Stage 3: Crafting (CRAFT)
- Deliver 100% complete, fully implemented code. Zero `// TODO` or placeholder comments.
- Follow existing project style and UI design tokens (`ui-ux-arsenal`).
- Keep modules focused, loosely coupled, and deterministic.

## Stage 4: Auditing (AUDIT)
- Run `antislop_audit` to eliminate AI clichés, unearned design tropes, and lazy comments.
- Audit security boundaries: validate inputs, prevent path traversal, protect secret credentials.
- Verify edge cases: empty collections, null states, timeouts, and network failure modes.

## Stage 5: Verification (VERIFY)
- Run deterministic tests and linters: `verify("<command>")` or `workshop doctor`.
- Check compiler diagnostics and exit codes. Never conclude a task with unverified code.
- If a tricky bug was solved, document it in `vault/02 - Post-Mortems/` (PM-xxx).
