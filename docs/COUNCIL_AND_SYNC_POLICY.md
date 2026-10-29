# 🏛️ SUPREME COUNCIL SPECIFICATION & VENDORED SKILL SYNC POLICY

> Operational manual for the Universal Supreme Council multi-persona dialectic engine and the lifecycle maintenance policy for vendored skills across the 7 Sovereign Houses.

---

## 1. Universal Supreme Council: Operational Specification

The **Universal Supreme Council** (`workshop court council` / `scripts/workshop_council.py`) is an adversarial multi-persona dialectic engine designed to eliminate confirmation bias and single-model blind spots before committing to critical engineering decisions.

### 1.1 The 4 Cognitive Personas

1. **The Skeptical Inquisitor:** Red-teams assumptions, maps cascading failure modes, identifies catastrophic tail risks, and probes boundary invariants.
2. **The Radical Minimalist:** Enforces YAGNI (You Aren't Gonna Need It) and the KISS principle. Targets bloated dependencies, unnecessary microservices, and premature abstraction.
3. **The UI/UX Craft Architect:** Defends typographic hierarchy, spatial cadence, responsive predictability, and WCAG AA accessibility compliance.
4. **The Zero-Trust SRE:** Assumes catastrophic infrastructure failure at 3 AM. Mandates idempotency, graceful backpressure, circuit breakers, and structured telemetry.

### 1.2 Model Routing & Provider Configuration

The Council supports dynamic provider routing configured via environment variables:

| Provider | Supported Models | Environment Variable | Default Model |
| :--- | :--- | :--- | :--- |
| **OpenRouter (Default)** | Claude 3.5 Sonnet, GPT-4o, Llama 3.3 70B | `OPENROUTER_API_KEY` | `anthropic/claude-3.5-sonnet` |
| **Anthropic Direct** | Claude 3.5 Sonnet, Claude 3.5 Haiku | `ANTHROPIC_API_KEY` | `claude-3-5-sonnet-latest` |
| **Google Gemini** | Gemini 1.5 Pro, Gemini 2.0 Flash | `GEMINI_API_KEY` | `gemini-1.5-pro` |
| **OpenAI Direct** | GPT-4o, GPT-4o-mini | `OPENAI_API_KEY` | `gpt-4o` |
| **Offline Heuristic Engine** | Built-in Rule Engine (Zero-Cost) | *None required* | Deterministic Local Matrix |

### 1.3 Token Economics & Cost Estimates

Each 4-persona adversarial deliberation executes a multi-turn synthesis:

* **Prompt Context:** ~1,200 tokens (system prompts, persona schemas, problem context).
* **Generation Context:** ~600–900 tokens (deliberation across 4 perspectives + final synthesis).
* **Estimated Cost per Deliberation:**
  * Claude 3.5 Sonnet: `~$0.016 USD`
  * Gemini 1.5 Pro: `~$0.005 USD`
  * Gemini 2.0 Flash: `~$0.0008 USD`
  * **Offline Heuristic Mode:** **`$0.00 USD` (Free / Instant)**

### 1.4 Offline Zero-Cost Fallback Mode

If no API keys are exported in the environment, the Council does not crash. It automatically engages the **Offline Heuristic Matrix**, synthesizing domain-specific architectural guidance, tradeoff checklists, and anti-pattern warnings derived from the Second Brain's episodic post-mortems (`vault/02 - Post-Mortems/`).

---

## 2. Vendored Skills Maintenance & Sync Policy

Workshop OS curates **2,147 verified skills** organized into the **7 Sovereign Houses**. Because vendored material is susceptible to ecosystem drift and upstream deprecation, the following operational lifecycle is enforced:

### 2.1 Upstream Source Tracking & Attribution

* Every borrowed or adapted skill repository is documented in [`VENDORED_LICENSES.md`](../VENDORED_LICENSES.md).
* Original license terms (MIT, Apache-2.0, BSD-3-Clause) are preserved verbatim within each sub-package.
* Skill files must conform to the standard YAML frontmatter specification (`name`, `description`, `metadata`).

### 2.2 Cryptographic Integrity Gate

* All skill files are continuously fingerprinted into `skills/manifest.sha256`.
* The CI pipeline (`test_skills_manifest.py`) verifies that 100% of discovered skills match their recorded SHA-256 digests.
* Any unvetted manual modification or accidental file corruption immediately halts the CI build.

### 2.3 Upstream Synchronization Cadence

* **Security & Vulnerability Sweeps (Continuous):** Automated scans via GitHub Dependabot, `pip-audit`, and Slop Court secret detectors intercept CVEs and exposed test keys.
* **Quarterly Semantic Upgrades:** Upstream skill packs are reviewed every quarter against their primary origin repositories.
* **Deprecation & Pruning Protocol:** Skills targeting deprecated APIs or unsupported framework versions are isolated into `deprecated/` or pruned during major version milestones.

### 2.4 Contributing New Skills

To submit a new skill to one of the 7 Sovereign Houses:
1. Model your file on the reference template in [`examples/02_skill_template/SKILL.md`](../examples/02_skill_template/SKILL.md).
2. Run `python scripts/workshop_skills.py` to regenerate `skills/manifest.sha256`.
3. Submit a pull request verified by `workshop court trial --staged`.
