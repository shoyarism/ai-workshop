---
adrid: ADR-001
title: Slop Court Judicial Quality Tribunal Implementation
status: Accepted
date: 2026-08-06
authors: ["shoyarism", "Antigravity", "Slop Court Magistrate"]
---

# ADR-001: Slop Court Judicial Quality Tribunal Implementation

## Context

AI coding agents consistently produce degraded codebases with:
- Truncated code placeholders (ellipses in comments)
- Silent error swallowing (`except: pass`)
- Fabricated telemetry claims (`10M+ users`)
- Generic AI content without distinct character

Traditional linters rely on external rules and cannot enforce holistic craft quality.

## Decision

Implement a 3-juror judicial tribunal that evaluates staged code as a unified quality gate:

### Juror 1: Craft & Tone (40% weight)
- Flags marketing fluff and AI clichés
- Detects tautological comments
- Identifies fake placeholder stats
- Checks for default purple-indigo gradients

### Juror 2: Architecture & AST (30% weight)
- Python AST parsing for structural analysis
- Flags functions >150 statements (god-functions)
- Detects control flow nesting >5 levels
- Identifies wildcard imports

### Juror 3: Security & Invariants (30% weight)
- Intercepts `except: pass` patterns
- Detects hardcoded secrets/tokens
- Flags dangerous `eval()`/`exec()` calls
- Identifies SQL injection patterns

## Consequences

### Positive
- **Zero-slop guarantee**: Commits blocked until all felonies resolved
- **Unanimous requirement**: Forces consensus on quality gates
- **Cryptographic docket**: SHA-256 tamper-evident audit trail
- **Git Bailiff**: Automatic pre-commit/pre-push enforcement

### Negative
- Initial learning curve for developers
- Occasional false positives on edge cases
- Requires `@court-exempt` annotations for legitimate exceptions

## Related

- ADR-002: Multi-Persona Supreme Council Debate Framework
- ADR-003: Obsidian Second Brain Persistent Memory
- ADR-004: FastMCP Protocol Server Integration