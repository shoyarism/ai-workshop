---
name: github-skill-scanner
description: Automatically discover, search, audit, and install high-quality agent skills from GitHub repositories conforming to the Agent Skills and Anthropic specification.
---

# GitHub Skill Scanner & Automated Curator

Autonomous intelligence skill for discovering, evaluating, and installing agent skills from GitHub.

## Core Capabilities
- **GitHub Search Matrix**: Scans GitHub Code and Repositories for `SKILL.md` files matching domain requirements.
- **Spec Verification**: Validates YAML frontmatter, naming conventions, and description length (<1024 characters).
- **Safety Screening**: Inspects scripts for malicious downloaders, unauthenticated execution loops, or suspicious network calls.
- **One-Command Installation**: Clones or downloads validated skills directly into `Workshop/skills/`.

## Execution Patterns
```bash
# Search for skills across GitHub
python scripts/scan_github_skills.py search "pentesting"

# Discover curated agent skill repositories
python scripts/scan_github_skills.py curate --topic "agent-skills"

# Install a skill from GitHub
python scripts/scan_github_skills.py install "<raw_url_to_SKILL.md>" --name "new-skill" --desc "Description of new skill"
```
