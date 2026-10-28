---
name: github-ecosystem-recon
description: Autonomous discovery, monitoring, and inspection of GitHub repositories, trending AI frameworks, topics, and software releases. Use when researching open-source repositories, checking star velocity, or inspecting release notes.
---

# GitHub Ecosystem Reconnaissance Skill

This skill provides operational patterns, invariants, and CLI commands for inspecting the **GitHub open-source software ecosystem** (`https://github.com`).

---

## 1. Interface & Commands

```bash
# 1. Inspect trending repositories by AI topic
uv run python scripts/workshop.py github trending --topic agents --limit 10
uv run python scripts/workshop.py github trending --topic llm --limit 10
uv run python scripts/workshop.py github trending --topic tools --limit 10

# 2. Search GitHub repositories with stars/forks/languages
uv run python scripts/workshop.py github search "mcp server" --limit 10
uv run python scripts/workshop.py github search "web agent" --sort stars

# 3. Deeply inspect repository statistics, releases, and licenses
uv run python scripts/workshop.py github inspect browser-use/browser-use
uv run python scripts/workshop.py github inspect OpenHands/openhands
```

---

## 2. Invariants & Ground Truths

1. **Anonymous Rate Limits**:
   - Unauthenticated GitHub API calls are capped at 60 requests per hour per IP. For high-volume automated CI workflows, supply `GITHUB_TOKEN` in headers.
2. **Release Version Extraction**:
   - Inspecting `/releases/latest` provides the authoritative tag name (e.g. `0.13.10`), which should be checked before pulling submodules or upgrading local dependencies.
