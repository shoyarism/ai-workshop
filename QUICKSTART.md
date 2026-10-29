# 🚀 Workshop OS — Quick Start Guide

Get up and running with Workshop OS and the Slop Court quality gate in under 60 seconds.

---

## 1. Installation

Choose **one** of the following options based on your workflow:

### Option A: Using `uv` (Recommended)

```bash
# Clone the repository
git clone https://github.com/shoyarism/ai-workshop.git
cd ai-workshop

# Sync virtual environment and dependencies
uv sync
```

### Option B: Using standard `pip`

```bash
git clone https://github.com/shoyarism/ai-workshop.git
cd ai-workshop

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install editable package
pip install -e .
```

---

## 2. Verify Your Environment

Run the built-in diagnostic suite:

```bash
uv run python scripts/workshop.py doctor
```

All core subsystems should display `[OK]`.

---

## 3. First Judicial Review: Run the Slop Court

Audit any file or staged git diff for code slop, bare exception blackholes, and truncated stubs:

```bash
# Trial a specific file or directory
uv run python scripts/workshop.py court trial scripts/

# Trial all currently staged git changes
uv run python scripts/workshop.py court trial --staged
```

### Example Verdict:
```text
======================================================================
 ⚖️  SLOP COURT v3.5: SUPREME JUDICIAL TRIBUNAL TRIAL REPORT
======================================================================
 Target      : Staged Git Diffs (1 files | 84 lines)
 Slop Index  : 0.0% | Penalties: 0 pts | Felonies: 0 | Misdemeanors: 0
----------------------------------------------------------------------
 [FINAL JUDICIAL RULING]
  🎉 VERDICT: ACQUITTED WITH HONORS (UNANIMOUS)
  Certificate of Cleanliness granted for commit and push.
======================================================================
```

---

## 4. Install the Git Bailiff Hook (Automated Pre-Commit Gate)

Automate enforcement so code with sustained Capital Felonies is rejected before commit:

```bash
uv run python scripts/workshop.py court bailiff install
```

To remove the hook:
```bash
uv run python scripts/workshop.py court bailiff uninstall
```

---

## 5. Search 2,147 Verified Domain Skills

Find implementation runbooks across the 7 Sovereign Houses:

```bash
# Search by keyword
uv run python scripts/workshop.py search "tailscale"
uv run python scripts/workshop.py search "react performance"
uv run python scripts/workshop.py search "jwt authentication"
```

---

## 6. Run an Adversarial Council Deliberation

Stress-test a design decision using the 4-persona Supreme Council:

```bash
uv run python scripts/workshop.py council convene "Should we migrate from PostgreSQL to DynamoDB for our event log?"
```
