---
source: "https://github.com/iOfficeAI/AionUi"
name: aion-ui
description: "Use when the user wants to launch or interact with AionUi — the open-source 24/7 AI agent cowork app by iOfficeAI. AionUi is a desktop GUI companion to OfficeCLI, supporting Claude Code, Codex, OpenCode, OpenClaw, Gemini CLI, Hermes, and 20+ CLI agents. Use when building agent teams, managing multi-agent workflows, or when the user mentions AionUi, agent cowork app, or agent team management."
risk: unknown
---

# AionUi Skill

[GitHub](https://github.com/iOfficeAI/AionUi) · ⭐ 32,472 · TypeScript · Apache-2.0

AionUi is the open-source 24/7 Cowork app for OpenClaw, Hermes, Claude Code, Codex, OpenCode, and 20+ more CLI Agents. Customize your assistants, team them up, and run them in a visual desktop environment.

## Install

```bash
# Download from GitHub Releases
# https://github.com/iOfficeAI/AionUi/releases
# Or via their installer script (if available)
curl -fsSL https://aionui.ai/install.sh | bash
```

## When to Use

- User wants to **launch AionUi** or needs it installed
- User wants to **create an agent team** or configure multiple AI agents to work together
- User mentions **AI cowork app**, **agent desktop**, or **agent management UI**
- User wants a **visual interface** for managing OfficeCLI-generated documents alongside other agents
- User needs to **orchestrate multiple CLI agents** (Claude Code + Codex + Gemini CLI together)

## Key Features

| Feature | Description |
|---------|-------------|
| Multi-Agent Teams | Team up Claude Code, Codex, Gemini CLI, OpenCode, Hermes, and 20+ agents |
| OfficeCLI Integration | Deep integration with OfficeCLI for document automation |
| Custom Assistants | Customize agent personalities, skills, and tool access |
| 24/7 Operation | Run agents continuously in the background |
| Visual Workspace | Desktop GUI for monitoring and controlling agents |

## Commands

```bash
# Launch AionUi
aionui

# Check version
aionui --version

# List available agent templates
aionui agents list
```

## Relationship to OfficeCLI

AionUi is the **GUI companion** to [OfficeCLI](../officecli/SKILL.md). When both are installed:

- AionUi provides the visual workspace and agent orchestration
- OfficeCLI provides the document automation backend
- Together they form a complete AI-powered office suite

## Agent Compatibility

| Agent | Supported |
|-------|-----------|
| Claude Code | ✅ |
| Codex (OpenAI) | ✅ |
| Gemini CLI | ✅ |
| OpenCode | ✅ |
| OpenClaw | ✅ |
| Hermes | ✅ |
| Cursor | ✅ |
| GitHub Copilot | ✅ |

## Resources

- **GitHub**: https://github.com/iOfficeAI/AionUi
- **Releases**: https://github.com/iOfficeAI/AionUi/releases
- **Website**: https://aionui.ai
