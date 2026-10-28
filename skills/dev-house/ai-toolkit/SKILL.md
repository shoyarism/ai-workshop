---
name: ai-toolkit
description: >
  Research operations toolkit for AI labs. Dataset curation, RL training, evaluation
  infrastructure, and multi-actor training. Use when building RL pipelines,
  evaluating models, or managing AI research datasets.
  Reference: https://github.com/abi-sabbir/ai-toolkit
---

# AI Toolkit — Research Operations for AI Labs

Production toolkit for dataset curation, RL training, evaluation infrastructure, and multi-actor training.

## Installation

```bash
# Install from GitHub
pip install git+https://github.com/abi-sabbir/ai-toolkit.git

# Or from local checkout
git clone https://github.com/abi-sabbir/ai-toolkit.git
cd ai-toolkit
pip install -e .
```

## Core Components

### Dataset Curation
- Dataset generation and curation pipelines
- Data cleaning and validation
- Format conversion (JSONL, Parquet)

### RL Training Infrastructure
- Multi-actor training support
- Reward model integration
- PPO/GRPO/SLF fine-tuning

### Evaluation
- Leaderboard tracking
- Batch evaluation pipelines
- Custom benchmark integration

### Orchestration
- Cluster management
- Job scheduling
- Resource allocation

## Quick Start

```python
from ai_toolkit import Dataset, Trainer, Evaluator

# Load and curate dataset
dataset = Dataset.from_jsonl("train.jsonl")
dataset = dataset.filter(lambda x: x["quality_score"] > 0.8)

# Initialize trainer
trainer = Trainer(
    model="your-model",
    dataset=dataset,
    reward_model="reward-model"
)

# Run training
trainer.train(epochs=3)

# Evaluate
evaluator = Evaluator(model=trainer.model)
results = evaluator.run(benchmark="leaderboard")
```

## Use Cases

- **RLHF pipelines** - Reward modeling + PPO training
- **SFT datasets** - Curate instruction-following data
- **Evaluation** - Run consistent benchmarks
- **Multi-actor** - Scale training across workers

## Integration Points

- vLLM serving
- HuggingFace Transformers
- Ray cluster
- Weights & Biases logging
