#!/usr/bin/env python3
"""
Workshop Central Catalog & Index Generator
=========================================
Builds machine-readable CATALOG.json and INDEX.md for AI agents,
categorizing all repositories, subsystems, MCP servers, and skills.

Usage:
    python scripts/workshop_indexer.py
"""

import sys
import json
import subprocess
from pathlib import Path

# Ensure UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent

SUBSYSTEMS_META = {
    # Autonomous Agents & Platforms
    "openhands": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "OpenHands Software Engineer Platform",
        "description": "Full-stack platform for autonomous AI software development agents that plan, write code, run terminals, execute tests, and iterate autonomously.",
        "entrypoints": [
            "openhands/core/main.py",
            "poetry run python -m openhands.core.main",
        ],
        "capabilities": [
            "Autonomous SWE",
            "Docker sandbox execution",
            "SWE-bench solver",
            "GitHub issue resolution",
        ],
        "tags": ["agents", "coding", "autonomous", "swe", "docker"],
    },
    "browser-use": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "Browser-Use Autonomous Vision Agent",
        "description": "Vision and DOM-based autonomous web navigation framework for AI agents to interact with any website.",
        "entrypoints": ["browser_use/agent/service.py", "scripts/run_browser_agent.py"],
        "capabilities": [
            "Vision browsing",
            "DOM extraction",
            "Form filling",
            "Live stream recording",
        ],
        "tags": ["browser", "agent", "vision", "automation"],
    },
    "openclaw": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "OpenClaw Autonomous Execution Engine",
        "description": "Lightweight, modular autonomous agent framework with structured execution loops, tool chaining, and event streams.",
        "entrypoints": ["index.js", "npm start"],
        "capabilities": ["Agent execution", "Tool routing", "Event streaming"],
        "tags": ["agents", "runtime", "execution"],
    },
    "eliza": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "ElizaOS Autonomous Agent Swarms",
        "description": "Multi-agent conversational and autonomous character framework with persistent memory, Twitter/Discord connectors, and plugin architecture.",
        "entrypoints": ["packages/core/src/index.ts", "pnpm start"],
        "capabilities": [
            "Character agents",
            "Social integrations",
            "Memory embeddings",
            "Multi-agent swarms",
        ],
        "tags": ["eliza", "agents", "characters", "social"],
    },
    "strix": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "Strix AI Security & Pentesting Agent",
        "description": "Autonomous AI penetration testing and vulnerability analysis framework scanning OWASP vulnerabilities with deterministic reports.",
        "entrypoints": ["strix/cli.py", "python -m strix.cli"],
        "capabilities": [
            "Automated pentesting",
            "Vulnerability discovery",
            "CVSS scoring",
            "Mitigation patching",
        ],
        "tags": ["security", "pentest", "vulnerability", "agent"],
    },
    "langflow": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "Langflow Multi-Agent & RAG Orchestrator",
        "description": "Visual and programmatic framework for composing multi-agent architectures, RAG pipelines, and vector tools.",
        "entrypoints": ["src/backend/base/langflow/main.py", "langflow run"],
        "capabilities": [
            "Visual canvas",
            "Multi-agent routing",
            "RAG graph execution",
            "Python code export",
        ],
        "tags": ["langflow", "rag", "agents", "visual-builder"],
    },
    "auto-company": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "Auto-Company Multi-Agent Enterprise Simulator",
        "description": "Simulated autonomous corporate hierarchy with executive, product, design, and engineering agent swarms executing multi-phase missions.",
        "entrypoints": ["main.py", "company.json"],
        "capabilities": [
            "Enterprise hierarchy simulation",
            "Multi-agent departmental collaboration",
            "Mission orchestration",
        ],
        "tags": ["agents", "company", "simulation", "enterprise"],
    },
    "openworker": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "OpenWorker Autonomous Task Execution System",
        "description": "Lightweight and robust autonomous task execution worker for long-running batch workflows and background agent tasks.",
        "entrypoints": ["worker.py", "task_runner.py"],
        "capabilities": [
            "Task queue handling",
            "Background execution",
            "Worker lifecycle",
        ],
        "tags": ["worker", "agents", "automation", "tasks"],
    },
    "google-adk": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "Google Agent Development Kit (ADK)",
        "description": "Open-source agent development framework for building, debugging, and deploying reliable AI agents at enterprise scale. Supports Python, Go, and TypeScript with built-in MCP support and development UI.",
        "entrypoints": [
            "google-adk/python/src/google/adk/agents/__init__.py",
            "agents-cli setup",
        ],
        "capabilities": [
            "Agent development lifecycle",
            "MCP tool integration",
            "Multi-agent orchestration",
            "Development UI",
            "Vertex AI deployment",
        ],
        "tags": ["adk", "agents", "google", "vertex-ai", "mcp"],
        "status": "READY",  # Added by Workshop OS admin
    },
    "skillclaw": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "SkillClaw Collective Skill Evolution Engine",
        "description": "Autonomous collective skill evolution framework for OpenClaw and Hermes Agent ecosystems, synthesizing, evaluating, and evolving reusable agent skills.",
        "entrypoints": [
            "skillclaw/main.py",
            "skillclaw/README.md",
        ],
        "capabilities": [
            "Collective skill evolution",
            "Hermes & OpenClaw skill synthesis",
            "Automated skill refinement",
        ],
        "tags": ["skillclaw", "skills", "evolution", "hermes", "openclaw"],
        "status": "READY",
    },
    "minions": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "Minions Kanban Mission Control for Hermes",
        "description": "Kanban mission control and multi-agent task orchestration dashboard built for Hermes Agent workflows.",
        "entrypoints": [
            "minions/package.json",
            "minions/README.md",
        ],
        "capabilities": [
            "Kanban mission control",
            "Hermes Agent task board",
            "Subagent status tracking",
        ],
        "tags": ["minions", "kanban", "hermes", "mission-control", "dashboard"],
        "status": "READY",
    },
    "mastra": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "Mastra TypeScript AI Framework",
        "description": "TypeScript framework for building AI agents and AI-powered applications with built-in graph-based workflows, memory, RAG, evals, and guardrails. Full production stack in TypeScript.",
        "entrypoints": ["mastra/packages/mastra/src/index.ts", "mastra/scripts/dev.sh"],
        "capabilities": [
            "TypeScript-first agents",
            "Graph-based workflows",
            "Memory and RAG",
            "Evaluations and guardrails",
            "Observability built-in",
        ],
        "tags": ["mastra", "agents", "typescript", "workflows", "rag"],
    },
    "openai-agents-sdk": {
        "category": "autonomous_agents",
        "category_label": "Autonomous Agents & Platforms",
        "name": "OpenAI Agents SDK",
        "description": "Lightweight, production-ready framework for building agentic AI apps with multi-agent orchestration, automatic context compaction, programmatic tool calling, and MCP server support.",
        "entrypoints": [
            "openai-agents-sdk/src/agents/__init__.py",
            "openai-agents-sdk/examples/",
        ],
        "capabilities": [
            "Multi-agent orchestration",
            "MCP server support",
            "Automatic context compaction",
            "Programmatic tool calling",
            "Production-ready",
        ],
        "tags": ["openai", "agents", "sdk", "mcp", "multi-agent"],
    },
    # Web Scraping & Browser Automation
    "Scrapling": {
        "category": "scraping_browser",
        "category_label": "Web Scraping & Browser Automation",
        "name": "Scrapling Undetectable Web Scraper",
        "description": "Ultra-fast, undetectable Python web scraping framework with stealth fingerprinting, adaptive CSS/XPath parsing, and markdown extraction.",
        "entrypoints": ["scrapling/core/fetcher.py", "scrapling install"],
        "capabilities": [
            "Anti-bot bypass",
            "Adaptive parsing",
            "Stealth TLS fingerprinting",
            "Markdown generation",
        ],
        "tags": ["scraping", "stealth", "parser", "crawler"],
    },
    "camofox-browser": {
        "category": "scraping_browser",
        "category_label": "Web Scraping & Browser Automation",
        "name": "Camofox Stealth Anti-Detect Browser",
        "description": "Stealth anti-detect headless browser with fingerprint masking and native MCP server integration on Port 9377.",
        "entrypoints": ["server.js", "node server.js"],
        "capabilities": [
            "Anti-detect masking",
            "Port 9377 API",
            "MCP server",
            "Fingerprint spoofing",
        ],
        "tags": ["browser", "anti-detect", "mcp", "stealth"],
    },
    "stagehand": {
        "category": "scraping_browser",
        "category_label": "Web Scraping & Browser Automation",
        "name": "Stagehand Playwright AI Web Automator",
        "description": "AI web automation engine built on Playwright with natural language actions (act, extract, observe) without fragile selectors.",
        "entrypoints": ["lib/index.ts", "npx stagehand"],
        "capabilities": [
            "Natural language actions",
            "Structured extraction",
            "Playwright integration",
            "Self-healing DOM",
        ],
        "tags": ["browser", "playwright", "stagehand", "automation"],
    },
    "open-seo": {
        "category": "scraping_browser",
        "category_label": "Web Scraping & Browser Automation",
        "name": "OpenSEO Technical SEO Audit Engine",
        "description": "Open-source technical SEO auditing, sitemap crawling, Core Web Vitals, and search performance scorecards.",
        "entrypoints": ["src/index.ts", "pnpm build"],
        "capabilities": [
            "Technical SEO audit",
            "Sitemap crawl",
            "Canonical verification",
            "Structured data check",
        ],
        "tags": ["seo", "audit", "web", "crawler"],
    },
    # AI Knowledge & Application Accelerators
    "open-notebook": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "Open Notebook Multi-Model Research Engine",
        "description": "Open-source multi-model AI notebook and research companion with grounded citations, note synthesis, and audio overview podcasts.",
        "entrypoints": ["backend/main.py", "npm run dev"],
        "capabilities": [
            "Document grounding",
            "Multi-model support",
            "Audio overview podcasts",
            "Exact citations",
        ],
        "tags": ["notebook", "research", "rag", "grounding"],
    },
    "awesome-llm-apps": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "Awesome LLM Apps Architecture Catalog",
        "description": "Curated collection of 100+ production-grade LLM applications (Advanced RAG, Agentic Swarms, Voice/Vision Multimodal, Financial AI).",
        "entrypoints": ["README.md"],
        "capabilities": [
            "100+ App Blueprints",
            "Agentic RAG templates",
            "Voice agent architectures",
            "Pydantic schema tools",
        ],
        "tags": ["llm-apps", "blueprints", "rag", "swarms"],
    },
    "book-to-skill": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "Book-to-Skill Knowledge Distiller",
        "description": "Compiler that distills entire technical books, whitepapers, and comprehensive PDFs into production-ready SKILL.md packages for AI agents.",
        "entrypoints": ["main.py", "python main.py"],
        "capabilities": [
            "Book distillation",
            "Rule extraction",
            "Skill generator",
            "Pattern recognition",
        ],
        "tags": ["skills", "distillation", "books", "knowledge"],
    },
    "graphify": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "Graphify Codebase AST Knowledge Graph",
        "description": "Codebase knowledge graph generator mapping AST structures, call flows, function dependencies, and architecture hierarchies.",
        "entrypoints": [
            "graphify extract",
            "graphify explain",
            "graphify path",
            "graphify antigravity install",
        ],
        "capabilities": [
            "AST dependency mapping",
            "Multi-language tree-sitter support",
            "Call graph analysis",
            "Interactive HTML export",
            "Obsidian vault export",
        ],
        "tags": ["graph", "ast", "codebase", "architecture", "knowledge-graph"],
    },
    "agent-skills": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "Addy Osmani Production Agent Skills Platform",
        "description": "Production-grade engineering skills for AI coding agents across the full lifecycle: spec, plan, build, test, review, and ship.",
        "entrypoints": ["skills/", "commands/", "AGENTS.md"],
        "capabilities": [
            "25 production skills",
            "Red-green-refactor TDD",
            "Atomic task planning",
            "Code review & simplification",
            "Chrome DevTools testing",
        ],
        "tags": [
            "skills",
            "agents",
            "engineering",
            "quality",
            "tdd",
            "planning",
            "review",
        ],
    },
    "ponytail": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "Ponytail Lazy Senior Developer & YAGNI Engine",
        "description": "Disciplined minimalism engine for AI agents cutting 54% unnecessary code through the YAGNI -> reuse -> stdlib -> native platform ladder.",
        "entrypoints": ["skills/ponytail", "ponytail-mcp/index.js", "npm test"],
        "capabilities": [
            "7-rung minimalism ladder",
            "YAGNI code reduction",
            "Ponytail audit & debt detector",
            "Ponytail MCP server",
        ],
        "tags": ["ponytail", "minimalism", "yagni", "clean-code", "refactoring"],
    },
    "litellm": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "LiteLLM Universal Model Proxy & Gateway",
        "description": "Unified gateway routing 100+ LLMs (OpenAI, Anthropic, Gemini, DeepSeek, Local Ollama) using the standard OpenAI format.",
        "entrypoints": ["litellm/proxy/proxy_server.py", "litellm --port 4000"],
        "capabilities": [
            "100+ model proxy",
            "Load balancing",
            "Fallback routing",
            "OpenAI API compatibility",
        ],
        "tags": ["litellm", "proxy", "gateway", "llm-router"],
    },
    "open-generative-ai": {
        "category": "ai_knowledge_apps",
        "category_label": "AI Knowledge & Application Accelerators",
        "name": "Open Generative AI Starters",
        "description": "Collection of open-source generative AI components, prompts, and developer scaffolding.",
        "entrypoints": ["README.md"],
        "capabilities": ["Generative AI components", "Scaffolding templates"],
        "tags": ["generative-ai", "starters", "templates"],
    },
    # Design, UI/UX & Media
    "open-design": {
        "category": "design_multimedia",
        "category_label": "Design, UI/UX & Media Engines",
        "name": "OpenDesign System & Token Architecture",
        "description": "Open-source design system, design token engine, UI component specifications, and Figma-to-code workflows.",
        "entrypoints": ["package.json", "pnpm dev"],
        "capabilities": [
            "Design tokens",
            "Tailwind integration",
            "Component specs",
            "Figma workflows",
        ],
        "tags": ["design", "ui-ux", "tokens", "components"],
    },
    "ui-ux-arsenal": {
        "category": "design_multimedia",
        "category_label": "Design, UI/UX & Media Engines",
        "name": "UI/UX Master Arsenal & Design Tokens",
        "description": "Workshop master design system blueprint, Tailwind v4 design tokens, and aesthetic UI archetypes.",
        "entrypoints": ["DESIGN_SYSTEM_MASTER.md", "tokens/design_tokens.json"],
        "capabilities": [
            "Tailwind v4 tokens",
            "Clean SaaS blueprint",
            "Glassmorphism archetype",
            "Industrial brutalism",
        ],
        "tags": ["design-system", "tailwind", "tokens", "archetypes"],
    },
    "hyperframes": {
        "category": "design_multimedia",
        "category_label": "Design, UI/UX & Media Engines",
        "name": "Hyperframes Programmatic Motion Studio",
        "description": "High-fidelity programmatic animation and video generation framework with 20 motion skills.",
        "entrypoints": ["packages/core/src/index.ts", "skills/"],
        "capabilities": [
            "Programmatic animation",
            "Video rendering",
            "Motion design skills",
            "Keyframe timing",
        ],
        "tags": ["motion", "animation", "video", "hyperframes"],
    },
    "photoreal-studio": {
        "category": "design_multimedia",
        "category_label": "Design, UI/UX & Media Engines",
        "name": "Ultra-Realistic FLUX Photoreal Studio",
        "description": "First-principles photographic optical physics engine and high-resolution FLUX.1 synthesis studio with natural language director and Leica UI.",
        "entrypoints": [
            "photoreal-studio/run_studio.py",
            "python scripts/workshop.py photoreal studio",
            "python scripts/workshop.py photoreal generate",
        ],
        "capabilities": [
            "BSSRDF skin physics",
            "Lens & sensor optics",
            "Natural language director",
            "FLUX.1-realism synthesis",
            "300% detail loupe UI",
        ],
        "tags": [
            "photorealism",
            "flux",
            "image-generation",
            "optics",
            "photography",
            "ai-art",
        ],
    },
    "anti-slop": {
        "category": "design_multimedia",
        "category_label": "Design, UI/UX & Media Engines",
        "name": "Anti-Slop AI Filter & Quality Gate",
        "description": "Rules and liveliness engine for AI coding agents to filter out generic AI-generated UI designs, copy, and code comments with 38 rules, Purpose-Gates, and Delivery Gate verification.",
        "entrypoints": [
            "anti-slop/antislop.md",
            "python scripts/workshop.py antislop rules",
            "python scripts/workshop.py antislop gate",
        ],
        "capabilities": [
            "38 Anti-slop rules (R-01..R-38)",
            "Purpose-Gate & Liveliness dials",
            "4-Block Delivery Gate",
            "WCAG contrast checker",
            "Anti-AI copywriting audit",
            "Clean code comment filtering",
        ],
        "tags": [
            "anti-slop",
            "design-filter",
            "ui-ux",
            "copywriting",
            "accessibility",
            "liveliness",
            "clean-code",
        ],
    },
    # MCP Servers & Protocols
    "mcp-servers-official": {
        "category": "mcp_servers_protocols",
        "category_label": "Model Context Protocol (MCP) Toolsets",
        "name": "Official Reference MCP Servers",
        "description": "Reference Model Context Protocol implementations for Git, Memory, SQLite, PostgreSQL, Filesystem, Fetch, Docker, and Puppeteer.",
        "entrypoints": ["src/index.ts"],
        "capabilities": [
            "Official MCP tools",
            "Database inspection",
            "Memory graph",
            "DevTools inspection",
        ],
        "tags": ["mcp", "official", "tools", "protocol"],
    },
    "awesome-mcp-servers": {
        "category": "mcp_servers_protocols",
        "category_label": "Model Context Protocol (MCP) Toolsets",
        "name": "Awesome MCP Servers Directory",
        "description": "Curated index of hundreds of community and enterprise Model Context Protocol servers across domains.",
        "entrypoints": ["README.md"],
        "capabilities": [
            "Ecosystem MCP directory",
            "Searchable servers",
            "Setup recipes",
        ],
        "tags": ["mcp", "directory", "tools", "catalog"],
    },
    "mcp-inspector": {
        "category": "mcp_servers_protocols",
        "category_label": "Model Context Protocol (MCP) Toolsets",
        "name": "Official MCP Inspector & Debugger",
        "description": "Interactive developer test harness and web UI for testing and debugging Model Context Protocol servers.",
        "entrypoints": ["package.json", "npx @modelcontextprotocol/inspector"],
        "capabilities": [
            "Interactive UI",
            "JSON-RPC traffic analysis",
            "Tool testing",
            "Prompt inspection",
        ],
        "tags": ["mcp", "inspector", "debugging", "developer-tools"],
    },
    # Curated Knowledge & Developer Resources
    "public-apis": {
        "category": "curated_resources",
        "category_label": "Curated Knowledge & Developer Resources",
        "name": "Public APIs Collective Index",
        "description": "Comprehensive index of 1,500+ free and public REST APIs across 50+ categories with auth and CORS specs.",
        "entrypoints": ["README.md"],
        "capabilities": [
            "1,500+ REST APIs",
            "50+ categories",
            "Auth/HTTPS/CORS filtering",
        ],
        "tags": ["apis", "rest", "free-apis", "directory"],
    },
    "free-for-dev": {
        "category": "curated_resources",
        "category_label": "Curated Knowledge & Developer Resources",
        "name": "Free for Developers Cloud Tiers",
        "description": "Massive curated directory of free cloud tiers, databases, compute, authentication, and SaaS developer services.",
        "entrypoints": ["README.md"],
        "capabilities": [
            "Free cloud tiers",
            "Database hosting",
            "Auth providers",
            "CI/CD & Monitoring",
        ],
        "tags": ["cloud", "free-tier", "hosting", "infrastructure"],
    },
    "awesome-selfhosted": {
        "category": "curated_resources",
        "category_label": "Curated Knowledge & Developer Resources",
        "name": "Awesome Self-Hosted Infrastructure",
        "description": "Curated directory of open-source network services, self-hosted applications, and infrastructure software.",
        "entrypoints": ["README.md"],
        "capabilities": [
            "Self-hosted infrastructure",
            "Docker compose stacks",
            "Privacy-first services",
        ],
        "tags": ["self-hosted", "infrastructure", "open-source", "docker"],
    },
    "awesome": {
        "category": "curated_resources",
        "category_label": "Curated Knowledge & Developer Resources",
        "name": "Sindresorhus Master Awesome Index",
        "description": "The definitive index of curated awesome lists across programming languages, AI, security, and computing.",
        "entrypoints": ["readme.md"],
        "capabilities": [
            "Master topic index",
            "Software engineering lists",
            "Ecosystem navigation",
        ],
        "tags": ["awesome", "index", "curated", "topics"],
    },
    "i-have-adhd": {
        "category": "curated_resources",
        "category_label": "Curated Knowledge & Developer Resources",
        "name": "ADHD Executive Function & Focus Toolbox",
        "description": "Actionable neurodivergent workflows, low-friction task chunking, and cognitive load reduction tools.",
        "entrypoints": ["README.md"],
        "capabilities": [
            "Executive function strategies",
            "Task chunking",
            "Focus workflows",
            "Tool recommendations",
        ],
        "tags": ["adhd", "focus", "productivity", "workflows"],
    },
    "botdirectory-ai": {
        "category": "curated_resources",
        "category_label": "Curated Knowledge & Developer Resources",
        "name": "BotDirectory.ai Global Agent Index",
        "description": "Comprehensive directory and taxonomy of AI bots, autonomous agents, and integrations across business, developer, and research domains.",
        "entrypoints": ["README.md"],
        "capabilities": [
            "Agent ecosystem directory",
            "Category taxonomy",
            "Bot discovery",
        ],
        "tags": ["bots", "agents", "directory", "catalog"],
    },
    # Research & Intelligence
    "agent-reach": {
        "category": "research_intelligence",
        "category_label": "Research & Multi-Platform Intelligence",
        "name": "Agent Reach Internet & Social Intelligence Engine",
        "description": "Universal multi-platform intelligence gathering agent supporting Web, YouTube, GitHub, Twitter/X, Bilibili, Reddit, Facebook, Instagram, Xiaohongshu, LinkedIn, Boss直聘, V2EX, Xueqiu, Podcasts, and Exa.",
        "entrypoints": ["agent-reach/cli.py", "agent-reach doctor --json"],
        "capabilities": [
            "14+ platform scraping",
            "Exa search integration",
            "Transcript extraction",
            "Social OSINT",
        ],
        "tags": ["agent-reach", "osint", "research", "scraping", "social-intelligence"],
    },
    # Digital Forensics & Security
    "iLEAPP": {
        "category": "forensics_security",
        "category_label": "Digital Forensics & Security Analysis",
        "name": "iLEAPP iOS Forensic Artifacts Extractor",
        "description": "Comprehensive iOS triage and forensic artifact analysis tool parsing system databases, knowledgeC, mobile assets, location telemetry, and application caches.",
        "entrypoints": ["ileapp.py", "python ileapp.py"],
        "capabilities": [
            "iOS triage",
            "KnowledgeC parsing",
            "Location forensics",
            "App cache extraction",
        ],
        "tags": ["forensics", "ios", "ileapp", "triage", "security"],
    },
    # Central Workshop Engine
    "skills": {
        "category": "workshop_core",
        "category_label": "Central Workshop Engine",
        "name": "Workshop Domain Skills Library",
        "description": "865+ curated domain skills with SKILL.md specs across engineering, security, cloud, frontend, and research.",
        "entrypoints": ["skills/"],
        "capabilities": [
            "865+ agent skills",
            "Instant activation",
            "Type-safe instructions",
            "CLI recipes",
        ],
        "tags": ["skills", "arsenal", "instructions", "core"],
    },
    "scripts": {
        "category": "workshop_core",
        "category_label": "Central Workshop Engine",
        "name": "Master Workshop CLI & Automation Suite",
        "description": "Master CLI (workshop.py), search engine (workshop_search.py), vision engine (workshop_vision.py), live browser hub, and doctor.",
        "entrypoints": [
            "scripts/workshop.py",
            "scripts/workshop_search.py",
            "scripts/workshop_vision.py",
            "scripts/workshop_doctor.py",
        ],
        "capabilities": [
            "Universal CLI",
            "Sub-second search",
            "Multimodal vision engine",
            "Live browser stream (:7860)",
        ],
        "tags": ["cli", "scripts", "doctor", "vision", "search"],
    },
    "prompts": {
        "category": "workshop_core",
        "category_label": "Central Workshop Engine",
        "name": "System Prompts & Personas",
        "description": "Production system prompts, agent personas, and task templates for deterministic AI execution.",
        "entrypoints": ["prompts/"],
        "capabilities": [
            "Agent prompts",
            "Architecture templates",
            "Persona definitions",
        ],
        "tags": ["prompts", "personas", "templates"],
    },
}


def generate_catalog():
    catalog = {
        "workspace": "Workshop",
        "version": "3.0.0",
        "description": "Centralized Universal AI Operating System & Engineering Arsenal",
        "master_cli": "python scripts/workshop.py",
        "total_subsystems": len(SUBSYSTEMS_META),
        "subsystems": {},
    }

    for folder_name, meta in SUBSYSTEMS_META.items():
        p = WORKSHOP_DIR / folder_name
        is_ready = p.exists() and (len(list(p.iterdir())) > 1 if p.is_dir() else True)

        git_remote = None
        git_dir = p / ".git"
        if git_dir.exists():
            try:
                git_remote = subprocess.check_output(
                    ["git", "config", "--get", "remote.origin.url"],
                    cwd=str(p),
                    text=True,
                    timeout=2,
                ).strip()
            except Exception:  # @court-exempt: handled fallback
                pass

        catalog["subsystems"][folder_name] = {
            **meta,
            "path": folder_name,
            "status": "READY" if is_ready else "PENDING",
            "git_remote": git_remote,
        }

    catalog_path = WORKSHOP_DIR / "CATALOG.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(
        f"[*] Generated machine-readable catalog: {catalog_path} ({len(catalog['subsystems'])} subsystems)"
    )
    return catalog


def generate_index_markdown(catalog):
    categories = {}
    for k, v in catalog["subsystems"].items():
        cat = v.get("category", "other")
        label = v.get("category_label", cat.replace("_", " ").title())
        if cat not in categories:
            categories[cat] = {"label": label, "items": []}
        categories[cat]["items"].append((k, v))

    lines = [
        "# Workshop Master Index & AI Agent Navigation Catalog",
        "",
        "> **Universal Master CLI**: `python scripts/workshop.py`  ",
        '> **Arsenal Search**: `python scripts/workshop.py search "<keyword>"`  ',
        "> **Health Doctor**: `python scripts/workshop.py doctor`  ",
        "> **Machine Catalog**: [`CATALOG.json`](CATALOG.json)",
        "",
        "---",
        "",
        "## Centralized Subsystem Taxonomy",
        "",
    ]

    for cat_id, cat_data in categories.items():
        lines.append(f"### {cat_data['label']}")
        lines.append("")
        lines.append("| Subsystem | Folder | Status | Capabilities & Purpose |")
        lines.append("| :--- | :--- | :---: | :--- |")
        for key, item in cat_data["items"]:
            status_badge = "`READY`" if item["status"] == "READY" else "`PENDING`"
            desc = item["description"]
            lines.append(
                f"| **{item['name']}** | [`{key}/`]({key}/) | {status_badge} | {desc} |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## Master CLI Quick Execution Reference",
            "",
            "```bash",
            "# 🔍 1. High-Speed Search Across 2,150+ Skills, MCPs, APIs & Subsystems",
            'python scripts/workshop.py search "<query>" [--category skills|mcps|apis|repos]',
            'python scripts/workshop.py search "pentest"',
            'python scripts/workshop.py search "scrapling"',
            'python scripts/workshop.py search "graph"',
            "",
            "# 📋 2. Subsystem Briefing & Metadata",
            "python scripts/workshop.py info <subsystem_name>   # e.g. python scripts/workshop.py info scrapling",
            "",
            "# 🩺 3. Environment Health & Diagnostics",
            "python scripts/workshop.py doctor",
            "",
            "# 👁️ 4. Multimodal Media & Vision Inspector",
            'python scripts/workshop.py see "<file_or_dir>" [--prompt "<question>"]',
            'python scripts/workshop.py vision inspect "<image_path>"',
            'python scripts/workshop.py vision storyboard "<video_path>"',
            "",
            "# 🌐 5. Live Streaming Browser Dashboard (Port 7860)",
            "python scripts/workshop.py hub --port 7860",
            "",
            "# 🛠️ 6. MCP Server Testing & Execution",
            "python scripts/workshop.py mcp list",
            "python scripts/workshop.py mcp test playwright",
            "python scripts/workshop.py mcp start camofox-browser",
            "",
            "# 🔄 7. Regenerate Catalog & Index",
            "python scripts/workshop.py index",
            "```",
            "",
            "---",
            "",
            "## Guidelines for AI Agents",
            '1. **Reconnaissance First**: Query `python scripts/workshop.py search "<task_topic>"` to discover matching domain skills and tools before writing code.',
            "2. **Deterministic Verification**: Every tool addition or modification must be validated via `python scripts/workshop.py doctor` or automated tests.",
            "3. **Modular Subsystem Usage**: Consult the dedicated skills in `skills/` for copy-pasteable execution patterns.",
            "",
        ]
    )

    index_path = WORKSHOP_DIR / "INDEX.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[*] Generated master index: {index_path}")


def main():
    cat = generate_catalog()
    generate_index_markdown(cat)


if __name__ == "__main__":
    main()
