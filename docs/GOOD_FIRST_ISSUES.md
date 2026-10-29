# 🌱 WORKSHOP OS — CURATED STARTER TASKS & GOOD FIRST ISSUES

> A curated list of approachable entry-level contributions designed for developers and synthetic contributors exploring Workshop OS.
> To claim one of these, open an issue using the [Starter Issue Template](../.github/ISSUE_TEMPLATE/good_first_issue.md).

---

### Task 01: Add `vitest-tdd-workflow` Skill to The Dev House
* **House:** `skills/dev-house/`
* **Objective:** Author a clean `SKILL.md` establishing Test-Driven Development (TDD) red-green-refactor invariants for modern TypeScript projects using Vitest.
* **Requirements:**
  * Must conform to YAML frontmatter schema (`name`, `description`).
  * Include runnable commands (`npx vitest run`, `--coverage`).
  * Zero marketing clichés and zero truncated code placeholders.

---

### Task 02: Replicate CLI Latency Benchmarks on Linux ARM64
* **House / Area:** `BENCHMARKS.md`
* **Objective:** Run the replication protocol from [`BENCHMARKS.md`](../BENCHMARKS.md) on ARM64 architectures (e.g. AWS Graviton, Apple Silicon, Raspberry Pi 5).
* **Requirements:**
  * Record cold and warm latencies for `workshop search`, `workshop house inspect`, and `workshop court trial --staged`.
  * Submit numbers via PR to expand the Hardware Profiles section of `BENCHMARKS.md`.

---

### Task 03: Author German (Deutsch) Translation of Core README
* **House / Area:** `docs/i18n/`
* **Objective:** Translate `README.md` into high-density, idiomatic technical German (`docs/i18n/README.de.md`).
* **Requirements:**
  * Preserve Markdown anchor links and code blocks.
  * Add language link to the README header badge row.

---

### Task 04: FastMCP Weather & Geospatial Reference Implementation
* **House / Area:** `examples/`
* **Objective:** Add an `examples/05_fastmcp_custom_server.py` demonstrating how to author a custom FastMCP server that connects directly to `workshop mcp`.
* **Requirements:**
  * Include schema annotations and input validation with Pydantic.
  * Add docstrings with zero slop comments.

---

### Task 05: Add Monorepo Directory Boundary Test
* **House / Area:** `tests/`
* **Objective:** Add an automated unit test ensuring no top-level directories in the repository contain spaces in their folder names.
* **Requirements:**
  * Implement in `tests/test_paths_and_boundaries.py`.
  * Must pass on Windows, macOS, and Linux runners.
