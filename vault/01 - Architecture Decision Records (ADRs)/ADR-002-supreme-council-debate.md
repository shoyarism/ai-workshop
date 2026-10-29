---
adrid: ADR-002
title: Universal Supreme Council Multi-Persona Debate Framework
status: Accepted
date: 2026-08-06
authors: ["shoyarism", "Antigravity", "Skeptical Inquisitor", "Radical Minimalist", "UI/UX Craft Architect", "Battle-Tested SRE"]
---

# ADR-002: Universal Supreme Council Multi-Persona Debate Framework

## Context

Single-agent reasoning suffers from:
- **Confirmation bias**: Models agree with themselves
- **Echo chamber effect**: No adversarial stress-testing
- **Blind spot amplification**: Unstated assumptions go unchallenged

Critical decisions (architecture, business, product) require broader cognitive perspectives.

## Decision

Implement a Universal Supreme Council that convenes 4 conflicting cognitive postures for adversarial debate:

### Domain Benches

#### General Court (4 personas)
1. **The Ambitious Visionary** (OPTIMIST) - "What is the 10x upside?"
2. **The Skeptical Inquisitor** (PESSIMIST) - "What kills this? Hidden assumptions?"
3. **The Pragmatic Realist** (PRAGMATIST) - "Maintenance cost, mental bandwidth"
4. **The Structural Contrarian** (SKEPTIC) - "Invert: if everyone agrees, what are we blind to?"

#### Architecture Court (4 personas)
1. **The Principal Systems Architect** (SPECIALIST) - "Data invariants under load"
2. **The Radical Minimalist** (PRAGMATIST) - "Can we delete this entirely?"
3. **The Adversarial Security Assessor** (PESSIMIST) - "Blast radius of breach"
4. **The Battle-Tested SRE** (PRAGMATIST) - "Debugging at 3 AM"

#### Business Court (4 personas)
1. **The Venture Growth Hawk** (OPTIMIST) - "Viral acquisition loop"
2. **The Unit Economics Auditor** (PESSIMIST) - "CAC inflation, runway"
3. **The Customer Advocate** (PRAGMATIST) - "Does user actually care?"
4. **The Competitive Moat Strategist** (SKEPTIC) - "Clone in 48 hours?"

#### Creative Court (4 personas)
1. **The Ruthless Chief Editor** (PRAGMATIST) - "Cut 50% of words"
2. **The Resonance Storyteller** (OPTIMIST) - "Visceral tension, hook"
3. **The Anti-Slop Aesthetic Arbiter** (PESSIMIST) - "Generic AI regurgitation?"
4. **The Skeptical Cynic** (SKEPTIC) - "Will readers cringe?"

### Deliberation Flow
```
[ROUND 1] Opening Arguments (AYE/NAY/AMEND)
[ROUND 2] Cross-Examination (Direct challenges)
[ROUND 3] Voting Tally + Magistrate Decree
```

## Consequences

### Positive
- **Exposes unstated blind spots** before commitment
- **Forces explicit trade-offs** through voting
- **Actionable injunctions** for remediation
- **Domain-specialized** postures

### Negative
- Verbose output for simple decisions
- Requires prompt engineering for each persona

## CLI Interface

```bash
python scripts/workshop.py court council "Should we rewrite in Rust?" --domain architecture
python scripts/workshop.py court council "LAUNCH $99/mo API?" --domain business
```

## Related

- ADR-001: Slop Court Implementation
- ADR-005: Workshop CLI Command Architecture