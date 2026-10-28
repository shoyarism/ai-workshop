#!/usr/bin/env python3
"""
API Scout — Instant Search Engine for Public APIs, Free-for-Dev, and Self-Hosted Catalogs.
Parses and queries over 1,500+ curated APIs and developer resources in Workshop.
"""

import os
import re
import json
import argparse
from pathlib import Path

WORKSHOP_DIR = Path(__file__).resolve().parent.parent.parent
PUBLIC_APIS_MD = WORKSHOP_DIR / "public-apis" / "README.md"
FREE_DEV_MD = WORKSHOP_DIR / "free-for-dev" / "README.md"
SELF_HOSTED_MD = WORKSHOP_DIR / "awesome-selfhosted" / "README.md"
CACHE_FILE = Path(__file__).resolve().parent / "public_apis_cache.json"

def parse_public_apis():
    if not PUBLIC_APIS_MD.exists():
        return []
    
    with open(PUBLIC_APIS_MD, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    
    apis = []
    current_category = "General"
    
    for line in lines:
        line_str = line.strip()
        if line_str.startswith("### "):
            current_category = line_str.replace("### ", "").strip()
            continue
        
        if line_str.startswith("|") and not line_str.startswith("|:") and not line_str.startswith("| API"):
            parts = [p.strip() for p in line_str.split("|")[1:-1]]
            if len(parts) >= 5:
                raw_name_link = parts[0]
                desc = parts[1]
                auth = parts[2].replace("`", "")
                https = parts[3]
                cors = parts[4]
                
                # Match [Name](url)
                m = re.match(r"\[(.*?)\]\((.*?)\)", raw_name_link)
                if m:
                    name = m.group(1)
                    url = m.group(2)
                else:
                    name = raw_name_link
                    url = ""
                
                apis.append({
                    "name": name,
                    "url": url,
                    "category": current_category,
                    "description": desc,
                    "auth": auth,
                    "https": https,
                    "cors": cors
                })
    return apis

def get_apis():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    apis = parse_public_apis()
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(apis, f, indent=2)
    except Exception:
        pass
    return apis

def search_free_for_dev(query):
    if not FREE_DEV_MD.exists():
        return []
    with open(FREE_DEV_MD, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    results = []
    for line in content.splitlines():
        if query.lower() in line.lower() and ("http://" in line or "https://" in line):
            results.append(line.strip())
    return results[:15]

def search_self_hosted(query):
    if not SELF_HOSTED_MD.exists():
        return []
    with open(SELF_HOSTED_MD, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    results = []
    for line in content.splitlines():
        if query.lower() in line.lower() and ("http://" in line or "https://" in line):
            results.append(line.strip())
    return results[:15]

def main():
    parser = argparse.ArgumentParser(description="Query public APIs and developer resources in Workshop")
    parser.add_argument("query", nargs="?", default="", help="Keyword to search in API name or description")
    parser.add_argument("--category", "-c", help="Filter by category (e.g., Cryptocurrency, Weather, Machine Learning)")
    parser.add_argument("--no-auth", action="store_true", help="Only show APIs that require No Auth / API key")
    parser.add_argument("--cors", action="store_true", help="Only show APIs with CORS support (Yes)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--free-dev", action="store_true", help="Search free-for-dev catalog")
    parser.add_argument("--self-hosted", action="store_true", help="Search awesome-selfhosted catalog")
    parser.add_argument("--limit", type=int, default=20, help="Max results to display")
    
    args = parser.parse_args()
    
    if args.free_dev:
        res = search_free_for_dev(args.query)
        print(f"=== Free-For-Dev Results ({len(res)}) ===")
        for r in res:
            print(r)
        return

    if args.self_hosted:
        res = search_self_hosted(args.query)
        print(f"=== Awesome-Selfhosted Results ({len(res)}) ===")
        for r in res:
            print(r)
        return
    
    apis = get_apis()
    q = args.query.lower()
    
    matches = []
    for api in apis:
        if args.category and args.category.lower() not in api["category"].lower():
            continue
        if args.no_auth and api["auth"].lower() != "no":
            continue
        if args.cors and api["cors"].lower() != "yes":
            continue
        if q:
            text = f"{api['name']} {api['category']} {api['description']}".lower()
            if q not in text:
                continue
        matches.append(api)
    
    matches = matches[:args.limit]
    
    if args.json:
        print(json.dumps(matches, indent=2))
        return
    
    print(f"Found {len(matches)} matching Public APIs (showing up to {args.limit}):\n")
    for i, api in enumerate(matches, 1):
        auth_tag = f"[Auth: {api['auth']}]" if api['auth'] else "[Auth: None]"
        cors_tag = "[CORS: Yes]" if api['cors'].lower() == 'yes' else ""
        print(f"{i}. {api['name']} ({api['category']}) - {api['url']}")
        print(f"   Description: {api['description']}")
        print(f"   Security: {auth_tag} {cors_tag} [HTTPS: {api['https']}]\n")

if __name__ == "__main__":
    main()
