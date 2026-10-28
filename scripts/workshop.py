#!/usr/bin/env python3
"""
Centralized Workshop Master CLI
==============================
The single, universal entrypoint for all AI agents, tools, and human developers.
Provides search, health diagnostics, live browser automation, MCP management, vision inspection, catalog indexing, and briefings.

Usage:
    python scripts/workshop.py search "<query>"
    python scripts/workshop.py info <subsystem_name>
    python scripts/workshop.py index
    python scripts/workshop.py doctor
    python scripts/workshop.py see "<file_or_dir>" [--prompt "<question>"]
    python scripts/workshop.py vision [inspect|frames|storyboard|ocr|transcribe] ...
    python scripts/workshop.py browser --url "<url>" [--task "<task>"] [--live]
    python scripts/workshop.py hf [trending|search|inspect|papers] ...
    python scripts/workshop.py openrouter [free|search|inspect|cheapest] ...
    python scripts/workshop.py github [trending|search|inspect] ...
    python scripts/workshop.py drift [--fetch] [--sync]
    python scripts/workshop.py hub [--port 7860]
    python scripts/workshop.py mcp [list|test|start] [<server>]
    python scripts/workshop.py status
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent

_VENV_PY = WORKSHOP_DIR / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
if _VENV_PY.exists() and Path(sys.executable).resolve() != _VENV_PY.resolve() and not os.environ.get("_WORKSHOP_VENV_REEXEC"):
    os.environ["_WORKSHOP_VENV_REEXEC"] = "1"
    sys.exit(subprocess.call([str(_VENV_PY), *sys.argv]))

# Load local environment variables (.env) if present
try:
    from dotenv import load_dotenv
    load_dotenv(WORKSHOP_DIR / ".env")
except Exception:  # @court-exempt: optional dotenv fallback
    pass

def cmd_see(args):
    """Execute smart multimodal vision inspector."""
    from workshop_vision import see_media
    res = see_media(args.path, prompt=args.prompt if args.prompt else None, make_storyboard=not args.no_storyboard)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=======================================================")
        print(f" 👁️ WORKSHOP VISION INSPECTOR: {Path(args.path).name}")
        print("=======================================================\n")
        if "ansi_preview" in res:
            print(res["ansi_preview"])
            print()
        if "storyboard_preview" in res:
            print("🎬 Storyboard Grid Preview:")
            print(res["storyboard_preview"])
            print(f"\nStoryboard image saved: {res.get('storyboard_image')}\n")
        for k, v in res.items():
            if k not in ("ansi_preview", "storyboard_preview"):
                print(f" • {k:<20}: {v}")
        print("\n=======================================================\n")

def cmd_vision(args):
    """Execute vision subcommands."""
    import workshop_vision
    sys.argv = ["workshop_vision.py"] + sys.argv[2:]
    workshop_vision.main()

def cmd_search(args):
    """Execute centralized arsenal search."""
    from workshop_search import main as search_main
    sys.argv = ["workshop_search.py", args.query]
    if args.category:
        sys.argv.extend(["--category", args.category])
    if args.limit:
        sys.argv.extend(["--limit", str(args.limit)])
    if args.json:
        sys.argv.append("--json")
    search_main()

def cmd_info(args):
    """Output machine/agent readable briefing on a subsystem."""
    catalog_path = WORKSHOP_DIR / "CATALOG.json"
    if not catalog_path.exists():
        from workshop_indexer import main as index_main
        index_main()
    
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    subsystems = data.get("subsystems", {})
    query = args.name.lower().strip()
    
    # Exact match or substring
    matched_key = None
    if query in subsystems:
        matched_key = query
    else:
        for k in subsystems:
            if query in k.lower() or query in subsystems[k].get("name", "").lower():
                matched_key = k
                break
                
    if not matched_key:
        print(f"[!] Subsystem '{args.name}' not found. Try searching with: python scripts/workshop.py search '{args.name}'")
        return
        
    info = subsystems[matched_key]
    if args.json:
        print(json.dumps(info, indent=2))
        return
        
    print("\n=======================================================")
    print(f" 📦 WORKSHOP SUBSYSTEM BRIEFING: {info.get('name', matched_key)}")
    print("=======================================================\n")
    print(f" • Identifier    : {matched_key}")
    print(f" • Category      : {info.get('category_label', 'N/A')}")
    print(f" • Path          : {info.get('path', 'N/A')}")
    print(f" • Status        : {info.get('status', 'UNKNOWN')}")
    print(f" • Remote Git    : {info.get('git_remote', 'Local Subsystem')}")
    print(f" • Description   : {info.get('description', '')}")
    print("\n 🚀 Entrypoints & Commands:")
    for ep in info.get("entrypoints", []):
        print(f"   - {ep}")
    print("\n ⚡ Core Capabilities:")
    for cap in info.get("capabilities", []):
        print(f"   • {cap}")
    print("\n 🏷️ Tags: " + ", ".join(info.get("tags", [])))
    print("\n=======================================================\n")


def cmd_house(args):
    """List or inspect Workshop Sovereign Houses."""
    skills_dir = WORKSHOP_DIR / "skills"
    houses = [
        ("🎨 The Design House", "design-house", "Visual Systems, Typography, Layout, Vector Craft, Color Theory, Decks, Diagrams"),
        ("⚡ The Dev & Engineering House", "dev-house", "Senior Dev Invariants, Strict Typing, Runtimes, AST, Frameworks, TDD"),
        ("🔬 The Research & Intelligence House", "intel-house", "Codebase Knowledge Graphs, Web Scraping, Reverse Engineering, OSINT"),
        ("🏎️ The Operations & Token Diet House", "ops-house", "Token Efficiency, Spec-Driven Development, Context Management, GSD/BMAD"),
        ("🎬 The Media & Video House", "media-house", "Programmatic Video Code, Autonomous Video Studio, Voice/Audio, Optics Synthesis"),
        ("📢 The Marketing & Growth House", "growth-house", "Authentic Human Voice, Conversion Copywriting, Brand, SEO, Social Distribution"),
        ("🛡️ The Forensics & Security House", "security-house", "Adversarial Quality Gates (Slop Court), Pentesting, Digital Forensics"),
        ("🌐 Cloud & Platform APIs", "cloud-and-apis", "Cloud Infrastructure (AWS, Azure, GCP) & Platform Connectors")
    ]
    
    if args.action == "list" and not args.target:
        print("\n=======================================================")
        print(" 🏛️  WORKSHOP SOVEREIGN HOUSES (DOMAIN GUILDS)")
        print("=======================================================\n")
        total_skills = 0
        for title, slug, desc in houses:
            p = skills_dir / slug
            cnt = len(list(p.rglob("SKILL.md"))) if p.exists() else 0
            total_skills += cnt
            print(f" {title} (`skills/{slug}/`)")
            print(f"   • Skills  : {cnt} skills")
            print(f"   • Mission : {desc}\n")
        print(f" Total House Skills Indexed: {total_skills}")
        print(" Use: python scripts/workshop.py house inspect <slug> to explore any house.")
        print("=======================================================\n")
        return

    # Inspect target house
    target = (args.target or args.action).lower().strip().replace(" ", "-")
    matched = None
    for title, slug, desc in houses:
        if target in slug or target in title.lower():
            matched = (title, slug, desc)
            break
            
    if not matched:
        print(f"[!] House '{target}' not found. Available houses: " + ", ".join([h[1] for h in houses]))
        return

    title, slug, desc = matched
    p = skills_dir / slug
    skill_files = sorted(list(p.rglob("SKILL.md"))) if p.exists() else []
    subdirs = [f.parent.name for f in skill_files]

    print("\n=======================================================")
    print(f" 🏛️  HOUSE INSPECTION: {title}")
    print("=======================================================\n")
    print(f" • Directory : skills/{slug}/")
    print(f" • Mission   : {desc}")
    print(f" • Count     : {len(subdirs)} skills\n")
    print(" 📦 Registered Skills:")
    for i, s in enumerate(subdirs, 1):
        print(f"   {i:3d}. {s}")
    print("\n=======================================================\n")

def cmd_index(args):
    """Regenerate CATALOG.json and INDEX.md."""
    from workshop_indexer import main as index_main
    index_main()

def cmd_doctor(args):
    """Run health diagnostic check."""
    from workshop_doctor import main as doctor_main
    doctor_main(strict=getattr(args, "strict", False))

def cmd_hub(args):
    """Start live browser hub web dashboard."""
    from live_browser_hub import run_server
    run_server(args.port)

def cmd_browser(args):
    """Run browser agent task with optional live watching, CDP attachment, or profile mounting."""
    url = getattr(args, "url", None)
    cdp = getattr(args, "cdp", None)
    if url or cdp:
        from run_browser_agent import run_agent_session
        run_agent_session(
            url,
            task=getattr(args, "task", ""),
            headed=getattr(args, "headed", False),
            live=getattr(args, "live", False),
            browser_type=getattr(args, "browser", "chromium") or "chromium",
            cdp=cdp,
            profile=getattr(args, "profile", None)
        )
    else:
        sub_argv = sys.argv[2:]
        subprocess.run([sys.executable, str(SCRIPTS_DIR / "run_browser_agent.py")] + sub_argv)

def cmd_mcp(args):
    """Inspect and launch MCP servers."""
    from mcp_launcher import list_servers, test_server
    if args.action == "list":
        list_servers()
    elif args.action == "test":
        test_server(args.name)
    elif args.action == "start":
        from mcp_launcher import MCP_REGISTRY
        if args.name in MCP_REGISTRY:
            cmd = MCP_REGISTRY[args.name]["command"]
            print(f"[*] Starting MCP Server: {args.name}...")
            subprocess.run(cmd, shell=True if os.name == 'nt' else False)
        else:
            print(f"[!] Unknown MCP server: {args.name}")

def cmd_services(args):
    """Manage Workshop persistent services and gateways."""
    import workshop_services
    action = getattr(args, "service_action", "status") or "status"
    targets = getattr(args, "targets", ["all"]) or ["all"]
    if action == "status":
        workshop_services.cmd_status()
    elif action == "start":
        workshop_services.cmd_start(targets)
    elif action == "stop":
        workshop_services.cmd_stop(targets)
    elif action == "restart":
        workshop_services.cmd_restart(targets)

def cmd_up(args):
    """Start all Workshop persistent background services and gateways."""
    import workshop_services
    print("\n=======================================================")
    print(" 🚀 WORKSHOP UP: Bootstrapping Local Services & Gateways")
    print("=======================================================\n")
    workshop_services.cmd_start(["all"])

def cmd_down(args):
    """Stop all Workshop persistent background services and gateways."""
    import workshop_services
    print("\n=======================================================")
    print(" 🛑 WORKSHOP DOWN: Graceful Shutdown of Gateways")
    print("=======================================================\n")
    workshop_services.cmd_stop(["all"])

def cmd_desktop(args):
    """Execute native OS desktop automation commands."""
    import workshop_desktop
    sys.argv = ["workshop_desktop.py"] + sys.argv[2:]
    workshop_desktop.main()

def cmd_forensic(args):
    """Execute Digital Forensics & Data Recovery commands."""
    sub_argv = sys.argv[2:]
    subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_forensics.py")] + sub_argv)

def cmd_osint(args):
    """Execute OSINT & Auspex Intelligence Suite commands."""
    sub_argv = sys.argv[2:]
    subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_osint.py")] + sub_argv)


def cmd_event_bus(args):
    """Execute Agent Nervous System event bus commands."""
    sys.argv = ["workshop_event_bus.py"] + sys.argv[2:]
    # Execute script directly
    subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_event_bus.py")] + sys.argv[1:])

def cmd_guard(args):
    """Execute Adversarial Verification Guard."""
    import workshop_adversarial_guard
    sys.exit(workshop_adversarial_guard.audit_codebase())

def cmd_forge(args):
    """Execute Dynamic Tool Forge."""
    # Remove the 'forge' command from sys.argv before passing to sub-script
    sub_argv = ["workshop_tool_forge.py"] + sys.argv[2:]
    sys.argv = sub_argv
    subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_tool_forge.py")] + sub_argv[1:])

def cmd_route(args):
    """Execute Local Inference Router."""
    sys.argv = ["workshop_local_router.py"] + sys.argv[2:]
    subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_local_router.py")] + sys.argv[1:])

def cmd_evolve(args):
    """Execute Self-Evolution Engine."""
    sys.argv = ["workshop_evolution.py"] + sys.argv[2:]
    subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_evolution.py")] + sys.argv[1:])

def cmd_semantic(args):
    """Execute Semantic Skill Indexer and Search."""
    # Pass the semantic subcommand args to the sub-script
    sub_argv = ["workshop_semantic_indexer.py"]
    if hasattr(args, 'action') and args.action:
        sub_argv.append(args.action)
    if hasattr(args, 'query') and args.query:
        sub_argv.extend(["--query", args.query])
    if hasattr(args, 'limit') and args.limit:
        sub_argv.extend(["--limit", str(args.limit)])
    sys.argv = sub_argv
    subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_semantic_indexer.py")] + sub_argv[1:])

def cmd_onboard(args):
    """Generate agent-specific config files."""
    import workshop_onboard
    sys.argv = ["workshop_onboard.py", args.agent_type, "--output-dir", args.output_dir]
    workshop_onboard.main()

def cmd_sync(args):
    """Synchronize all AI agent harnesses, MCP servers, and core skills from manifest."""
    import workshop_sync
    sys.argv = ["workshop_sync.py"]
    if getattr(args, "dry_run", False):
        sys.argv.append("--dry-run")
    if getattr(args, "check", False):
        sys.argv.append("--check")
    workshop_sync.main()

def cmd_eval(args):
    """Run deterministic benchmark evaluation across all agent harnesses."""
    import workshop_eval
    sys.argv = ["workshop_eval.py"]
    if getattr(args, "reasoning", False):
        sys.argv.append("--reasoning")
    if getattr(args, "all", False):
        sys.argv.append("--all")
    if getattr(args, "json", False):
        sys.argv.append("--json")
    workshop_eval.main()

def cmd_drift(args):
    """Audit and synchronize subsystem drift against upstream git remotes."""
    import workshop_drift
    sys.argv = ["workshop_drift.py"] + sys.argv[2:]
    workshop_drift.main()

def cmd_hf(args):
    """Execute Hugging Face Hub CLI engine."""
    import workshop_hf
    sys.argv = ["workshop_hf.py"] + sys.argv[2:]
    workshop_hf.main()

def cmd_openrouter(args):
    """Execute OpenRouter Model Gateway commands."""
    import workshop_openrouter
    sys.argv = ["workshop_openrouter.py"] + sys.argv[2:]
    workshop_openrouter.main()

def cmd_github(args):
    """Execute GitHub Ecosystem Inspector commands."""
    import workshop_github
    sys.argv = ["workshop_github.py"] + sys.argv[2:]
    workshop_github.main()

def cmd_routine(args):
    """Execute Routine Bi-Daily Maintenance Supervisor."""
    sub_argv = sys.argv[2:]
    subprocess.run([sys.executable, "-u", str(SCRIPTS_DIR / "workshop_routine.py")] + sub_argv)

def cmd_status(args):
    """Print centralized Workshop status."""
    catalog_path = WORKSHOP_DIR / "CATALOG.json"
    if not catalog_path.exists():
        from workshop_indexer import main as index_main
        index_main()
        
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    subsystems = data.get("subsystems", {})
    
    print("\n=======================================================")
    print(" 🌐 CENTRALIZED WORKSHOP STATUS & REPOSITORY MATRIX")
    print(f" Root Workspace: {WORKSHOP_DIR}")
    print(f" Total Integrated Subsystems: {len(subsystems)}")
    print("=======================================================\n")
    
    categories = {}
    for k, v in subsystems.items():
        cat = v.get("category_label", "General")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((k, v))
        
    for cat_name, items in categories.items():
        print(f" [{cat_name}]")
        for key, item in items:
            p = WORKSHOP_DIR / item.get("path", key)
            is_ready = p.exists() and (len(list(p.iterdir())) > 1 if p.is_dir() else True)
            status = "[READY]" if is_ready else "[PENDING]"
            name = item.get("name", key)
            if len(name) > 38:
                name = name[:35] + "..."
            print(f"  {status:<9} {name:<40} : {item.get('path')}")
        print()
    print("=======================================================\n")

def cmd_vault(args):
    """Execute Obsidian Second Brain vault commands."""
    import obsidian_vault
    sys.argv = ["obsidian_vault.py"] + sys.argv[2:]
    obsidian_vault.main()

def cmd_backup(args):
    """Execute Workshop backup synchronization."""
    import workshop_backup
    sys.argv = ["workshop_backup.py"] + sys.argv[2:]
    workshop_backup.main()

def cmd_photoreal(args):
    """Execute Ultra-Realistic FLUX Photoreal Studio commands."""
    photoreal_dir = WORKSHOP_DIR / "photoreal-studio"
    if not photoreal_dir.exists():
        print("[!] Photoreal Studio directory not found.")
        return

    sub = getattr(args, "subaction", None) or "studio"
    if sub == "studio":
        port = getattr(args, "port", 8000) or 8000
        print(f"[*] Launching Photoreal Web Studio on http://127.0.0.1:{port}...")
        script = photoreal_dir / "run_studio.py"
        subprocess.run([sys.executable, str(script)], cwd=str(photoreal_dir))
    elif sub == "generate":
        cli_script = photoreal_dir / "cli.py"
        cmd = [sys.executable, str(cli_script)]
        if getattr(args, "subject", None):
            cmd.append(args.subject)
        if getattr(args, "preset", None):
            cmd.extend(["--preset", args.preset])
        if getattr(args, "camera", None):
            cmd.extend(["--camera", args.camera])
        if getattr(args, "lens", None):
            cmd.extend(["--lens", args.lens])
        if getattr(args, "lighting", None):
            cmd.extend(["--lighting", args.lighting])
        if getattr(args, "provider", None):
            cmd.extend(["--provider", args.provider])
        if getattr(args, "aspect", None):
            cmd.extend(["--aspect", args.aspect])
        if getattr(args, "enhance", False):
            cmd.append("--enhance")
        if getattr(args, "prompt_only", False):
            cmd.append("--prompt-only")
        subprocess.run(cmd, cwd=str(photoreal_dir))
    elif sub == "presets":
        cli_script = photoreal_dir / "cli.py"
        subprocess.run([sys.executable, str(cli_script), "--list-presets"], cwd=str(photoreal_dir))
    elif sub == "test":
        test_script = photoreal_dir / "test_system.py"
        print("[*] Running Photoreal Studio test suite...")
        subprocess.run([sys.executable, str(test_script)], cwd=str(photoreal_dir))
    else:
        print(f"[!] Unknown photoreal action '{sub}'. Use: studio, generate, presets, or test.")

def cmd_graphify(args):
    """Execute Graphify codebase AST knowledge graph engine."""
    import shutil
    graphify_bin = shutil.which("graphify") or "graphify"
    cmd = [graphify_bin] + (getattr(args, "args", []) or [])
    subprocess.run(cmd, cwd=str(WORKSHOP_DIR))

def cmd_repomix(args):
    """Execute Repomix AI codebase context packer."""
    import shutil
    repomix_bin = shutil.which("repomix") or "repomix"
    sub_args = getattr(args, "args", []) or []
    subprocess.run([repomix_bin] + sub_args, cwd=str(WORKSHOP_DIR))

def cmd_ast_grep(args):
    """Execute ast-grep structural code search and AST rewriting."""
    import shutil
    ast_bin = shutil.which("ast-grep") or "ast-grep"
    sub_args = getattr(args, "args", []) or []
    subprocess.run([ast_bin] + sub_args, cwd=str(WORKSHOP_DIR))

def cmd_antislop(args):
    """Execute Anti-Slop filter suite, rules, gates, and audits."""
    sub = getattr(args, "subaction", None)
    antislop_dir = WORKSHOP_DIR / "anti-slop"
    skills_dir = WORKSHOP_DIR / "skills"

    if sub == "rules":
        print("\n=======================================================")
        print(" 🛡️ ANTI-SLOP OPERATING RULES (38 RULES / 3 TIERS)")
        print("=======================================================\n")
        print(" [TIER 1: HARD GATES - ABSOLUTE PROHIBITIONS]")
        print("  • R-01: No generic visual technique without documented functional purpose.")
        print("  • R-02: No AI copywriting clichés ('seamless', 'cutting-edge', 'revolutionize', 'elevate').")
        print("  • R-03: No fake placeholder stats ('10M+ users', '99.9% satisfaction') without factual telemetry.")
        print("  • R-04: No generic AI code comments repeating obvious syntax ('// calculate total').")
        print("  • R-05: No truncated code or lazy '// TODO' placeholders.")
        print("  • R-06: No unstyled default purple-indigo AI gradients without brand purpose.")
        print("  • R-07: No cookie-cutter bento-grids without content hierarchy justification.")
        print("  • R-08: No fake product terminal mockups if the product has no CLI.")
        print()
        print(" [TIER 2: PURPOSE-GATES - ALLOWED WITH WRITTEN PURPOSE TEST]")
        print("  • R-10: Glassmorphism / backdrop-blur allowed only if separating distinct z-index layers.")
        print("  • R-11: Motion / micro-interactions allowed only with defined UX feedback rationale.")
        print("  • R-12: Card grids allowed only when cards represent discrete, equal-weighted domain entities.")
        print("  • R-13: Badges / pills allowed only for dynamic state indicators (status, tag, count).")
        print("  • R-14: Dark mode styling must use intentional palette tokens (ui-ux-arsenal), not pure #000000.")
        print()
        print(" [TIER 3: QUALITY LOCKS & LIVELINESS DIALS]")
        print("  • R-20: Contrast ratio must meet WCAG 2.1 AA (4.5:1 for body text, 3:1 for >=18px).")
        print("  • R-21: Mobile touch targets must be at least 44x44px with 8px padding.")
        print("  • R-22: All interactive controls must support visible keyboard focus rings.")
        print("  • R-25: Liveliness dials must be set: ENERGY (1-5), RHYTHM (1-5), MOTION (1-5).")
        print("  • R-35: Click-through smoke test: Every interactive element must be tested and recorded.")
        print("  • R-38: Mandatory 4-Block Delivery Gate report before shipping.")
        print("\n=======================================================\n")
    elif sub == "gate":
        print("\n=======================================================")
        print(" 📋 ANTI-SLOP DELIVERY GATE: PRE-FLIGHT VERIFICATION")
        print("=======================================================\n")
        print(" Before declaring any UI, copy, or code deliverable complete, run this audit:")
        print()
        print(" [BLOCK 1: PURPOSE READ]")
        print("  [ ] Every visual technique serves a documented user/hierarchy purpose.")
        print("  [ ] Zero generic purple-indigo gradients or unearned glassmorphism.")
        print("  [ ] Distinct character: If logo and brand name were swapped, would design remain distinct?")
        print()
        print(" [BLOCK 2: LIVELINESS READ & DIALS]")
        print("  [ ] Energy level (1-5) calibrated to product intent.")
        print("  [ ] Rhythm & visual pacing avoids monotone uniform spacing.")
        print("  [ ] Motion & transitions communicate spatial continuity without gratuitous delay.")
        print()
        print(" [BLOCK 3: TECHNICAL GATES & SMOKE TEST]")
        print("  [ ] R-35 Click-through test: Every button, link, and form input exercised and verified.")
        print("  [ ] Responsive viewport verified across desktop, tablet, and 375px mobile.")
        print("  [ ] Zero console errors or unhandled promises.")
        print()
        print(" [BLOCK 4: CONTRAST & ACCESSIBILITY]")
        print("  [ ] Normal text contrast >= 4.5:1 (checked via `python scripts/workshop.py antislop contrast`).")
        print("  [ ] Large text contrast >= 3.0:1.")
        print("  [ ] Full keyboard navigation operable via Tab / Shift-Tab with focus visible.")
        print("\n=======================================================\n")
    elif sub == "skills":
        print("\n=======================================================")
        print(" 📦 ANTI-SLOP SPECIALIZED AGENT SKILLS")
        print("=======================================================\n")
        skills_info = [
            ("antislop", "Core filter: 38 rules, Purpose-Gates, Liveliness dials, and Delivery Gate.", "skills/antislop/SKILL.md"),
            ("antislop-ui", "UI visual craft: palette, layout, components, decoration, motion, hierarchy.", "skills/antislop-ui/SKILL.md"),
            ("antislop-copywriting", "Copywriting hygiene: anti-AI prose, natural headlines, CTA clarity, tone.", "skills/antislop-copywriting/SKILL.md"),
            ("antislop-human", "Accessibility: WCAG contrast check, keyboard navigation, focus states.", "skills/antislop-human/SKILL.md"),
            ("antislop-layoutmobile", "Mobile responsive: breakpoints, touch targets (>=44px), reflow, overflow.", "skills/antislop-layoutmobile/SKILL.md"),
            ("antislop-code", "Code comment sanitization: remove tautological comments, keep architectural rationales.", "skills/antislop-code/SKILL.md"),
        ]
        for name, desc, p in skills_info:
            print(f" • {name:<22} : {desc}")
            print(f"   Path: {p}\n")
        print("=======================================================\n")
    elif sub == "contrast":
        checker = skills_dir / "antislop-human" / "contrast-check.py"
        if not checker.exists():
            checker = antislop_dir / "skills" / "antislop-human" / "contrast-check.py"
        colors = getattr(args, "colors", [])
        if colors:
            subprocess.run([sys.executable, str(checker)] + colors)
        else:
            subprocess.run([sys.executable, str(checker), "--selftest"])
    elif sub == "audit":
        target = Path(args.target) if getattr(args, "target", None) else WORKSHOP_DIR
        print(f"\n[*] Running Anti-Slop heuristic scan on: {target}...")
        slop_words = ["seamlessly", "cutting-edge", "revolutionize", "game-changer", "supercharge", "unleash", "elevate", "delve into", "testament to"]
        slop_comments = ["// calculate", "// import", "// return result", "// TODO: implement", "// ... existing code"]
        findings = []
        exts = {".html", ".js", ".ts", ".jsx", ".tsx", ".py", ".md", ".css"}
        scan_files = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in exts and not any(part.startswith((".", "node_modules", "venv", "__pycache__", "dist")) for part in p.parts)]

        for f in scan_files[:100]:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                for w in slop_words:
                    if w in content.lower():
                        findings.append((f, f"Contains AI buzzword '{w}'"))
                for c in slop_comments:
                    if c in content:
                        findings.append((f, f"Contains redundant AI comment '{c}'"))
            except Exception:  # @court-exempt: binary file read fallback
                pass

        print(f"[+] Scanned {len(scan_files[:100])} files.")
        if findings:
            print(f"[!] Found {len(findings)} potential slop items:")
            for f, msg in findings[:15]:
                try:
                    rel = f.relative_to(WORKSHOP_DIR)
                except ValueError:
                    rel = f
                print(f"   - {rel}: {msg}")
            if len(findings) > 15:
                print(f"   ... and {len(findings) - 15} more.")
        else:
            print("[✓] Zero overt AI buzzwords or redundant comments detected in sampled files.")
def cmd_court(args):
    """Execute Slop Court adversarial quality tribunal."""
    court_script = SCRIPTS_DIR / "workshop_court.py"
    court_args = getattr(args, "court_args", [])
    cmd = [sys.executable, str(court_script)] + court_args
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

def cmd_vox(args):
    """Execute Vox-Inspired Editorial Explainer Video Production Agent."""
    vox_script = SCRIPTS_DIR / "vox_production_agent.py"
    cmd = [sys.executable, str(vox_script)] + (args.args if hasattr(args, "args") and args.args else [])
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(
        description="Centralized Workshop Master CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Search
    p_search = subparsers.add_parser("search", help="Search 865+ skills, Subsystems, MCPs, APIs")
    p_search.add_argument("query", nargs="?", default="", help="Query keyword")
    p_search.add_argument("--category", "-c", choices=["all", "skills", "repos", "mcps", "apis"], default="all")
    p_search.add_argument("--limit", "-l", type=int, default=15)
    p_search.add_argument("--refresh", action="store_true", help="Force refresh skills cache")
    p_search.add_argument("--json", action="store_true")

    # Info
    p_info = subparsers.add_parser("info", help="Get AI agent briefing on any subsystem")
    p_info.add_argument("name", help="Subsystem or tool name (e.g. 'scrapling', 'strix', 'openhands')")
    p_info.add_argument("--json", action="store_true", help="Output raw JSON")

    # Index
    subparsers.add_parser("index", help="Regenerate machine CATALOG.json and INDEX.md")

    # See (Smart Media Visualizer)
    p_see = subparsers.add_parser("see", help="Smart visual inspection of images/videos/directories")
    p_see.add_argument("path", help="Path to image, video, audio, or directory")
    p_see.add_argument("--prompt", "-p", default="", help="Optional question/prompt for multimodal vision")
    p_see.add_argument("--no-storyboard", action="store_true", help="Skip video storyboard creation")
    p_see.add_argument("--json", action="store_true", help="Output raw JSON")

    # Vision Subcommands
    p_vision = subparsers.add_parser("vision", help="Multimodal vision suite (inspect, frames, storyboard, ocr, transcribe)")
    p_vision.add_argument("subcommand", nargs=argparse.REMAINDER)

    # Doctor
    p_doc = subparsers.add_parser("doctor", help="Run health diagnostics on Workshop")
    p_doc.add_argument("--strict", action="store_true", help="Exit with code 1 on any critical failure")

    # Live Browser Hub
    p_hub = subparsers.add_parser("hub", help="Start Live Browser Hub (http://localhost:7860)")
    p_hub.add_argument("--port", type=int, default=7860)

    # MCP
    p_mcp = subparsers.add_parser("mcp", help="Inspect and test MCP servers")
    p_mcp.add_argument("action", choices=["list", "test", "start"], nargs="?", default="list")
    p_mcp.add_argument("name", nargs="?", default="")

    # Status
    subparsers.add_parser("status", help="Show centralized workshop status")
    # Photoreal Studio
    p_photo = subparsers.add_parser("photoreal", help="Ultra-Realistic FLUX Photoreal Studio (optics, synthesis, web UI)")
    p_photo_subs = p_photo.add_subparsers(dest="subaction", help="Photoreal action")
    
    p_p_studio = p_photo_subs.add_parser("studio", help="Launch interactive dark-mode web studio")
    p_p_studio.add_argument("--port", type=int, default=8000, help="Port to run server on")
    
    p_p_gen = p_photo_subs.add_parser("generate", help="Synthesize photorealistic image from prompt or preset")
    p_p_gen.add_argument("subject", nargs="?", default=None, help="Photographic subject")
    p_p_gen.add_argument("--preset", "-p", default=None, help="Preset key")
    p_p_gen.add_argument("--camera", "-c", default=None, help="Camera body")
    p_p_gen.add_argument("--lens", "-l", default=None, help="Lens optical profile")
    p_p_gen.add_argument("--lighting", default=None, help="Lighting scheme")
    p_p_gen.add_argument("--provider", default="flux_dev_realism", help="Inference provider")
    p_p_gen.add_argument("--aspect", default="3:4", help="Aspect ratio")
    p_p_gen.add_argument("--enhance", "-e", action="store_true", help="Enhance subject with physical micro-details")
    p_p_gen.add_argument("--prompt-only", action="store_true", help="Display enhanced prompt without generation")
    
    p_photo_subs.add_parser("presets", help="List all master photographic optical presets")
    p_photo_subs.add_parser("test", help="Run automated test suite for photoreal engine")


    # Anti-Slop Filter & Quality Gate
    p_anti = subparsers.add_parser("antislop", help="Anti-Slop AI filter, 38 rules, liveliness dials, and delivery gates")
    p_anti_subs = p_anti.add_subparsers(dest="subaction", help="Anti-Slop action")
    p_anti_subs.add_parser("rules", help="Display all 38 anti-slop rules across 3 tiers")
    p_anti_subs.add_parser("gate", help="Display 4-block Delivery Gate pre-flight verification checklist")
    p_anti_subs.add_parser("skills", help="List all 6 anti-slop agent skills")
    p_anti_audit = p_anti_subs.add_parser("audit", help="Run heuristic scan for AI slop clichés and comments")
    p_anti_audit.add_argument("target", nargs="?", default="", help="Path to file or directory to scan")
    p_anti_contrast = p_anti_subs.add_parser("contrast", help="Check WCAG 2.1 AA/AAA contrast ratios")
    p_anti_contrast.add_argument("colors", nargs=argparse.REMAINDER, help="Hex foreground and background colors or none for selftest")

    # Slop Court: Adversarial Quality Tribunal
    p_court = subparsers.add_parser("court", help="Slop Court: Adversarial Quality Tribunal & Anti-Slop Enforcement System")
    p_court.add_argument("court_args", nargs=argparse.REMAINDER, help="Court action (trial, indict, bailiff, reform, statutes)")

    # Persistent Services & Gateways Supervisor
    p_services = subparsers.add_parser("services", help="Manage persistent services & gateways (Browser Hub, Camofox)")
    p_services.add_argument("service_action", choices=["status", "start", "stop", "restart"], nargs="?", default="status")
    p_services.add_argument("targets", nargs="*", default=["all"], help="Service name(s) or 'all'")

    # Hugging Face Hub Engine & CLI
    p_hf = subparsers.add_parser("hf", help="Hugging Face Hub engine (trending, search, inspect, papers)")
    p_hf.add_argument("args", nargs=argparse.REMAINDER)

    # OpenRouter Model Gateway & Pricing
    p_or = subparsers.add_parser("openrouter", help="OpenRouter model gateway (free, search, inspect, cheapest)")
    p_or.add_argument("args", nargs=argparse.REMAINDER)

    # GitHub Ecosystem & Repo Inspector
    p_gh = subparsers.add_parser("github", help="GitHub repo search, trending topics, and release inspector")
    p_gh.add_argument("args", nargs=argparse.REMAINDER)

    # Subsystem Drift & Upstream Sync
    p_drift = subparsers.add_parser("drift", help="Audit & sync subsystem drift against upstream git remotes")
    p_drift.add_argument("args", nargs=argparse.REMAINDER)

    # Agent Onboarding & Universal Sync
    p_onboard = subparsers.add_parser("onboard", help="Generate agent-specific config files (cursor, claude, windsurf, etc.)")
    p_onboard.add_argument("agent_type", choices=["cursor", "claude", "windsurf", "generic", "copilot", "all"], help="Target agent/IDE type")
    p_onboard.add_argument("--output-dir", "-o", default=".", help="Output directory")

    p_sync = subparsers.add_parser("sync", help="Synchronize all AI agent harnesses, MCP servers, and core skills from manifest")
    p_sync.add_argument("--dry-run", action="store_true", help="Preview sync changes without writing")
    p_sync.add_argument("--check", action="store_true", help="Verify all harness configurations are up-to-date")

    p_eval = subparsers.add_parser("eval", help="Run deterministic evaluation benchmark across agent harnesses")
    p_eval.add_argument("--reasoning", action="store_true", help="Run the 8-task reasoning & behavioral discipline benchmark")
    p_eval.add_argument("--all", action="store_true", help="Run both plumbing integration and reasoning benchmarks")
    p_eval.add_argument("--json", action="store_true", help="Output machine-readable JSON results")

    # Desktop Automation Engine
    p_desktop = subparsers.add_parser("desktop", help="Native OS desktop automation (screenshot, click, type, windows, launch)")
    p_desktop.add_argument("args", nargs=argparse.REMAINDER)
    
    # Virtual Browser Computer
    p_browser = subparsers.add_parser("browser", help="Launch Virtual AI Computer (standalone desktop window + persistent browser)")
    p_browser.add_argument("action", choices=["start", "stop", "restart", "status"], nargs="?", default="status")
    
    # Semantic Skill Indexer
    p_sem = subparsers.add_parser("semantic", help="Hybrid Semantic + Lexical Skill Indexer")
    p_sem.add_argument("action", choices=["index", "search"], default="search", nargs="?")
    p_sem.add_argument("--query", default="")
    p_sem.add_argument("--limit", type=int, default=10)
    # Event Bus & Agent Nervous System
    p_eb = subparsers.add_parser("event-bus", help="Workshop Agent Nervous System Event Bus")
    p_eb.add_argument("args", nargs=argparse.REMAINDER)
    # Adversarial Verification Guard
    p_guard = subparsers.add_parser("guard", help="Run Workshop Adversarial & Quality Verification Gate")
    p_guard.add_argument("args", nargs=argparse.REMAINDER)
    # Dynamic Tool Forge
    p_forge = subparsers.add_parser("forge", help="Dynamic Tool Forge: synthesize MCP wrappers for unknown APIs")
    p_forge.add_argument("--spec", required=True, help="Target API spec (JSON file path or inline JSON)")
    p_forge.add_argument("--test-args", help="Test arguments (JSON file path or inline JSON)")
    p_forge.add_argument("--name", help="Service name override")
    # Local Inference Router
    p_route = subparsers.add_parser("route", help="Local Inference Tier: route tasks between local and cloud models")
    p_route.add_argument("--task", default="code_review", help="Task type to route")
    p_route.add_argument("--stats", action="store_true", help="Show model stats")
    # Self-Evolution Engine
    p_evo = subparsers.add_parser("evolve", help="Self-Evolution Engine: skill freshness, auto-update, deprecation detection")
    p_evo.add_argument("action", choices=["scan", "recommend", "update", "status"], default="scan", nargs="?")
    p_evo.add_argument("--skill", help="Skill name for update action")
    p_evo.add_argument("--execute", action="store_true", help="Actually execute updates (not dry run)")
    # Auto-Updater
    p_update = subparsers.add_parser("update", help="Auto-Updater: subsystem drift sync & skill refresh")
    p_update.add_argument("--dry-run", action="store_true", default=True, help="Check only, don't pull")
    p_update.add_argument("--execute", action="store_true", help="Actually execute updates")
    # Digital Forensics & Data Recovery Engine
    p_forensic = subparsers.add_parser("forensic", help="Digital Forensics & Data Recovery (TSK 4.15, TestDisk 7.3, Dissect, Hashes)")
    p_forensic.add_argument("args", nargs=argparse.REMAINDER)

    # OSINT & Investigation Suite
    p_osint = subparsers.add_parser("osint", help="OSINT & Auspex Intelligence Suite (Username, Email, Phone, Domain, IP)")
    p_osint.add_argument("args", nargs=argparse.REMAINDER)

    # Obsidian Second Brain Vault
    p_vault = subparsers.add_parser("vault", help="Obsidian Second Brain Vault (status, search, adr, postmortem, journal)")
    p_vault.add_argument("args", nargs=argparse.REMAINDER)

    # Workshop Backup Synchronization
    p_backup = subparsers.add_parser("backup", help="Synchronize Workshop vault, configs, and scripts to Backup repository")
    p_backup.add_argument("args", nargs=argparse.REMAINDER)

    # Routine Bi-Daily Maintenance Supervisor
    p_routine = subparsers.add_parser("routine", help="Routine Bi-Daily Maintenance Supervisor (audit, sync, scheduled task)")
    p_routine.add_argument("args", nargs=argparse.REMAINDER)

    # Graphify Knowledge Graph Engine
    p_graphify = subparsers.add_parser("graphify", help="Graphify Codebase AST Knowledge Graph (extract, query, explain, path, tree)")
    p_graphify.add_argument("args", nargs=argparse.REMAINDER)

    # Repomix Codebase Context Packer
    p_repomix = subparsers.add_parser("repomix", help="Repomix Codebase Context Packer for AI Agents")
    p_repomix.add_argument("args", nargs=argparse.REMAINDER)

    # ast-grep Structural Search & Rewriting
    p_sg = subparsers.add_parser("ast-grep", help="ast-grep Tree-sitter Structural Code Search & Rewriting")
    p_sg.add_argument("args", nargs=argparse.REMAINDER)

    # Vox-Inspired Editorial Explainer Video Production Agent
    p_vox = subparsers.add_parser("vox", help="Vox Explainer Video Production Agent (validate, audio, render)")
    p_vox.add_argument("args", nargs=argparse.REMAINDER)

    # Workshop Up / Down Lifecycle
    subparsers.add_parser("up", help="Bootstrap and start all background gateways and services")
    subparsers.add_parser("down", help="Gracefully stop all background gateways and services")

        # Workshop Houses: Domain Guilds & Taxonomy
    p_house = subparsers.add_parser("house", help="Workshop Sovereign Houses: list, inspect, and explore houses")
    p_house.add_argument("action", choices=["list", "inspect"], nargs="?", default="list", help="House action")
    p_house.add_argument("target", nargs="?", default="", help="House slug to inspect")

    args, extra = parser.parse_known_args()
    if extra and hasattr(args, "args") and isinstance(args.args, list):
        args.args.extend(extra)

    if args.command == "routine":
        cmd_routine(args)
    elif args.command == "see":
        cmd_see(args)
    elif args.command == "vision":
        cmd_vision(args)
    elif args.command == "house":
        cmd_house(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "info":
        cmd_info(args)
    elif args.command == "index":
        cmd_index(args)
    elif args.command == "doctor":
        cmd_doctor(args)
    elif args.command == "hub":
        cmd_hub(args)
    elif args.command == "browser":
        cmd_browser(args)
    elif args.command == "hf":
        cmd_hf(args)
    elif args.command == "openrouter":
        cmd_openrouter(args)
    elif args.command == "github":
        cmd_github(args)
    elif args.command == "drift":
        cmd_drift(args)
    elif args.command == "onboard":
        cmd_onboard(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "eval":
        cmd_eval(args)
    elif args.command == "desktop":
        cmd_desktop(args)
    elif args.command == "event-bus":
        cmd_event_bus(args)
    elif args.command == "guard":
        cmd_guard(args)
    elif args.command == "forge":
        cmd_forge(args)
    elif args.command == "route":
        cmd_route(args)
    elif args.command == "evolve":
        cmd_evolve(args)
    elif args.command == "semantic":
        cmd_semantic(args)
    elif args.command == "mcp":
        cmd_mcp(args)
    elif args.command == "photoreal":
        cmd_photoreal(args)
    elif args.command == "antislop":
        cmd_antislop(args)
    elif args.command == "court":
        cmd_court(args)
    elif args.command == "services":
        cmd_services(args)
    elif args.command == "forensic":
        cmd_forensic(args)
    elif args.command == "osint":
        cmd_osint(args)
    elif args.command == "vault":
        cmd_vault(args)
    elif args.command == "backup":
        cmd_backup(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "vox":
        cmd_vox(args)
    elif args.command == "up":
        cmd_up(args)
    elif args.command == "down":
        cmd_down(args)
    elif args.command == "graphify":
        cmd_graphify(args)
    elif args.command == "repomix":
        cmd_repomix(args)
    elif args.command == "ast-grep":
        cmd_ast_grep(args)
    else:
        cmd_status(args)
        parser.print_help()

if __name__ == "__main__":
    main()
