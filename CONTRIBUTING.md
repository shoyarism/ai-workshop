# 🤝 Contributing to Workshop OS

Thank you for your interest in contributing to **Workshop OS**! We welcome high-craft contributions from both human software engineers and autonomous AI agent systems.

---

## 🏛️ The Non-Negotiable Quality Standard: Zero Slop

Workshop OS is governed by **Slop Court v3.5**. All pull requests and commits are put on trial before our 3-Juror Bench (Craft, Architecture, Security). 

We do **not** accept:
- Truncated code or lazy omission placeholders (`[truncated code omitted]`, placeholder stubs).
- Tautological comments (`// increment counter`, `// return result`).
- AI clichés and buzzwords (`seamlessly`, `cutting-edge`, `revolutionize`, `game-changer`).
- Unearned default purple-indigo AI gradients without brand design justification.
- Silent error blackholes (`except: pass`, empty `catch (e) {}` with no logging).
- Extreme control flow nesting (> 5 levels of control flow).

Any PR failing the Slop Court tribunal will be automatically remanded by CI.

---

## 🚀 Development Workflow

### 1. Prerequisites
- **Python:** `>= 3.11` (Python 3.12 recommended)
- **Package Manager:** [`uv`](https://github.com/astral-sh/uv) (strongly recommended) or `pip`
- **Node.js:** `>= 18.0` (for web/browser subsystems)
- **Git:** Git 2.30+

### 2. Setup
```bash
git clone https://github.com/shoyarism/ai-workshop.git
cd ai-workshop

# Install dependencies using uv
uv sync

# Run health diagnostics
python scripts/workshop.py doctor

# Install the Slop Court Bailiff pre-commit hook
python scripts/workshop.py court bailiff install
```

### 3. Adding a New Skill
Skills live in `skills/<skill-name>/SKILL.md` with standard YAML frontmatter:
```markdown
---
name: my-new-skill
description: "Clear, concise trigger conditions and domain purpose."
allowed-tools: Read Write Edit Glob Grep Bash
---

# My New Skill Title

## Instructions & Runbook...
```

### 4. Running the Pre-Flight Quality Gate
Before staging or committing any code, run:
```bash
# Trial your changes through the Slop Court
python scripts/workshop.py court trial --staged

# View detailed 3-juror deliberation votes
python scripts/workshop.py court jury --staged

# Auto-rehabilitate minor comment or whitespace smells
python scripts/workshop.py court reform path/to/file.py
```

You must achieve:
```
🎉 VERDICT: ACQUITTED WITH HONORS (UNANIMOUS)
```

---

## 📜 Pull Request Guidelines

1. **Atomic Commits:** Keep commits focused, descriptive, and well-typed (`feat:`, `fix:`, `docs:`, `refactor:`).
2. **Verify Subsystem Health:** Ensure `python scripts/workshop.py doctor` passes without regressions.
3. **Defense Exemptions:** If a test fixture or platform shim legitimately requires an exception, document it explicitly:
   ```python
   except OSError:  # @court-exempt: intentional platform shim fallback
       pass
   ```
4. **Be Concise:** Zero sycophantic PR descriptions. State the axioms, changes made, and verification output.
