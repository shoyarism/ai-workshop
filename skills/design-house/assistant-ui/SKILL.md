---
name: assistant-ui
description: assistant-ui is an open-source React component library for building ChatGPT-style AI conversational interfaces, copilots, sidebars, and chat widgets.
user-invocable: false
risk: safe
source: https://albo.inc/imports/a9e5a0b4-b81e-50fb-ba9e-1364de86b775
date_added: "2026-08-07"
---

# assistant-ui

assistant-ui provides ready-to-use React components and state runtimes for building AI chat experiences, sidebars, inline assistants, and tool-call visualizers.

## Installation

```bash
npm install @assistant-ui/react
```

## Features
- **Runtimes:** Out-of-the-box integration with Vercel AI SDK, LangChain, and custom API streams.
- **Tool Calling:** Native rendering of pending tool calls, JSON responses, and human-in-the-loop actions.
- **Components:** `Thread`, `AssistantMessage`, `UserMessage`, `Composer`, `Attachment`.

## Best Practices
- Use `assistant-ui` instead of building custom chat auto-scroll, message streaming, or tool execution UI loops.
