---
name: workshop-watch
description: >
  Monitor the Workshop OS at . for updates, new skills,
  subsystem changes, or vault modifications. Run periodically or before starting
  work to ensure your context is fresh. Use when Workshop might have changed,
  when you need the latest capabilities, or to detect drift.
---

# Workshop Watch — Auto-Evolution Monitor

## Purpose
Keeps this agent in sync with Workshop OS updates. Detects new skills, subsystem
additions, vault changes, and evolution events. Ensures no stale capabilities.

## When to Trigger
- On session start if more than 24h since last check
- Before starting any non-trivial task
- When user mentions "workshop", "new skill", "update"
- Periodically via cron (if configured)

## Monitoring Protocol

### Step 1: Check Evolution State
```bash
uv run python ./scripts/workshop_evolution.py status
```
This returns stats: total skills, freshness distribution, critical/stale counts.

### Step 2: Detect New/Changed Files
```bash
cd . && git log --oneline --since="24 hours ago"
```
Or without git:
```bash
# Check for recent modifications in key dirs
find ./skills -name "*.md" -mtime -1 2>/dev/null
find ./vault -name "*.md" -mtime -1 2>/dev/null
find ./subsystems -maxdepth 2 -type d -mtime -1 2>/dev/null
```

### Step 3: Check Drift
```bash
uv run python ./scripts/workshop_drift.py --json
```
Compares current state against known baselines.

### Step 4: Run Sync (if changes detected)
```bash
# From Workshop root, compile manifest into harness configs
cd . && uv run python scripts/workshop.py sync
```

### Step 5: Update Skills Index
```bash
uv run python ./scripts/workshop.py index
```
Reparses all skill frontmatter and updates the search index.

## Decision Logic

| Condition | Action |
|-----------|--------|
| No changes detected | Report: "Workshop current, no sync needed" |
| New skills added | Run `index` to pick them up |
| Subsystem updated | Run `sync` to update harness configs |
| Vault modified | Report ADRs/post-mortems that changed |
| Evolution critical | Alert user, suggest `workshop_evolution.py update` |
| Drift detected | Run full sync + index |

## Integration with Hermes

Store watch state in `~/.hermes/.workshop_watch.json`:
```json
{
  "last_check": "2026-10-06T12:00:00Z",
  "last_hash": "abc123...",
  "new_skills": [],
  "changed_files": []
}
```

Check interval: 24 hours (configurable)

## Quick Reference
```bash
# Full status check
uv run python ./scripts/workshop.py doctor

# Evolution scan (detect stale skills)
uv run python ./scripts/workshop_evolution.py scan

# Get update recommendations
uv run python ./scripts/workshop_evolution.py recommend

# Sync all harness configs
uv run python ./scripts/workshop.py sync

# Index skills
uv run python ./scripts/workshop.py index
```

## Error Handling
- If Workshop root not found: Report path issue, don't crash
- If sync fails: Log error, continue with existing capabilities
- If git unavailable: Fall back to filesystem mtime checks
- If yaml module missing: Install before sync (`pip install pyyaml ruamel.yaml`)
