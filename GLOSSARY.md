# 📖 Workshop OS — Architectural Glossary

This glossary defines the foundational concepts, terminology, and invariants used throughout Workshop OS.

---

## Core Systems & Governance

### Slop Court
The automated quality tribunal in Workshop OS that inspects code, diffs, and documentation for artificial degradation patterns.
- **Python Scope**: Deterministic syntax tree parsing via Python's standard `ast` module.
- **Polyglot Scope**: Pattern heuristics for JavaScript, TypeScript, Go, Rust, and shell scripts.
- **Penal Code**: 38 codified statutes categorized into Capital Felonies (`FEL-01..08`) and Misdemeanors (`MIS-01..06`).

### Git Bailiff
The automated interceptor that hooks directly into `.git/hooks/pre-commit` and `.git/hooks/pre-push`. When staged changes contain a sustained Capital Felony, the Bailiff aborts the git operation with exit code 1 and outputs the judicial tribunal report.

### Supreme Council
An adversarial multi-persona deliberation engine that stress-tests architectural, product, and systems decisions before committing to code. Consists of four distinct cognitive postures:
1. **The Skeptical Inquisitor**: Focuses on failure modes, tail risks, and adversarial edge cases.
2. **The Radical Minimalist**: Enforces YAGNI (You Aren't Gonna Need It) and prunes unnecessary dependencies.
3. **The UI/UX Craft Architect**: Audits typography hierarchy, contrast ratios, and design tokens.
4. **The Battle-Tested SRE**: Audits backpressure, idempotency, failure domains, and logging.

---

## Skill Architecture

### Sovereign Houses
The seven primary operational domains under `skills/` used to organize 2,147 verified runbooks:
1. **Security House (`skills/security-house/`)**: Defensive monitoring, incident response, AST arrest, forensics, and secret detection (835 skills).
2. **Dev House (`skills/dev-house/`)**: Strict type safety, test-driven development, AST refactoring, and code simplification (357 skills).
3. **Media House (`skills/media-house/`)**: Programmatic motion graphics, video pipelines, and photoreal rendering (178 skills).
4. **Ops & Tokens House (`skills/ops-tokens-house/`)**: Token budget optimization, spec-driven development, and execution workflows (166 skills).
5. **Design House (`skills/design-house/`)**: Design systems, typography, CSS tokens, and layout guidelines (132 skills).
6. **Intel House (`skills/intel-house/`)**: Knowledge graph construction, OSINT research, and reverse engineering (90 skills).
7. **Growth House (`skills/growth-house/`)**: Authentic tone documentation, technical SEO, and release playbooks (79 skills).

### SKILL.md
The canonical format for an executable agent skill, consisting of:
- **YAML Frontmatter**: Name, description, domain, subdomain, tags, version, author, license, and compliance tags (NIST CSF, MITRE ATT&CK where applicable).
- **Markdown Body**: Prerequisites, architecture, step-by-step implementation, code snippets, verification tests, and references.

---

## Slop Court Penal Code Categories

### Capital Felonies (`FEL`)
High-severity violations that trigger an immediate commit abort (Verdict: Conviction):
- `FEL-01`: **Truncated Code Fraud** — Using placeholder comments like `// ... existing code ...`, `/* rest unchanged */`, or `# rest of file`. <!-- @court-exempt: specification definition -->
- `FEL-02`: **Lazy Stubbing** — Leaving unhandled `pass`, `TODO`, or `throw NotImplementedError()` in concrete methods.
- `FEL-03`: **Naked Exception Blackhole** — Empty `except:` or empty `catch (e) {}` blocks that swallow runtime errors without logging.
- `FEL-04`: **Fabricated Telemetry** — Hardcoded claims like "99.9% uptime" or ungrounded statistics in documentation without verification.
- `FEL-05`: **Sycophantic Conversational Fluff** — AI preamble in code or commit messages (`Certainly!`, `Here is the solution`).
- `FEL-06`: **Plaintext Secrets Exposure** — Hardcoded private keys, access tokens, or credentials in tracked files.

### Misdemeanors (`MIS`)
Craft and styling offenses that incur penalty points:
- `MIS-01`: **Tautological Comments** — Syntax-level obvious comments (e.g., `i += 1  # increment counter`).
- `MIS-02`: **Marketing Clichés** — Overused AI marketing buzzwords (`cutting-edge`, `revolutionize`, `game-changer`).
- `MIS-03`: **Unearned Purple Gradients** — Default purple-indigo AI gradients without documented palette tokens.
- `MIS-04`: **Generic 3-Card Bento Box** — Boilerplate card layouts lacking visual hierarchy.
- `MIS-05`: **Naked Any & Wildcards** — Unconstrained `any` types or wildcard imports (`from module import *`).
