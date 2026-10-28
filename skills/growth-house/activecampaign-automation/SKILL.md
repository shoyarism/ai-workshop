---
name: activecampaign-automation
description: "Automate ActiveCampaign tasks via Rube MCP (Composio): manage contacts, tags, list subscriptions, automation enrollment, and tasks. Always search tools first for current schemas."
risk: critical
source: community
date_added: "2026-02-27"
---

# ActiveCampaign Automation via Rube MCP

Automate ActiveCampaign CRM and marketing automation operations through Composio's ActiveCampaign toolkit via Rube MCP.

## Prerequisites

- Rube MCP must be connected (RUBE_SEARCH_TOOLS available)
- Active ActiveCampaign connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `active_campaign`
- Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas

## Setup

**Get Rube MCP**: Add `https://rube.app/mcp` as an MCP server in your client configuration. No API keys needed — just add the endpoint and it works.


1. Verify Rube MCP is available by confirming `RUBE_SEARCH_TOOLS` responds
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `active_campaign`
3. If connection is not ACTIVE, follow the returned auth link to complete ActiveCampaign authentication
4. Confirm connection status shows ACTIVE before running any workflows

## Core Workflows

### 1. Create and Find Contacts

**When to use**: User wants to create new contacts or look up existing ones

**Tool sequence**:
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - Search for an existing contact [Optional]
2. `ACTIVE_CAMPAIGN_CREATE_CONTACT` - Create a new contact [Required]

**Key parameters for find**:
- `email`: Search by email address
- `id`: Search by ActiveCampaign contact ID
- `phone`: Search by phone number

**Key parameters for create**:
- `email`: Contact email address (required)
- `first_name`: Contact first name
- `last_name`: Contact last name
- `phone`: Contact phone number
- `organization_name`: Contact's organization
- `job_title`: Contact's job title
- `tags`: Comma-separated list of tags to apply

**Pitfalls**:
- `email` is the only required field for contact creation