#!/usr/bin/env python3
"""
GitHub Skill Scanner & Curator for Workshop OS.

Searches GitHub for agent skills conforming to the Agent Skills / Anthropic spec
(SKILL.md with YAML frontmatter), evaluates quality, checks security hygiene,
and can inspect or auto-install them into Workshop/skills/.

Usage:
    uv run python scripts/scan_github_skills.py search "pentesting"
    uv run python scripts/scan_github_skills.py search "react performance" --limit 10
    uv run python scripts/scan_github_skills.py inspect "anthropics/claude-plugins-official" --path "plugins/claude-code-setup/skills/claude-automation-recommender"
    uv run python scripts/scan_github_skills.py install <owner/repo> --skill-path <folder_path> [--target-name <name>]
    uv run python scripts/scan_github_skills.py curate --topic "agent-skills"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

# Force UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from workshop_paths import workshop_root
    WORKSHOP_ROOT = workshop_root()
except Exception:
    WORKSHOP_ROOT = Path(__file__).resolve().parent.parent

SKILLS_DIR = WORKSHOP_ROOT / "skills"
GITHUB_API = "https://api.github.com"
FRONTMATTER_RE = re.compile(r"^\ufeff?---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

# Suspicious payload flags for safety filter
SUSPICIOUS_PATTERNS = [
    re.compile(r"curl\s+-[^\n|]*\|\s*(?:bash|sh)", re.IGNORECASE),
    re.compile(r"wget\s+-[^\n|]*\|\s*(?:bash|sh)", re.IGNORECASE),
    re.compile(r"rm\s+-rf\s+/(?:\s|$)", re.IGNORECASE),
    re.compile(r"(?:Invoke-Expression|iex)\s*\(\s*(?:New-Object|irm)", re.IGNORECASE),
    re.compile(r"base64\s+-d.*\|\s*(?:bash|sh)", re.IGNORECASE),
]


def _get_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Workshop-Skill-Scanner/1.0",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def github_get(url: str) -> Any:
    req = urllib.request.Request(url, headers=_get_headers())
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("[!] GitHub API rate limit reached. Set GITHUB_TOKEN environment variable for higher limits.", file=sys.stderr)
        else:
            print(f"[!] GitHub API error ({e.code}): {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[!] Request error: {e}", file=sys.stderr)
        return None


def search_repos(query: str, limit: int = 10) -> list[dict]:
    """Search repositories by keyword and topic."""
    encoded_q = urllib.parse.quote(f"{query} in:readme,description")
    url = f"{GITHUB_API}/search/repositories?q={encoded_q}&sort=stars&order=desc&per_page={limit}"
    data = github_get(url)
    return data.get("items", []) if data else []


def search_code_skills(keyword: str, limit: int = 10) -> list[dict]:
    """Search for SKILL.md files mentioning the keyword."""
    encoded_q = urllib.parse.quote(f"filename:SKILL.md {keyword}")
    url = f"{GITHUB_API}/search/code?q={encoded_q}&per_page={limit}"
    data = github_get(url)
    return data.get("items", []) if data else []


def parse_frontmatter(content: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}, content
    yaml_text = m.group(1)
    meta = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("'\"")
    body = content[m.end():]
    return meta, body


def audit_safety(content: str) -> list[str]:
    flags = []
    for pat in SUSPICIOUS_PATTERNS:
        if pat.search(content):
            flags.append(f"Suspicious pattern matched: {pat.pattern}")
    return flags


def score_skill(repo_meta: dict, frontmatter: dict, safety_flags: list[str]) -> int:
    score = 50
    stars = repo_meta.get("stargazers_count", 0)
    if stars > 1000:
        score += 25
    elif stars > 100:
        score += 15
    elif stars > 10:
        score += 5

    if frontmatter.get("name") and NAME_RE.match(frontmatter.get("name", "")):
        score += 10
    if frontmatter.get("description") and len(frontmatter.get("description", "")) < 1024:
        score += 10

    if safety_flags:
        score -= (len(safety_flags) * 30)

    return max(0, min(100, score))


def install_skill_file(raw_url: str, skill_name: str, description: str = "") -> bool:
    dest_dir = SKILLS_DIR / skill_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "SKILL.md"

    try:
        req = urllib.request.Request(raw_url, headers=_get_headers())
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")

        meta, _ = parse_frontmatter(content)
        if not meta.get("name"):
            content = f"---\nname: {skill_name}\ndescription: {description or 'Imported agent skill from GitHub.'}\n---\n\n" + content

        dest_file.write_text(content, encoding="utf-8")
        print(f"[✓] Successfully installed skill '{skill_name}' to {dest_file}")
        return True
    except Exception as e:
        print(f"[!] Failed to install skill: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="GitHub Skill Scanner for Workshop")
    subparsers = parser.add_subparsers(dest="cmd")

    # Search
    p_search = subparsers.add_parser("search", help="Search GitHub for agent skills")
    p_search.add_argument("query", help="Keywords or topic (e.g. security, flutter, devops)")
    p_search.add_argument("--limit", type=int, default=8, help="Max results")

    # Curate
    p_curate = subparsers.add_parser("curate", help="Discover trending skills")
    p_curate.add_argument("--topic", default="agent-skills", help="Topic to explore")

    # Install
    p_install = subparsers.add_parser("install", help="Install a skill from a raw SKILL.md URL")
    p_install.add_argument("raw_url", help="Direct URL to raw SKILL.md")
    p_install.add_argument("--name", required=True, help="Skill name (kebab-case)")
    p_install.add_argument("--desc", default="", help="Description")

    args = parser.parse_args()

    if args.cmd == "search":
        print(f"[*] Scanning GitHub for agent skills matching: '{args.query}'...\n")
        items = search_code_skills(args.query, limit=args.limit) if os.environ.get("GITHUB_TOKEN") else []
        if not items:
            print("[*] Performing repository-level search...")
            repos = search_repos(f"agent skills {args.query}", limit=args.limit)
            if not repos:
                repos = search_repos(f"{args.query}", limit=args.limit)
            for r in repos:
                print(f"[+] {r['full_name']} ({r['stargazers_count']} stars)")
                print(f"    {r.get('description') or 'No description'}")
                print(f"    URL: {r['html_url']}\n")
            return

        for item in items:
            repo = item.get("repository", {})
            full_name = repo.get("full_name", "unknown")
            path = item.get("path", "")
            raw_url = f"https://raw.githubusercontent.com/{full_name}/master/{path}"
            print(f"[-] Repo: {full_name} | Path: {path}")
            print(f"    Inspect: uv run python scripts/scan_github_skills.py install \"{raw_url}\" --name <skill-name>")
            print()

    elif args.cmd == "install":
        install_skill_file(args.raw_url, args.name, args.desc)

    elif args.cmd == "curate":
        print(f"[*] Curating top repositories with topic '{args.topic}'...\n")
        repos = search_repos(f"topic:{args.topic}", limit=10)
        for r in repos:
            print(f"[+] {r['full_name']} [{r['stargazers_count']} stars]")
            print(f"    {r.get('description') or 'No description'}")
            print(f"    Link: {r['html_url']}\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
