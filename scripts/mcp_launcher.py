#!/usr/bin/env python3
"""
Workshop MCP Server Manager & Launcher
======================================
Inspect, test, and launch official and custom Model Context Protocol (MCP) servers.

Usage:
    python scripts/mcp_launcher.py list
    python scripts/mcp_launcher.py test <server-name>
    python scripts/mcp_launcher.py start <server-name>
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception as err:  # @court-exempt: handled fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(WORKSHOP_DIR / ".env")
except ImportError:  # @court-exempt: optional dotenv fallback
    pass

MCP_REGISTRY = {
    "playwright": {
        "command": ["npx", "-y", "@playwright/mcp"],
        "description": "Interactive browser automation, DOM inspection, clicking and typing",
    },
    "puppeteer": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-puppeteer"],
        "description": "Headless browser scraping, PDF generation, and DOM extraction",
    },
    "chrome-devtools": {
        "command": ["npx", "-y", "chrome-devtools-mcp@latest"],
        "description": "Chrome DevTools Protocol debugging and runtime inspection",
    },
    "memory": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-memory"],
        "description": "Persistent knowledge graph memory across agent sessions",
    },
    "sequential-thinking": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-sequential-thinking"],
        "description": "Dynamic multi-step reasoning and root-cause analysis",
    },
    "fetch": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-fetch"],
        "description": "Web fetch and HTML-to-markdown conversion",
    },
    "github": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
        "description": "GitHub PRs, issues, commits, and repository management",
    },
    "git": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-git"],
        "description": "Local Git repository inspection and operations",
    },
    "filesystem": {
        "command": [
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(WORKSHOP_DIR),
        ],
        "description": "Direct workspace filesystem operations",
    },
    "camofox-browser": {
        "command": ["node", str(WORKSHOP_DIR / "camofox-browser" / "server.js")],
        "description": "Stealth Anti-Detect browser server with fingerprint protection",
    },
    "sqlite": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-sqlite"],
        "description": "SQLite database inspection and query execution",
    },
    "postgres": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-postgres"],
        "description": "PostgreSQL database management and inspection",
    },
    "docker": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-docker"],
        "description": "Docker container management and containerized inspection",
    },
    "firebase": {
        "command": ["npx", "-y", "firebase-tools@latest", "mcp"],
        "description": "Firebase Cloud services and Data Connect management",
    },
    "terraform": {
        "command": ["npx", "-y", "mcp-terraform"],
        "description": "Terraform Infrastructure-as-Code automation and management",
    },
    "brave-search": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-brave-search"],
        "description": "Brave Web Search API integration for real-time web querying",
    },
    "time": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-time"],
        "description": "Timezone, temporal calculations, and clock conversion tools",
    },
    "sentry": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-sentry"],
        "description": "Sentry error tracking, issue triage, and stack trace inspection",
    },
    "linear": {
        "command": ["npx", "-y", "@modelcontextprotocol/server-linear"],
        "description": "Linear project management, issue tracking, and workflow automation",
    },
    "exa-search": {
        "command": ["npx", "-y", "exa-mcp-server"],
        "description": "Neural search engine for web, code, and documentation research",
    },
    "notion": {
        "command": ["npx", "-y", "@notionhq/notion-mcp-server"],
        "description": "Official Notion MCP server — create, query, and update pages and databases",
    },
    "google-workspace": {
        "command": ["npx", "-y", "google-workspace-mcp"],
        "description": "Google Workspace integration — Gmail, Drive, Sheets, Docs, Slides, Calendar",
        "env": {"GOOGLE_APPLICATION_CREDENTIALS": "${GOOGLE_APPLICATION_CREDENTIALS}"},
    },
    "microsoft-graph": {
        "command": ["npx", "-y", "microsoft-graph-mcp"],
        "description": "Microsoft 365 integration — Outlook, Teams, OneDrive, Excel Online, Planner",
        "env": {
            "MICROSOFT_TENANT_ID": "${MICROSOFT_TENANT_ID}",
            "MICROSOFT_CLIENT_ID": "${MICROSOFT_CLIENT_ID}",
        },
    },
    "airtable": {
        "command": ["npx", "-y", "airtable-mcp-server"],
        "description": "Airtable database integration — read, write, and automate base operations",
        "env": {"AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}"},
    },
    "stripe": {
        "command": ["npx", "-y", "@stripe/mcp"],
        "description": "Stripe payment integration — transactions, customers, subscriptions, invoices",
        "env": {"STRIPE_API_KEY": "${STRIPE_API_KEY}"},
    },
    "mcp-inspector": {
        "command": ["npx", "-y", "@modelcontextprotocol/inspector"],
        "description": "Official MCP Inspector developer test harness and inspection UI",
    },
    "stagehand": {
        "command": ["npx", "-y", "@browserbasehq/stagehand"],
        "description": "Stagehand Playwright AI browser automation and natural language actions",
    },
    "supabase": {
        "command": ["npx", "-y", "@supabase/mcp"],
        "description": "Supabase database management — PostgreSQL, Auth, Storage, Realtime",
        "env": {
            "SUPABASE_URL": "${SUPABASE_URL}",
            "SUPABASE_ANON_KEY": "${SUPABASE_ANON_KEY}",
        },
    },
}


def list_servers():
    print("\n=======================================================")
    print(
        f" 🛠️  Registered Workshop MCP Servers ({len(MCP_REGISTRY)} Extended Toolsets)"
    )
    print("=======================================================\n")
    for name, info in MCP_REGISTRY.items():
        cmd_str = " ".join(info["command"])
        print(f" • \033[1;36m{name:<20}\033[0m : {info['description']}")
        print(f"   Command: {cmd_str}\n")


def test_server(name: str):
    if name not in MCP_REGISTRY:
        print(
            f"[!] Server '{name}' not found. Available servers: {', '.join(MCP_REGISTRY.keys())}"
        )
        return
    info = MCP_REGISTRY[name]
    print(f"[*] Testing launch for MCP server: '{name}'...")
    try:
        # Check command executable availability
        cmd_exe = info["command"][0]
        p = subprocess.Popen(
            info["command"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True if os.name == "nt" else False,
        )
        time_to_wait = 2.0
        import time

        time.sleep(time_to_wait)
        if p.poll() is None:
            print(
                f"[OK] MCP Server '{name}' spawned successfully and is waiting for JSON-RPC messages."
            )
            p.terminate()
        else:
            stderr = p.stderr.read().decode("utf-8", errors="ignore")
            print(f"[!] MCP Server exited with code {p.returncode}: {stderr[:300]}")
    except Exception as e:
        print(f"[!] Error launching server: {e}")


def main():
    parser = argparse.ArgumentParser(description="Workshop MCP Server Launcher")
    parser.add_argument(
        "action",
        choices=["list", "test", "start"],
        nargs="?",
        default="list",
        help="Action to perform",
    )
    parser.add_argument(
        "name", nargs="?", default="", help="Server name (e.g. 'playwright', 'memory')"
    )

    args = parser.parse_args()
    if args.action == "list":
        list_servers()
    elif args.action == "test":
        if not args.name:
            print(
                "Please specify a server name to test (e.g. python scripts/mcp_launcher.py test memory)"
            )
        else:
            test_server(args.name)
    elif args.action == "start":
        if not args.name or args.name not in MCP_REGISTRY:
            print(f"Please specify a valid server name: {list(MCP_REGISTRY.keys())}")
        else:
            cmd = MCP_REGISTRY[args.name]["command"]
            print(f"[*] Starting MCP Server: {args.name}...")
            subprocess.run(cmd, shell=True if os.name == "nt" else False)


if __name__ == "__main__":
    main()
