---
name: pinchtab
description: >
  PinchTab — Browser control for AI agents. Standalone HTTP server that gives AI
  agents direct control over Chrome: headless navigation, headed profiles, DOM
  scraping, screenshots, and MCP integration. Use when the user mentions
  PinchTab, browser automation for agents, headless Chrome control, Chrome MCP,
  agent browser server, pinchtab.
  Reference: https://github.com/pinchtab/pinchtab
---

# PinchTab — Browser Control for AI Agents

PinchTab is a small Go binary with an HTTP API that gives AI agents direct control
over Chrome. It is designed to be token-efficient compared to raw DOM or screenshot
pipelines.

## What it does

- Headless navigation and DOM scraping
- Headed Chrome profiles for interactive debugging
- Screenshots, console capture, network inspection
- MCP server for Claude/Codex/Cursor integration
- Site audits (accessibility, Core Web Vitals, broken assets)

## Installation (Windows)

```powershell
# Download the latest release binary
Invoke-WebRequest -Uri "https://github.com/pinchtab/pinchtab/releases/latest/download/pinchtab-windows-amd64.zip" -OutFile "pinchtab.zip"
Expand-Archive -Path "pinchtab.zip" -DestinationPath ".\bin\pinchtab" -Force
```

Or use the official installer:
```powershell
irm https://pinchtab.com/install.ps1 | iex
```

## Quick Start

```powershell
# Run the control-plane server directly
pinchtab server

# Or install as a user-level daemon
pinchtab daemon install

# Navigate and extract content
Invoke-RestMethod -Uri "http://127.0.0.1:8932/v1/navigate" -Method POST -Body (@{ url = "https://example.com" } | ConvertTo-Json) -ContentType "application/json"

# Take a screenshot
Invoke-RestMethod -Uri "http://127.0.0.1:8932/v1/screenshot" -Method POST
```

## MCP Server

PinchTab ships an MCP server. Add it to your MCP config:

```json
{
  "mcpServers": {
    "pinchtab": {
      "command": "npx",
      "args": ["-y", "pinchtab-mcp-server"]
    }
  }
}
```

Or point to the local binary if installed globally.

## Security Notes

- Binds to `127.0.0.1` by default
- Sensitive endpoint families are disabled by default
- IDPI (Integrated Development Privacy Infrastructure) restricts browsing to
  local-only websites until explicitly expanded
- Do NOT expose to the public internet without explicit security review

## Useful Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /v1/navigate` | Navigate to a URL |
| `POST /v1/screenshot` | Take a viewport screenshot |
| `POST /v1/evaluate` | Execute JavaScript in the page |
| `POST /v1/click` | Click an element by selector |
| `POST /v1/type` | Type text into an input |
| `GET /v1/dom` | Get accessible DOM tree |
| `POST /v1/audit` | Full site audit (CWV, a11y, errors) |
