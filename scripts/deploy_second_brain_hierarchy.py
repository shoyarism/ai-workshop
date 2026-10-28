#!/usr/bin/env python3
"""
[DEPRECATED - Use scripts/obsidian_vault.py instead]
Deploy Comprehensive AI Agent Second Brain Hierarchy (Legacy Notion)
=====================================================================
NOTE: Superseded by local-first Obsidian Vault located at `vault/` per ADR-005.
All 6 sub-spaces are fully migrated and live locally in `vault/`.
"""

import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Any
from notion_client import Client

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
PARENT_PAGE_ID = "3cc6d0c8-ba0c-80c1-980b-cd0a2b601008"

notion = Client(auth=NOTION_TOKEN)

# ==============================================================================
# BLOCK BUILDERS
# ==============================================================================

def h1(text: str) -> Dict[str, Any]:
    return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h2(text: str) -> Dict[str, Any]:
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h3(text: str) -> Dict[str, Any]:
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def p(text: str, bold_prefix: str = "") -> Dict[str, Any]:
    rich_text = []
    if bold_prefix:
        rich_text.append({"type": "text", "text": {"content": bold_prefix}, "annotations": {"bold": True}})
    rich_text.append({"type": "text", "text": {"content": text}})
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich_text}}

def bullet(text: str, bold_prefix: str = "") -> Dict[str, Any]:
    rich_text = []
    if bold_prefix:
        rich_text.append({"type": "text", "text": {"content": bold_prefix}, "annotations": {"bold": True}})
    rich_text.append({"type": "text", "text": {"content": text}})
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": rich_text}}

def code_block(code_str: str, language: str = "bash") -> Dict[str, Any]:
    lang_clean = "plain text" if language in ["plaintext", "text"] else language
    return {"object": "block", "type": "code", "code": {"rich_text": [{"type": "text", "text": {"content": code_str}}], "language": lang_clean}}

def callout(text: str, emoji: str = "💡", bold_title: str = "") -> Dict[str, Any]:
    rich_text = []
    if bold_title:
        rich_text.append({"type": "text", "text": {"content": bold_title + "\n"}, "annotations": {"bold": True}})
    rich_text.append({"type": "text", "text": {"content": text}})
    return {"object": "block", "type": "callout", "callout": {"rich_text": rich_text, "icon": {"type": "emoji", "emoji": emoji}}}

def divider() -> Dict[str, Any]:
    return {"object": "block", "type": "divider", "divider": {}}

# ==============================================================================
# SUB-PAGE DEFINITIONS
# ==============================================================================

def build_post_mortem_page() -> List[Dict[str, Any]]:
    blocks = [
        callout(
            "Episodic memory of verified solutions to edge-case bugs, environmental quirks, and integration errors.\n"
            "AI agents MUST check this knowledge base before debugging complex issues.",
            emoji="🛠️",
            bold_title="ERROR POST-MORTEM & DETERMINISTIC FIXES"
        ),
        divider(),
        h2("1. Subprocess UTF-8 Pipe Decoding on Windows"),
        p("Windows default subprocess pipe decoding throws `UnicodeDecodeError: 'charmap' codec can't decode byte 0x90` on emojis or special characters when using `text=True`."),
        code_block(
            "# ALWAYS pass encoding='utf-8', errors='replace' to subprocess.run:\n"
            "res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')\n\n"
            "# Configure standard output at top of CLI scripts:\n"
            "if hasattr(sys.stdout, 'reconfigure'):\n"
            "    sys.stdout.reconfigure(encoding='utf-8', errors='replace')\n"
            "    sys.stderr.reconfigure(encoding='utf-8', errors='replace')",
            language="python"
        ),
        divider(),
        h2("2. Multi-Gigabyte Git Repositories Cloning Hangs"),
        p("Massive repositories (e.g. `open-design`, `langflow`) with gigabytes of git history cause multi-minute hangs and timeout failures."),
        code_block(
            "# ALWAYS use blobless shallow clone for massive repositories:\n"
            "git clone --filter=blob:none --depth 1 https://github.com/org/repo.git destination",
            language="bash"
        ),
        divider(),
        h2("3. Notion API Code Block Language Validation"),
        p("Notion API rejects `'plaintext'` or `'text'` with a 400 ValidationError. The exact valid string is `'plain text'` (with space)."),
        code_block(
            "# Map plain text correctly in Notion block payloads:\n"
            "lang = 'plain text' if lang in ['plaintext', 'text'] else lang",
            language="python"
        ),
        divider(),
        h2("4. Zero-Binary High-Speed OCR in Python"),
        p("Traditional Tesseract requires system binary installation in `%PATH%`. `rapidocr_onnxruntime` runs purely inside Python via ONNX with zero external binary dependencies and outputs exact spatial bounding boxes."),
        code_block(
            "from rapidocr_onnxruntime import RapidOCR\n"
            "ocr = RapidOCR()\n"
            "result, elapse = ocr(numpy_image_array)\n"
            "# result -> [[[x1,y1],[x2,y2],[x3,y3],[x4,y4]], text, confidence]",
            language="python"
        ),
        divider(),
        h2("5. PowerShell Nested Quote Stripping"),
        p("Running inline `python -c \"...\"` commands containing nested double quotes or backslashes gets mangled by PowerShell's parser."),
        bullet("Write temporary scripts to `brain/<conversation-id>/scratch/` or use file-based execution instead of fragile inline shell strings.")
    ]
    return blocks

def build_user_dna_page() -> List[Dict[str, Any]]:
    blocks = [
        callout(
            "Persistent profile of user engineering standards, workspace topology, tech stack preferences, and output rules.\n"
            "Eliminates repetitive briefing and ensures zero architectural drift.",
            emoji="👤",
            bold_title="USER DNA & ENVIRONMENT PROFILE"
        ),
        divider(),
        h2("1. Operating Identity & Core Mandate"),
        bullet("Elite Principal Systems Architect & Senior Staff Engineer.", bold_prefix="Role Persona: "),
        bullet("Zero sycophancy, zero pleasantries, immediate technical density.", bold_prefix="Communication Style: "),
        bullet("100% complete, runnable, type-safe code. Never use `// TODO` placeholders.", bold_prefix="Completeness Rule: "),
        bullet("Every deliverable must be verified with automated test runs or live executions.", bold_prefix="Verification: "),
        divider(),
        h2("2. Workspace & Hardware Topology"),
        bullet("os.environ.get('WORKSHOP_ROOT', './') (Relative path notation preferred).", bold_prefix="Primary Workspace: "),
        bullet("Windows 11 x64 with PowerShell and Windows Terminal.", bold_prefix="Host OS & Shell: "),
        bullet("Python 3.11 with `uv` fast package manager.", bold_prefix="Python Environment: "),
        bullet("Node.js v22+, NPM, PNPM, NPX, Bun.", bold_prefix="Node Toolchain: "),
        bullet("FFmpeg and FFprobe (Gyan build on PATH).", bold_prefix="Media & Video Tools: "),
        divider(),
        h2("3. Design & Architecture Standards"),
        bullet("Tailwind CSS v4 design tokens from `ui-ux-arsenal/tokens/design_tokens.json` and `open-design/`.", bold_prefix="Frontend/UI: "),
        bullet("FastAPI, Pydantic v2, async WebSockets, typed models.", bold_prefix="Backend/API: "),
        bullet("RapidOCR (ONNX) + Faster-Whisper (CTranslate2).", bold_prefix="Vision & Audio: "),
        bullet("Model Context Protocol (23 servers registered in `scripts/mcp_launcher.py`).", bold_prefix="Tool Protocol: ")
    ]
    return blocks

def build_adrs_page() -> List[Dict[str, Any]]:
    blocks = [
        callout(
            "Architecture Decision Records (ADRs) documenting critical design choices, rationale, and consequences.",
            emoji="📐",
            bold_title="ARCHITECTURE DECISION RECORDS (ADRs)"
        ),
        divider(),
        h2("ADR-001: Centralized Universal CLI Architecture"),
        bullet("Accepted", bold_prefix="Status: "),
        bullet("Replaced disconnected standalone scripts with a single master CLI (`python scripts/workshop.py [search|info|index|doctor|see|vision|hub|browser|mcp|status]`).", bold_prefix="Decision: "),
        bullet("Unified agent entrypoint, sub-millisecond skill search, and simplified tool discovery.", bold_prefix="Consequence: "),
        divider(),
        h2("ADR-002: Machine-Readable Machine Catalog (CATALOG.json)"),
        bullet("Accepted", bold_prefix="Status: "),
        bullet("Implemented automated AST/filesystem cataloger (`scripts/workshop_indexer.py`) generating `CATALOG.json` and `INDEX.md`.", bold_prefix="Decision: "),
        bullet("AI agents can instantly query structured subsystem metadata via `python scripts/workshop.py info <name>`.", bold_prefix="Consequence: "),
        divider(),
        h2("ADR-003: Zero-Binary ONNX OCR & Media Deconstruction"),
        bullet("Accepted", bold_prefix="Status: "),
        bullet("Integrated `RapidOCR` and `Faster-Whisper` into `scripts/workshop_vision.py` with spatial layout and ANSI/ASCII character art.", bold_prefix="Decision: "),
        bullet("Enables text-only AI models to read screenshots, UI mockups, and videos without multimodal model dependencies.", bold_prefix="Consequence: "),
        divider(),
        h2("ADR-004: Blobless Shallow Git Strategy for Arsenal Ingestion"),
        bullet("Accepted", bold_prefix="Status: "),
        bullet("Adopted `git clone --filter=blob:none --depth 1` for all external tool repositories.", bold_prefix="Decision: "),
        bullet("Saved over 10 GB disk space and accelerated repo clones from 10 minutes to under 5 seconds.", bold_prefix="Consequence: ")
    ]
    return blocks

def build_task_queue_page() -> List[Dict[str, Any]]:
    blocks = [
        callout(
            "Active task queue, asynchronous sprint tracker, and structured agent session handoffs.",
            emoji="⚡",
            bold_title="AUTONOMOUS TASK QUEUE & SESSION HANDOFFS"
        ),
        divider(),
        h2("1. Completed Milestones (Archive)"),
        bullet("Ingested 18 target repositories (OpenHands, Scrapling, Strix, Langflow, Open-Notebook, Graphify, etc.).", bold_prefix="[DONE] Repo Ingestion: "),
        bullet("Created 14 domain skill packages in `skills/` (total 905+ active skills).", bold_prefix="[DONE] Domain Skills: "),
        bullet("Built machine-readable `CATALOG.json` and `INDEX.md` indexer.", bold_prefix="[DONE] Master Catalog: "),
        bullet("Implemented ONNX RapidOCR, Spatial Layout Deconstruction & Faster-Whisper.", bold_prefix="[DONE] Vision Engine: "),
        bullet("Synchronized AI AGENT WORKSHOP and AI AGENT SECOND BRAIN to Notion.", bold_prefix="[DONE] Notion Sync: "),
        divider(),
        h2("2. Session Handoff Protocol Template"),
        p("When ending a long-running session, document the handoff in this format:"),
        code_block(
            "### [Session Handoff - YYYY-MM-DD]\n"
            "- Goal: <High level objective>\n"
            "- Completed: <List of verified deliverables>\n"
            "- State & Context: <Active branches, running background services>\n"
            "- Blockers / Notes: <Known edge cases or open questions>\n"
            "- Next Actions: <Immediate next steps for next agent session>",
            language="markdown"
        )
    ]
    return blocks

def build_service_registry_page() -> List[Dict[str, Any]]:
    blocks = [
        callout(
            "Live registry of local gateways, background daemons, network ports, and MCP server endpoints.",
            emoji="🌐",
            bold_title="LOCAL SERVICE & GATEWAY REGISTRY"
        ),
        divider(),
        h2("1. Local Network Ports & Web Dashboards"),
        bullet("`http://localhost:7860` — Real-time visual canvas and browser agent stream (`python scripts/workshop.py hub`).", bold_prefix="Live Browser Hub (Port 7860): "),
        bullet("`http://localhost:9377` — Headless anti-detect browser server with fingerprint protection (`camofox-browser`).", bold_prefix="Camofox Stealth Browser (Port 9377): "),
        bullet("`http://localhost:20128/v1` — Unified local LLM proxy and model router (`OMNIROUTE_URL`).", bold_prefix="OmniRoute / LiteLLM Proxy (Port 20128): "),
        divider(),
        h2("2. Model Context Protocol (MCP) Servers Matrix"),
        bullet("23 Registered Servers in `scripts/mcp_launcher.py` (Playwright, Puppeteer, Memory, Sequential Thinking, GitHub, Git, SQLite, Postgres, Supabase, Docker, Firebase, Terraform, Brave, Time, Sentry, Linear, Exa, Notion, MCP-Inspector, Stagehand, etc.).", bold_prefix="Total Active MCPs: "),
        divider(),
        h2("3. Standard Environment Variables"),
        bullet("`NOTION_TOKEN` — Notion integration token for sync and database operations.", bold_prefix="Notion: "),
        bullet("`OMNIROUTE_URL` & `OMNIROUTE_API_KEY` — Local LLM gateway configuration.", bold_prefix="OmniRoute: "),
        bullet("`CAMOFOX_BASE_URL` — Stealth browser URL (`http://localhost:9377`).", bold_prefix="Camofox: ")
    ]
    return blocks

def build_sops_page() -> List[Dict[str, Any]]:
    blocks = [
        callout(
            "Standard Operating Procedures (SOPs), algorithm formulas, and meta-prompts for autonomous agents.",
            emoji="📖",
            bold_title="META-PROMPTS & SOP PLAYBOOKS"
        ),
        divider(),
        h2("SOP 1: Universal 5-Stage Problem Solving Protocol"),
        p("Every agent follows this deterministic cycle:"),
        code_block(
            "Stage 1 (Recon): Run 'python scripts/workshop.py search <query>' & inspect target ASTs.\n"
            "Stage 2 (Architecture): Blueprint data models, API schemas, and test plans.\n"
            "Stage 3 (Implementation): Implement complete, type-safe, modular code without placeholders.\n"
            "Stage 4 (Audit): Security review, input sanitization, performance profiling.\n"
            "Stage 5 (Verification): Automated test execution and live validation.",
            language="plain text"
        ),
        divider(),
        h2("SOP 2: UI/UX Craft & Design Token Enforcement"),
        bullet("Never write hardcoded magic numbers for colors, radii, or spacing.", bold_prefix="Rule 1: "),
        bullet("Always import tokens from `ui-ux-arsenal/tokens/design_tokens.json` or `open-design/`.", bold_prefix="Rule 2: "),
        bullet("Ensure minimum 4.5:1 contrast ratios for WCAG AA compliance.", bold_prefix="Rule 3: "),
        bullet("Use spring motion physics (`stiffness: 300, damping: 25`) for interactive elements.", bold_prefix="Rule 4: "),
        divider(),
        h2("SOP 3: Book-to-Skill Distillation Formula"),
        bullet("Ingest raw source text or PDF document.", bold_prefix="Step 1: "),
        bullet("Extract domain taxonomy, mental models, and decision heuristics.", bold_prefix="Step 2: "),
        bullet("Format into standardized `SKILL.md` with YAML frontmatter, actionable CLI recipes, and copy-paste code patterns.", bold_prefix="Step 3: "),
        bullet("Register in `skills/` and refresh index via `python scripts/workshop.py index`.", bold_prefix="Step 4: ")
    ]
    return blocks

# ==============================================================================
# MAIN DEPLOYMENT PIPELINE
# ==============================================================================

def main():
    print("\n=======================================================")
    print(" 🚀 Deploying AI Agent Second Brain Sub-Pages to Notion")
    print(f" Parent Page ID: {PARENT_PAGE_ID}")
    print("=======================================================\n")

    sub_pages = [
        ("🛠️ Error Post-Mortem & Fixes Database", "🛠️", build_post_mortem_page()),
        ("👤 User DNA & Environment Profile", "👤", build_user_dna_page()),
        ("📐 Architecture Decision Records (ADRs)", "📐", build_adrs_page()),
        ("⚡ Autonomous Task Queue & Session Handoffs", "⚡", build_task_queue_page()),
        ("🌐 Local Service & Gateway Registry", "🌐", build_service_registry_page()),
        ("📖 Meta-Prompts & SOP Playbooks", "📖", build_sops_page()),
    ]

    created_pages = []

    for title, icon, blocks in sub_pages:
        print(f"[*] Creating sub-page: '{title}'...")
        try:
            # Create sub-page
            new_page = notion.pages.create(
                parent={"page_id": PARENT_PAGE_ID},
                icon={"type": "emoji", "emoji": icon},
                properties={
                    "title": {"title": [{"text": {"content": title}}]}
                }
            )
            page_id = new_page["id"]
            page_url = new_page.get("url", f"https://notion.so/{page_id.replace('-', '')}")
            created_pages.append((title, icon, page_url, page_id))
            print(f"  [OK] Created page: {page_id}")

            # Append content blocks
            batch_size = 50
            total_batches = (len(blocks) + batch_size - 1) // batch_size
            for i in range(0, len(blocks), batch_size):
                batch = blocks[i:i + batch_size]
                notion.blocks.children.append(
                    block_id=page_id,
                    children=batch
                )
                time.sleep(0.3)
            print(f"  [OK] Uploaded {len(blocks)} blocks successfully.")

        except Exception as e:
            print(f"  [!] Failed to create {title}: {e}")

    print("\n=======================================================")
    print(" 🎉 AI Agent Second Brain Sub-Pages Deployed Successfully!")
    for title, icon, url, pid in created_pages:
        print(f" • {icon} {title:<45} : {url}")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
