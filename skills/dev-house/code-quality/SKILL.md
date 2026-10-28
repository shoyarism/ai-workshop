---
name: code-quality
description: Enforce code quality standards across a codebase. Use when asked to audit code quality, review for maintainability, find anti-patterns, enforce coding standards, measure technical debt, or improve code hygiene before merge.
---

# Code Quality

Systematic code quality auditing and enforcement for any language or stack. Run these checks when reviewing a PR, auditing a codebase, or before shipping changes.

## Operating Principles

1. **Standards first.** Identify the project's explicit standards (linters, formatters, type checkers, style guides) before judging code. If none exist, propose sensible defaults.
2. **Evidence over opinion.** Every finding must cite the file, line, and the specific rule or principle it violates. No generic "this could be better" notes.
3. **Severity tiers.** Classify every issue:
   - **Blocker** — correctness bugs, security vulnerabilities, data loss, broken contracts.
   - **Warning** — maintainability, performance, or design problems that will bite later.
   - **Nit** — style, naming, or formatting that is below standard but not harmful.
4. **Fixable before abstractable.** Prefer small, concrete fixes over sweeping refactors. Suggest the minimal change that restores quality.
5. **Follow the codebase's conventions.** Match existing patterns, libraries, and idioms. Never impose a stack.

## Audit Checklist

### Correctness & Robustness
- Error paths handled (no swallowed exceptions, no silent `except`/`catch`).
- Edge cases: empty inputs, nulls, concurrency, timezones, encodings, large inputs.
- Resource management: connections, files, streams, temp dirs closed/released.
- No dead code, unreachable branches, or placeholder stubs (`TODO`, `FIXME`, `XXX` reviewed).
- Boundaries and invariants enforced (input validation, assertions on assumptions).

### Security
- No secrets, keys, tokens, or credentials committed (env vars / secret stores only).
- Injection risks: SQL, shell, path traversal, XSS, SSRF. Never build queries/shell via string concat.
- AuthZ: authorization checked at every entrypoint, not just the UI.
- Dependencies: known-vulnerable or abandoned packages flagged.

### Maintainability
- Functions/methods small and single-purpose; low cyclomatic complexity.
- Naming is descriptive; code reads like prose.
- Duplication removed or deliberately justified.
- Comments explain *why*, not *what*.
- Architecture: layering respected; no god objects, no circular dependencies.
- Tests cover the change: unit for logic, integration for flows, snapshot for UI.

### Performance
- No obvious O(n²)+ hot paths; loops, queries, and rendering bounded.
- No work done twice; caching used where it clearly helps.
- Network/DB calls batched; no N+1 patterns.

### Consistency
- Formatting matches project config (Prettier/Black/gofmt/etc.).
- Naming conventions and import style match the rest of the codebase.

## Workflow

1. **Map the surface.** List changed/new files (for PRs) or the module under audit.
2. **Run the toolchain.** Execute the project's lint, format-check, type-check, and tests. Record exact pass/fail output.
3. **Read for intent.** Skim to understand what each unit is supposed to do before judging it.
4. **Audit in passes.** Do a correctness pass, a security pass, a maintainability pass, then a consistency pass.
5. **Report.** Produce a findings table with `file:line`, severity, rule, and a concrete fix. Give an overall quality verdict (ship / ship-with-fixes / rework).

## Report Format

```markdown
## Code Quality Report — <scope>

**Verdict:** ship / ship-with-fixes / rework
**Stats:** N blocker, M warning, K nit (across X files)

| Severity | File:Line | Issue | Rule / Principle | Suggested Fix |
|---|---|---|---|---|
| Blocker | src/api.ts:44 | ... | ... | ... |

### Top 3 Fixes
1. ...
```
