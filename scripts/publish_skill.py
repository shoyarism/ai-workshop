#!/usr/bin/env python3
"""
Workshop Remote Skill Publisher
================================
Allows any AI agent or developer to push, update, or remove skills directly
in the remote GitHub repository (shoyarism/ai-workshop) WITHOUT needing to clone it.

Requirements:
    Environment variable GITHUB_TOKEN with 'Contents: Read and write' permission.

Usage:
    # Publish / Update a skill:
    python publish_skill.py push <skill-name> <path/to/SKILL.md>

    # View a remote skill:
    python publish_skill.py get <skill-name>

    # List all remote skills:
    python publish_skill.py list
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

REPO = "shoyarism/ai-workshop"
API_BASE = f"https://api.github.com/repos/{REPO}"


def _get_token() -> str:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("[!] Error: GITHUB_TOKEN environment variable is not set.", file=sys.stderr)
        print("    Create a fine-grained Personal Access Token with 'Contents: Read and write' permission.", file=sys.stderr)
        sys.exit(1)
    return token


def _api_request(url: str, method: str = "GET", data: dict = None) -> tuple[int, dict]:
    token = _get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Workshop-Remote-Sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(error_body)
        except Exception:
            err_json = {"message": error_body}
        return e.code, err_json


def push_skill(skill_name: str, file_path: str):
    """Create or update a skill in the remote repo."""
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    b64_content = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    target_path = f"skills/{skill_name}/SKILL.md"
    url = f"{API_BASE}/contents/{target_path}"

    # Check if file already exists to get its SHA (required for updates)
    status, res = _api_request(url, method="GET")
    existing_sha = res.get("sha") if status == 200 else None

    action = "update" if existing_sha else "add"
    payload = {
        "message": f"feat(skills): {action} {skill_name} skill via agent",
        "content": b64_content,
        "branch": "main",
    }
    if existing_sha:
        payload["sha"] = existing_sha

    put_status, put_res = _api_request(url, method="PUT", data=payload)
    if put_status in (200, 201):
        commit_sha = put_res.get("commit", {}).get("sha", "unknown")[:8]
        print(f"[✓] Successfully {action}d skill '{skill_name}' on GitHub (commit: {commit_sha})")
        print(f"    URL: https://github.com/{REPO}/tree/main/{target_path}")
    else:
        print(f"[!] Failed to publish skill: {put_res.get('message')}", file=sys.stderr)
        sys.exit(1)


def get_skill(skill_name: str):
    """Fetch raw SKILL.md content from GitHub."""
    target_path = f"skills/{skill_name}/SKILL.md"
    url = f"{API_BASE}/contents/{target_path}"
    token = _get_token()
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw+json",
            "User-Agent": "Workshop-Remote-Sync",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[!] Skill '{skill_name}' not found in remote repository.", file=sys.stderr)
        else:
            print(f"[!] Error fetching skill ({e.code}): {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)


def list_skills():
    """List all available skills in the remote repo."""
    url = f"{API_BASE}/contents/skills"
    status, res = _api_request(url)
    if status == 200 and isinstance(res, list):
        dirs = [item["name"] for item in res if item.get("type") == "dir"]
        print(f"=== Total Skills in Remote Workshop: {len(dirs)} ===")
        for d in sorted(dirs):
            print(f"  - {d}")
    else:
        print(f"[!] Error listing skills: {res.get('message')}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "push":
        if len(sys.argv) < 4:
            print("Usage: python publish_skill.py push <skill-name> <path/to/SKILL.md>")
            sys.exit(1)
        push_skill(sys.argv[2], sys.argv[3])
    elif cmd == "get":
        if len(sys.argv) < 3:
            print("Usage: python publish_skill.py get <skill-name>")
            sys.exit(1)
        get_skill(sys.argv[2])
    elif cmd == "list":
        list_skills()
    else:
        print(f"[!] Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
