# 🛡️ Security Policy & Threat Model

## 1. Supported Versions

| Version | Supported          | Status |
| ------- | ------------------ | ------ |
| 3.5.x   | :white_check_mark: | Active Release (Sovereign Houses Architecture) |
| < 3.5   | :x:                | Deprecated |

---

## 2. Threat Model & Operational Boundaries

Workshop OS is an engineering orchestration layer and skill catalog designed to empower autonomous coding agents. Understanding its threat model and execution boundaries is essential for secure operation.

### A. Command Guardrails vs. Sandboxing
- **Advisory Pre-Flight Guardrails**: The regex filters in `workshop_hooks.py` and the MCP `verify` tool (`check_command_safety`) are designed to catch **accidental human and AI errors** (e.g., recursive root deletions, accidental `.env` exfiltration, and disk format commands).
- **Not an Operating System Sandbox**: Pattern matching and blocklists are **speed bumps, not security containers**. They cannot prevent intentional adversarial evasion (e.g., using alternate interpreters or encoded commands).
- **Container Isolation Requirement**: When granting an agent shell execution access (`shell=True`) on untrusted repositories or with third-party models, operators **MUST** run the agent inside an isolated container (Docker, Podman, or Firecracker microVM) with restricted network egress and mounted non-root permissions.

### B. Container Operation & Recommended Isolation Setup
Workshop OS includes a pre-configured [`Dockerfile`](Dockerfile) and [`docker-compose.yml`](docker-compose.yml) to facilitate rapid containerized execution:
```bash
# Build and run isolated containerized runtime diagnostics:
docker compose run --rm runtime

# Start sandboxed local browser and gateway hubs:
docker compose up -d hub
```
This isolates agent subprocess spawning, file-system mutations, and local gateway bindings from your primary host system.

### C. Skill Supply Chain & Prompt Injection
- **Markdown-as-Code**: Skills in Workshop OS are structured Markdown documents (`SKILL.md`) that serve as system instructions for LLM agents.
- **Supply Chain Risks**: Loading unreviewed third-party skills or synchronizing external skill repositories can expose agents to indirect prompt injection or malicious workflow guidance.
- **Audit Mandate**: Operators should inspect skill manifests and run `python scripts/workshop.py court trial <path>` before promoting community skills into production agent contexts.

### C. Security House Artifacts
- The `skills/security-house/` directory bundles forensic triage, defensive monitoring, vulnerability auditing, and offensive security playbooks (such as canaries and privilege escalation assessments).
- **Authorized Use Only**: These playbooks are provided strictly for defensive engineering, authorized penetration testing, forensic incident response, and security posture validation.

### D. Automated Setup Scripts
- `setup.sh` and `setup.bat` facilitate rapid installation by downloading Astral `uv` via official distribution endpoints (`https://astral.sh/uv/install.sh` / `https://astral.sh/uv/install.ps1`).
- In hardened, air-gapped, or regulated environments, operators are advised to pre-install `uv` and `python >= 3.11` manually through corporate package managers.

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability, credential leak, or critical defect in Workshop OS, please disclose it responsibly. Do **NOT** open a public issue.

### Safe Reporting Protocol
1. Email details directly to `shoyarism@proton.me` or contact the lead maintainer via verified channels.
2. Include full reproduction steps, affected environment specifications, and proof-of-concept manifests where applicable.
3. Acknowledgments are sent within 24 hours. Validated fixes and advisory notes are published within 72 hours.
