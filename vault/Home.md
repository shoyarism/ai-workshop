# 🧠 WORKSHOP OS — OBSIDIAN SECOND BRAIN VAULT
**Master Hub** | **Local-First Cognitive Engine** | **Plaintext AST + Git Versioning**

---

## 📁 Vault Structure

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `00 - Meta/` | Environment & Identity | User DNA, System Profile, Agent Configs |
| `01 - Architecture Decision Records (ADRs)/` | Immutable Architecture Decisions | ADR-001+, YAML frontmatter, status tracking |
| `02 - Post-Mortems/` | Error Forensics & Fixes | PM-001+, root cause, fix verification, prevention |
| `03 - Project Context/` | Active Project State | Specs, decisions, context for multi-session work |
| `04 - Tasks & Sprints/` | Work Management | Autonomous queue, session handoffs, sprint plans |

---

## 🔗 Quick Navigation

### Architecture Decisions
- [[01 - Architecture Decision Records (ADRs)/README.md|Architecture Decision Records]]

### Error Post-Mortems
- [[02 - Post-Mortems/README.md|Error Post-Mortems]]

### Active Context
- [[03 - Project Context/README.md|Project Context]]

### Task Queue
- [[04 - Tasks & Sprints/Autonomous Task Queue & Session Handoffs.md|Task Queue & Sprints]]

### Meta
- [[00 - Meta/User DNA & Environment Profile.md|User DNA & Environment Profile]]

---

## 📋 Vault Protocols

### ADR Creation
```bash
python scripts/workshop.py vault adr new "<title>"
```

### Post-Mortem Creation
```bash
python scripts/workshop.py vault postmortem new "<title>"
```

### Search Vault
```bash
python scripts/workshop.py vault search "<query>"
```

---

## 🏛️ Governance

- **Immutable**: ADRs and Post-Mortems are append-only after merge
- **Versioned**: All changes tracked via git in the Workshop repository root
- **Cross-Session**: Survives agent restarts, context clears, /clear commands
- **MCP Accessible**: `memory_recall` / `memory_write` tools for agents

---

## 📊 Health Metrics

| Metric | Target | Status |
|--------|--------|--------|
| ADR Coverage | ≥ 1 per major decision | 🟢 Active |
| Post-Mortem Coverage | 100% of P0/P1 incidents | 🟢 Active |
| Search Latency | < 10ms (SSD) | 🟢 Active |
| Git Sync | Auto on commit | 🟢 Active |

---

*Vault Initialized: 2026-10-28 | Workshop OS v2.2.0*