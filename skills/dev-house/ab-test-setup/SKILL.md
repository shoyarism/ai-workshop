---
name: ab-test-setup
description: "Structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness."
risk: unknown
source: community
date_added: "2026-02-27"
---

# A/B Test Setup

## 1️⃣ Purpose & Scope

Ensure every A/B test is **valid, rigorous, and safe** before a single line of code is written.

- Prevents "peeking"
- Enforces statistical power
- Blocks invalid hypotheses

---

## 2️⃣ Pre-Requisites

You must have:

- A clear user problem
- Access to an analytics source
- Roughly estimated traffic volume

### Hypothesis Quality Checklist

A valid hypothesis includes:

- Observation or evidence
- Single, specific change
- Directional expectation
- Defined audience
- Measurable success criteria

---

### 3️⃣ Hypothesis Lock (Hard Gate)

Before designing variants or metrics, you MUST:

- Present the **final hypothesis**
- Specify:
  - Target audience
  - Primary metric
  - Expected direction of effect
  - Minimum Detectable Effect (MDE)

Ask explicitly:

> “Is this the final hypothesis we are committing to for this test?”

**Do NOT proceed until confirmed.**

---

### 4️⃣ Assumptions & Validity Check (Mandatory)

Explicitly list assumptions about:

- Traffic stability
- User independence
- Metric reliability
- Randomization quality
- External factors (seasonality, campaigns, releases)

If assumptions are weak or violated:

- Warn the user
- Recommend delaying or redesigning the test

---

### 5️⃣ Test Type Selection

Choose the simplest valid test:

- **A/B Test** – single change, two variants
- **A/B/n Test** – multiple variants, higher traffic required
- **Multivariate Test (MVT)** – interaction effects, very high traffic
- **Split URL Test** – major structural changes

Default to **A/B** unless there is a clear reason otherwise.

---

### 6️⃣ Metrics Definition

#### Primary Metric (Mandatory)

- Single metric used to evaluate success
- Directly tied to the hypothesis
- Pre-defined and frozen before launch