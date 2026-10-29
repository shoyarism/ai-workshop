---
adrid: ADR-003
title: Obsidian Second Brain Persistent Memory System
status: Accepted
date: 2026-08-06
authors: ["shoyarism", "Knowledge Synthesizer"]
---

# ADR-003: Obsidian Second Brain Persistent Memory System

## Context

LLM sessions suffer from:

1. **Context Amnesia**: Every session restarts from scratch
2. **No memory of past decisions**: Architectural choices lost
3. **No episodic error tracking**: Same bugs recur
4. **Knowledge fragmentation**: Learnings scattered across repos

## Decision

Implement a **Local-First Obsidian Second Brain** vault with:

### Directory Structure

```
vault/
├── 00 - Meta/
│   ├── User DNA & Environment Profile.md
│   └── Agent Configs/
├── 01 - Architecture Decision Records (ADRs)/
│   ├── ADR-001-slug.md
│   ├── ADR-002-slug.md
│   └── ADR-003-slug.md
├── 02 - Post-Mortems/
│   ├── PM-001-summary.md
│   └── PM-002-summary.md
├── 03 - Project Context/
│   ├── Specs.md
│   └── Decisions.md
└── 04 - Tasks & Sprints/
    ├── Autonomous Task Queue.md
    └── Session Handoffs.md
```

### Wiki-Link Protocol

All cross-references use Obsidian wikilinks:
```markdown
See [[ADR-001-slop-court-implementation]] for the judicial tribunal design.
Related: [[ADR-002-supreme-council-debate#Section]]
```

### Integration Points

1. **MCP Memory Server**: `memory_recall`/`memory_write` tools
2. **Git Hooks**: Auto-commit entries on ADR/Post-Mortem creation
3. **CLI Access**: `python scripts/workshop.py vault search "<query>"`
4. **Agent Prompts**: Direct reference to vault paths in system prompts

## Consequences

### Positive
- **Cross-session memory**: Persists through /clear commands
- **Immutable history**: ADRs append-only, traceable decisions
- **Searchable knowledge**: Fast lexical search via `vault search`
- **MCP accessible**: Programmatic memory access for agents

### Negative
- Learning curve for wikilink syntax
- Maintenance overhead for large vaults
- Requires careful namespace management

## Related

- ADR-001: Slop Court Implementation
- ADR-006: Git Bailiff Enforcement System