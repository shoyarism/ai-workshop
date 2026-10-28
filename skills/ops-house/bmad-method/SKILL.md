---
name: bmad-method
description: "Breakthrough Method for Agile AI-Driven Development by Brian Madison. Enforces phased lifecycle gates (Idea -> PRD -> Spec -> Architecture -> Build -> Review) with Scrum and Developer personas."
userFacing: true
---

# 🏗️ BMAD Method: Agile AI Engineering Gates

> **Purpose:** Prevents the "AI slop apocalypse" by guiding software projects through 6 disciplined agile lifecycle stages, keeping humans in the loop at explicit transition checkpoints.

---

## 1. The 6 Phased Stage Gates

```
[ Gate 1: Idea Forge ] ──> [ Gate 2: PRD Synthesis ] ──> [ Gate 3: Spec & Tech Stack ]
                                                                     │
[ Gate 6: Review & Ship ] <── [ Gate 5: TDD Build ] <── [ Gate 4: Architecture Plan ]
```

| Gate | Deliverable | Exit Criteria |
|---|---|---|
| **1. Idea Forge** | Problem brief & audience definition | Clear hypothesis & user validation |
| **2. PRD Synthesis** | User stories, non-goals, functional requirements | Explicit out-of-scope boundaries |
| **3. Tech Spec** | Data models, schemas, component interfaces | Zero ambiguous endpoints |
| **4. Architecture** | System topology, sequence flows, failure modes | Verified scalability and security model |
| **5. TDD Build** | Modular code + automated unit/integration tests | 100% test pass rate |
| **6. Review & Ship**| Code review, linting, security audit, changelog | Clean git commit & zero felonies |

---

## 2. Invariant Rules

- Never begin coding (Gate 5) without a signed-off Tech Spec (Gate 3) and Architecture Plan (Gate 4).
- Each gate requires human sign-off before proceeding to the next phase.
