---
name: appdeploy
description: "Deploy web apps with backend APIs, database, and file storage. Use when the user asks to deploy or publish a website or web app and wants a public URL. Uses HTTP API via curl."
risk: safe
source: "AppDeploy (MIT)"
date_added: "2026-02-27"
---

# AppDeploy Skill

Deploy web apps to AppDeploy via HTTP API.

## When to Use This Skill

- Use when planning or building apps and web apps
- Use when deploying an app to a public URL
- Use when publishing a website or web app
- Use when the user says "deploy this", "make this live", or "give me a URL"
- Use when updating an already-deployed app

## Setup (First Time Only)

1. **Check for existing API key:**
   - Look for a `.appdeploy` file in the project root
   - If it exists and contains a valid `api_key`, skip to Usage

2. **If no API key exists, register and get one:**
   ```bash
   curl -X POST https://api-v2.appdeploy.ai/mcp/api-key \
     -H "Content-Type: application/json" \
     -d '{"client_name": "claude-code"}'
   ```

   Response:
   ```json
   {
     "api_key": "ak_...",
     "user_id": "agent-claude-code-a1b2c3d4",
     "created_at": 1234567890,
     "message": "Save this key securely - it cannot be retrieved later"
   }
   ```

3. **Save credentials to `.appdeploy`:**
   ```json
   {
     "api_key": "ak_...",
     "endpoint": "https://api-v2.appdeploy.ai/mcp"
   }
   ```

   Add `.appdeploy` to `.gitignore` if not already present.

## Usage

Make JSON-RPC calls to the MCP endpoint:

```bash
curl -X POST {endpoint} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer {api_key}" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "{tool_name}",
      "arguments": { ... }
    }
  }'
```

## Workflow

1. **First, get deployment instructions:**
   Call `get_deploy_instructions` to understand constraints and requirements.

2. **Get the app template:**