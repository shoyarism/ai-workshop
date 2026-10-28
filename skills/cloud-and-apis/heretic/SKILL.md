---
name: heretic
description: >
  Fully automatic censorship removal for language models using directional ablation.
  Decensor models without expensive post-training. Use when working with local LLMs
  and need uncensored variants.
  Reference: https://github.com/p-e-w/heretic
---

# Heretic — Automatic Censorship Removal

Heretic removes censorship (safety alignment) from transformer-based language models using advanced directional ablation with TPE-based parameter optimization.

## Installation

```bash
# Install with uv (recommended)
pip install -U heretic-llm

# Or with uv directly
uv run heretic
```

## Usage

```bash
# Decensor a model
heretic Qwen/Qwen3-4B-Instruct-2507

# With custom config
heretic google/gemma-3-12b-it

# Evaluate after decensoring
heritic --model google/gemma-3-12b-it --evaluate-model p-e-w/gemma-3-12b-it-heretic
```

## Features

- **Fully automatic** - No manual parameter tuning required
- **Multi-architecture support** - Dense models, MoE, hybrid (Qwen3.5)
- **Quantization support** - bitsandbytes bnb_4bit for low VRAM
- **Research mode** - Plot residual vectors, analyze geometry

```bash
# Install research extras
pip install -U 'heretic-llm[research]'

# Plot residual vectors
heretic Qwen/Qwen3-4B-Instruct-2507 --plot-residuals

# Print residual geometry
heretic Qwen/Qwen3-4B-Instruct-2507 --print-residual-geometry
```

## How It Works

1. Computes residual vectors for harmful vs harmless prompts
2. Identifies residual directions per layer
3. Optimizes ablation weights using Optuna/TPE
4. Applies orthogonal projection to inhibit safety directions

## Post-Process Options

After decensoring completes:
- Save model locally
- Upload to Hugging Face
- Chat with model to test
- Run benchmarks (MMLU, GSM8K)

## Requirements

- Python 3.10+
- PyTorch 2.2+ (2.6+ for some models)
- CUDA-compatible GPU recommended
