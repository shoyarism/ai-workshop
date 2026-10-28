# ⚙️ Continuous Integration (CI)

Workshop OS enforces deterministic CI verification across multiple operating systems and Python versions.

## Remote GitHub Actions CI

Automated multi-platform CI is configured and active in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).
It runs on Ubuntu, Windows, and macOS against Python 3.11 and 3.12, executing all 6 core quality gates:
1. **Unit Test Suite** (`tests/`)
2. **Ruff Linter Analysis** (`scripts/` and `tests/`)
3. **Slop Court Judicial Review** (`scripts/workshop_court.py trial scripts`)
4. **Secret Scanning & Redaction Gate** (`scripts/scan_secrets.py`)
5. **Workshop Doctor Health Diagnostics** (`scripts/workshop.py doctor --strict`)
6. **Agent Instruction Drift Gate** (`scripts/workshop_sync.py --check`)

## Local CI Execution

You can run the identical 6-gate verification suite locally at any time without pushing to GitHub:

```bash
python ci/run_local_ci.py
```

Or run individual gate steps:
```bash
python -m unittest discover tests
uv run python scripts/workshop_court.py trial scripts
uv run python scripts/scan_secrets.py
uv run python scripts/workshop.py doctor --strict
uv run python scripts/workshop_sync.py --check
```
