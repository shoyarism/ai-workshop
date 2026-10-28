---
name: repomix
description: Pack entire codebases, directories, or scoped modules into a single, AI-friendly, token-efficient format with security scrubbing and compression.
---

# Repomix: Codebase Context Packing for AI Agents

Repomix is a developer CLI tool that packs entire codebases into structured XML, Markdown, or plain text formats, specifically designed for LLMs and AI agent prompts.

## Core Capabilities
- **AI-Optimized Output**: Formats files with hierarchical metadata, token counts, and file-tree manifests.
- **Security Scrubbing**: Automatically detects and redacts secret keys, credentials, and sensitive tokens.
- **Token Compression**: Strips unnecessary comments, whitespace, and formatting to maximize context window capacity.
- **Synergy with Graphify**:
  - Use Graphify to identify the exact community/cluster of files involved in a feature.
  - Run Repomix to bundle just those files into high-density prompt context.

## Quick CLI Recipes

```bash
# Pack the current repository into repomix-output.xml
repomix

# Pack specific directories or files
repomix --include "scripts/**,skills/**"

# Output as markdown with token counts
repomix --style markdown --output context.md

# Ignore large or build files
repomix --ignore "**/*.min.js,**/*.lock"

# Copy output directly to clipboard
repomix --copy
```
