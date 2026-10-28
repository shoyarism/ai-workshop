---
source: "https://github.com/huggingface/skills/tree/main/skills/hf-cli"
name: hugging-face-cli
description: "Use the Hugging Face Hub CLI (`hf`) to download, upload, and manage models, datasets, and Spaces."
risk: unknown
---

Install by downloading the installer script first, reviewing it, and then running it locally. Example:
`curl -LsSf https://hf.co/cli/install.sh -o /tmp/hf-install.sh && less /tmp/hf-install.sh && bash /tmp/hf-install.sh`

## When to Use
Use this skill when you need the `hf` CLI for Hub authentication, downloads, uploads, repo management, or basic compute operations.

The Hugging Face Hub CLI tool `hf` is available. IMPORTANT: The `hf` command replaces the deprecated `huggingface-cli` command.

Use `hf --help` to view available functions. Note that auth commands are now all under `hf auth` e.g. `hf auth whoami`.

Generated with `huggingface_hub v1.8.0`. Run `hf skills add --force` to regenerate.

## Commands

- `hf download REPO_ID` — Download files from the Hub. `[--type CHOICE --revision TEXT --include TEXT --exclude TEXT --cache-dir TEXT --local-dir TEXT --force-download --dry-run --quiet --max-workers INTEGER]`
- `hf env` — Print information about the environment.
- `hf sync` — Sync files between local directory and a bucket. `[--delete --ignore-times --ignore-sizes --plan TEXT --apply TEXT --dry-run --include TEXT --exclude TEXT --filter-from TEXT --existing --ignore-existing --verbose --quiet]`
- `hf upload REPO_ID` — Upload a file or a folder to the Hub. Recommended for single-commit uploads. `[--type CHOICE --revision TEXT --private --include TEXT --exclude TEXT --delete TEXT --commit-message TEXT --commit-description TEXT --create-pr --every FLOAT --quiet]`
- `hf upload-large-folder REPO_ID LOCAL_PATH` — Upload a large folder to the Hub. Recommended for resumable uploads. `[--type CHOICE --revision TEXT --private --include TEXT --exclude TEXT --num-workers INTEGER --no-report --no-bars]`