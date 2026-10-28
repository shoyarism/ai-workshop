---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-jobs"
name: hugging-face-jobs
description: Run workloads on Hugging Face Jobs with managed CPUs, GPUs, TPUs, secrets, and Hub persistence.
license: Complete terms in LICENSE.txt
risk: unknown
---

# Running Workloads on Hugging Face Jobs

## Overview

Run any workload on fully managed Hugging Face infrastructure. No local setup required—jobs run on cloud CPUs, GPUs, or TPUs and can persist results to the Hugging Face Hub.

**Common use cases:**
- **Data Processing** - Transform, filter, or analyze large datasets
- **Batch Inference** - Run inference on thousands of samples
- **Experiments & Benchmarks** - Reproducible ML experiments
- **Model Training** - Fine-tune models (see `model-trainer` skill for TRL-specific training)
- **Synthetic Data Generation** - Generate datasets using LLMs
- **Development & Testing** - Test code without local GPU setup
- **Scheduled Jobs** - Automate recurring tasks

**For model training specifically:** See the `model-trainer` skill for TRL-based training workflows.

## When to Use This Skill

Use this skill when users want to:
- Run Python workloads on cloud infrastructure
- Execute jobs without local GPU/TPU setup
- Process data at scale
- Run batch inference or experiments
- Schedule recurring tasks
- Use GPUs/TPUs for any workload
- Persist results to the Hugging Face Hub

## Key Directives

When assisting with jobs:

1. **ALWAYS use `hf_jobs()` MCP tool** - Submit jobs using `hf_jobs("uv", {...})` or `hf_jobs("run", {...})`. The `script` parameter accepts Python code directly. Do NOT save to local files unless the user explicitly requests it. Pass the script content as a string to `hf_jobs()`.

2. **Always handle authentication** - Jobs that interact with the Hub require `HF_TOKEN` via secrets. See Token Usage section below.