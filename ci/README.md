# ⚙️ Continuous Integration (CI)

This directory contains the GitHub Actions workflow definition for Workshop OS (`ci.yml`).

## Enabling GitHub Actions on your Repository

To activate automated testing and Slop Court verification on pushes and PRs:
1. Ensure your GitHub Personal Access Token has the `workflow` scope (or use the GitHub Web UI / GitHub CLI).
2. Move `ci/ci.yml` to `.github/workflows/ci.yml`:
   ```bash
   mkdir -p .github/workflows
   cp ci/ci.yml .github/workflows/ci.yml
   git add .github/workflows/ci.yml
   git commit -m "ci: enable github actions workflow"
   git push
   ```

## Local CI Execution

You can run the full test suite locally at any time without waiting for GitHub Actions:
```bash
python tests/test_court.py
python scripts/scan_secrets.py
python scripts/workshop.py doctor
```
