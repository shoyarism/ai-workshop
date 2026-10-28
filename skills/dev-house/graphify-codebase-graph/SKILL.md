---
name: graphify-codebase-graph
description: Codebase knowledge graph extraction, AST dependency analysis, and structural architecture visualization using Graphify.
---

# Graphify Codebase Knowledge Graph

Graphify extracts complete AST knowledge graphs from source repositories, mapping functions, classes, imports, call graphs, and architectural dependencies into queryable graph structures.

## Core Capabilities
- **Multi-Language AST Parsing**: Python, TypeScript, JavaScript, Rust, Go, and Java.
- **Dependency Flow & Call Graphs**: Trace function execution paths and cross-module couplings.
- **Agent Knowledge Context**: Export codebase graphs to JSON/GraphML for LLM context compression.

## Execution Patterns
`ash
# Build knowledge graph of current workspace
python -m graphify.cli build --source . --output graph.json

# Query architectural relations
python -m graphify.cli query --graph graph.json --from 'auth_handler' --depth 3
`
