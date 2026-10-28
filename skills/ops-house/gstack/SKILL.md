---
name: gstack
description: "Garry Tan's Y Combinator startup team simulator. Enforces structured roles (CEO for product strategy, EM for architecture, Designer for anti-slop, QA Lead, Release Manager) via slash commands."
userFacing: true
---

# 🏢 gstack: Y Combinator Virtual Startup Team

> **Purpose:** Simulates an entire multi-disciplinary engineering and product organization inside AI coding assistants, enforcing role separation and preventing unchecked solo vibe-coding.

---

## 1. The 5 Core Team Roles & Slash Commands

| Command | Persona Role | Responsibilities |
|---|---|---|
| `/office-hours` | **The CEO** | Challenges the value proposition, user problem, ICP, and MVP scope. Cuts unnecessary complexity before code starts. |
| `/architecture` | **Engineering Manager** | Evaluates data structures, API invariants, modular boundaries, and technical scalability. |
| `/design-review`| **Staff Product Designer**| Audits layout, typography, micro-interactions, and eliminates AI aesthetic clichés. |
| `/qa` | **QA & Test Lead** | Executes edge-case stress tests, boundary checks, and browser click-through smoke tests. |
| `/ship` | **Release Manager** | Verifies clean commits, changelog generation, dependency locks, and production rollouts. |

---

## 2. Operating Protocol

1. **Before Building:** Run `/office-hours` to refine the 1-page PRD.
2. **Before Committing:** Run `/architecture` and `/design-review` to ensure the diff meets senior staff engineering standards.
3. **Before Shipping:** Run `/qa` to confirm tests pass with 0 regressions.
