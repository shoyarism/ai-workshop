---
name: ai-dev-jobs-mcp
description: "Search 8,400+ AI and ML jobs across 489 companies, inspect listings and employers, match roles, and view salary and market stats via AI Dev Jobs MCP"
category: mcp
risk: safe
source: "https://aidevboard.com"
source_type: community
date_added: "2026-04-16"
author: unitedideas
tags: [mcp, jobs, ai-jobs, ml-jobs, recruiting, job-search, career]
tools: [claude, cursor, gemini]
---

# AI Dev Jobs MCP

## Overview

AI Dev Jobs is a remote MCP server that gives AI agents access to a live index of AI and ML job listings. As of April 17, 2026, the live MCP stats report 8,405 active roles across 489 companies, a $213,500 median salary, and 600 new jobs this week. Agents can search jobs by role, location, or company, retrieve full job details, list hiring companies, match roles to a profile, and get salary or aggregate market statistics. It is designed for AI agents that assist with job searching, recruiting, or labor market analysis.

## When to Use This Skill

- Use when helping a user search for AI or ML engineering jobs
- Use when an agent needs to look up which companies are hiring for specific AI roles
- Use when building recruiting or talent-matching workflows
- Use when analyzing the AI job market (open positions, top companies, role distribution)

## MCP Configuration

Add the AI Dev Jobs MCP server to your client configuration. The endpoint uses streamable HTTP and requires no authentication.

### Claude Desktop / Cursor / Windsurf

```json
{
  "mcpServers": {
    "ai-dev-jobs": {
      "url": "https://aidevboard.com/mcp"
    }
  }
}
```

No API key or authentication is required.

## Available Tools

### `search_jobs`

Search the job index by keyword, location, company, or work arrangement. Returns matching listings with title, company, location, and salary information.

```
search_jobs({ query: "machine learning engineer", location: "remote" })
```

### `get_job`