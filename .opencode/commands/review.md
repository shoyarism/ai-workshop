---
description: "Review recent git diff or code changes for quality and anti-slop compliance"
agent: reviewer
subtask: true
---

Review the recent git changes:
!`git diff HEAD~1`

Audit these changes strictly against the 38 Anti-Slop rules, WCAG contrast >= 4.5:1, and type-safety contracts. Focus on critical blockers and anti-slop hygiene.
