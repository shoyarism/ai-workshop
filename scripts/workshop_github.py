#!/usr/bin/env python3
"""
Workshop GitHub Ecosystem & Repository Inspector
================================================
Searches, inspects, and monitors trending GitHub repositories,
topics, and releases across open-source AI and developer ecosystems.

Usage:
    python scripts/workshop_github.py search "<query>" [--limit 10]
    python scripts/workshop_github.py trending [--topic agents|llm|tools] [--limit 10]
    python scripts/workshop_github.py inspect <owner/repo>
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
from typing import Dict, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

GITHUB_API_BASE = "https://api.github.com"
USER_AGENT = "Workshop-GitHub-Inspector/2.0 (Windows NT 10.0; Win64; x64) Python/3.12"


def _api_get(endpoint: str, params: Dict[str, Any] = None) -> Any:
    """Execute GET request to GitHub API."""
    url = f"{GITHUB_API_BASE}/{endpoint.lstrip('/')}"
    if params:
        url += f"?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github.v3+json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "status": e.code}
    except Exception as e:
        return {"error": str(e), "status": 500}


def format_number(n: Any) -> str:
    try:
        val = float(n)
        if val >= 1_000_000:
            return f"{val / 1_000_000:.1f}M"
        if val >= 1_000:
            return f"{val / 1_000:.1f}k"
        return str(int(val))
    except (ValueError, TypeError):
        return str(n)


def cmd_search(args):
    """Search repositories on GitHub."""
    query = args.query
    limit = getattr(args, "limit", 10) or 10
    sort = getattr(args, "sort", "stars") or "stars"
    
    res = _api_get("search/repositories", {
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": limit
    })
    
    if isinstance(res, dict) and "error" in res:
        print(f"[!] Error querying GitHub: {res['error']}")
        return
        
    items = res.get("items", [])
    
    print("\n=======================================================")
    print(f" 🐙 GITHUB SEARCH: '{query}' (Found: {res.get('total_count', len(items)):,} Repositories)")
    print("=======================================================\n")
    
    print(f"{'Repository':<38} | {'Stars':<8} | {'Forks':<7} | {'Language':<12} | {'Description'}")
    print("-" * 95)
    
    for item in items:
        name = item.get("full_name", "")[:36]
        stars = format_number(item.get("stargazers_count", 0))
        forks = format_number(item.get("forks_count", 0))
        lang = (item.get("language") or "N/A")[:10]
        desc = (item.get("description") or "No description")[:32].replace("\n", " ")
        print(f"{name:<38} | {stars:<8} | {forks:<7} | {lang:<12} | {desc}...")
        
    print("-" * 95)
    print()


def cmd_trending(args):
    """Show trending and popular repositories by AI topic."""
    topic = getattr(args, "topic", "ai-agents") or "ai-agents"
    limit = getattr(args, "limit", 10) or 10
    
    topic_query_map = {
        "agents": "topic:ai-agents stars:>1000",
        "llm": "topic:llm stars:>2000",
        "tools": "topic:developer-tools stars:>2000",
        "vision": "topic:computer-vision stars:>1000"
    }
    q = topic_query_map.get(topic, f"topic:{topic} stars:>1000")
    
    res = _api_get("search/repositories", {
        "q": q,
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    })
    
    if isinstance(res, dict) and "error" in res:
        print(f"[!] Error fetching trending repos: {res['error']}")
        return
        
    items = res.get("items", [])
    
    print("\n=======================================================")
    print(f" 🔥 GITHUB POPULAR & TRENDING [Topic: {topic.upper()}]")
    print("=======================================================\n")
    
    print(f"{'Repository':<38} | {'Stars':<8} | {'Language':<12} | {'Description'}")
    print("-" * 90)
    
    for item in items:
        name = item.get("full_name", "")[:36]
        stars = format_number(item.get("stargazers_count", 0))
        lang = (item.get("language") or "N/A")[:10]
        desc = (item.get("description") or "No description")[:34].replace("\n", " ")
        print(f"{name:<38} | {stars:<8} | {lang:<12} | {desc}...")
        
    print("-" * 90)
    print()


def cmd_inspect(args):
    """Inspect a specific GitHub repository's stats, license, and releases."""
    repo = args.repo.strip()
    if repo.startswith("https://github.com/"):
        repo = repo.replace("https://github.com/", "").strip("/")
        
    data = _api_get(f"repos/{repo}")
    if isinstance(data, dict) and "error" in data:
        print(f"[!] Could not inspect repo '{repo}': {data['error']}")
        return
        
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
        
    # Also fetch latest release
    rel = _api_get(f"repos/{repo}/releases/latest")
    latest_ver = rel.get("tag_name", "No releases") if isinstance(rel, dict) and "tag_name" in rel else "None"
    
    print("\n=======================================================")
    print(f" 🐙 GITHUB REPOSITORY INSPECTION: {data.get('full_name')}")
    print("=======================================================\n")
    print(f" • Repository     : {data.get('full_name')}")
    print(f" • Description    : {data.get('description', 'N/A')}")
    print(f" • Stars / Watch  : {format_number(data.get('stargazers_count', 0))} stars | {format_number(data.get('subscribers_count', 0))} watchers")
    print(f" • Forks          : {format_number(data.get('forks_count', 0))}")
    print(f" • Open Issues    : {format_number(data.get('open_issues_count', 0))}")
    print(f" • Primary Lang   : {data.get('language', 'N/A')}")
    print(f" • License        : {data.get('license', {}).get('spdx_id', 'N/A') if data.get('license') else 'None'}")
    print(f" • Default Branch : {data.get('default_branch', 'main')}")
    print(f" • Latest Release : {latest_ver}")
    print(f" • Topics         : {', '.join(data.get('topics', [])[:8])}")
    print(f"\n 🔗 GitHub URL    : {data.get('html_url')}")
    print("=======================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Workshop GitHub Ecosystem & Repository Inspector")
    subparsers = parser.add_subparsers(dest="subaction", help="GitHub action")
    
    # search
    p_s = subparsers.add_parser("search", help="Search repositories on GitHub")
    p_s.add_argument("query", help="Search query (e.g. 'mcp server', 'playwright', 'rag')")
    p_s.add_argument("--limit", "-l", type=int, default=10, help="Result limit")
    p_s.add_argument("--sort", "-s", choices=["stars", "forks", "updated"], default="stars")
    
    # trending
    p_t = subparsers.add_parser("trending", help="Show popular repositories by topic")
    p_t.add_argument("--topic", "-t", choices=["agents", "llm", "tools", "vision"], default="agents")
    p_t.add_argument("--limit", "-l", type=int, default=10, help="Result limit")
    
    # inspect
    p_i = subparsers.add_parser("inspect", help="Inspect detailed repository metrics and releases")
    p_i.add_argument("repo", help="Repository slug (e.g. 'browser-use/browser-use')")
    p_i.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    if args.subaction == "search":
        cmd_search(args)
    elif args.subaction == "trending" or not args.subaction:
        cmd_trending(args)
    elif args.subaction == "inspect":
        cmd_inspect(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
