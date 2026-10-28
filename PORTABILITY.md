# 🌐 Workshop OS — Portability Guide
## Use This Drive on Any Machine

This document explains how to make the Workshop OS work on any system,
whether it's your main machine, a work laptop, or a friend's computer.

---

## How It Works

The Workshop is **self-contained and portable** by design:

1. **Dynamic path resolution** — Scripts find the Workshop root automatically, no matter what drive letter it's on
2. **`uv` managed** — No persistent `.venv` needed; `uv run` installs dependencies on-the-fly
3. **Harness config is local** — Local agent harness configs stay machine-specific; the drive stays untouched
4. **Skills are read-only** — The `skills/` directory is immutable; all modifications happen locally

---

## Quick Start on Any Machine

### Step 1: Plug in the Drive
Insert the external drive. Note the drive letter (e.g., E:, G:, H:).

### Step 2: Verify uv is Installed
```bash
uv --version
```
If missing, install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Step 3: Run Onboard Script
```bash
cd /path/to/Workshop
uv run python scripts/workshop_onboard.py --full-sync
```

This will:
- Verify Python and uv are present
- Mount Tier 0 core skills into `.workshop_state/skills-core/`
- Run a health check

### Step 4: Verify
```bash
uv run python scripts/workshop.py doctor
```

All checks should pass. You're ready to use the Workshop.

---

## What Gets Set Up Where

| Item | Location | Notes |
|------|----------|-------|
| Workshop root | Any cloned directory or drive root | Resolved dynamically via Path(__file__) |
| Core skills | `.workshop_state/skills-core/` | Symlinks/copy on first sync |
| Harness config | Machine-specific local config | Machine-specific, never on drive |
| Skills library | `skills/` | Read-only, shared across machines |
| Obsidian vault | `vault/` | Local-first, git-versioned |
| Backups | User-configured backup directory | Configured via `workshop_backup.py` |

---

## Troubleshooting

### "Workshop root not found"
Set environment variable before running:
```bash
export WORKSHOP_ROOT=/path/to/Workshop
# or on Windows:
set WORKSHOP_ROOT=D:\ai-workshop
```

### ".venv not working on different OS"
The `.venv` is machine-locked (compiled extensions). Use `uv run` instead:
```bash
# Don't use: .venv/Scripts/python scripts/workshop.py
# Do use:
uv run python scripts/workshop.py doctor
```

### "yaml module not found"
First run will auto-install via `uv`. If it fails:
```bash
uv pip install pyyaml ruamel.yaml --system
```

### Harness can't find Workshop
Run the onboard script again with `--full-sync`:
```bash
uv run python scripts/workshop_onboard.py --full-sync
```

---

## Architecture Decision

### Why Not Copy to Internal Drive?

The external drive approach has advantages:
- **Data sovereignty** — Your skills, vault, and configs stay on your drive
- **Version consistency** — All machines use the same Workshop version
- **Zero install** — No per-machine setup beyond `uv`
- **Portability** — Plug into any machine and work immediately

However, for **high-performance workflows** (compilation, large builds), consider:
- Keeping the drive connected during long sessions
- Using `--full-sync` if you move between machines frequently
- Running periodic backups of `vault/` to cloud storage

---

## When to Copy Instead

Copy the Workshop to an internal drive only if:
1. You're doing heavy compilation (Rust, large Node builds)
2. The external drive is too slow for your workflow
3. You need offline access without the drive present

To copy:
```bash
# Keep the external drive as the source of truth
rsync -a /media/workshop/ ~/internal-workshop/
# Update WORKSHOP_ROOT to point to the copy
```

---

## Summary

- **Use external drive** for all normal operations
- **Run `workshop_onboard.py`** once per machine
- **Use `uv run`** instead of `.venv` directly
- **Keep `vault/` backed up** to cloud for multi-machine sync
- **Never edit `skills/` directly** — follow standard skills contribution guidelines
