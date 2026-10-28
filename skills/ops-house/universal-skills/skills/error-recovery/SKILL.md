---
name: error-recovery
description: Use when a tool call, command or search fails or returns something unexpected.
---

# Error Recovery

1. Read the full error message. Identify the cause in one sentence.
2. Change exactly one thing, then retry. Never repeat the identical call.
3. Maximum two retries per approach. Then try a different approach.
4. After three failed attempts, stop. Report what you tried, what happened and what you suggest.
5. Never hide a failure. Never say something worked when it did not.
6. If a rate limit appears, wait or switch method; do not hammer the same endpoint.
