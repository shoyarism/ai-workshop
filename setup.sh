#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "======================================================================"
echo "          WORKSHOP OS - PORTABLE ONBOARDING BOOTSTRAP (POSIX)"
echo "======================================================================"

if ! command -v uv &> /dev/null; then
    echo "[*] Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

echo "[*] Running onboard..."
uv run python scripts/workshop_onboard.py

echo "[*] Running doctor..."
uv run python scripts/workshop.py doctor

echo "[✓] Workshop OS Ready on this machine!"
