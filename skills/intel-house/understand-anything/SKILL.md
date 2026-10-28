---
name: understand-anything
description: "Codebase cartography and mental model engine. Combines deterministic Tree-sitter AST analysis and semantic indexing to explain unfamiliar repositories, call graphs, and architectural layers."
userFacing: true
---

# 🧠 Understand Anything: Codebase Comprehension Engine

> **Purpose:** Ingests unfamiliar codebases, large monorepos, and foreign software architectures, decomposing them into clear mental models, execution entrypoints, and architectural layers.

---

## 1. The 4-Layer Deconstruction Methodology

```
Layer 4: User/Client Surface    (CLI commands, HTTP endpoints, UI components)
                ▼
Layer 3: Orchestration Layer    (Routers, business services, state managers)
                ▼
Layer 2: Domain Logic & AST     (Pure algorithms, data invariants, calculation models)
                ▼
Layer 1: Persistence & Storage  (Database schemas, disk caches, network adapters)
```

---

## 2. Execution Steps

1. **Topological Survey:**
   - Scan manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`).
   - Identify main execution entrypoints and runtime environment requirements.
2. **AST Dependency Mapping:**
   - Map module import flows and identify core domain entities.
   - Flag "god files" (>800 lines or >15 dependent modules) vs modular leaf nodes.
3. **Execution Walkthrough Synthesis:**
   - Produce a step-by-step trace of a primary user action (e.g. "What happens when a user clicks Submit / runs `cli action`?").
   - Highlight where state mutations occur and where external network calls leave the system.
