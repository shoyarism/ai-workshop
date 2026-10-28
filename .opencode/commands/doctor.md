---
description: "Run Workshop OS health and diagnostic checks"
agent: build
---

Execute full health and diagnostic audit for Workshop OS:
!`uv run python scripts/workshop.py doctor`

Analyze the diagnostic output. If any errors or warnings are reported, identify the failing components and recommend targeted remediation steps.
