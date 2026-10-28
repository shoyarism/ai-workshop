---
name: agent-tool-builder
description: Tools are how AI agents interact with the world. A well-designed
  tool is the difference between an agent that works and one that hallucinates,
  fails silently, or costs 10x more tokens than necessary. This skill covers
  tool design from schema to error handling.
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Agent Tool Builder

Tools are how AI agents interact with the world. A well-designed tool is the
difference between an agent that works and one that hallucinates, fails
silently, or costs 10x more tokens than necessary.

This skill covers tool design from schema to error handling. JSON Schema
best practices, description writing that actually helps the LLM, validation,
and the emerging MCP standard that's becoming the lingua franca for AI tools.

Key insight: Tool descriptions are more important than tool implementations.
The LLM never sees your code - it only sees the schema and description.

## Principles

- Description quality > implementation quality for LLM accuracy
- Aim for fewer than 20 tools - more causes confusion
- Every tool needs explicit error handling - silent failures poison agents
- Return strings, not objects - LLMs process text
- Validation gates before execution - reject, fix, or escalate, never silent fail
- Test tools with the LLM, not just unit tests

## Capabilities

- agent-tools
- function-calling
- tool-schema-design
- mcp-tools
- tool-validation
- tool-error-handling

## Scope

- multi-agent-coordination → multi-agent-orchestration
- agent-memory → agent-memory-systems
- api-design → api-designer
- llm-prompting → prompt-engineering

## Tooling

### Standards

- JSON Schema - When: All tool definitions Note: The universal format for tool schemas
- MCP (Model Context Protocol) - When: Building reusable, cross-platform tools Note: Anthropic's open standard, widely adopted

### Frameworks