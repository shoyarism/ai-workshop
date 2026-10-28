---
name: claude-code-setup
description: Analyze project structure and recommend tailored Claude Code automations, skills, hooks, subagents, and Model Context Protocol (MCP) servers.
---

# Claude Code Setup & Project Automation Recommender

Automates the configuration and enhancement of Claude Code and agentic coding harnesses. Analyzes tech stacks, build tools, dependencies, and test setups to recommend matching plugins, MCP servers, and hooks.

## Recommended Integrations
- **Architecture Analysis**: Inspects repository root files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.).
- **MCP Server Matching**: Recommends official and community Model Context Protocol servers for databases, testing frameworks, and cloud providers.
- **Workflow Automation**: Proposes lifecycle hooks (`SessionStart`, `PreToolUse`, `PostToolUse`) and specialized subagents.

## Usage
Refer to `claude-automation-recommender` for the full recommendation pipeline and execution rules.
