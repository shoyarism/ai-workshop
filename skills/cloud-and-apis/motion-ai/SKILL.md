---
name: motion-ai
description: Motion AI is an automated motion design framework and MCP tool for generating video assets, promotional clips, and animations directly within AI agents like Claude.
user-invocable: false
risk: safe
source: https://albo.inc/imports/bd314169-7480-5635-93e9-e20f6e86dab7
date_added: "2026-08-07"
---

# Motion AI & Claude MCP Integration

Motion AI automates motion graphics and video editing via text prompts and Model Context Protocol (MCP) integrations inside Claude.

## Integration via MCP

Add the Motion connector to your Claude configuration (`claude.json` / MCP Settings):

```json
{
  "mcpServers": {
    "motion": {
      "command": "npx",
      "args": ["-y", "@motion-ai/mcp-server"]
    }
  }
}
```

## Capabilities
- **Prompt-to-Video:** Generate motion graphics, video ads, and animated captions using natural language prompts.
- **Automated Workflow:** Trigger video render pipelines from AI chat prompts without opening manual video editing software.
