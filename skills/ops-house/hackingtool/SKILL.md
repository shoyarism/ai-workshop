---
name: hackingtool
description: >
  AI-guided, all-in-one security testing toolkit. 215 curated tools across 21
  categories — recon, OSINT, web, wireless, phishing, forensics, post-exploitation
  and more — with an AI layer that turns plain English into the right tool and
  the exact command. Use when the user mentions hackingtool, security testing,
  penetration testing toolkit, authorized security testing, OSINT tools, CTF
  tools, red team tools, blue team tools, bug bounty tools.
  Reference: https://github.com/Z4nzu/hackingtool
---

# HackingTool — AI-Guided Security Testing Toolkit

215 curated tools across 21 categories with an AI layer that turns plain English
into the right tool and the exact documented command.

**Built for**: penetration testers, red teamers, blue-team/SOC and DFIR analysts,
OSINT researchers, bug-bounty hunters, CTF players, security researchers and students.
All working **legally, on systems they own or are authorised to test**.

## Tool Categories

- Reconnaissance & OSINT
- Web Application Testing
- Wireless Attacks
- Social Engineering / Phishing
- Forensics & Incident Response
- Post-Exploitation
- Vulnerability Analysis
- Password Attacks
- SQL Injection
- XSS & Web Exploits
- DDoS Tools
- Remote Access
- Reporting & Documentation
- ...and 7 more categories (63 tags total)

## Installation

```bash
# From source with pipx (recommended)
pipx install hackingtool

# Or directly
pip install hackingtool

# Docker
docker run -it z4nzu/hackingtool
```

## Quick Commands

```bash
hackingtool              # Launch interactive TUI
hackingtool /find <query>  # Search the 215-tool catalog
hackingtool /goal <objective>  # Plan and execute an engagement step by step
hackingtool /recommend   # Say what you want in plain English, get tool+command
```

## AI-Guided Features

### `/find` — Tool discovery
Searches the 215-tool catalog first, then the GitHub API, showing real maintained
projects ranked by relevance.

### `/goal` — Objective planner
Plans an engagement step by step: recon -> enumeration -> exploitation -> reporting.

### `/recommend` — Plain English to commands
Say "find subdomains of example.com" and get the exact tool + documented command.

## Safety Guarantees

- Standard installs, **no `curl | bash`**
- Downloads pinned + SHA-256 verified
- List-form `subprocess`, no forced `sudo`
- Signed releases with SBOM
- Nothing auto-executes and nothing is fabricated
