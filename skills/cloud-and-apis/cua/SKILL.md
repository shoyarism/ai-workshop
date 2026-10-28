---
name: cua
description: >
  Cua — Scale computer-use 2.0 with open-source drivers, cross-OS fleets, and
  benchmarks for training, evaluation, and data generation. Provides background
  computer-use on macOS, Windows, and Linux. Drive native desktop apps in the
  background. Includes sandbox SDK, benchmarks, and Lume macOS VM management.
  Use when the user mentions cua, computer use agent, desktop automation, screen
  scraping, UI automation for AI, computer use 2.0, sandbox automation.
  Reference: https://github.com/trycua/cua
---

# Cua — Computer-Use 2.0 for AI Agents

Scale computer-use with open-source drivers, cross-OS fleets, and benchmarks for
training, evaluation, and data generation.

## Components

| Package | Description |
|---------|-------------|
| `cua-driver` | Background computer-use agent for macOS, Windows, Linux |
| `cua-agent` | AI agent framework for computer-use tasks |
| `cua-sandbox` | SDK for creating and controlling sandboxes |
| `cua-bench` | Benchmarks and RL environments for computer-use |
| `lume` | macOS/Linux VM management on Apple Silicon |

## Installation

### Cua Driver (background desktop automation)

```powershell
# Windows
irm https://cua.ai/driver/install.ps1 | iex

# macOS / Linux
/bin/bash -c "$(curl -fsSL https://cua.ai/driver/install.sh)"
```

### Cua Sandbox SDK

```bash
pip install cua
# Requires Python 3.11+
```

## Quick Start

```python
from cua import Sandbox, Image

async with Sandbox.ephemeral(Image.linux()) as sb:
    result = await sb.shell.run("echo hello")
    screenshot = await sb.screenshot()
    await sb.mouse.click(100, 200)
    await sb.keyboard.type("Hello from Cua!")
    await sb.mobile.gesture((100, 500), (100, 200))  # multi-touch gestures
```

## Supported Runtimes

| Runtime | Linux Container | Linux VM | macOS | Windows | Android |
|---------|----------------|----------|-------|---------|---------|
| Cloud (cua.ai) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Local (QEMU) | ✅ | ✅ | ✅ | ✅ | ✅ |

## Lume — macOS Virtualization

```bash
# Install Lume
/bin/bash -c "$(curl -fsSL https://cua.ai/lume/install.sh)"

# Create and start a macOS VM
curl -L "$(lume ipsw | tail -n 1)" -o ~/Downloads/macos-tahoe.ipsw
lume create macos-tahoe --ipsw ~/Downloads/macos-tahoe.ipsw --unattended tahoe
lume run macos-tahoe
```

## Cua-Bench — Evaluation

```bash
# Install
git clone https://github.com/trycua/cua && cd cua/cua-bench
uv tool install -e . && cb image create linux-docker

# Run benchmark
cb run dataset datasets/cua-bench-basic --agent cua-agent --max-parallel 4
```

## MCP Integration

Cua provides an MCP server for agent integration. Add to your MCP config:

```json
{
  "mcpServers": {
    "cua": {
      "command": "cua",
      "args": ["mcp"]
    }
  }
}
```
