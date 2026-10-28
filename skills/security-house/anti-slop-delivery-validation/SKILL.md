---
name: anti-slop-delivery-validation
description: "Verify UI components, copywriting, and code comments against the 38 Anti-Slop rules and WCAG contrast before shipping"
metadata:
  version: 2.0.0
  author: Workshop Autonomous Engine
---

# Skill: Anti-Slop Delivery Validation

> **First-Principles Distillation**: Formulated from validated task trajectories and grounded in operational invariants.

## 1. Goal & Intent
Verify UI components, copywriting, and code comments against the 38 Anti-Slop rules and WCAG contrast before shipping

## 2. First-Principle Invariants & Axioms
These fundamental truths dictate the success of this skill (cannot be compromised):
- **Axiom**: Every UI element must pass a written functional purpose test
- **Axiom**: Normal text contrast ratio must satisfy WCAG 2.1 AA (>= 4.5:1)

## 3. Operational Execution Protocol
Step-by-step instructions for deterministic reproduction:
1. Run contrast check via workshop.py antislop contrast fg bg
2. Conduct click-through smoke test per R-35
3. Verify 4-Block Delivery Gate report

## 4. Anti-Patterns & Pitfalls (What Fails & Why)
Observed failure modes and the foundational reasons they degrade performance:
- ⚠️ **Anti-Pattern**: Do not use generic purple-indigo gradients without brand identity
- ⚠️ **Anti-Pattern**: Do not write redundant code comments like // calculate total

## 5. Verification & Oracle Checks
Run these commands to deterministically verify skill execution:
```bash
python scripts/workshop.py antislop gate
```

## 6. Multi-Source Grounded Research & Empirical References
Rigorous scientific, architectural, and empirical foundations backing this skill:
- **Peer-Reviewed Journals & Papers**: Literature establishing theoretical bounds, algorithms, and models.
- **RFCs & Engineering Standards**: Official protocol specs (IETF, W3C, ISO, IEEE) ensuring standards compliance.
- **Upstream Source ASTs & Docs**: Official framework specifications and API contracts.
- **Engineering Post-Mortems & Whitepapers**: Production battle-tested solutions from industry leaders.
- **Empirical Benchmarks & Telemetry**: Quantitative measurements and reproducible test results.

- 📚 Shinn et al. (NeurIPS 2023), Reflexion: Language Agents with Verbal Reinforcement Learning
- 📚 W3C (2018), Web Content Accessibility Guidelines (WCAG) 2.1
- 📚 Wang et al. (NeurIPS 2023), Voyager: An Open-Ended Embodied Agent with Large Language Models
