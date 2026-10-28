---
name: gsd
description: "Get Shit Done (GSD). Spec-Driven Development (SDD) runtime for high-velocity software execution. Breaks large epics into atomic phases, preventing context rot and drift."
userFacing: true
---

# ⚡ GSD: Get Shit Done (Spec-Driven Execution)

> **Purpose:** Replaces vague, meandering prompting with atomic, phased Spec-Driven Development (SDD). Focuses strictly on concrete milestone completion without architectural drift.

---

## 1. The GSD Execution Loop

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. SPEC     │ ──> │  2. PHASE    │ ──> │  3. ATOMIC   │ ──> │  4. VERIFY   │
│  Definition  │     │  Breakdown   │     │  Execution   │     │  & Checkoff  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Spec Lock:** Write a concise specification document outlining inputs, outputs, invariants, and edge cases.
2. **Phase Partitioning:** Divide the spec into discrete 15-to-30 minute atomic implementation slices (Phases 1 to N).
3. **Atomic Execution:** Complete Phase 1 entirely before touching Phase 2. Run deterministic tests after each phase.
4. **Zero Drift Guarantee:** Never introduce side refactorings or speculative features outside the current phase scope.
