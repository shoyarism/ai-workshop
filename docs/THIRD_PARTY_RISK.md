# 🛡️ Third-Party Skill Supply Chain & Security Risk Advisory

**Workshop OS Specification 3.5 — Security Architecture Group**

---

## 1. Threat Model & Executive Summary

Workshop OS indexes and organizes over 2,140+ agent skills across 7 Sovereign Houses. Because AI agent skills are natural-language instructions parsed directly into LLM agent context, third-party skills represent an **instruction supply-chain surface**.

When adopting skills into production agent harnesses, operators must understand the threat model, isolation boundaries, and defense-in-depth controls built into Workshop OS.

---

## 2. Primary Risk Vectors & Mitigations

### Vector A: Prompt Injection & Instruction Hijacking
- **The Risk**: An unvetted third-party `SKILL.md` file loaded into agent memory could contain adversarial directives (e.g. prompt injection, instruction override, or exfiltration instructions).
- **Workshop OS Defense**:
  - **Modular Context Loading (Tier 0 vs. On-Demand)**: Workshop OS never loads the entire skill catalog into agent memory. Only 35 curated core skills are mounted by default.
  - **Slop Court Gate**: All code and instructions committed to the repository are audited by the Slop Court AST tribunal for secret patterns, malicious eval hooks, and truncated stubs.
  - **Reconnaissance First**: Operators should review specific `SKILL.md` runbooks before granting autonomous execution permissions.

### Vector B: Offensive Security & Pentesting Runbooks
- **The Risk**: The `security-house` and `ops-house` packs vendor educational, forensic, and penetration-testing runbooks (e.g., AD abuse, shadow-credential audit, ransomware defense canaries).
- **Workshop OS Defense**:
  - **Defensive Labeling**: These skills are strictly categorized under `security-house` and intended solely for authorized security audits, penetration testing, and incident response simulations.
  - **No Autonomous Execution**: Skills are static markdown documentation; they cannot execute arbitrary code unless explicitly invoked by a human operator or permitted agent.

### Vector C: Tool Execution & MCP Security Boundaries
- **The Risk**: MCP execution tools (e.g. `verify`) executing arbitrary shell commands without sandbox restrictions.
- **Workshop OS Defense**:
  - **Default-Deny Role Architecture**: MCP write and execution tools (`verify`, `memory_write`) are strictly locked by default. An agent must declare an authorized role (`architect`, `debugger`, `reviewer`, `security-auditor`) via `WORKSHOP_ROLE` to invoke them.
  - **Strict Allowlist Execution (`shell=False`)**: The `verify` tool does NOT invoke a shell (`shell=False`). Commands are tokenized via `shlex.split` and restricted to an explicit binary allowlist (`pytest`, `ruff`, `python`, `git`, `npm`, `uv`, `cargo`, `go`).
  - **Sensitive File Guardrails**: Commands attempting to read `.env`, `.ssh/id_rsa`, or credentials are intercept-blocked before execution.

### Vector D: Installer Script Verification
- **The Risk**: Automated bootstrap scripts (`setup.sh`, `setup.bat`) fetching external package managers.
- **Workshop OS Defense**:
  - Bootstrap scripts download official binaries from [Astral](https://astral.sh) (`uv`). Operators who prefer air-gapped or manual installation can simply install Python 3.11+ and run `uv pip install pyyaml pydantic requests`.

---

## 3. Recommended Operator Checklist

For high-security or corporate deployments:

1. **Keep Default-Deny Active**: Do not expose `WORKSHOP_ROLE=architect` to untrusted agents.
2. **Review Custom Skills**: Inspect individual `SKILL.md` runbooks prior to pinning them to production workflows.
3. **Use Isolated Sandboxes**: Run autonomous agents inside containerized or virtualized environments (e.g., Docker, WSL2, or VM) when granting write permissions.
4. **Run Pre-Flight CI**: Execute `python ci/run_local_ci.py` to verify all cryptographic and judicial invariants.
