---
name: cli-anything
description: >
  Make any CLI tool agent-native. Install from CLI-Hub registry or generate new harnesses.
  Triggers: "install CLI", "agent-native CLI", "make CLI work with agents", "cli-hub",
  "generate CLI harness", "make software agent-ready", "CLI-Anything".
  Reference: https://github.com/HKUDS/CLI-Anything
---

# CLI-Anything — Agent-Native CLI Harness Generator

CLI-Anything bridges the gap between AI agents and the world's software by generating agent-native CLIs.

## Quick Install

```bash
# Install CLI-Hub registry
pip install cli-anything-hub

# Browse available CLIs
cli-hub list
cli-hub search <keyword>

# Install a CLI
cli-hub install <name>

# Launch an installed CLI
cli-hub launch <name> [args...]
```

## Installation via npx (for SKILL-compatible agents)

```bash
npx skills add HKUDS/CLI-Anything --skill cli-hub-meta-skill -g -y
```

## Workflow

1. **Search**: `cli-hub search <tool-name>` to find existing harnesses
2. **Install**: `cli-hub install <name>` to add to PATH
3. **Launch**: `cli-hub launch <name> [args...]` to run

## Available Harnesses (examples)

- `blender` - 3D modeling
- `gimp` - Image editing
- `obsidian` - Knowledge management
- `zoom` - Video conferencing
- `n8n` - Workflow automation
- `chromadb` - Vector database
- `ollama` - Local LLMs

## When Registry Lacks Your Tool

Use the 7-phase harness generator:
1. Analyze target software
2. Design CLI commands
3. Implement CLI wrapper
4. Add agent-specific features
5. Generate SKILL.md
6. Test with agent
7. Deploy

## Safety

- Uses subprocess list-form (never shell=True)
- Validates URLs and paths
- Sandboxed execution where available
