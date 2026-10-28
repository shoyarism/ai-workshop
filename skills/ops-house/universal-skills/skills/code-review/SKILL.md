---
name: code-review
description: Use when reviewing code for quality, bugs or security.
---

# Code Review

Order of review:
1. Does it do what it should? Trace one normal and one edge case.
2. Bugs and error handling.
3. Security: secrets, injection, unsafe input, permissions.
4. Readability: names, structure, duplication.
5. Performance only if it matters.
Report: top issues first, each with the line, why it matters and a suggested fix. Keep praise short and specific.
