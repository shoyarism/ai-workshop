---
name: slop-court
description: "Slop Court v2.0: Supreme Adversarial AI Quality Tribunal & Legal System. Enforces multi-agent judicial review, AST code smell analysis, 3-juror deliberation, and cryptographic acquittal proofs before code can be committed or pushed."
allowed-tools: Read Write Edit Glob Grep Bash Command
---

# ⚖️ Slop Court v2.0: Supreme Adversarial AI Quality Tribunal

> **The Sovereign Multi-Agent Quality Tribunal for Autonomous AI Agents**
> 
> "No code shall be committed, no PR opened, and no deliverable shipped without a verifiable Certificate of Acquittal from the Slop Court."

---

## 1. Architectural Mission & Theoretical Grounding

Based on 2025–2026 peer-reviewed literature (*CourtEval*, *SCBench*, *MacroscopeBench*, and *Unanimous LLM Juries*), single-agent prompt evaluations produce self-preference echo chambers.

**Slop Court v2.0** models code evaluation as an adversarial courtroom trial across 4 distinct chambers:
1. **The Grand Prosecutor:** High-sensitivity AST smell and pattern analysis.
2. **The Adversarial Defense Counsel:** Rigorous context evaluation, testing mitigations, and false-positive exemptions.
3. **The 3-Juror Bench:** Multi-perspective consensus across **Craft & Tone**, **Architecture & AST**, and **Security & Invariants**.
4. **The Chief Magistrate:** Calculates the Slop Index (0.0% to 100.0%) and issues binding rulings (`ACQUITTED WITH HONORS`, `REMANDED`, `CONTEMPT OF COURT`).
5. **The Cryptographic Docket:** Generates tamper-evident SHA-256 signed acquittal certificates (`.court_docket/`).
6. **The Bailiff:** Git pre-commit and pre-push physical interceptor.

```
                              ┌────────────────────────────────────────┐
                              │       CODIFIED PENAL CODE v2.0         │
                              │  AST Smells | Tautologies | Felonies   │
                              └───────────────────┬────────────────────┘
                                                  │
                         ┌────────────────────────┴───────────────────────┐
                         ▼                                                ▼
              ┌─────────────────────┐                          ┌─────────────────────┐
              │   THE PROSECUTOR    │                          │   DEFENSE COUNSEL   │
              │  AST Smell Scanners │  ◄── Adversarial Cross ──► Context Mitigations │
              │   Entropy Metrics   │       Examination        │  Pragmas & Shims    │
              └──────────┬──────────┘                          └──────────┬──────────┘
                         │                                                │
                         └────────────────────────┬───────────────────────┘
                                                  │
                                                  ▼
                                 ┌──────────────────────────────────┐
                                 │       THE JURY BENCH (3 LENSES)  │
                                 │  • Juror 1: Craft & Hygiene      │
                                 │  • Juror 2: Architecture & AST   │
                                 │  • Juror 3: Security & Invariant │
                                 └────────────────┬─────────────────┘
                                                  │
                                                  ▼
                                 ┌──────────────────────────────────┐
                                 │      THE CHIEF MAGISTRATE        │
                                 │    Calculates Slop Index v2      │
                                 │    Issues Binding Ruling         │
                                 └────────────────┬─────────────────┘
                                                  │
                         ┌────────────────────────┴───────────────────────┐
                         ▼                                                ▼
              ┌─────────────────────┐                          ┌─────────────────────┐
              │     THE BAILIFF     │                          │ CRYPTOGRAPHIC DOCKET│
              │ Git Pre-Commit/Push │                          │  SHA-256 Acquittal  │
              │  Hard Interceptor   │                          │  Audit Certificate  │
              └─────────────────────┘                          └─────────────────────┘
```

---

## 2. Codified Penal Code (v2.0 Statutes)

### Title I: Capital Slop Felonies (Automatic Gate Rejection - Exit Code 1)
Any single sustained Felony immediately results in **CONTEMPT OF COURT**, blocking commits and pushes:

| Statute | Domain | Title | Penalty | Offense Invariant |
| :--- | :--- | :--- | :---: | :--- |
| **FEL-01** | CRAFT | Truncated Code Fraud | 50 pts | Lazy placeholder stubs (`// ... existing code ...`, `/* rest unchanged */`, `# rest of code`). |
| **FEL-02** | ARCHITECTURE | Lazy Function Stubbing | 40 pts | Functions containing only `pass`, `TODO`, or `throw NotImplementedError` instead of implemented logic. |
| **FEL-03** | SECURITY | Naked Exception Blackhole | 35 pts | Silent error swallowing (`except: pass`, empty `catch (e) {}`) without logging, telemetry, or rethrow. |
| **FEL-04** | CRAFT | Fabricated Telemetry | 30 pts | Synthetic marketing metrics (`10M+ users`, `99.9% uptime`) without verifiable telemetry tagging. |
| **FEL-05** | CRAFT | Sycophantic AI Preamble | 30 pts | Conversational throat-clearing (`Certainly!`, `As an AI language model`, `Here is the code you requested`). |
| **FEL-06** | SECURITY | Plaintext Secret Exposure | 100 pts | Committed tokens (`ghp_`, `github_pat_`, `AKIA`, private keys). |

### Title II: Slop Misdemeanors (Craft, Structural & Aesthetic Smells)
Accumulation of > 5 Misdemeanors or Slop Index > 15% results in Contempt of Court:

| Statute | Domain | Title | Penalty | Offense Invariant |
| :--- | :--- | :--- | :---: | :--- |
| **MIS-01** | CRAFT | Tautological Comments | 10 pts | Comments repeating syntax verbatim (`// increment counter`, `// return result`, `# import libraries`). |
| **MIS-02** | CRAFT | Banned AI Clichés | 10 pts | `seamlessly`, `cutting-edge`, `revolutionize`, `game-changer`, `supercharge`, `delve into`, `testament to`. |
| **MIS-03** | CRAFT | Unearned AI Gradients | 15 pts | Generic Tailwind/CSS purple-indigo gradients (`from-purple-500 to-indigo-500`, `#6366f1` to `#a855f7`). |
| **MIS-04** | CRAFT | Bento Box Syndrome | 10 pts | Generic identical 3-card layout without semantic hierarchy or content differentiation. |
| **MIS-05** | ARCHITECTURE | Wildcard / Naked Imports | 10 pts | `from module import *` or untyped `any` destroying AST clarity. |
| **MIS-06** | ARCHITECTURE | Extreme Control Flow Nesting | 15 pts | Deeply nested control flow (> 5 levels of control flow) indicating unrefactored patches and structural erosion. |

### Title III: Infractions
- **INF-01 (CRAFT):** Excessive trailing whitespace or 3+ consecutive empty lines.
- **INF-02 (ARCHITECTURE):** Public API missing contract docstring.
- **INF-03 (ARCHITECTURE):** God-function anomaly (> 150 statements).

---

## 3. The 3-Juror Deliberation Bench

1. **Juror 1: Craft & Tone**
   - Assesses comment hygiene, copywriting, tone, and UI design craft.
   - Requires zero clichés and clean typography/token hierarchy.
2. **Juror 2: Architecture & AST**
   - Assesses control flow nesting, god functions, modular boundaries, and import cleanliness.
   - Requires clean AST structures and separation of concerns.
3. **Juror 3: Security & Failure Invariants**
   - Assesses credential leakage, naked exception blackholes, and unhandled promise rejections.
   - Requires explicit failure modes and zero secret exposure.

---

## 4. Master CLI Reference

```bash
# 1. Convene a full trial with 3-juror deliberation
python scripts/workshop.py court trial path/to/code [--staged]

# 2. Inspect 3-juror voting breakdown
python scripts/workshop.py court jury path/to/code

# 3. View historical cases and cryptographic SHA-256 certificates
python scripts/workshop.py court docket
python scripts/workshop.py court docket --case CR-20261027-B521

# 4. View Prosecutor's Bill of Indictment
python scripts/workshop.py court indict path/to/code

# 5. Deploy / check the Git Bailiff interceptor
python scripts/workshop.py court bailiff install
python scripts/workshop.py court bailiff status

# 6. Automated Code Rehabilitation
python scripts/workshop.py court reform path/to/file.py

# 7. Print codified Penal Code
python scripts/workshop.py court statutes
```

---

## 5. Defense Immunity Pragmas

When an exception is genuinely required (e.g. test harnesses, platform shims):
```python
except (AttributeError, ValueError):  # @court-exempt: intentional platform shim
    pass
```
```python
# pragma: no-slop-court
```
```html
<!-- court: exempt -->
```
