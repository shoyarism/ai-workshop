---
name: karpathy-skills
description: "Andrej Karpathy's senior developer guidelines: zero ungrounded assumptions, strict anti-overengineering (no 50-to-500 line expansions), irreducible local invariants, and minimal cognitive footprint."
userFacing: true
---

# 🧠 Karpathy Skills: Senior Engineering Invariants

> **Philosophy:** The best code is minimal, explicit, transparent, and grounded in irreducible computational truth. Never solve an imaginary problem. Never expand 50 lines of clean code into a 500-line maze of speculative abstractions.

---

## 1. The 4 Karpathy Directives

### 1. Refusal to Guess (Zero Ungrounded Assumptions)
- Never assume an API, library contract, or schema without inspecting source ASTs or live tests.
- When facing uncertainty, verify against the runtime environment before implementing code.

### 2. The Anti-Overengineering Rule
- If a task requires computing a mean or filtering a list, write the 3 lines of direct code. Do not introduce a `GenericFilteringStrategyFactoryProvider`.
- Code expansion ratio: If you find yourself modifying 10 files and adding 300 lines for a simple bug fix, stop immediately. Step back and find the 3-line surgical fix.

### 3. Irreducible Local Invariants
- Keep state machines simple. Minimize mutable state.
- Prefer pure functions, explicit inputs, explicit outputs, and deterministic error returns.
- Keep data structures aligned with standard Python/TypeScript primitives rather than unnecessary deep object graphs.

### 4. Direct Observability
- If a system fails, print the exact tensor shape, memory address, or response payload.
- Never write generic catch-all blocks (`catch (e) {}` or `except Exception: pass`) that swallow root causes.
