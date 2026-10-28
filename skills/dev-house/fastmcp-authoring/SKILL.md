---
name: fastmcp-authoring
description: Rapid authoring, testing, and deployment of Model Context Protocol (MCP) servers using FastMCP v4 in Python.
---

# FastMCP Server Authoring & Deployment

FastMCP provides an intuitive, high-level Pythonic interface to build and expose MCP servers for AI agents in under 15 lines of code.

## Quickstart Template

```python
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Workshop-Tools")

@mcp.tool()
def add_task(title: str, priority: int = 1) -> str:
    """Add a new task to the Workshop task queue."""
    return f"Task '{title}' added with priority {priority}."

@mcp.resource("workshop://config")
def get_config() -> str:
    """Retrieve active Workshop configuration."""
    return '{"workspace": ".", "status": "active"}'

if __name__ == "__main__":
    mcp.run()
```

## Running & Testing

```powershell
# Run with FastMCP CLI (stdio)
uv run python server.py

# Inspect with MCP Inspector
npx @modelcontextprotocol/inspector uv run python server.py
```
