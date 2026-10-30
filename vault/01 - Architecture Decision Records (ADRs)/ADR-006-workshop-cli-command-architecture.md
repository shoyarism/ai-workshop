---
adrid: ADR-006
title: Workshop Master CLI Command Architecture
status: Accepted
date: 2026-09-22
authors: Claude Code, Antigravity
related:
  - ADR-001: Slop Court Judicial Quality Tribunal Implementation
  - ADR-005: Git Bailiff Pre-Commit/Pre-Push Enforcement System
---

# ADR-006: Workshop Master CLI Command Architecture

## Decision

**We will implement a unified CLI command architecture for the Workshop OS master CLI (`scripts/workshop.py`) following a subcommand pattern with extensible plugin architecture.**

## Status

Accepted on 2026-09-22 after peer review by Slop Court and Architectural Council.

## Context

The Workshop OS requires a unified entry point for all 50+ commands spanning:
- `search`: Query 2,140+ domain skills
- `doctor`: Comprehensive system health diagnostics
- `council`: Multi-persona adversarial deliberation
- `court`: Slop Court quality tribunal
- `vault`: Obsidian vault operations
- `graphify`: AST knowledge graph exploration

The challenge is maintaining a single, coherent CLI interface while allowing domain teams to extend functionality without centralized bottlenecks.

## Decision Drivers

1. **Single Source of Truth**: One master CLI entry point (`scripts/workshop.py`)
2. **Subcommand Pattern**: `workshop.py <command> [args]` for discoverability
3. **Plugin Architecture**: Commands auto-discovered from `scripts/` directory
4. **Domain Routing**: Sovereign Houses own their command namespaces
5. **Backward Compatibility**: Existing command invocations unchanged

## Considered Options

| Option | Description | Decision |
|--------|-------------|----------|
| Monolithic | Single file with all commands | Rejected - no extensibility |
| Subcommand CLI | `workshop.py court trial ...` | **Accepted** - standard pattern |
| Plugin Registry | Commands in separate modules | Accepted - complementary approach |
| HTTP Gateway | REST API for all operations | Rejected - local workflow focus |

## Solution

### Command Namespace Structure

```
workshop.py
├── search <query>                    # Skill search
├── doctor                           # Health diagnostics
├── council convene <query>          # Supreme Council debates
├── court trial <path> [--staged]    # Slop Court trials
├── court bailiff install            # Git hooks
├── court reform <file>              # Code cleanup
├── vault adr new <title>           # ADR creation
├── vault postmortem new <title>    # PM creation
├── vault search <query>            # Vault queries
├── see <file>                       # Multimodal inspection
└── graphify query <question>       # AST exploration
```

### Architecture Layers

```
┌─────────────────────────────────┐
│     Master CLI Entry Point      │ scripts/workshop.py
├─────────────────────────────────┤
│    Command Dispatcher (argparse)│
├─────────────────────────────────┤
│  Domain-Specific Handlers       │ scripts/*_domain*.py
│  - workshop_search.py           │
│  - workshop_court.py            │
│  - workshop_council.py          │
│  - workshop_doctor.py           │
│  - workshop_vault.py            │
└─────────────────────────────────┘
```

### Plugin Discovery Pattern

```python
def load_command_handlers():
    """Auto-discover command handlers from scripts directory."""
    handlers = {}
    for module in Path("scripts").glob("workshop_*.py"):
        if module.stem != "workshop":
            handler = importlib.import_module(f"scripts.{module.stem}")
            if hasattr(handler, "register_commands"):
                handler.register_commands(subparser)
    return handlers
```

### Sovereign House Command Ownership

| House | Commands | Maintainer Role |
|-------|----------|-----------------|
| Security House | `court`, `council`, search | Security lead |
| Dev House | `vault`, `doctor`, `graphify` | Dev lead |
| Design House | `see` | Design lead |
| Ops House | All | Ops lead |

## Implementation Plan

1. **Phase 1**: Consolidate existing CLI entry points into `workshop.py`
2. **Phase 2**: Implement subcommand dispatcher with argparse
3. **Phase 3**: Add plugin discovery mechanism
4. **Phase 4**: Document command ownership per Sovereign House
5. **Phase 5**: Add `--help` command discovery

## Consequences

### Positive
- Unified command discovery: `workshop.py --help` shows all commands
- Domain autonomy: Each house maintains their commands
- Extensibility: New commands added via plugin pattern
- Backward compatible: Existing invocations work unchanged

### Negative
- Slight startup overhead for plugin discovery
- Need coordination when adding commands to same namespace

## Monitoring

Success metrics:
- `workshop.py --help` completes in < 500ms
- All commands discoverable without memorization
- No breaking changes to existing CI/CD workflows

## Related Decisions

- [[ADR-001-slop-court-implementation|ADR-001]] - Slop Court command structure (`court trial`, `court bailiff`)
- [[ADR-005-git-bailiff-enforcement-system|ADR-005]] - Git Bailiff enforcement commands
- [[ADR-007-zero-clone-cloud-streaming|ADR-007]] - Zero-Clone streaming commands

## Approval

Approved by Architectural Council on 2026-09-22:
- Claude Code (Architect)
- Skeptic Person (Reviewer)  
- Security Person (Reviewer)
- Operator Person (Reviewer)

---
*Co-Authored-By: Claude Code & Antigravity*