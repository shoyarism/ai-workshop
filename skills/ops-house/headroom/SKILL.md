---
name: headroom
description: "Context headroom supervisor and output compression layer. Reversibly compresses large tool outputs, compiler logs, and file dumps to maintain maximum token budget during long tasks."
userFacing: true
---

# 🛡️ Headroom: Context Budgeting & Token Compression

> **Purpose:** Monitors conversation token consumption and prevents context window exhaustion by reversibly compressing voluminous tool results, build logs, and file read outputs.

---

## 1. Context Headroom Invariants

1. **The 70% Guardrail:** When conversation context exceeds 70% of the active model window, engage aggressive compression mode.
2. **Reversible Output Summarization:**
   - Instead of emitting 500 lines of compiler stdout, emit the 5-line summary + exact error line numbers.
   - Store full verbose logs in scratch disk files (`scratch/build.log`) rather than polluting conversation history.
3. **Selective AST Reading:**
   - Use `ast-grep` or targeted byte ranges (`StartLine`/`EndLine`) instead of reading 2,000-line files end-to-end.
4. **Context Compaction Triggers:**
   - Recommend `/compact` or summarize task checkpoints when transitioning between major milestone epics.
