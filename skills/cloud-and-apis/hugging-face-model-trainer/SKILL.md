---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-llm-trainer"
name: hugging-face-model-trainer
description: Train or fine-tune TRL language models on Hugging Face Jobs, including SFT, DPO, GRPO, and GGUF export.
license: Complete terms in LICENSE.txt
risk: unknown
---

# TRL Training on Hugging Face Jobs

## Overview

Train language models using TRL (Transformer Reinforcement Learning) on fully managed Hugging Face infrastructure. No local GPU setup required—models train on cloud GPUs and results are automatically saved to the Hugging Face Hub.

**TRL provides multiple training methods:**
- **SFT** (Supervised Fine-Tuning) - Standard instruction tuning
- **DPO** (Direct Preference Optimization) - Alignment from preference data
- **GRPO** (Group Relative Policy Optimization) - Online RL training
- **Reward Modeling** - Train reward models for RLHF

**For detailed TRL method documentation:**
```python
hf_doc_search("your query", product="trl")
hf_doc_fetch("https://huggingface.co/docs/trl/sft_trainer")  # SFT
hf_doc_fetch("https://huggingface.co/docs/trl/dpo_trainer")  # DPO
# etc.
```

**See also:** `references/training_methods.md` for method overviews and selection guidance

## When to Use This Skill

Use this skill when users want to:
- Fine-tune language models on cloud GPUs without local infrastructure
- Train with TRL methods (SFT, DPO, GRPO, etc.)
- Run training jobs on Hugging Face Jobs infrastructure
- Convert trained models to GGUF for local deployment (Ollama, LM Studio, llama.cpp)
- Ensure trained models are permanently saved to the Hub
- Use modern workflows with optimized defaults

### When to Use Unsloth

Use **Unsloth** (`references/unsloth.md`) instead of standard TRL when:
- **Limited GPU memory** - Unsloth uses ~60% less VRAM
- **Speed matters** - Unsloth is ~2x faster
- Training **large models (>13B)** - memory efficiency is critical
- Training **Vision-Language Models (VLMs)** - Unsloth has `FastVisionModel` support