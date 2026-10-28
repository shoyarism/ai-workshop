---
name: ast-grep
description: Fast polyglot tool for structural code search, linting, and AST-based rewriting across 20+ languages using tree-sitter syntax trees.
---

# ast-grep: Structural Code Search & Rewriting

`ast-grep` (sg) is a CLI and library for syntax-aware code search and refactoring. Unlike regex or text-based search (grep/ripgrep), `ast-grep` understands code structure, comments, strings, scopes, and AST nodes across Python, TypeScript, JavaScript, Go, Rust, Java, C, C++, and more.

## Core Capabilities
- **Structural Search**: Find code patterns using meta-variables (`$VAR`, `$$$ARGS`) that match syntax trees regardless of whitespace or formatting.
- **AST Rewriting**: Safely rewrite and refactor code without accidental string or comment collisions.
- **Rule-Based Linting**: Enforce architectural and stylistic invariants with YAML rule configs.
- **Synergy with Graphify & Ponytail**:
  - Graphify locates the high-level call graphs, dependencies, and communities.
  - ast-grep executes surgical structural transforms to simplify bloated code (Ponytail principles).

## Quick CLI Recipes

```bash
# Search for function calls matching a pattern in Python
ast-grep run --pattern 'def $FUNC($$$PARAMS): $$$BODY' --lang python

# Search for insecure or deprecated APIs in TypeScript/JavaScript
ast-grep run --pattern 'fetch($URL, { headers: { Authorization: $TOKEN } })' --lang ts

# Structural rewrite: replace bloated boilerplate with one-liners
ast-grep run --pattern 'if ($X === null || $X === undefined) { return $DEFAULT; }' \
             --rewrite 'return $X ?? $DEFAULT;' \
             --lang ts

# Interactive rewrite confirmation
ast-grep run --pattern 'os.path.join($A, $B)' --rewrite 'Path($A) / $B' --lang python --interactive

# Scan with rule configuration
ast-grep scan
```

## Meta-Variable Reference
- `$VAR`: Matches a single AST node (expression, identifier, literal).
- `$$$VARS`: Matches zero or more AST nodes (arguments list, statements block).
- `$_`: Anonymous wildcard matching any single node.
