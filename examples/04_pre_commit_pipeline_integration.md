# 🛠️ COOKBOOK: PRE-COMMIT & CI PIPELINE INTEGRATION

> Step-by-step recipe for integrating the Slop Court quality tribunal into your local development loop, git hooks, and continuous integration pipelines.

---

## 1. Native Git Bailiff (Fastest Workstation Setup)

Workshop OS includes a built-in hook installer that arms the Git pre-commit and pre-push lifecycle without needing third-party hook managers:

```bash
# 1. Install pre-commit & pre-push hooks directly into .git/hooks/
workshop court bailiff install

# 2. Verify installation status
workshop court bailiff status
```

When a developer or AI agent attempts `git commit`, the Bailiff automatically runs:
* **Scope:** Analyzes only staged files.
* **Enforcement:** Halts with exit code 1 if any Capital Felony (`FEL-01..FEL-06`) is detected.
* **Certificate:** Issues a SHA-256 clearance token on acquittal.

---

## 2. Standard Python `pre-commit` Integration

If your project already uses the industry-standard [`pre-commit`](https://pre-commit.com) framework, add Workshop OS directly to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/shoyarism/ai-workshop
    rev: v3.5.0
    hooks:
      - id: slop-court
        name: Slop Court Quality Gate
        stages: [pre-commit, pre-push]
```

Then install:
```bash
pre-commit install
```

---

## 3. GitHub Actions CI Quality Gate

Enforce Slop Court compliance on every pull request and push to `main` using GitHub Actions:

```yaml
name: Slop Court Tribunal CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  court-tribunal:
    name: Slop Court Judicial Review
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Run Slop Court Prosecution
        run: |
          python scripts/workshop_court.py trial .
```

---

## 4. Bypassing False Positives via Suppression Pragmas

Legitimate exceptions (e.g. low-level OS decoding fallbacks, mock fixtures in test suites) can be cleanly exempted using inline pragmas:

```python
try:
    decoded = raw_bytes.decode("utf-8")
except UnicodeDecodeError:  # @court-exempt: fallback to latin-1 encoding
    decoded = raw_bytes.decode("latin-1")
```

The pragma requires a documented reason following `# @court-exempt: <reason>`, creating an auditable trail that Juror Security will acquit.
