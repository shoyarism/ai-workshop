---
adrid: ADR-004
title: FastMCP Protocol Server Native Integration
status: Accepted
date: 2026-08-06
authors: ["shoyarism", "Antigravity"]
---

# ADR-004: FastMCP Protocol Server Native Integration

## Context

Model Context Protocol (MCP) servers enable LLMs to:
- Access external tools and data sources
- Maintain state across conversations
- Execute agentic workflows

However, traditional MCP implementations suffer from:
- Slow Node.js startup times
- Heavy dependency trees
- No native Python integration

## Decision

Adopt **FastMCP** (Fast Model Context Protocol) as the native server framework:

### Why FastMCP?

| Feature | FastMCP | Traditional MCP |
|---------|---------|-----------------|
| Language | Native Python | Node.js |
| Startup | ~50ms | ~500ms+ |
| Dependencies | Minimal stdlib | Heavy npm install |
| Type Safety | Pydantic | TypeScript/Any |
| Integration | pip install | npm/yarn |

### Core Integration Points

1. **Memory Server**: Persistent conversation state
2. **Fileserver**: Project file browsing
3. **Gitserver**: Repository operations
4. **Browser**: Web automation
5. **Custom Tools**: User-defined MCPs

### Workshop MCP Registry

```python
MCP_REGISTRY = {
    "camofox-browser": {
        "command": ["python", "-m", "camofox_mcp"],
        "port": 9377,
        "features": ["browser", "stealth", "mcp"]
    },
    "browser-use-mcp": {
        "command": ["python", "scripts/mcp_browser_use.py"],
        "port": 9380,
        "features": ["vision", "dom", "automation"]
    }
}
```

## Implementation

### Server Template

```python
from fastmcp import FastMCP

mcp = FastMCP("workshop-tools")

@mcp.tool()
def analyze_code(path: str) -> dict:
    """Run Slop Court analysis on code file."""
    return {"result": "analysis"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Client Integration

```python
import mcp_client

async def list_tools():
    tools = await mcp_client.call("mcp.list_tools")
    return [t["name"] for t in tools]
```

## Consequences

### Positive
- Sub-100ms tool response times
- Native Python debugging (pdb, logging)
- Pydantic validation for all inputs
- Seamless workshop CLI integration

### Negative
- Node.js tools require wrapper scripts
- Some legacy MCPs not yet migrated

## Roadmap

1. Migrate core tools to FastMCP (Q1 2026)
2. Browser automation MCP (Q2 2026)
3. Cloud provider MCPs (Q3 2026)

## Related

- ADR-003: Obsidian Second Brain
- ADR-007: Zero-Clone Cloud Streaming Protocol