---
name: plan-act-verify
description: "Algorithmic execution discipline for AI agents and local models: mandatory 3-step loop (Plan Contract -> Atomic Act -> Deterministic Verify) to prevent hallucination and incomplete code."
---

# Plan-Act-Verify Execution Protocol

When executing engineering tasks—especially when running local models, constrained contexts, or complex refactors—follow this rigid state machine:

```
[ 1. PLAN CONTRACT ] ──▶ [ 2. ATOMIC ACT ] ──▶ [ 3. DETERMINISTIC VERIFY ]
          ▲                                                 │
          └───────────────── (If Failed) ───────────────────┘
```

## Step 1: The Plan Contract
Before modifying or creating any file, write down:
1. **Target Files**: Absolute or workspace-relative paths of only the files being altered.
2. **Type Contract / Invariants**: Function signatures, argument types, and error conditions.
3. **Verification Command**: The exact terminal command or test that will prove correctness (e.g. `pytest tests/test_foo.py` or `uv run python script.py`).
4. **Self-Review Escort**: If the logic involves multi-file architecture, invoke the `critique` MCP tool or review against known post-mortems in `memory_recall`.

## Step 2: Atomic Action (Act)
- Perform surgical edits on one module at a time.
- Deliver 100% complete implementations:
  - Zero `// TODO` or `/* implement later */` stubs.
  - Zero `... rest unchanged ...` truncations.
  - Full exception handling and parameter validation.

## Step 3: Deterministic Verification (Verify)
- Run the Verification Command via `verify("<command>")` or terminal tool.
- Inspect the output:
  - Status must be exit code 0.
  - No warnings or untracked tracebacks.
- If verification fails:
  - Treat the error output as ground truth.
  - Do NOT apologize or guess.
  - Formulate a hypothesis, return to Step 1, and fix the root cause.
- Only report success to the user when the verification command has passed cleanly.
