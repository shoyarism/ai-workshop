#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

if ! command -v uv &> /dev/null; then
    bash "$DIR/setup.sh"
fi

echo "Starting Workshop Environment..."
uv run python scripts/workshop.py status
bash
