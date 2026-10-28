---
name: devcontainer-setup
description: Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes. Use when adding devcontainer support to a project, setting up isolated development environments, or configuring sandboxed Claude Code workspaces.
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-03-06
---

# Devcontainer Setup Skill

Creates a pre-configured devcontainer with Claude Code and language-specific tooling.

## When to Use
- User asks to "set up a devcontainer" or "add devcontainer support"
- User wants a sandboxed Claude Code development environment
- User needs isolated development environments with persistent configuration

## When NOT to Use

- User already has a devcontainer configuration and just needs modifications
- User is asking about general Docker or container questions
- User wants to deploy production containers (this is for development only)

## Workflow

```mermaid
flowchart TB
    start([User requests devcontainer])
    recon[1. Project Reconnaissance]
    detect[2. Detect Languages]
    generate[3. Generate Configuration]
    write[4. Write files to .devcontainer/]
    done([Done])

    start --> recon
    recon --> detect
    detect --> generate
    generate --> write
    write --> done
```

## Phase 1: Project Reconnaissance

### Infer Project Name

Check in order (use first match):

1. `package.json` → `name` field
2. `pyproject.toml` → `project.name`
3. `Cargo.toml` → `package.name`
4. `go.mod` → module path (last segment after `/`)
5. Directory name as fallback

Convert to slug: lowercase, replace spaces/underscores with hyphens.

### Detect Language Stack

| Language | Detection Files |
|----------|-----------------|
| Python | `pyproject.toml`, `*.py` |
| Node/TypeScript | `package.json`, `tsconfig.json` |
| Rust | `Cargo.toml` |
| Go | `go.mod`, `go.sum` |

### Multi-Language Projects