# 🏛️ Architecture Decision Records (ADRs)

Immutable records of significant architectural and design decisions made for Workshop OS.

All ADRs follow the format: `ADR-XXX-title-slug.md`

## Index of ADRs

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [[ADR-001-slop-court-implementation\|ADR-001]] | Slop Court Judicial Quality Tribunal Implementation | Accepted | 2026-08-06 |
| [[ADR-002-supreme-council-debate\|ADR-002]] | Universal Supreme Council Multi-Persona Debate Framework | Accepted | 2026-08-06 |
| [[ADR-003-obsidian-second-brain\|ADR-003]] | Obsidian Second Brain Persistent Memory System | Accepted | 2026-08-06 |
| [[ADR-004-fastmcp-protocol-server\|ADR-004]] | FastMCP Protocol Server Native Integration | Accepted | 2026-08-06 |
| [[ADR-005-git-bailiff-enforcement-system\|ADR-005]] | Git Bailiff Pre-Commit/Pre-Push Enforcement System | Accepted | 2026-09-22 |
| [[ADR-006-workshop-cli-command-architecture\|ADR-006]] | Workshop Master CLI Command Architecture | Accepted | 2026-09-22 |
| [[ADR-007-zero-clone-cloud-streaming\|ADR-007]] | Zero-Clone Cloud Streaming Protocol | Accepted | 2026-09-22 |

## Creating New ADRs

```bash
# Generate new ADR template
python scripts/workshop.py vault adr new "<title>"

# Or manually create
touch "vault/01 - Architecture Decision Records (ADRs)/ADR-XXX-title-slug.md"
```

## ADR Template

```markdown
---
adrid: ADR-XXX
title: <Title>
status: <Draft | Accepted | Superseded | Deprecated>
date: YYYY-MM-DD
authors: ["Author Name"]
---

# ADR-XXX: <Title>

## Context

## Decision

## Consequences

### Positive

### Negative

## Related

- [[ADR-XXX-previous-decision]]
```

## ADR Creation Protocol

1. **Identify Decision Point**: Major architectural or design choice
2. **Draft Context**: Problem statement, trade-offs, constraints
3. **Define Decision**: Clear description of what was chosen
4. **Analyze Consequences**: Positive and negative impacts
5. **Link Related**: Cross-reference other ADRs
6. **Mark Accepted**: Final status after review

## Status Key

- **Draft**: Proposed, under review
- **Accepted**: Approved and implemented
- **Superseded**: Replaced by newer ADR
- **Deprecated**: No longer relevant, but kept for history