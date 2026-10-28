---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-paper-publisher"
name: hugging-face-paper-publisher
description: Publish and manage research papers on Hugging Face Hub. Supports creating paper pages, linking papers to models/datasets, claiming authorship, and generating professional markdown-based research articles.
risk: unknown
---

# Overview

## When to Use
Use this skill when a user wants to publish, link, index, or manage research papers on the Hugging Face Hub.
This skill provides comprehensive tools for AI engineers and researchers to publish, manage, and link research papers on the Hugging Face Hub. It streamlines the workflow from paper creation to publication, including integration with arXiv, model/dataset linking, and authorship management.

## Integration with HF Ecosystem
- **Paper Pages**: Index and discover papers on Hugging Face Hub
- **arXiv Integration**: Automatic paper indexing from arXiv IDs
- **Model/Dataset Linking**: Connect papers to relevant artifacts through metadata
- **Authorship Verification**: Claim and verify paper authorship
- **Research Article Template**: Generate professional, modern scientific papers

# Version
1.0.0

# Dependencies
The included script uses PEP 723 inline dependencies. Prefer `uv run` over
manual environment setup.

- huggingface_hub>=0.26.0
- pyyaml>=6.0.3
- requests>=2.32.5
- markdown>=3.5.0
- python-dotenv>=1.2.1

# Core Capabilities

## 1. Paper Page Management
- **Index Papers**: Add papers to Hugging Face from arXiv
- **Claim Authorship**: Verify and claim authorship on published papers
- **Manage Visibility**: Control which papers appear on your profile
- **Paper Discovery**: Find and explore papers in the HF ecosystem

## 2. Link Papers to Artifacts
- **Model Cards**: Add paper citations to model metadata
- **Dataset Cards**: Link papers to datasets via README
- **Automatic Tagging**: Hub auto-generates arxiv:<PAPER_ID> tags