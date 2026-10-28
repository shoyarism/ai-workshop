---
name: coucou-integration
description: |
  Integrate Coucou (Mochi) notch/menubar AI session monitor with Antigravity, Hermes, and OpenCode desktop apps.
  Installs coucou hooks for live session monitoring, approvals, and chat from the notch/menubar.
  Repository: https://github.com/Louis-CFM/coucou
---

# Coucou Integration Skill

## Overview

Coucou is a tiny companion (Mochi) that lives in your macOS notch, Windows menubar, or Linux top-edge and keeps an eye on your AI coding agent sessions. It shows live session state, file diffs, approval requests, and lets you chat with agents without leaving your current context.

**Repository:** https://github.com/Louis-CFM/coucou  
**Website:** https://louis-cfm.github.io/coucou/  
**iPhone App:** TestFlight beta (Live Activities, Dynamic Island, widgets, Siri)

---

## Features

- 🤖 **Multi-agent support** — Claude Code, Cursor, Codex, Gemini CLI, Antigravity, Hermes, OpenCode
- ✅ **Approve from notch/menubar** — Allow/Deny/Always for permissions; pick answers for questions
- 📊 **Live diffs** — See file modifications with +N/−M counts in ticker
- 💬 **Chat with any model** — Anthropic, Google AI, OpenAI, Ollama, LM Studio
- 📱 **iPhone companion** — Lock Screen, Dynamic Island, widgets, Face ID approvals
- 🔒 **Private by design** — Keys in Keychain/Credential Manager/Secret Service, no telemetry

---

## Installation

### Quick Install (All Agents)

```bash
# Dry run to preview
python scripts/coucou_integration.py dry-run

# Install hooks for Antigravity, Hermes, OpenCode
python scripts/coucou_integration.py install

# Verify installation
python scripts/coucou_integration.py verify
```

### Individual Agent Install

```bash
python scripts/coucou_integration.py install --agent antigravity
python scripts/coucou_integration.py install --agent hermes
python scripts/coucou_integration.py install --agent opencode
```

### Generate CLAUDE.md Section

```bash
python scripts/coucou_integration.py claude-md
```

---

## Supported Platforms

| Platform | Hook Executable | Socket Path |
|----------|----------------|-------------|
| macOS (GitHub) | `nb-hook` | `~/Library/Application Support/NotchBuddy/nb.sock` |
| macOS (App Store) | `nb-hook` | `~/Library/Containers/fr.louisraille.Coucou/Data/nb.sock` |
| Windows | `coucou-hook.exe` | `\\.\pipe\coucou-<user-SID>` |
| Linux | `~/.local/share/coucou/bin/coucou-hook` | `$XDG_RUNTIME_DIR/coucou.sock` |

---

## Hook Events

All standard Claude Code hook events except `PermissionRequest`:

| Event | Effect |
|-------|--------|
| `SessionStart` | Creates pill, sets state to idle |
| `UserPromptSubmit` | State → thinking; prompt in ticker |
| `PreToolUse` | State → working; tool label in ticker |
| `PostToolUse` / `PostToolUseFailure` | State → working |
| `Notification` | Rate-limit or question state |
| `Stop` | State → finished (5s), declared pills reset to idle |
| `StopFailure` | State → error |
| `SessionEnd` | Declared pills reset to idle |
| `SubagentStart` / `SubagentStop` | Step added to ticker |

---

## Declared Pills (Persistent)

Agents checked in **Settings → Active pills** persist across sessions:

- `agent_antigravity` — Antigravity/agy
- `agent_gemini` — Gemini CLI
- `agent_cursor` — Cursor
- `agent_codex` — Codex (GitHub build only)

---

## Configuration Files Created

### Windows
- `%LOCALAPPDATA%\gemini\config\hooks.json` (Antigravity)
- `%LOCALAPPDATA%\hermes\hooks.json` (Hermes)
- `%LOCALAPPDATA%\opencode\hooks.json` (OpenCode)

### macOS
- `~/.gemini/config/hooks.json` (Antigravity)
- `~/.config/hermes/hooks.json` (Hermes)
- `~/.config/opencode/hooks.json` (OpenCode)

### Linux
- `~/.gemini/config/hooks.json` (Antigravity)
- `~/.config/hermes/hooks.json` (Hermes)
- `~/.config/opencode/hooks.json` (OpenCode)

---

## Quick Test

```bash
# Windows
echo '{"hook_event_name":"UserPromptSubmit","session_id":"t1","prompt":"hello","coucou_agent":"demo"}' ^
  | coucou-hook.exe --agent demo

# macOS/Linux
echo '{"hook_event_name":"UserPromptSubmit","session_id":"t1","prompt":"hello","coucou_agent":"demo"}' \
  | nb-hook --agent demo
```

A "demo" pill should appear in the notch/menubar.

---

## Coucou + Workshop OS Integration

This skill integrates with Workshop OS through:

1. **AGENTS.md** — Section 6 documents the coucou integration
2. **scripts/coucou_integration.py** — Installation and verification script
3. **Workshop hooks** — Can be chained with workshop safety gates

### Workshop Hook Chain Example

```json
{
  "hooks": {
    "PreToolUse": [
      { "type": "command", "command": "coucou-hook.exe --agent antigravity" },
      { "type": "command", "command": "python scripts/workshop_hooks.py pre-tool" }
    ]
  }
}
```

---

## Requirements

- Coucou desktop app installed (download from GitHub Releases)
- Python 3.10+ for integration script
- Agent apps (Antigravity, Hermes, OpenCode) configured with hook support

---

## Troubleshooting

### Hook executable not found
```
⚠ coucou hook executable NOT found: coucou-hook.exe
```
**Fix:** Install Coucou from https://github.com/Louis-CFM/coucou/releases

### Hooks not triggering
1. Verify agent app is restarted after hook installation
2. Check hook config JSON syntax
3. Ensure coucou app is running (menu bar/notch icon visible)

### PermissionRequest not working for third-party agents
This is a known limitation — approval cards only work for Claude Code currently. Other agents re-ask in terminal.

---

## Related Skills

- `agent-reach` — Internet research for coucou updates
- `workshop-operating-loop` — 6-stage discipline including verification
- `verification-before-completion` — Verify hooks work before declaring done

---

## License

Coucou code: MIT  
Coucou assets (name, Mochi character, icon, sounds): © Louis Raillé, all rights reserved

This integration skill: MIT