---
source: "https://github.com/imxv/Pretty-mermaid-skills"
name: pretty-mermaid-skills
description: "Use when the user wants to generate beautiful Mermaid diagrams as SVG, PNG, or terminal ASCII. Supports 15 themes, 6 diagram types, batch rendering, and works with Claude Code, Cursor, Codex, Gemini CLI, and other AI agents. Triggers: 'pretty mermaid', 'mermaid diagram', 'render mermaid', 'beautiful diagram', 'mermaid SVG', 'terminal ASCII diagram'."
risk: low
---

# Pretty Mermaid Skills

[GitHub](https://github.com/imxv/Pretty-mermaid-skills) · ⭐ 1,171 · Node.js · MIT

AI Agent Skill to generate and render beautiful Mermaid diagrams as SVG or terminal ASCII — 15 themes, 6 diagram types, batch CLI, no browser required.

## Install

```bash
# Install via skills.sh (recommended for AI agents)
npx skills add imxv/pretty-mermaid-skills@pretty-mermaid -g -y

# Or install globally
npm install -g pretty-mermaid
```

## When to Use

- User wants to **render Mermaid diagrams** as SVG, PNG, or ASCII
- User needs **themed diagrams** (15 built-in themes)
- User wants **batch rendering** of multiple diagrams
- User needs diagrams in **terminal/ASCII** format
- User mentions **Pretty Mermaid**, **mermaid rendering**, or **diagram generation**

## Quick Start

```bash
# Render a Mermaid diagram to SVG
pretty-mermaid 'flowchart TD\n  A --> B' --output diagram.svg

# Render to PNG
pretty-mermaid 'flowchart TD\n  A --> B' --output diagram.png

# Render to terminal ASCII
pretty-mermaid 'flowchart TD\n  A --> B' --format ascii

# Use a theme
pretty-mermaid 'flowchart TD\n  A --> B' --theme tokyo-night --output diagram.svg
```

## Supported Diagram Types

| Type | Syntax | Example |
|------|--------|---------|
| Flowchart | `flowchart` | Decision trees, process flows |
| Sequence | `sequenceDiagram` | API call flows, interactions |
| State | `stateDiagram-v2` | State machines, lifecycle |
| Class | `classDiagram` | UML class diagrams |
| ER | `erDiagram` | Database schemas |
| XY Chart | `xychart-beta` | Charts and graphs |

## 15 Built-in Themes

| Light Themes | Dark Themes | Other |
|-------------|-------------|-------|
| zinc-light | zinc-dark | nord |
| tokyo-night-light | tokyo-night | nord-light |
| catppuccin-latte | tokyo-night-storm | dracula |
| github-light | catppuccin-mocha | one-dark |
| solarized-light | github-dark | |
| | solarized-dark | |

## Batch Rendering

```bash
# Render multiple diagrams from a file
pretty-mermaid diagrams.mmd --batch --output-dir ./renders/

# diagrams.mmd format:
# ---
# theme: tokyo-night
# ---
# flowchart TD
#   A --> B

# ---
# theme: catppuccin-mocha
# ---
# sequenceDiagram
#   Alice ->> Bob: Hello
```

## CLI Reference

```bash
pretty-mermaid <mermaid-code> [options]

# Options
--output, -o <file>     # Output file path
--format, -f <svg|png|ascii>  # Output format (default: svg)
--theme <theme>         # Theme name (default: zinc-dark)
--batch                 # Enable batch mode
--output-dir <dir>      # Directory for batch output
--width <px>            # Image width (for PNG)
--height <px>           # Image height (for PNG)
--help, -h              # Show help
--version, -v           # Show version
```

## AI Agent Integration

Seamlessly integrates with:

| Agent | Integration |
|-------|-------------|
| Claude Code | ✅ Via npx skills |
| Cursor | ✅ Via MCP |
| Codex | ✅ Via CLI |
| Gemini CLI | ✅ Via CLI |
| OpenCode | ✅ Via CLI |
| qoder | ✅ Via CLI |
| Antigravity | ✅ Via CLI |

## Common Use Cases

```bash
# Architecture diagram for documentation
pretty-mermaid 'flowchart LR\n  Client --> API\n  API --> DB\n  API --> Cache' \
  --theme tokyo-night --output arch.svg

# Sequence diagram for API docs
pretty-mermaid 'sequenceDiagram\n  User->>API: POST /login\n  API->>DB: Query user\n  DB-->>API: User found\n  API-->>User: Token' \
  --theme catppuccin-mocha --output flow.svg

# Class diagram for code docs
pretty-mermaid 'classDiagram\n  class Animal {\n    +String name\n    +makeSound()\n  }\n  class Dog {\n    +fetch()\n  }\n  Animal <|-- Dog' \
  --theme github-light --output classes.svg

# ER diagram for database docs
pretty-mermaid 'erDiagram\n  CUSTOMER ||--o{ ORDER : places\n  ORDER ||--|{ ITEM : contains\n  CUSTOMER {string name}\n  ORDER {int id date}\n  ITEM {string name float price}' \
  --theme nord --output schema.svg
```

## Compare: Pretty Mermaid vs mermaid-cli

| Feature | Pretty Mermaid | mermaid-cli |
|---------|---------------|-------------|
| Themes | 15 curated | Basic |
| ASCII output | ✅ | ❌ |
| Batch rendering | ✅ | ❌ |
| Browser required | ❌ | ✅ (Chromium) |
| AI agent skills | ✅ Pre-built | ❌ |
| Node.js | ✅ | ✅ |
| npm install | ✅ | ✅ |

Use **Pretty Mermaid** when you need beautiful themed diagrams without a browser. Use **mermaid-cli** for basic rendering with full browser control.

## Resources

- **GitHub**: https://github.com/imxv/Pretty-mermaid-skills
- **Skills.sh**: https://www.skills.sh/imxv/pretty-mermaid-skills/pretty-mermaid
- **Theme Gallery**: https://github.com/imxv/Pretty-mermaid-skills/blob/main/docs/THEME_GALLERY.md
