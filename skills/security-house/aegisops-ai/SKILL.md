---
name: aegisops-ai
description: "Autonomous DevSecOps & FinOps Guardrails. Orchestrates Gemini 3 Flash to audit Linux Kernel patches, Terraform cost drifts, and K8s compliance."
risk: safe
source: community
author: Champbreed
date_added: "2026-03-24"
---

# /aegisops-ai — Autonomous Governance Orchestrator

AegisOps-AI is a professional-grade "Living Pipeline" 
that integrates advanced AI reasoning directly into 
the SDLC. It acts as an intelligent gatekeeper for 
systems-level security, cloud infrastructure costs, 
and Kubernetes compliance.

## Goal

To automate high-stakes security and financial audits by:
1. Identifying logic-based vulnerabilities (UAF, Stale 
State) in Linux Kernel patches.
2. Detecting massive "Silent Disaster" cost drifts in 
Terraform plans.
3. Translating natural language security intent into 
hardened K8s manifests.

## When to Use
- **Kernel Patch Review:** Auditing raw C-based Git diffs for memory safety.
- **Pre-Apply IaC Audit:** Analyzing `terraform plan` outputs to prevent bill spikes.
- **Cluster Hardening:** Generating "Least Privilege" securityContexts for deployments.
- **CI/CD Quality Gating:** Blocking non-compliant merges via GitHub Actions.

## When Not to Use

- **Web App Logic:** Do not use for standard web vulnerabilities (XSS, SQLi); use dedicated SAST scanners.
- **Non-C Memory Analysis:** The patch analyzer is optimized for C-logic; avoid using it for high-level languages like Python or JS.
- **Direct Resource Mutation:** This is an *auditor*, not a deployment tool. It does not execute `terraform apply` or `kubectl apply`.
- **Post-Mortem Analysis:** For analyzing *why* a previous AI session failed, use `/analyze-project` instead.

---
## 🤖 Generative AI Integration

AegisOps-AI leverages the **Google GenAI SDK** to implement a "Reasoning Path" for autonomous security and financial audits: