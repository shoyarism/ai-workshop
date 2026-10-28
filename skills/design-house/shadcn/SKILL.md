---
name: shadcn
description: Manages shadcn/ui components and projects, providing context, documentation, and usage patterns for building modern design systems.
user-invocable: false
risk: safe
source: https://github.com/shadcn-ui/ui/tree/main/skills/shadcn
date_added: "2026-03-07"
---

# shadcn/ui

A framework for building ui, components and design systems. Components are added as source code to the user's project via the CLI.

> **IMPORTANT:** Run all CLI commands using the project's package runner: `npx shadcn@latest`, `pnpm dlx shadcn@latest`, or `bunx --bun shadcn@latest` — based on the project's `packageManager`. Examples below use `npx shadcn@latest` but substitute the correct runner for the project.

## When to Use
- Use when adding new components from shadcn/ui or community registries.
- Use when styling, composing, or debugging existing shadcn/ui components.
- Use when initializing a new project or switching design system presets.
- Use to retrieve component documentation, examples, and API references.

## Current Project Context

```json
!`npx shadcn@latest info --json 2>/dev/null || echo '{"error": "No shadcn project found. Run shadcn init first."}'`
```

The JSON above contains the project config and installed components. Use `npx shadcn@latest docs <component>` to get documentation and example URLs for any component.

## Principles

1. **Use existing components first.** Use `npx shadcn@latest search` to check registries before writing custom UI. Check community registries too.
2. **Compose, don't reinvent.** Settings page = Tabs + Card + form controls. Dashboard = Sidebar + Card + Chart + Table.
3. **Use built-in variants before custom styles.** `variant="outline"`, `size="sm"`, etc.
4. **Use semantic colors.** `bg-primary`, `text-muted-foreground` — never raw values like `bg-blue-500`.

## Critical Rules

These rules are **always enforced**. Each links to a file with Incorrect/Correct code pairs.