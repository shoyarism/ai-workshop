---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-trackio"
name: hugging-face-trackio
description: Track ML experiments with Trackio using Python logging, alerts, and CLI metric retrieval.
risk: unknown
---

# Trackio - Experiment Tracking for ML Training

Trackio is an experiment tracking library for logging and visualizing ML training metrics. It syncs to Hugging Face Spaces for real-time monitoring dashboards.

## Three Interfaces

| Task | Interface | Reference |
|------|-----------|-----------|
| **Logging metrics** during training | Python API | [references/logging_metrics.md](references/logging_metrics.md) |
| **Firing alerts** for training diagnostics | Python API | [references/alerts.md](references/alerts.md) |
| **Retrieving metrics & alerts** after/during training | CLI | [references/retrieving_metrics.md](references/retrieving_metrics.md) |

## When to Use Each

### Python API → Logging

Use `import trackio` in your training scripts to log metrics:

- Initialize tracking with `trackio.init()`
- Log metrics with `trackio.log()` or use TRL's `report_to="trackio"`
- Finalize with `trackio.finish()`

**Key concept**: For remote/cloud training, pass `space_id` — metrics sync to a Space dashboard so they persist after the instance terminates.

→ See [references/logging_metrics.md](references/logging_metrics.md) for setup, TRL integration, and configuration options.

### Python API → Alerts

Insert `trackio.alert()` calls in training code to flag important events — like inserting print statements for debugging, but structured and queryable:

- `trackio.alert(title="...", level=trackio.AlertLevel.WARN)` — fire an alert
- Three severity levels: `INFO`, `WARN`, `ERROR`
- Alerts are printed to terminal, stored in the database, shown in the dashboard, and optionally sent to webhooks (Slack/Discord)