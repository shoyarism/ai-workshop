---
name: ecc
description: >
  ECC (Agent Harness Operating System) — gives AI agents a coordinated engineering
  system: plan before build, verify with tests, review work, remember what matters,
  turn wins into reusable skills. 68 agents, 286 skills, 94 commands, hooks,
  memory, continuous learning, and AgentShield security scanning.
  Use when the user mentions ECC, agent harness, engineering system for AI,
  agent workflow orchestration, automated code review, TDD for agents,
  epic management, skill health, agent memory.
  Reference: https://github.com/affaan-m/ECC
---

# ECC — Agent Harness Operating System

ECC gives AI agents a coordinated engineering system:

```
plan -> test -> implement -> review -> verify -> remember -> improve
```

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| Agents | 68 | Planning, review, build repair, security, architecture |
| Skills | 286 | TDD, research, security, docs, frontend, data, ML, ops |
| Commands | 94 | Convenient entry points |
| Hooks & Memory | Runtime | Enforcement, session summaries, continuous learning |
| Rules | Selective | Always-loaded standards by language or project |
| AgentShield | Included | Scanning for prompts, hooks, MCP config, permissions, secrets |

## Installation

```powershell
# Via npm (Universal)
npm install -g ecc-universal

# Via Claude Code plugin
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

## Core Commands

| Command | What it does |
|---------|-------------|
| `/plan` | Restate requirements, assess risks, write step-by-step plan — waits for confirmation before touching code |
| `/plan-canvas` | Open a plan in the browser for annotate-and-approve review |
| `/feature-dev` | Guided feature development with architecture focus |
| `/code-review` | Review local changes or GitHub PR |
| `/build-fix` | Detect and fix build errors, delegates to right agent |
| `/quality-gate` | Quality gate check against project standards |
| `/test-coverage` | Analyze coverage, identify gaps, generate missing tests |
| `/evolve` | Continuous improvement loop — learn from past sessions |
| `/sessions` | View and manage agent sessions |
| `/security-scan` | AgentShield security scanning |
| `/skill-health` | Audit and improve your skills |
| `/instinct-status` | View learned patterns and instincts |
| `/learn` | Continuous learning from past work |

## Platform Support

ECC provides adapters for: Claude Code, Codex, Cursor, OpenCode, Gemini, Zed,
GitHub Copilot, Antigravity, Qwen, and other harnesses.

## Skills Directory

Skills are installed into the workspace at:
`.\skills\ECC\commands\`

Key skill categories:
- **Build**: go-build, rust-build, cpp-build, flutter-build, react-build, etc.
- **Review**: python-review, go-review, rust-review, react-review, etc.
- **Test**: go-test, rust-test, flutter-test, react-test, etc.
- **Workflow**: plan, epic-decompose, epic-publish, multi-execute, etc.
- **Security**: security-scan, harness-audit, code-review
