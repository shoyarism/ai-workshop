---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-community-evals"
name: hugging-face-community-evals
description: Run local evaluations for Hugging Face Hub models with inspect-ai or lighteval.
risk: unknown
---

# Overview

## When to Use
Use this skill for local model evaluation, backend selection, and GPU smoke tests outside the Hugging Face Jobs workflow.

This skill is for **running evaluations against models on the Hugging Face Hub on local hardware**.

It covers:
- `inspect-ai` with local inference
- `lighteval` with local inference
- choosing between `vllm`, Hugging Face Transformers, and `accelerate`
- smoke tests, task selection, and backend fallback strategy

It does **not** cover:
- Hugging Face Jobs orchestration
- model-card or `model-index` edits
- README table extraction
- Artificial Analysis imports
- `.eval_results` generation or publishing
- PR creation or community-evals automation

If the user wants to **run the same eval remotely on Hugging Face Jobs**, hand off to the `hugging-face-jobs` skill and pass it one of the local scripts in this skill.

If the user wants to **publish results into the community evals workflow**, stop after generating the evaluation run and hand off that publishing step to `~/code/community-evals`.

> All paths below are relative to the directory containing this `SKILL.md`.

# When To Use Which Script

| Use case | Script |
|---|---|
| Local `inspect-ai` eval on a Hub model via inference providers | `scripts/inspect_eval_uv.py` |
| Local GPU eval with `inspect-ai` using `vllm` or Transformers | `scripts/inspect_vllm_uv.py` |
| Local GPU eval with `lighteval` using `vllm` or `accelerate` | `scripts/lighteval_vllm_uv.py` |
| Extra command patterns | `examples/USAGE_EXAMPLES.md` |

# Prerequisites

- Prefer `uv run` for local execution.
- Set `HF_TOKEN` for gated/private models.
- For local GPU runs, verify GPU access before starting:

```bash
uv --version
printenv HF_TOKEN >/dev/null