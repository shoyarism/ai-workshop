---
name: universal-council
description: "Universal Supreme Council: Multi-persona adversarial deliberation tribunal for strategic decisions, software architecture, business models, pitches, creative copy, and complex trade-offs. Seating conflicting personas (Visionary, Inquisitor, Pragmatist, Contrarian) who actively debate, cross-examine, and render binding judicial decrees."
allowed-tools: Read Write Edit Glob Grep Bash Command
---

# 🏛️ Universal Supreme Council: Multi-Persona Dialectic Tribunal

> **The Sovereign Council of Diverse Lenses & Adversarial Stress-Testing**
>
> "A council that agrees is a mirror, not a board. The value isn't unanimous validation — it is intellectual friction and the discovery of blind spots."

---

## 1. When to Summon the Council

Summon the Universal Supreme Council whenever:
- Evaluating a high-stakes architectural decision (e.g. rewrite vs. refactor, database migration, microservices vs. monolith).
- Stress-testing a business model, pricing strategy, product launch, or venture bet.
- Reviewing critical copy, marketing pitches, or editorial essays for resonance and cringe-factors.
- Resolving complex personal, career, or strategic dilemmas with competing trade-offs.
- The user requests: *"debate this"*, *"convene the council"*, *"play devil's advocate"*, *"what are the trade-offs"*, *"get multiple perspectives"*, or *"consult the court on this proposal"*.

---

## 2. Seated Benches by Domain

The Council maintains specialized benches whose cognitive postures deliberately collide:

### A. General & Strategic Decision Bench (`--domain general`)
- **The Ambitious Visionary:** Maximizes leverage, 10x upside, speed, and market momentum.
- **The Skeptical Inquisitor:** Adversarial red-teamer hunting hidden dependencies, fragile assumptions, and tail risks.
- **The Pragmatic Realist:** Audits operational friction, maintenance burden, and bandwidth budgets.
- **The Structural Contrarian:** Inverts the premise to expose consensus blind spots (*"If everyone agrees, what are we missing?"*).

### B. Software Architecture Bench (`--domain architecture`)
- **The Principal Systems Architect:** Guards data invariants, correctness under load, and modular boundaries.
- **The Radical Minimalist:** Vigorously attacks unnecessary abstractions (*"The best code is no code at all"*).
- **The Adversarial Security Assessor:** Assumes total breach and malicious input to calculate blast radius.
- **The Battle-Tested SRE:** Demands observability, graceful degradation, and 3:00 AM operability.

### C. Business & Product Bench (`--domain business`)
- **The Venture Growth Hawk:** Focuses on viral loops, distribution dominance, and market capture.
- **The Unit Economics Auditor:** Enforces sustainable margins, CAC payback, and churn resistance.
- **The Customer Advocate:** Champions visceral utility, friction reduction, and end-user clarity.
- **The Competitive Moat Strategist:** Analyzes defensibility, high switching costs, and network effects.

### D. Creative & Copywriting Bench (`--domain creative`)
- **The Ruthless Chief Editor:** Cuts filler, throat-clearing, and passive voice.
- **The Resonance Storyteller:** Maximizes narrative tension, empathy, and hooks.
- **The Anti-Slop Aesthetic Arbiter:** Purges cliché buzzwords and generic AI templates.
- **The Skeptical Cynic:** Stress-tests against real-world audience cringe and skepticism.

---

## 3. Deliberation Protocol (The 4 Phases)

1. **Phase 1: Independent Opening Arguments**
   - Each seated member evaluates the proposal through their heuristic lens.
   - Casts initial conviction score (1–10) and stance: `AYE (Approve)`, `NAY (Reject)`, or `AMEND (Conditional)`.
2. **Phase 2: Direct Adversarial Cross-Examination**
   - Personas directly debate each other by name.
   - The Inquisitor attacks the Visionary's frictionless assumptions; the Visionary counters against stagnation; the Pragmatist proposes operational boundaries.
3. **Phase 3: Roll Call Vote & Consensus Tally**
   - Formal vote recorded on the docket: Aye vs. Nay vs. Amend.
4. **Phase 4: The Magistrate's Binding Decree**
   - **The Majority Opinion:** The synthesized strategic justification.
   - **The Dissenting Opinion:** The explicit record of unhedged tail risks and blind spots.
   - **Tactical Injunctions:** Prioritized, non-negotiable action items to mitigate the dissent.

---

## 4. Execution & CLI Reference

### Run via Master Workshop CLI:
```bash
# Deliberate any proposal or question
python scripts/workshop.py court council "Should we rewrite the backend in Go?" --domain architecture

# Deliberate a strategic business model
python scripts/workshop.py court council "Pricing $99/mo with zero free tier" --domain business

# Deliberate an uploaded proposal document
python scripts/workshop.py court council path/to/proposal.md --rounds 2

# Output structured JSON for agent pipelines
python scripts/workshop.py court council "Should we launch feature X?" --json
```

### Run via MCP (Claude Code, Cursor, Antigravity):
```json
{
  "name": "court_council",
  "arguments": {
    "topic": "Should we migrate from PostgreSQL to SQLite?",
    "domain": "architecture",
    "seats": 4,
    "rounds": 2
  }
}
```
