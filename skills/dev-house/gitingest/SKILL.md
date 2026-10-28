---
name: gitingest
description: Ingest local repositories or GitHub URLs into prompt-friendly text summaries with directory structures, statistics, and token size estimates.
---

# Gitingest: Fast Code & Repo Ingestion

`gitingest` turns any Git repository, GitHub URL, or local project folder into a clean, LLM-ready text summary including directory hierarchy, file size statistics, and token count estimates.

## Core Capabilities
- **Direct GitHub Ingestion**: Analyze any public GitHub repository directly from CLI without cloning.
- **Local Tree Ingestion**: Summarize local project folders and codebases for quick context stuffing.
- **Token Estimation**: Immediate breakdown of tokens per directory and file.

## Quick CLI Recipes

```bash
# Ingest local directory to text file
gitingest . -o digest.txt

# Ingest a remote GitHub repository directly
gitingest https://github.com/Graphify-Labs/graphify

# Set max file size threshold (e.g. 50KB)
gitingest . --max-size 50000

# Exclude specific patterns
gitingest . --exclude-patterns "*.test.*,*.spec.*"
```
