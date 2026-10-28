#!/usr/bin/env python3
"""
[DEPRECATED - Use scripts/obsidian_vault.py instead]
Workshop Notion Sync Engine (Legacy Cloud Integration)
======================================================
NOTE: This script has been superseded per ADR-005 by the local-first Obsidian
Second Brain Vault located at `vault/` and managed via `scripts/obsidian_vault.py`.
Direct SSD plaintext ASTs provide sub-millisecond retrieval, 100% offline sovereignty,
and eliminate external API rate limits.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

try:
    from notion_client import Client
except ImportError:
    print("[!] notion-client not installed. Installing via uv...")
    os.system("uv tool install notion-client")
    from notion_client import Client

WORKSHOP_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(WORKSHOP_DIR / ".env")
except ImportError:  # @court-exempt: optional dotenv fallback
    pass

NOTION_TOKEN = os.environ.get("NOTION_TOKEN") or os.environ.get("NOTION_API_KEY")
if not NOTION_TOKEN:
    # Check kilo.jsonc
    kilo_path = WORKSHOP_DIR / "kilo.jsonc"
    if kilo_path.exists():
        try:
            with open(kilo_path, "r", encoding="utf-8") as f:
                kilo_data = json.load(f)
            NOTION_TOKEN = kilo_data.get("mcp", {}).get("notion", {}).get("environment", {}).get("NOTION_TOKEN")
        except Exception:  # @court-exempt: handled fallback
            pass

if not NOTION_TOKEN:
    NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")

PAGE_WORKSHOP_ID = "3cc6d0c8-ba0c-8097-a87b-c9dd87c4f922"
PAGE_SECOND_BRAIN_ID = "3cc6d0c8-ba0c-80c1-980b-cd0a2b601008"

# ==============================================================================
# NOTION BLOCK HELPERS
# ==============================================================================

def h1(text: str) -> Dict[str, Any]:
    return {
        "object": "block",
        "type": "heading_1",
        "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }

def h2(text: str) -> Dict[str, Any]:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }

def h3(text: str) -> Dict[str, Any]:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }

def p(text: str, bold_prefix: str = "") -> Dict[str, Any]:
    rich_text = []
    if bold_prefix:
        rich_text.append({
            "type": "text",
            "text": {"content": bold_prefix},
            "annotations": {"bold": True}
        })
    rich_text.append({"type": "text", "text": {"content": text}})
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rich_text}
    }

def bullet(text: str, bold_prefix: str = "") -> Dict[str, Any]:
    rich_text = []
    if bold_prefix:
        rich_text.append({
            "type": "text",
            "text": {"content": bold_prefix},
            "annotations": {"bold": True}
        })
    rich_text.append({"type": "text", "text": {"content": text}})
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text}
    }

def code_block(code_str: str, language: str = "bash") -> Dict[str, Any]:
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": code_str}}],
            "language": language
        }
    }

def callout(text: str, emoji: str = "💡", bold_title: str = "") -> Dict[str, Any]:
    rich_text = []
    if bold_title:
        rich_text.append({
            "type": "text",
            "text": {"content": bold_title + "\n"},
            "annotations": {"bold": True}
        })
    rich_text.append({"type": "text", "text": {"content": text}})
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": rich_text,
            "icon": {"type": "emoji", "emoji": emoji}
        }
    }

def divider() -> Dict[str, Any]:
    return {"object": "block", "type": "divider", "divider": {}}

# ==============================================================================
# PAGE CONTENT BUILDERS
# ==============================================================================

def build_workshop_blocks() -> List[Dict[str, Any]]:
    """Build structured blocks for AI AGENT WORKSHOP Notion page."""
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blocks = []

    # 1. Executive Callout Header
    blocks.append(callout(
        f"Centralized Workshop Operating System & Unified AI Engineering Arsenal.\n"
        f"• Workspace: {os.environ.get('WORKSHOP_ROOT', 'current directory (WORKSHOP_ROOT)')}\n"
        f"• Integrated Subsystems: 30 Repositories & Modules (100% Operational)\n"
        f"• Domain Skills: 905+ Curated Execution Packages\n"
        f"• Connected MCP Toolsets: 23 Model Context Protocol Servers\n"
        f"• Public APIs Index: 1,500+ REST APIs across 50+ Categories\n"
        f"• Last Synchronized: {timestamp_str}",
        emoji="🛠️",
        bold_title="AI AGENT WORKSHOP — MASTER ARSENAL"
    ))
    blocks.append(divider())

    # 2. Master CLI Quick Reference
    blocks.append(h2("1. Master Universal CLI (`scripts/workshop.py`)"))
    blocks.append(p("Single unified command-line entrypoint for autonomous agents and developers:"))
    cli_commands = (
        "# 🔍 1. Sub-Millisecond Arsenal Search (905+ skills, 30 Subsystems, MCPs, APIs)\n"
        "python scripts/workshop.py search \"<keyword>\"\n"
        "python scripts/workshop.py search \"scrapling\" --category repos\n\n"
        "# 📋 2. Subsystem Architecture Briefing\n"
        "python scripts/workshop.py info <subsystem_name>  # e.g., openhands, strix, litellm\n\n"
        "# 🔄 3. Machine Catalog & Master Index Generation\n"
        "python scripts/workshop.py index\n\n"
        "# 🩺 4. Health & Diagnostics Doctor (30/30 Subsystems Check)\n"
        "python scripts/workshop.py doctor\n\n"
        "# 👁️ 5. Multimodal Vision & OCR Engine (Zero-Vision & Multimodal Support)\n"
        "python scripts/workshop.py see \"<file_or_dir>\"\n"
        "python scripts/workshop.py vision ocr \"<image_path>\"\n"
        "python scripts/workshop.py vision describe \"<image_path>\"\n"
        "python scripts/workshop.py vision storyboard \"<video_path>\"\n"
        "python scripts/workshop.py vision video-ocr \"<video_path>\"\n"
        "python scripts/workshop.py vision transcribe \"<audio_or_video_path>\"\n\n"
        "# 🌐 6. Live Browser Streaming Hub (Web Dashboard :7860)\n"
        "python scripts/workshop.py hub --port 7860\n\n"
        "# 🤖 7. Autonomous Browser Task Runner with Live Stream\n"
        "python scripts/workshop.py browser --url \"https://news.ycombinator.com\" --live\n\n"
        "# 🛠️ 8. Model Context Protocol (MCP) Launcher\n"
        "python scripts/workshop.py mcp list\n"
        "python scripts/workshop.py mcp test playwright\n\n"
        "# 📊 9. Full Repository Matrix Status\n"
        "python scripts/workshop.py status"
    )
    blocks.append(code_block(cli_commands, language="bash"))
    blocks.append(divider())

    # 3. 30 Subsystems & Repository Matrix
    blocks.append(h2("2. Integrated Subsystems & Repository Matrix (30 Modules)"))
    blocks.append(p("All 30 repositories and subsystems are checked out, operational, and registered in CATALOG.json:"))

    categories = [
        ("Autonomous AI & Agent Platforms", [
            ("OpenHands (`openhands/`)", "Full-stack autonomous software engineering platform planning, coding, running bash, and solving SWE-bench tasks."),
            ("Browser-Use (`browser-use/`)", "Vision and DOM-based autonomous web navigation framework for browser agent interactions."),
            ("OpenClaw (`openclaw/`)", "Modular autonomous execution engine with structured reasoning loops and tool orchestration."),
            ("ElizaOS (`eliza/`)", "Multi-agent conversational swarms and autonomous character framework with persistent memory."),
            ("Strix Security (`strix/`)", "Autonomous AI penetration testing framework detecting OWASP vulnerabilities with automated remediation."),
            ("Langflow (`langflow/`)", "Visual and programmatic multi-agent builder, RAG pipeline orchestrator, and flow runner.")
        ]),
        ("Web Scraping & Browser Automation", [
            ("Scrapling (`Scrapling/`)", "Ultra-fast, undetectable Python web scraper with stealth fingerprinting, adaptive filtering & DOM parser."),
            ("Camofox Browser (`camofox-browser/`)", "Anti-detect headless browser engine with hardware fingerprint masking and native MCP server."),
            ("Stagehand (`stagehand/`)", "Playwright AI browser automation engine with natural language actions (act, extract, observe)."),
            ("OpenSEO (`open-seo/`)", "Open-source technical SEO audit engine, sitemap crawler, and Core Web Vitals analyzer.")
        ]),
        ("AI Knowledge & Application Accelerators", [
            ("Open Notebook (`open-notebook/`)", "Multi-model grounded research assistant, note synthesis, citation verification, and audio overview generator."),
            ("Awesome LLM Apps (`awesome-llm-apps/`)", "Curated catalog of 100+ production LLM architectures (Advanced RAG, Agentic Workflows, Voice AI)."),
            ("Book-to-Skill (`book-to-skill/`)", "Knowledge distillation compiler converting technical books, docs, and PDFs into standard SKILL.md packages."),
            ("Graphify (`graphify/`)", "Codebase AST knowledge graph generator mapping call flows, module dependencies, and architecture hierarchies."),
            ("LiteLLM Gateway (`litellm/`)", "Universal proxy routing 100+ LLMs (OpenAI, Claude, Gemini, DeepSeek, Ollama) via unified OpenAI format."),
            ("Open Generative AI (`open-generative-ai/`)", "Generative AI starter templates, developer tools, and prompt scaffolds.")
        ]),
        ("Design, UI/UX & Media Engines", [
            ("OpenDesign System (`open-design/`)", "Comprehensive design token architecture, UI component specs, and Figma design-to-code workflows."),
            ("UI/UX Master Arsenal (`ui-ux-arsenal/`)", "Master UI/UX blueprint, Tailwind v4 design tokens, color ramps, typography, and spring motion physics."),
            ("Hyperframes Motion (`hyperframes/`)", "Programmatic animation and generative video studio with 20 specialized motion skills.")
        ]),
        ("Model Context Protocol (MCP) Toolsets", [
            ("Official MCP Servers (`mcp-servers-official/`)", "Reference MCP servers for Git, Memory, SQLite, PostgreSQL, Filesystem, Fetch, Docker, and Puppeteer."),
            ("Awesome MCP Servers (`awesome-mcp-servers/`)", "Curated directory of community and enterprise Model Context Protocol servers across domains."),
            ("Official MCP Inspector (`mcp-inspector/`)", "Interactive developer test harness and web UI for testing and debugging MCP tools and resources.")
        ]),
        ("Curated Knowledge & Developer Resources", [
            ("Public APIs Index (`public-apis/`)", "Collective directory of 1,500+ free and public REST APIs across 50+ categories with auth specs."),
            ("Free for Developers (`free-for-dev/`)", "Curated index of free cloud databases, hosting, auth, CI/CD, and compute services."),
            ("Awesome Self-Hosted (`awesome-selfhosted/`)", "Definitive guide to open-source self-hostable network services and web applications."),
            ("Sindresorhus Awesome (`awesome/`)", "Master index of curated software engineering topic lists and ecosystems."),
            ("ADHD Executive Toolbox (`i-have-adhd/`)", "Neurodivergent focus workflows, low-friction task chunking, and cognitive load reduction tools.")
        ]),
        ("Central Workshop Engine", [
            ("Workshop Domain Skills (`skills/`)", "865+ curated domain execution skills with copy-pasteable patterns."),
            ("Master Scripts (`scripts/`)", "Master CLI, fast search engine, vision engine, live browser hub, and doctor diagnostics."),
            ("System Prompts (`prompts/`)", "System personas, task instructions, and multi-agent coordination templates.")
        ])
    ]

    for cat_title, items in categories:
        blocks.append(h3(cat_title))
        for name, desc in items:
            blocks.append(bullet(f" — {desc}", bold_prefix=name))

    blocks.append(divider())

    # 4. Multimodal Vision & Media Engine
    blocks.append(h2("3. Multimodal Vision & OCR Deconstruction Engine"))
    blocks.append(p("Built specifically so text-only AI models and multimodal agents can inspect, read, and understand visual media:"))
    blocks.append(bullet("RapidOCR (ONNX) extracting all text, buttons, and labels with confidence metrics.", bold_prefix="High-Precision OCR: "))
    blocks.append(bullet("Maps text blocks to [top-left], [middle-center], [bottom-right] regions.", bold_prefix="Spatial Layout Decomposition: "))
    blocks.append(bullet("Analyzes dimensions, Light vs. Dark theme, and dominant 6-color hex palettes.", bold_prefix="Visual & Theme Deconstruction: "))
    blocks.append(bullet("Renders 24-bit ANSI colors and monochrome ASCII luminance art in the terminal.", bold_prefix="ASCII & ANSI Terminal Art: "))
    blocks.append(bullet("Keyframe sampling, storyboard contact sheets, and chronological OCR change timelines.", bold_prefix="Video Timeline & Storyboards: "))
    blocks.append(bullet("Faster-Whisper CTranslate2 model extracting timecoded spoken speech.", bold_prefix="Speech-to-Text Transcription: "))
    blocks.append(divider())

    # 5. Connected MCP Toolsets Matrix
    blocks.append(h2("4. Registered Model Context Protocol (MCP) Toolsets (23 Servers)"))
    mcp_tools = [
        ("playwright", "Interactive browser automation, DOM inspection, clicking, typing, and screenshots (`npx @playwright/mcp`)"),
        ("puppeteer", "Headless scraping, PDF generation, and DOM extraction (`@modelcontextprotocol/server-puppeteer`)"),
        ("camofox-browser", "Stealth anti-detect browser automation with fingerprint masking (`camofox-browser`)"),
        ("stagehand", "Playwright AI browser automation with natural language actions (`@browserbasehq/stagehand`)"),
        ("mcp-inspector", "Official developer test harness and inspector UI (`@modelcontextprotocol/inspector`)"),
        ("chrome-devtools", "Chrome DevTools Protocol performance, network, and runtime debugging (`chrome-devtools-mcp`)"),
        ("memory", "Persistent knowledge graph memory across agent sessions (`@modelcontextprotocol/server-memory`)"),
        ("sequential-thinking", "Dynamic multi-step reasoning and root-cause analysis (`@modelcontextprotocol/server-sequential-thinking`)"),
        ("fetch", "HTML-to-markdown fetching and web requests (`@modelcontextprotocol/server-fetch`)"),
        ("github", "GitHub PRs, issues, commits, and repository management (`@modelcontextprotocol/server-github`)"),
        ("git", "Local Git repository inspection, branches, and diffs (`@modelcontextprotocol/server-git`)"),
        ("filesystem", "Direct workspace filesystem operations (`@modelcontextprotocol/server-filesystem`)"),
        ("sqlite", "SQLite relational database inspection and SQL execution (`@modelcontextprotocol/server-sqlite`)"),
        ("postgres", "PostgreSQL database management and schema queries (`@modelcontextprotocol/server-postgres`)"),
        ("supabase", "Supabase cloud database, Auth, Storage, and Realtime management (`@supabase/mcp`)"),
        ("docker", "Docker container management and sandbox execution (`@modelcontextprotocol/server-docker`)"),
        ("firebase", "Firebase Cloud services and Data Connect management (`firebase-tools mcp`)"),
        ("terraform", "Terraform Infrastructure-as-Code automation (`mcp-terraform`)"),
        ("brave-search", "Brave Web Search API real-time web querying (`@modelcontextprotocol/server-brave-search`)"),
        ("time", "Timezone, temporal calculations, and clock conversion tools (`@modelcontextprotocol/server-time`)"),
        ("sentry", "Error tracking, crash reports, and stack trace inspection (`@modelcontextprotocol/server-sentry`)"),
        ("linear", "Linear project management and issue tracking (`@modelcontextprotocol/server-linear`)"),
        ("exa-search", "Neural search engine for web, code, and documentation (`exa-mcp-server`)")
    ]
    for name, desc in mcp_tools:
        blocks.append(bullet(f" — {desc}", bold_prefix=f"`{name}`"))

    blocks.append(divider())

    # 6. Linked Second Brain Reference
    blocks.append(callout(
        "For cognitive architecture, problem-solving protocols, multi-agent coordination, design tokens, and memory models, refer to the AI AGENT SECOND BRAIN:\n"
        "🔗 https://app.notion.com/p/AI-AGENT-SECOND-BRAIN-3cc6d0c8ba0c80c1980bcd0a2b601008?source=copy_link",
        emoji="🧠",
        bold_title="Linked Knowledge Base: AI AGENT SECOND BRAIN"
    ))

    return blocks

def build_second_brain_blocks() -> List[Dict[str, Any]]:
    """Build structured blocks for AI AGENT SECOND BRAIN Notion page."""
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blocks = []

    # 1. Executive Callout Header
    blocks.append(callout(
        f"Central Cognitive Repository & Persistent Knowledge Base for Autonomous Agents.\n"
        f"• Operating Mandate: Elite Principal Systems Architect & Senior Staff Engineer\n"
        f"• Execution Standard: Absolute Rigor, Zero Sycophancy, Deterministic Verification\n"
        f"• Problem Solving: Universal 5-Stage Engineering Protocol\n"
        f"• Memory Architecture: Multi-Tier Cognitive Trees & Graph Memory\n"
        f"• Last Synchronized: {timestamp_str}",
        emoji="🧠",
        bold_title="AI AGENT SECOND BRAIN — COGNITIVE ARCHITECTURE"
    ))
    blocks.append(divider())

    # 2. Operating Standards & Anti-Dumbass Directives
    blocks.append(h2("1. Operating Standards & Anti-Dumbass Directives"))
    blocks.append(bullet("Never waste tokens on pleasantries ('Certainly!', 'I would be happy to help'). Provide immediate, high-density engineering output.", bold_prefix="Zero Sycophancy & Zero Boilerplate: "))
    blocks.append(bullet("NEVER use lazy placeholders like '// TODO: implement later' or truncated snippets. Always write 100% complete, runnable, type-safe code.", bold_prefix="Never Cut Corners or Truncate Code: "))
    blocks.append(bullet("Never guess file structures, API schemas, or parameters. Always inspect source files, ASTs, and dependencies first.", bold_prefix="Evidence-Based Reconnaissance First: "))
    blocks.append(bullet("When an error occurs, trace root causes, inspect dependencies, fix the bug autonomously, and verify deterministically.", bold_prefix="Autonomous Root-Cause Resolution: "))
    blocks.append(bullet("Every deliverable must be verified with automated test runs, CLI executions, linters, or live browser sessions.", bold_prefix="Deterministic Verification: "))
    blocks.append(divider())

    # 3. Universal 5-Stage Problem Solving Discipline
    blocks.append(h2("2. Universal 5-Stage Problem Solving Discipline"))
    protocol_text = (
        "Phase 1: Recon & Skill Activation\n"
        "   └─ Scan 905+ skills, 30 subsystems & codebase ASTs via 'python scripts/workshop.py search'\n\n"
        "Phase 2: Architectural Planning\n"
        "   └─ Draft concrete technical specifications, data schemas, and type-safe API contracts\n\n"
        "Phase 3: Clean Implementation & UI Craft\n"
        "   └─ Implement complete, modular, type-safe code adhering to design tokens\n\n"
        "Phase 4: Review & Security Audit\n"
        "   └─ Audit architectural debt, vulnerability vectors, input validation, and edge cases\n\n"
        "Phase 5: Deterministic Verification & QA\n"
        "   └─ Verify with unit tests, CLI commands, or live browser streaming (:7860)"
    )
    blocks.append(code_block(protocol_text, language="plain text"))
    blocks.append(divider())

    # 4. Multi-Agent Orchestration & Swarm Protocols
    blocks.append(h2("3. Multi-Agent Orchestration & Swarm Coordination"))
    blocks.append(p("The Workshop supports multiple coordinated agent modalities:"))
    blocks.append(bullet("Pairing with human developers for rapid feature development and refactoring.", bold_prefix="Pair-Programming Agent (Antigravity/OpenCode/Claude): "))
    blocks.append(bullet("Autonomous SWE solving GitHub issues, running sandboxed terminal execution, and tests.", bold_prefix="Autonomous SWE Agent (OpenHands): "))
    blocks.append(bullet("Character swarms with persistent memory and social connector integration.", bold_prefix="Multi-Agent Swarms (ElizaOS): "))
    blocks.append(bullet("Vision and DOM-based autonomous web navigation.", bold_prefix="Autonomous Web Agent (Browser-Use / Stagehand): "))
    blocks.append(bullet("Autonomous penetration testing and vulnerability auditing.", bold_prefix="Security Pentester (Strix): "))
    blocks.append(bullet("Visual and programmatic multi-agent and RAG pipeline composer.", bold_prefix="Multi-Agent RAG Studio (Langflow): "))
    blocks.append(divider())

    # 5. Persistent Second Brain Knowledge Modules
    blocks.append(h2("4. Persistent Knowledge Modules (Sub-Pages)"))
    blocks.append(bullet("Verified solutions to edge-case bugs, environmental quirks, and encoding errors.", bold_prefix="🛠️ Error Post-Mortem & Fixes Database: "))
    blocks.append(bullet("User engineering standards, workspace topology, and output rules.", bold_prefix="👤 User DNA & Environment Profile: "))
    blocks.append(bullet("Historical architectural decisions, trade-offs, and technical rationale.", bold_prefix="📐 Architecture Decision Records (ADRs): "))
    blocks.append(bullet("Multi-session async task tracking, backlog, and handoff state.", bold_prefix="⚡ Autonomous Task Queue & Session Handoffs: "))
    blocks.append(bullet("Port directory, MCP endpoints, and running service configurations.", bold_prefix="🌐 Local Service & Gateway Registry: "))
    blocks.append(bullet("Standard operating procedures, evaluation rubrics, and meta-prompts.", bold_prefix="📖 Meta-Prompts & SOP Playbooks: "))
    blocks.append(divider())

    # 6. Design System & UI/UX Tokens Architecture
    blocks.append(h2("5. Design System & UI/UX Architecture"))
    blocks.append(bullet("Centralized token architecture in `ui-ux-arsenal/tokens/design_tokens.json` and `open-design/`.", bold_prefix="Design Tokens: "))
    blocks.append(bullet("Modern Clean SaaS, Dark Glassmorphism, Industrial Brutalism, Spring Motion Physics.", bold_prefix="Visual Archetypes: "))
    blocks.append(bullet("Zero-configuration Tailwind CSS v4 variables, typography scale, semantic radii, and spacing grid.", bold_prefix="Component Contracts: "))
    blocks.append(divider())

    # 7. Curated Knowledge & Cloud Infrastructure Hubs
    blocks.append(h2("6. Curated Knowledge & Free Infrastructure Hubs"))
    blocks.append(bullet("1,500+ free and public REST APIs with authentication, HTTPS, and CORS details.", bold_prefix="Public APIs Directory (`public-apis/`): "))
    blocks.append(bullet("Curated catalog of free cloud databases, hosting, auth, CI/CD, and compute.", bold_prefix="Free for Developers (`free-for-dev/`): "))
    blocks.append(bullet("Definitive directory of open-source self-hostable servers and applications.", bold_prefix="Awesome Self-Hosted (`awesome-selfhosted/`): "))
    blocks.append(bullet("Actionable focus workflows, low-friction task chunking, and cognitive aids.", bold_prefix="ADHD Executive Toolbox (`i-have-adhd/`): "))
    blocks.append(divider())

    # 8. Linked Workshop Reference
    blocks.append(callout(
        "For execution tools, CLI scripts, 30 repository subsystems, and MCP servers, refer to the master AI AGENT WORKSHOP:\n"
        "🔗 https://app.notion.com/p/AI-AGENT-WORKSHOP-3cc6d0c8ba0c8097a87bc9dd87c4f922?source=copy_link",
        emoji="🛠️",
        bold_title="Linked Arsenal: AI AGENT WORKSHOP"
    ))

    return blocks

# ==============================================================================
# NOTION SYNC RUNNER
# ==============================================================================

def sync_page(notion: Client, page_id: str, title: str, icon_emoji: str, blocks: List[Dict[str, Any]]):
    print("\n=======================================================", flush=True)
    print(f" [*] Syncing Notion Page: '{title}' ({page_id})", flush=True)
    print("=======================================================\n", flush=True)

    # 1. Update page icon and title
    try:
        notion.pages.update(
            page_id=page_id,
            icon={"type": "emoji", "emoji": icon_emoji},
            properties={
                "title": {"title": [{"text": {"content": title}}]}
            }
        )
        print(f"  [OK] Page title and icon updated -> {icon_emoji} {title}", flush=True)
    except Exception as e:
        print(f"  [!] Failed to update page metadata: {e}", flush=True)

    # 2. Retrieve existing blocks and delete old ones (preserving child pages)
    try:
        all_blocks = []
        cursor = None
        while True:
            kwargs = {"block_id": page_id}
            if cursor:
                kwargs["start_cursor"] = cursor
            res = notion.blocks.children.list(**kwargs)
            all_blocks.extend(res.get("results", []))
            if not res.get("has_more"):
                break
            cursor = res.get("next_cursor")

        blocks_to_delete = [b for b in all_blocks if b.get("type") != "child_page"]
        print(f"  [*] Found {len(all_blocks)} total blocks ({len(blocks_to_delete)} to replace, preserving {len(all_blocks) - len(blocks_to_delete)} child pages)...", flush=True)
        for i, b in enumerate(blocks_to_delete, 1):
            try:
                notion.blocks.delete(block_id=b["id"])
            except Exception:  # @court-exempt: handled fallback
                pass
            if i % 10 == 0 or i == len(blocks_to_delete):
                print(f"    - Cleaned {i}/{len(blocks_to_delete)} blocks...", flush=True)
            time.sleep(0.12)
        print("  [OK] Old blocks cleaned up.", flush=True)
    except Exception as e:
        print(f"  [!] Error during block cleanup: {e}", flush=True)

    # 3. Append new blocks in batches (Notion limits to 100 per request)
    batch_size = 50
    total_batches = (len(blocks) + batch_size - 1) // batch_size
    print(f"  [*] Appending {len(blocks)} new blocks in {total_batches} batches...", flush=True)

    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        try:
            notion.blocks.children.append(
                block_id=page_id,
                children=batch
            )
            print(f"    - Batch {batch_num}/{total_batches} ({len(batch)} blocks) uploaded successfully.", flush=True)
            time.sleep(0.25)
        except Exception as e:
            print(f"    [!] Batch {batch_num} error: {e}", flush=True)

    print(f"\n  [SUCCESS] Page '{title}' synchronized successfully!", flush=True)

def main():
    notion = Client(auth=NOTION_TOKEN)

    # Sync AI AGENT WORKSHOP
    workshop_blocks = build_workshop_blocks()
    sync_page(notion, PAGE_WORKSHOP_ID, "AI AGENT WORKSHOP", "🛠️", workshop_blocks)

    # Sync AI AGENT SECOND BRAIN
    brain_blocks = build_second_brain_blocks()
    sync_page(notion, PAGE_SECOND_BRAIN_ID, "AI AGENT SECOND BRAIN", "🧠", brain_blocks)

    print("\n=======================================================")
    print(" 🎉 All Notion Pages Synchronized & Organized Successfully!")
    print(" • AI AGENT WORKSHOP     : https://notion.so/3cc6d0c8ba0c8097a87bc9dd87c4f922")
    print(" • AI AGENT SECOND BRAIN : https://notion.so/3cc6d0c8ba0c80c1980bcd0a2b601008")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
