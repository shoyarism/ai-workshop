---
description: "Run anti-slop audit and security check on files"
agent: build
---

Audit files for anti-slop compliance and security boundaries: $ARGUMENTS
!`uv run python scripts/workshop.py antislop audit "$ARGUMENTS"`

Report any anti-slop violations, contrast issues, or security flaws and provide clean replacements.
