---
name: mcp-ecosystem-master
description: Model Context Protocol (MCP) ecosystem engineer. Use when managing, configuring, authoring, and troubleshooting MCP servers, tool schemas, and transports.
---

# MCP Ecosystem Master Skill

This skill guides agents in discovering, testing, configuring, and authoring Model Context Protocol (MCP) servers.

## 1. Quick Testing & Management

Use the workshop MCP launcher to verify or start any server:

```bash
# List all registered MCP servers
python scripts/mcp_launcher.py list

# Test if an MCP server responds cleanly
python scripts/mcp_launcher.py test playwright
python scripts/mcp_launcher.py test memory
```

## 2. Supported Transports

1. **Stdio (Standard I/O)**: Local subprocesses communicating via newline-delimited JSON-RPC over stdin/stdout.
2. **SSE (Server-Sent Events)**: HTTP streaming server for remote or gateway-bridged MCP tools (e.g. OmniRoute on port 20128).

## 3. Registering New MCP Servers

Add server configurations to `kilo.jsonc` and `opencode.json` under the `"mcp"` section:

```jsonc
"mcp": {
  "my-custom-tool": {
    "type": "local",
    "command": ["npx", "-y", "my-mcp-package"],
    "enabled": true
  }
}
```
