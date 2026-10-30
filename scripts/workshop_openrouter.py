#!/usr/bin/env python3
"""
Workshop OpenRouter Model Gateway & Pricing Engine
==================================================
Real-time discovery, pricing analysis, and free-tier inspection across
445+ commercial and open-source models aggregated on OpenRouter.

Usage:
    python scripts/workshop_openrouter.py free
    python scripts/workshop_openrouter.py search "<query>" [--limit 10]
    python scripts/workshop_openrouter.py inspect <model_id>
    python scripts/workshop_openrouter.py cheapest [--min-context 32000] [--limit 10]
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
USER_AGENT = "Workshop-OpenRouter/2.0 (Windows NT 10.0; Win64; x64) Python/3.12"


def _fetch_models() -> List[Dict[str, Any]]:
    """Fetch all models metadata from OpenRouter API."""
    req = urllib.request.Request(OPENROUTER_MODELS_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", [])
    except Exception as e:
        print(f"[!] Error querying OpenRouter API: {e}")
        return []


def _format_price(price_str: Any) -> str:
    """Format per-token pricing to dollars per million tokens ($/M)."""
    try:
        val = float(price_str)
        if val == 0:
            return "$0.00 (FREE)"
        per_million = val * 1_000_000
        if per_million < 0.01:
            return f"${per_million:.4f}/M"
        return f"${per_million:.2f}/M"
    except (ValueError, TypeError):
        return str(price_str)


def format_number(n: Any) -> str:
    try:
        val = float(n)
        if val >= 1_000_000:
            return f"{val / 1_000_000:.1f}M"
        if val >= 1_000:
            return f"{val / 1_000:.0f}k"
        return str(int(val))
    except (ValueError, TypeError):
        return str(n)


def cmd_free(args):
    """List all completely free models on OpenRouter."""
    models = _fetch_models()
    free_models = [m for m in models if ":free" in m.get("id", "") or (
        float(m.get("pricing", {}).get("prompt", 1)) == 0 and
        float(m.get("pricing", {}).get("completion", 1)) == 0
    )]
    
    print("\n=======================================================")
    print(f" 🎁 OPENROUTER 100% FREE MODELS ({len(free_models)} Available)")
    print("=======================================================\n")
    
    print(f"{'Model ID':<48} | {'Context':<8} | {'Modality'}")
    print("-" * 75)
    
    for m in sorted(free_models, key=lambda x: x.get("id", "")):
        m_id = m.get("id", "")
        ctx = format_number(m.get("context_length", 0))
        arch = m.get("architecture", {})
        modality = arch.get("modality", "text->text")
        print(f"{m_id:<48} | {ctx:<8} | {modality}")
        
    print("-" * 75)
    print(" Tip: Use model IDs ending with ':free' in your API calls with zero billing.\n")


def cmd_search(args):
    """Search models by name, architecture, or provider."""
    query = args.query.lower().strip()
    limit = getattr(args, "limit", 10) or 10
    models = _fetch_models()
    
    matches = []
    for m in models:
        m_id = m.get("id", "").lower()
        name = m.get("name", "").lower()
        desc = m.get("description", "").lower()
        if query in m_id or query in name or query in desc:
            matches.append(m)
            
    print("\n=======================================================")
    print(f" 🔍 OPENROUTER SEARCH: '{args.query}' (Found: {len(matches)})")
    print("=======================================================\n")
    
    print(f"{'Model ID':<44} | {'Context':<7} | {'Prompt $/M':<12} | {'Output $/M'}")
    print("-" * 80)
    
    for m in matches[:limit]:
        m_id = m.get("id", "")[:42]
        ctx = format_number(m.get("context_length", 0))
        p_price = _format_price(m.get("pricing", {}).get("prompt", 0))
        c_price = _format_price(m.get("pricing", {}).get("completion", 0))
        print(f"{m_id:<44} | {ctx:<7} | {p_price:<12} | {c_price}")
        
    print("-" * 80)
    print(f" Showing top {min(len(matches), limit)} matches.\n")


def cmd_inspect(args):
    """Inspect detailed model parameters, context limits, and pricing."""
    model_id = args.model_id.strip()
    models = _fetch_models()
    
    target = None
    for m in models:
        if m.get("id", "").lower() == model_id.lower():
            target = m
            break
            
    if not target:
        for m in models:
            if model_id.lower() in m.get("id", "").lower():
                target = m
                break
                
    if not target:
        print(f"[!] Model '{model_id}' not found on OpenRouter.")
        return
        
    if getattr(args, "json", False):
        print(json.dumps(target, indent=2))
        return
        
    pricing = target.get("pricing", {})
    arch = target.get("architecture", {})
    
    print("\n=======================================================")
    print(f" 📦 OPENROUTER MODEL SPEC: {target.get('id')}")
    print("=======================================================\n")
    print(f" • Display Name     : {target.get('name', 'N/A')}")
    print(f" • Model Slug       : {target.get('id')}")
    print(f" • Context Window   : {target.get('context_length', 0):,} tokens")
    print(f" • Max Output Tokens: {target.get('top_provider', {}).get('max_completion_tokens', 'N/A')}")
    print(f" • Architecture     : {arch.get('instruct_type', 'N/A')} ({arch.get('modality', 'text->text')})")
    print(f" • Input Pricing    : {_format_price(pricing.get('prompt', 0))}")
    print(f" • Output Pricing   : {_format_price(pricing.get('completion', 0))}")
    print(f" • Image Pricing    : {_format_price(pricing.get('image', 0))}")
    print(f"\n Description:\n {target.get('description', 'No description provided.').strip()[:400]}...")
    print("\n=======================================================\n")


def cmd_cheapest(args):
    """Find the cheapest models meeting a minimum context length."""
    min_ctx = getattr(args, "min_context", 32000) or 32000
    limit = getattr(args, "limit", 10) or 10
    models = _fetch_models()
    
    qualified = []
    for m in models:
        ctx = m.get("context_length", 0)
        if ctx >= min_ctx:
            try:
                p_cost = float(m.get("pricing", {}).get("prompt", 999))
                c_cost = float(m.get("pricing", {}).get("completion", 999))
                if p_cost >= 0 and c_cost >= 0:
                    avg_cost = (p_cost + c_cost) / 2
                    qualified.append((avg_cost, m))
            except Exception:  # @court-exempt: handled fallback
                pass
                
    qualified.sort(key=lambda x: x[0])
    
    print("\n=======================================================")
    print(f" 💰 LOWEST COST MODELS (Min Context: {min_ctx:,} tokens)")
    print("=======================================================\n")
    
    print(f"{'Model ID':<44} | {'Context':<8} | {'Prompt $/M':<12} | {'Output $/M'}")
    print("-" * 80)
    
    for _, m in qualified[:limit]:
        m_id = m.get("id", "")[:42]
        ctx = format_number(m.get("context_length", 0))
        p_price = _format_price(m.get("pricing", {}).get("prompt", 0))
        c_price = _format_price(m.get("pricing", {}).get("completion", 0))
        print(f"{m_id:<44} | {ctx:<8} | {p_price:<12} | {c_price}")
        
    print("-" * 80)
    print()


def main():
    parser = argparse.ArgumentParser(description="Workshop OpenRouter Model Gateway & Pricing Engine")
    subparsers = parser.add_subparsers(dest="subaction", help="OpenRouter action")
    
    # free
    subparsers.add_parser("free", help="List all 100 percent free models on OpenRouter")
    
    # search
    p_s = subparsers.add_parser("search", help="Search models by name or query")
    p_s.add_argument("query", help="Search term (e.g. 'deepseek', 'claude', 'coder')")
    p_s.add_argument("--limit", "-l", type=int, default=10, help="Result limit")
    
    # inspect
    p_i = subparsers.add_parser("inspect", help="Inspect detailed model spec and pricing")
    p_i.add_argument("model_id", help="Model ID (e.g. 'deepseek/deepseek-r1')")
    p_i.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # cheapest
    p_c = subparsers.add_parser("cheapest", help="Find cheapest models by minimum context")
    p_c.add_argument("--min-context", "-c", type=int, default=32000, help="Minimum context length in tokens")
    p_c.add_argument("--limit", "-l", type=int, default=10, help="Result limit")
    
    args = parser.parse_args()
    
    if args.subaction == "free" or not args.subaction:
        cmd_free(args)
    elif args.subaction == "search":
        cmd_search(args)
    elif args.subaction == "inspect":
        cmd_inspect(args)
    elif args.subaction == "cheapest":
        cmd_cheapest(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
