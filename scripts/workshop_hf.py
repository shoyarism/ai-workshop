#!/usr/bin/env python3
"""
Workshop Hugging Face Hub Engine & CLI
======================================
First-principles interface for inspecting, searching, and monitoring the
Hugging Face Hub (Models, Datasets, Spaces, Daily Papers, and Telemetry).

Usage:
    python scripts/workshop_hf.py trending [--limit 5] [--json]
    python scripts/workshop_hf.py search "<query>" [--type models|datasets|spaces] [--limit 10]
    python scripts/workshop_hf.py inspect <repo_id> [--type model|dataset|space]
    python scripts/workshop_hf.py papers [--limit 5] [--json]
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

HF_API_BASE = "https://huggingface.co/api"
USER_AGENT = "Workshop-Agent/2.0 (Windows NT 10.0; Win64; x64) Python/3.12"


def _api_get(endpoint: str, params: Dict[str, Any] = None) -> Any:
    """Execute authenticated or anonymous GET request to Hugging Face API."""
    url = f"{HF_API_BASE}/{endpoint.lstrip('/')}"
    if params:
        url += f"?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "status": e.code}
    except Exception as e:
        return {"error": str(e), "status": 500}


def format_number(n: Any) -> str:
    """Format large numbers with readable metric suffixes (k, M, B)."""
    try:
        val = float(n)
        if val >= 1_000_000_000:
            return f"{val / 1_000_000_000:.2f}B"
        if val >= 1_000_000:
            return f"{val / 1_000_000:.2f}M"
        if val >= 1_000:
            return f"{val / 1_000:.1f}k"
        return str(int(val))
    except (ValueError, TypeError):
        return str(n) if n is not None else "0"


def cmd_trending(args):
    """List top trending models, datasets, spaces, and daily papers."""
    limit = getattr(args, "limit", 5) or 5
    
    print("\n=======================================================")
    print(" 🤗 HUGGING FACE HUB LIVE TRENDING TELEMETRY")
    print("=======================================================\n")
    
    # 1. Models by likes
    models = _api_get("models", {"limit": limit, "sort": "likes", "direction": -1})
    if isinstance(models, list):
        print(f" 🔥 TOP {len(models)} TRENDING MODELS (BY COMMUNITY LIKES):")
        for m in models:
            m_id = m.get("id", m.get("modelId", "unknown"))
            likes = format_number(m.get("likes", 0))
            downloads = format_number(m.get("downloads", 0))
            tag = m.get("pipeline_tag", "general")
            print(f"  • {m_id:<45} | Tag: {tag:<18} | Likes: {likes:<6} | Downloads: {downloads}")
        print()

    # 2. Spaces by likes
    spaces = _api_get("spaces", {"limit": limit, "sort": "likes", "direction": -1})
    if isinstance(spaces, list):
        print(f" 🚀 TOP {len(spaces)} POPULAR SPACES & APPLICATIONS:")
        for s in spaces:
            s_id = s.get("id", "unknown")
            likes = format_number(s.get("likes", 0))
            sdk = s.get("sdk", "custom")
            print(f"  • {s_id:<45} | SDK: {sdk:<10} | Likes: {likes}")
        print()

    # 3. Daily Papers
    papers = _api_get("daily_papers", {"limit": limit})
    if isinstance(papers, list):
        print(" 📑 LATEST DAILY RESEARCH PAPERS:")
        for entry in papers[:limit]:
            p = entry.get("paper", entry)
            title = p.get("title", "Untitled")
            p_id = p.get("id", "")
            upvotes = entry.get("paper", {}).get("upvotes", entry.get("upvotes", 0))
            if len(title) > 65:
                title = title[:62] + "..."
            print(f"  • [{p_id}] {title:<65} | Upvotes: {upvotes}")
        print()

    print("=======================================================\n")


def cmd_search(args):
    """Search models, datasets, or spaces on the Hub."""
    query = args.query
    search_type = getattr(args, "type", "models") or "models"
    limit = getattr(args, "limit", 10) or 10
    
    if search_type not in ["models", "datasets", "spaces"]:
        search_type = "models"
        
    res = _api_get(search_type, {"search": query, "limit": limit, "sort": "downloads", "direction": -1})
    
    if isinstance(res, dict) and "error" in res:
        print(f"[!] Error querying Hub: {res['error']}")
        return
        
    if getattr(args, "json", False):
        print(json.dumps(res, indent=2))
        return
        
    print("\n=======================================================")
    print(f" 🔍 HUGGING FACE SEARCH: '{query}' in {search_type.upper()} (Found: {len(res)})")
    print("=======================================================\n")
    
    for item in res:
        item_id = item.get("id", item.get("modelId", "unknown"))
        downloads = format_number(item.get("downloads", 0))
        likes = format_number(item.get("likes", 0))
        tag = item.get("pipeline_tag", item.get("sdk", ""))
        extra = f"Tag: {tag}" if tag else f"Author: {item.get('author', 'community')}"
        print(f"  • {item_id:<50} | {extra:<22} | DLs: {downloads:<8} | Likes: {likes}")
        
    print("\n=======================================================\n")


def cmd_inspect(args):
    """Inspect detailed metadata for a specific model, dataset, or space."""
    repo_id = args.repo_id.strip()
    target_type = getattr(args, "type", "model") or "model"
    
    endpoint_map = {
        "model": f"models/{repo_id}",
        "dataset": f"datasets/{repo_id}",
        "space": f"spaces/{repo_id}"
    }
    endpoint = endpoint_map.get(target_type, f"models/{repo_id}")
    
    data = _api_get(endpoint)
    if isinstance(data, dict) and "error" in data:
        print(f"[!] Could not inspect {target_type} '{repo_id}': {data['error']}")
        return
        
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
        
    print("\n=======================================================")
    print(f" 📦 HUGGING FACE {target_type.upper()} INSPECTION: {repo_id}")
    print("=======================================================\n")
    
    print(f" • Repository ID  : {data.get('id', repo_id)}")
    print(f" • Author / Org   : {data.get('author', repo_id.split('/')[0] if '/' in repo_id else 'unknown')}")
    print(f" • Downloads      : {format_number(data.get('downloads', 0))}")
    print(f" • Likes          : {format_number(data.get('likes', 0))}")
    print(f" • Private        : {data.get('private', False)}")
    print(f" • Gated / Auth   : {data.get('gated', False)}")
    if "pipeline_tag" in data:
        print(f" • Pipeline Tag   : {data.get('pipeline_tag')}")
    if "library_name" in data:
        print(f" • Library Engine : {data.get('library_name')}")
    if "cardData" in data and isinstance(data["cardData"], dict):
        card = data["cardData"]
        if "license" in card:
            print(f" • License        : {card.get('license')}")
        if "base_model" in card:
            print(f" • Base Model     : {card.get('base_model')}")
    if "tags" in data:
        print(f" • Key Tags       : {', '.join(data.get('tags', [])[:8])}")
    if "siblings" in data:
        files = [s.get("rfilename", "") for s in data["siblings"]]
        print(f" • File Count     : {len(files)} files in repository")
        safetensors = [f for f in files if f.endswith(".safetensors")]
        if safetensors:
            print(f" • Safetensors    : {len(safetensors)} tensor shard(s) detected")
            
    print(f"\n 🔗 Web URL: https://huggingface.co/{repo_id}")
    print("=======================================================\n")


def cmd_papers(args):
    """Retrieve trending papers from Hugging Face Daily Papers."""
    limit = getattr(args, "limit", 5) or 5
    papers = _api_get("daily_papers", {"limit": limit})
    
    if isinstance(papers, dict) and "error" in papers:
        print(f"[!] Error fetching daily papers: {papers['error']}")
        return
        
    if getattr(args, "json", False):
        print(json.dumps(papers, indent=2))
        return
        
    print("\n=======================================================")
    print(f" 📑 HUGGING FACE DAILY RESEARCH PAPERS (Latest {len(papers[:limit])})")
    print("=======================================================\n")
    
    for entry in papers[:limit]:
        p = entry.get("paper", entry)
        title = p.get("title", "Untitled")
        p_id = p.get("id", "")
        summary = p.get("summary", "").replace("\n", " ")
        if len(summary) > 220:
            summary = summary[:217] + "..."
        upvotes = entry.get("paper", {}).get("upvotes", entry.get("upvotes", 0))
        
        print(f" 📄 [{p_id}] {title}")
        print(f"    Upvotes: {upvotes} | Link: https://huggingface.co/papers/{p_id}")
        print(f"    Abstract: {summary}\n")
        
    print("=======================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Workshop Hugging Face Hub Engine & CLI")
    subparsers = parser.add_subparsers(dest="hf_command", help="Hugging Face subcommands")
    
    # trending
    p_trend = subparsers.add_parser("trending", help="Show live trending models, spaces, papers")
    p_trend.add_argument("--limit", "-l", type=int, default=5, help="Result limit")
    p_trend.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # search
    p_search = subparsers.add_parser("search", help="Search models, datasets, spaces")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--type", "-t", choices=["models", "datasets", "spaces"], default="models", help="Artifact type")
    p_search.add_argument("--limit", "-l", type=int, default=10, help="Result limit")
    p_search.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect model, dataset, space details")
    p_inspect.add_argument("repo_id", help="Repository ID (e.g. 'deepseek-ai/DeepSeek-R1')")
    p_inspect.add_argument("--type", "-t", choices=["model", "dataset", "space"], default="model", help="Artifact type")
    p_inspect.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # papers
    p_papers = subparsers.add_parser("papers", help="Show daily research papers")
    p_papers.add_argument("--limit", "-l", type=int, default=5, help="Result limit")
    p_papers.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    if args.hf_command == "trending" or not args.hf_command:
        cmd_trending(args)
    elif args.hf_command == "search":
        cmd_search(args)
    elif args.hf_command == "inspect":
        cmd_inspect(args)
    elif args.hf_command == "papers":
        cmd_papers(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
