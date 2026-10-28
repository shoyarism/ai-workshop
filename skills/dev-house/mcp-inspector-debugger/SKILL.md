---
name: mcp-inspector-debugger
description: Interactive developer test harness and diagnostic UI for Model Context Protocol (MCP) servers using the official MCP Inspector.
---

# MCP Server Inspector & Debugger

The official MCP Inspector provides an interactive developer web UI and CLI harness to test MCP tools, list resources, verify prompts, and inspect JSON-RPC traffic.

## Usage
`ash
# Launch MCP Inspector for a stdio server
npx @modelcontextprotocol/inspector node path/to/server.js

# Test Python MCP server
npx @modelcontextprotocol/inspector python -m my_mcp_server
`
