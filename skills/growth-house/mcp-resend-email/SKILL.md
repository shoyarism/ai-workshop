---
name: mcp-resend-email
description: Build an MCP server for Resend — send emails, manage domains, templates, audiences, and track events. Use when the user wants AI agents to send transactional or marketing emails via Resend's API through a standardized MCP interface. Triggers on: mcp, model context protocol, resend, email, send email, transactional email, marketing email, templates, audiences, email api, mcp server.
---

# MCP Resend Email Server

Build a Model Context Protocol server that exposes Resend email operations to AI agents. Agents can send transactional and marketing emails, manage domains, templates, and audiences through a standardized tool interface.

## When to trigger

- User wants AI agents to send emails (transactional, marketing, notifications)
- User needs to expose email operations via MCP to Claude Code, Cursor, or other MCP clients
- User is building an email-integrated agent workflow (alerts, reports, outreach)
- User wants tool-based email sending instead of raw API calls

## Prerequisites

```bash
pip install mcp resend python-dotenv
```

Environment variable:

```bash
RESEND_API_KEY=re_...
```

## Basic MCP server structure

```python
# resend_mcp_server.py
import os
import resend
from mcp.server.fastmcp import FastMCP

resend.api_key = os.getenv("RESEND_API_KEY")
mcp = FastMCP("resend-email-server")

@mcp.tool()
def send_email(to: str, subject: str, html: str, text: str | None = None, from_email: str | None = None, reply_to: str | None = None):
    """Send a single email via Resend."""
    params = {
        "from": from_email or "onboarding@resend.dev",
        "to": [to],
        "subject": subject,
        "html": html
    }
    if text:
        params["text"] = text
    if reply_to:
        params["reply_to"] = reply_to
    email = resend.Emails.send(params)
    return {
        "id": email.get("id"),
        "to": to,
        "subject": subject
    }

@mcp.tool()
def send_batch_email(recipients: list[str], subject: str, html: str, from_email: str | None = None):
    """Send the same email to multiple recipients."""
    results = []
    for to in recipients:
        email = resend.Emails.send({
            "from": from_email or "onboarding@resend.dev",
            "to": [to],
            "subject": subject,
            "html": html
        })
        results.append({"id": email.get("id"), "to": to})
    return {"sent": len(results), "results": results}

@mcp.tool()
def send_template_email(to: str, template_id: str, template_data: dict, from_email: str | None = None):
    """Send an email using a Resend template."""
    email = resend.Emails.send({
        "from": from_email or "onboarding@resend.dev",
        "to": [to],
        "template_id": template_id,
        "template_data": template_data
    })
    return {
        "id": email.get("id"),
        "to": to,
        "template_id": template_id
    }

@mcp.tool()
def list_domains():
    """List verified domains in the Resend account."""
    domains = resend.Domains.list()
    return domains.get("data", [])

@mcp.tool()
def list_templates():
    """List email templates."""
    templates = resend.Emails.list()  # templates via API v2
    return templates.get("data", [])

if __name__ == "__main__":
    mcp.run()
```

## MCP client configuration

```json
{
  "mcpServers": {
    "resend": {
      "command": "python",
      "args": ["/path/to/resend_mcp_server.py"],
      "env": {
        "RESEND_API_KEY": "re_..."
      }
    }
  }
}
```

## Best practices

- Use a verified domain for `from_email` in production (not `onboarding@resend.dev`)
- Handle bounce/complaint events via Resend webhooks for production email
- For marketing emails, include an unsubscribe link and honor opt-outs
- Rate-limit batch sends to avoid spam filtering

## Related Workshop skills

- `mcp-stripe-server` — payments MCP server companion
- `emails` — email strategy and sequence design
- `cold-email` — cold outreach email writing
- `mcp-builder` — general MCP server authoring patterns
