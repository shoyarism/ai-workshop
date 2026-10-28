#!/usr/bin/env python3

"""

Workshop Master MCP Server

==========================

The universal Model Context Protocol server exposing Workshop OS tools,

second-brain memory, skill search & loading, code critique, and verification

to ANY AI agent harness (Antigravity, Claude Code, OpenCode, Codex, Cursor, etc.).



Usage:

    uv run python scripts/workshop_mcp.py

"""



from __future__ import annotations



import json

import os

import re

import subprocess
import shlex
import shutil

import sys

from pathlib import Path

from typing import List, Optional



# UTF-8 stdout on Windows

if hasattr(sys.stdout, "reconfigure"):

    try:

        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    except Exception:  # @court-exempt: console encoding reconfigure

        pass



sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_paths import ROOT, SCRIPTS, VAULT, python_executable

import workshop_skills

import workshop_semantic_indexer



try:
    from mcp.server.mcpserver import MCPServer
except ImportError:  # @court-exempt: graceful fallback when running tools standalone
    MCPServer = None

IS_READ_ONLY = ("--read-only" in sys.argv) or (
    os.environ.get("WORKSHOP_READ_ONLY") == "1"
)

server_name = "workshop_ro" if IS_READ_ONLY else "workshop"

server = MCPServer(
    name=server_name,
    title=f"Workshop OS Master Server ({'Read-Only' if IS_READ_ONLY else 'Full'})",
    description="Universal agent interface for skills, memory, tools, and code verification",
    version="3.5.0",
) if MCPServer is not None else None


class _FallbackDecorator:
    @staticmethod
    def tool(name=None, description=None):
        def decorator(f):
            return f
        return decorator

    @staticmethod
    def resource(uri=None):
        def decorator(f):
            return f
        return decorator

    @staticmethod
    def prompt(name=None, description=None):
        def decorator(f):
            return f
        return decorator

server_decorator = server if server is not None else _FallbackDecorator()



# ==============================================================================

# SECRECY & PII SANITIZATION ENGINE (ENFORCING PRIVACY-AND-SENSITIVE-DATA)

# ==============================================================================



SECRET_PATTERNS = [

    (r"sk-[a-zA-Z0-9_\-]{20,}", "[REDACTED_API_KEY]"),

    (r"ghp_[a-zA-Z0-9]{20,}", "[REDACTED_GITHUB_TOKEN]"),

    (r"gho_[a-zA-Z0-9]{20,}", "[REDACTED_GITHUB_TOKEN]"),

    (r"github_pat_[a-zA-Z0-9_]{22,}", "[REDACTED_GITHUB_PAT]"),

    (r"AIzaSy[a-zA-Z0-9_\-]{33}", "[REDACTED_GOOGLE_API_KEY]"),

    (r"Bearer\s+[a-zA-Z0-9._\-]{20,}", "Bearer [REDACTED_BEARER_TOKEN]"),

    (

        r"-----BEGIN\s+[A-Z\s]+PRIVATE\s+KEY-----[\s\S]*?-----END\s+[A-Z\s]+PRIVATE\s+KEY-----",

        "[REDACTED_PRIVATE_KEY]",

    ),

    (

        r"(?i)(password|passwd|secret|api_key|token)(\s*[:=]\s*)['\"][^'\"]{6,}['\"]",

        r"\1\2'[REDACTED_CREDENTIAL]'",

    ),

]



PII_PATTERNS = [

    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "[REDACTED_EMAIL]"),

    (r"(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]"),

    (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),

]





def is_luhn_valid(number_str: str) -> bool:

    """Verifies Luhn checksum algorithm (MOD 10) for payment cards."""

    digits = [int(c) for c in number_str if c.isdigit()]

    if len(digits) < 13 or len(digits) > 19:

        return False

    checksum = 0

    reverse_digits = digits[::-1]

    for i, d in enumerate(reverse_digits):

        if i % 2 == 1:

            doubled = d * 2

            checksum += doubled - 9 if doubled > 9 else doubled

        else:

            checksum += d

    return checksum % 10 == 0





def redact_credit_cards(text: str) -> tuple[str, int]:

    """Scans for payment card patterns and validates via Luhn checksum."""

    count = 0

    card_pattern = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{1,4}\b|\b\d{13,19}\b")



    def replacer(match: re.Match) -> str:

        nonlocal count

        raw_val = match.group(0)

        digits_only = re.sub(r"\D", "", raw_val)

        if is_luhn_valid(digits_only):

            count += 1

            return "[REDACTED_CREDIT_CARD]"

        elif len(digits_only) in (15, 16):

            count += 1

            return "[REDACTED_CARD_LIKE_NUMBER]"

        return raw_val



    sanitized = card_pattern.sub(replacer, text)

    return sanitized, count





def load_sensitive_terms() -> List[str]:

    """Load configurable sensitive entities (names, clients, project codenames)."""

    terms_file = ROOT / ".workshop_state" / "sensitive_terms.json"

    if terms_file.is_file():

        try:

            data = json.loads(terms_file.read_text(encoding="utf-8"))

            return data.get("sensitive_terms", [])

        except (IOError, json.JSONDecodeError):  # @court-exempt: corrupt terms file fallback

            pass

    return []





def redact_secrets(text: str) -> tuple[str, int]:

    """

    Sanitizes credentials, secrets, PII, and sensitive terms from text.

    Returns (sanitized_text, count_of_redactions).

    """

    redacted = text

    count = 0



    # 1. API Keys & Secrets

    for pat, rep in SECRET_PATTERNS:

        matches = re.findall(pat, redacted)

        if matches:

            count += len(matches)

            redacted = re.sub(pat, rep, redacted)



    # 2. PII (Emails, Phones, SSNs)

    for pat, rep in PII_PATTERNS:

        matches = re.findall(pat, redacted)

        if matches:

            count += len(matches)

            redacted = re.sub(pat, rep, redacted)



    # 3. Credit Cards (Luhn Checksum Validated)

    redacted, cc_count = redact_credit_cards(redacted)

    count += cc_count



    # 4. Configurable Terms (Names, Clients, Codenames)

    custom_terms = load_sensitive_terms()

    for term in custom_terms:

        if term and term.lower() in redacted.lower():

            pattern = re.compile(re.escape(term), re.IGNORECASE)

            redacted, n = pattern.subn("[REDACTED_SENSITIVE_ENTITY]", redacted)

            count += n



    return redacted, count





# ==============================================================================

# ROLE-BASED ACCESS CONTROL (RBAC) & MCP TOOL ALLOWLIST

# ==============================================================================





def get_active_role() -> Optional[str]:

    """

    Determines active agent role from WORKSHOP_ROLE env or .workshop_state/active_role.json.

    """

    env_role = os.environ.get("WORKSHOP_ROLE")

    if env_role:

        return env_role.strip().lower()



    role_file = ROOT / ".workshop_state" / "active_role.json"

    if role_file.is_file():

        try:

            data = json.loads(role_file.read_text(encoding="utf-8"))

            return data.get("role", "").strip().lower() or None

        except (IOError, json.JSONDecodeError):  # @court-exempt: corrupt role file fallback

            pass

    return None





WRITE_EXEC_MCP_TOOLS = {"verify", "memory_write", "critique"}





def get_authorized_roles_for_tool(tool_name: str) -> List[str]:

    """Inspect subagent manifest to find which roles possess permission for a tool."""

    subagents_file = ROOT / ".agents" / "subagents.json"

    if not subagents_file.is_file():

        return []

    try:

        data = json.loads(subagents_file.read_text(encoding="utf-8"))

        return sorted(

            [

                r

                for r, cfg in data.get("subagents", {}).items()

                if tool_name in cfg.get("tools", [])

            ]

        )

    except Exception:

        return []





def check_role_permission(tool_name: str) -> tuple[bool, str]:

    """

    Validates whether the active agent role is permitted to invoke the requested tool.

    Enforces strict DEFAULT-DENY for write and execution tools when no role is declared.

    Returns (is_allowed, denial_reason).

    """

    active_role = get_active_role()



    # 1. DEFAULT-DENY: When no active role is declared, block all write and execution tools!

    if not active_role:

        if tool_name in WRITE_EXEC_MCP_TOOLS:

            permitted = get_authorized_roles_for_tool(tool_name)

            return False, (

                f"[PERMISSION_DENIED] Default-deny active: Tool '{tool_name}' requires an authorized role. "

                f"No authorized role declared for this session. Permitted roles: {permitted}."

            )

        # Safe read-only discovery tools remain accessible

        return True, ""



    # 2. ROLE-BASED ALLOWLIST: Verify against declared tools in subagents manifest

    subagents_file = ROOT / ".agents" / "subagents.json"

    if not subagents_file.is_file():

        if tool_name in WRITE_EXEC_MCP_TOOLS:

            return (

                False,

                f"[PERMISSION_DENIED] Subagents manifest missing; default-deny active for '{tool_name}'.",

            )

        return True, ""



    try:

        data = json.loads(subagents_file.read_text(encoding="utf-8"))

        role_cfg = data.get("subagents", {}).get(active_role)

        if not role_cfg:

            if tool_name in WRITE_EXEC_MCP_TOOLS:

                return (

                    False,

                    f"[PERMISSION_DENIED] Unknown role '{active_role}'; default-deny active for '{tool_name}'.",

                )

            return True, ""



        allowed_tools = set(role_cfg.get("tools", []))

        if tool_name not in allowed_tools:

            return False, (

                f"[PERMISSION_DENIED] Tool '{tool_name}' is prohibited for role '{active_role}'. "

                f"Role '{active_role}' is restricted to permitted tools: {sorted(allowed_tools)}."

            )

    except Exception as e:

        if tool_name in WRITE_EXEC_MCP_TOOLS:

            return False, f"[PERMISSION_DENIED] Error evaluating permissions: {e}"

        return True, ""



    return True, ""





# ==============================================================================

# 1. SKILL RETRIEVAL & LOADING (PROGRESSIVE DISCLOSURE)

# ==============================================================================





@server_decorator.tool(

    name="skill_search",

    description="Search 920+ specialized agent skills and Obsidian vault notes using hybrid semantic vector and BM25 ranking.",

)

def skill_search(query: str, limit: int = 8) -> str:

    """Search skills and memory notes. Returns list of matches with descriptions."""

    allowed, err = check_role_permission("skill_search")

    if not allowed:

        return err



    try:

        results = workshop_semantic_indexer.search(query, limit=limit, mode="hybrid")

        if not results:

            return f"No matching skills or notes found for query: '{query}'"



        output = [f"Found {len(results)} matches for '{query}':\n"]

        for idx, item in enumerate(results, 1):

            itype = item.get("item_type", "skill").upper()

            name = item.get("name", "Unknown")

            desc = item.get("description", "").strip()

            path = item.get("path", "")

            score = item.get("rrf_score", 0.0)

            output.append(

                f"{idx}. [{itype}] **{name}** (Score: {score})\n   Path: `{path}`\n   Description: {desc}\n"

            )



        return "\n".join(output)

    except Exception as e:

        return f"Error executing skill search: {str(e)}"





@server_decorator.tool(

    name="skill_load",

    description="Retrieve the complete instructions (SKILL.md) and asset list of any Workshop domain skill on demand.",

)

def skill_load(name: str) -> str:

    """Fetch complete skill instructions by name."""

    allowed, err = check_role_permission("skill_load")

    if not allowed:

        return err



    target_skill = workshop_skills.by_name(name)

    if not target_skill:

        # Fallback: search by prefix/partial

        candidates = [

            s for s in workshop_skills.discover() if name.lower() in s.name.lower()

        ]

        if candidates:

            target_skill = candidates[0]

        else:

            return f"Skill '{name}' not found. Use `skill_search('{name}')` to find the exact name."



    try:

        content = target_skill.path.read_text(encoding="utf-8", errors="replace")

        skill_dir = target_skill.dir

        files = [

            p.name

            for p in skill_dir.iterdir()

            if p.name != "SKILL.md" and not p.name.startswith(".")

        ]



        skill_path_str = str(target_skill.path).replace("\\", "/")

        res = [

            f"# Domain Skill: {target_skill.name}",

            f"Location: `{skill_path_str}`",

            f"Description: {target_skill.description}",

        ]

        if files:

            res.append(f"Associated Files/Assets: {', '.join(files)}")

        res.append("\n---\n")

        res.append(content)

        return "\n".join(res)

    except Exception as e:

        return f"Failed to load skill '{name}': {str(e)}"





# ==============================================================================

# 2. OBSIDIAN SECOND BRAIN (PERSISTENT MEMORY)

# ==============================================================================





@server_decorator.tool(

    name="memory_recall",

    description="Query persistent memory in the Obsidian Second Brain: Architecture Decision Records (ADRs), Error Post-Mortems (PM-xxx), and Task Queue.",

)

def memory_recall(query: str, limit: int = 5) -> str:

    """Query Obsidian Vault memory notes."""

    allowed, err = check_role_permission("memory_recall")

    if not allowed:

        return err



    try:

        from obsidian_vault import get_vault_notes, parse_frontmatter



        notes = get_vault_notes()

        q_lower = query.lower()

        matches = []

        for n in notes:

            content = n.read_text(encoding="utf-8", errors="replace")

            meta = parse_frontmatter(content)

            title = meta.get("title", n.stem)

            tags = meta.get("tags", "")

            if (

                q_lower in title.lower()

                or q_lower in content.lower()

                or q_lower in tags.lower()

            ):

                matches.append((n, title, meta.get("type", "note"), content[:1200]))

                if len(matches) >= limit:

                    break



        if not matches:

            return f"No memory records found matching: '{query}'"



        out = [f"Retrieved {len(matches)} memory records from Obsidian Vault:\n"]

        for p, title, ntype, preview in matches:

            rel = str(p.relative_to(ROOT)).replace("\\", "/")

            sanitized_preview, _ = redact_secrets(preview)

            out.append(

                f"### [[{title}]] ({ntype})\nFile: `{rel}`\n```markdown\n{sanitized_preview}...\n```\n"

            )

        return "\n".join(out)

    except Exception as e:

        return f"Error recalling memory: {str(e)}"





def memory_write(kind: str, title: str, content: str, tags: str = "") -> str:

    """Record an ADR, post-mortem, or handoff note."""

    allowed, err = check_role_permission("memory_write")

    if not allowed:

        return err



    kind = kind.lower().strip()

    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    now = __import__("datetime").datetime.now().strftime("%Y-%m-%d")



    if kind in ("adr", "architecture"):

        adr_dir = VAULT / "01 - Architecture Decision Records (ADRs)"

        adr_dir.mkdir(parents=True, exist_ok=True)

        count = len(list(adr_dir.glob("ADR-*.md"))) + 1

        filename = f"ADR-{count:03d} - {title}.md"

        out_file = adr_dir / filename

        fm = f"""---

title: {title}

type: adr

status: Proposed

date: {now}

tags: [{", ".join(tag_list or ["adr", "architecture"])}]

---



# ADR-{count:03d}: {title}



## Context & Problem Statement

{content}

"""

    elif kind in ("postmortem", "post-mortem", "bug"):

        pm_dir = VAULT / "02 - Post-Mortems"

        pm_dir.mkdir(parents=True, exist_ok=True)

        count = len(list(pm_dir.glob("PM-*.md"))) + 1

        filename = f"PM-{count:03d} - {title}.md"

        out_file = pm_dir / filename

        fm = f"""---

title: {title}

type: post-mortem

status: Resolved

date: {now}

tags: [{", ".join(tag_list or ["post-mortem", "bugfix"])}]

severity: Medium

---



# PM-{count:03d}: {title}



{content}

"""

    else:

        # Default note or task handoff

        task_dir = VAULT / "04 - Tasks & Sprints"

        task_dir.mkdir(parents=True, exist_ok=True)

        filename = f"Handoff - {now} - {title}.md"

        out_file = task_dir / filename

        fm = f"""---

title: {title}

type: handoff

date: {now}

tags: [{", ".join(tag_list or ["handoff", "session"])}]

---



# Session Handoff: {title}



{content}

"""



    out_file.write_text(fm, encoding="utf-8")

    out_path = str(out_file.relative_to(ROOT)).replace("\\", "/")
    return f"Saved memory record successfully to: `{out_path}`"





# ==============================================================================

# 3. REASONING & QUALITY ASSURANCE TOOLS (CLAUDE-PARITY GATES)

# ==============================================================================





def verify(command_or_path: str = "") -> str:

    """Run tests, linter, or health check deterministically."""

    allowed, err = check_role_permission("verify")

    if not allowed:

        return err



    target_cmd = command_or_path.strip()

    if not target_cmd:

        # Default verification: run workshop doctor and git status

        res = []

        doc_proc = subprocess.run(

            [str(python_executable()), str(SCRIPTS / "workshop.py"), "doctor"],

            capture_output=True,

            text=True,

            cwd=str(ROOT),

        )

        res.append("=== WORKSHOP DOCTOR ===\n" + (doc_proc.stdout or doc_proc.stderr))

        return "\n".join(res)



    # Interactive safety gate on custom verification commands
    from workshop_hooks import check_command_safety

    safe, reason = check_command_safety(target_cmd)
    if not safe:
        return f"[BLOCKED BY SAFETY GATE] Verification command rejected: {reason}"

    # Strict allowlist of executables (no arbitrary binaries or shell expansion)
    ALLOWED_VERIFY_EXECUTABLES = {
        "pytest", "ruff", "python", "python3", "uv", "git",
        "npm", "pnpm", "yarn", "node", "cargo", "go"
    }

    try:
        cmd_tokens = shlex.split(target_cmd)
    except Exception as e:
        return f"[BLOCKED BY SAFETY GATE] Invalid command syntax: {e}"

    if not cmd_tokens:
        return "[BLOCKED BY SAFETY GATE] Empty verification command provided."

    raw_exe = cmd_tokens[0]
    exe_name = Path(raw_exe).name.lower()
    for ext in [".exe", ".cmd", ".bat"]:
        if exe_name.endswith(ext):
            exe_name = exe_name[:-len(ext)]

    if exe_name not in ALLOWED_VERIFY_EXECUTABLES:
        allowed_list = ", ".join(sorted(ALLOWED_VERIFY_EXECUTABLES))
        return f"[BLOCKED BY SAFETY GATE] Executable '{raw_exe}' not in verify allowlist ({allowed_list})."

    # Resolve executable path safely without shell
    resolved_bin = shutil.which(cmd_tokens[0])
    exec_args = [resolved_bin if resolved_bin else cmd_tokens[0]] + cmd_tokens[1:]

    try:
        proc = subprocess.run(
            exec_args, shell=False, capture_output=True, text=True, cwd=str(ROOT), timeout=120
        )
        status = (
            "SUCCESS (exit code 0)"
            if proc.returncode == 0
            else f"FAILED (exit code {proc.returncode})"
        )
        return f"Verification Command: `{target_cmd}`\nStatus: {status}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
    except Exception as e:
        return f"[EXECUTION ERROR] Failed to run verification command: {e}"





def critique(code_or_plan: str, context: str = "") -> str:

    """Escalate review to local router / omniroute / critic model with privacy redaction."""

    allowed, err = check_role_permission("critique")

    if not allowed:

        return err



    import httpx



    # Privacy check (enforcing privacy-and-sensitive-data skill)

    clean_code, secrets_found = redact_secrets(code_or_plan)

    clean_context, _ = redact_secrets(context)



    is_explicit_sensitive = any(

        term in (code_or_plan + context).lower()

        for term in [

            "# sensitive",

            "sensitive: true",

            "tag: confidential",

            "classified",

        ]

    )



    endpoints = []

    # If explicitly marked sensitive, do NOT send to shared/free remote endpoints

    if not is_explicit_sensitive:

        endpoints = [

            {

                "name": "OmniRoute",

                "url": "http://127.0.0.1:20128/v1/chat/completions",

                "model": "auto/best-coding",

            },

            {

                "name": "FreeLLMAPI",

                "url": "http://127.0.0.1:31415/v1/chat/completions",

                "model": "auto",

            },

        ]



    prompt = f"""You are a Principal Systems Architect performing a rigorous peer review.

Review the following plan or code diff. Look for:

1. Computational complexity or memory layout bottlenecks

2. Unhandled edge cases and invalid invariant states

3. Security vulnerabilities or missing input sanitization

4. Anti-patterns or violations of first-principles design



Context:

{clean_context}



Content under review:

{clean_code}



Provide a structured, high-density critique with actionable recommendations.

"""



    redaction_notice = (

        f"\n*(Note: {secrets_found} secret token(s) were automatically redacted before analysis)*\n"

        if secrets_found

        else ""

    )



    for ep in endpoints:

        try:

            with httpx.Client(timeout=15.0) as client:

                resp = client.post(

                    ep["url"],

                    json={

                        "model": ep["model"],

                        "messages": [{"role": "user", "content": prompt}],

                        "temperature": 0.2,

                    },

                )

                if resp.status_code == 200:

                    data = resp.json()

                    review = (

                        data.get("choices", [{}])[0]

                        .get("message", {})

                        .get("content", "")

                    )

                    if review:

                        return f"### [Critique by {ep['name']} ({ep['model']})]{redaction_notice}\n\n{review}"

        except Exception:

            continue



    # Local fallback deterministic heuristic review

    findings = []

    lines = code_or_plan.splitlines()

    if any("// TODO" in l or "# TODO" in l for l in lines):

        findings.append(

            "⚠️ Contains TODO/placeholder comments. Implement completely without truncation."

        )

    if any("rm -rf" in l or "DROP TABLE" in l or "format " in l for l in lines):

        findings.append(

            "🚨 Contains destructive commands. Verify safety boundaries and user authorization."

        )

    if len(lines) > 200 and not any(

        "try:" in l or "catch" in l or "except" in l for l in lines

    ):

        findings.append(

            "⚠️ Large code block without explicit error recovery / exception handling."

        )



    summary = (

        "\n".join(f"- {f}" for f in findings)

        if findings

        else "- No obvious critical heuristic violations detected."

    )

    return f"### [Local Heuristic Review]\n(Frontier critic endpoint unavailable; evaluated via Workshop heuristic rules):\n\n{summary}\n\n*Recommendation:* Proceed with deterministic test verification (`verify` tool)."





# Register execution and write tools strictly in FULL mode (omitted in read-only mode)

if not IS_READ_ONLY:

    server_decorator.tool(

        name="memory_write",

        description="Save a new record into persistent memory (e.g. adr, postmortem, or task handoff) in the Obsidian Vault.",

    )(memory_write)



    server_decorator.tool(

        name="verify",

        description="Run verification suite: deterministic test execution, static analysis, or git status check before concluding a task.",

    )(verify)



    server_decorator.tool(

        name="critique",

        description="Escalate a proposed plan, diff, or architectural design to a high-capacity model (or local critic) for code review and flaw detection.",

    )(critique)





@server_decorator.tool(

    name="antislop_audit",

    description="Run the Anti-Slop 38-rule quality audit over code or documentation to detect AI clichés, unearned design tropes, and lazy comments.",

)

def antislop_audit(path: str = ".") -> str:

    """Run anti-slop audit."""

    allowed, err = check_role_permission("antislop_audit")

    if not allowed:

        return err



    target_path = Path(path).resolve()

    proc = subprocess.run(

        [

            str(python_executable()),

            str(SCRIPTS / "workshop.py"),

            "antislop",

            "audit",

            str(target_path),

        ],

        capture_output=True,

        text=True,

        cwd=str(ROOT),

    )

    return proc.stdout or proc.stderr

@server_decorator.tool(
    name="court_trial",
    description="Convene the Adversarial Anti-Slop Court System to adjudicate code, copy, or UI changes. Enforces zero tolerance on AI slop, truncated stubs, and tautological comments.",
)
def court_trial(path: str = ".", staged: bool = False, strict: bool = True) -> str:
    """Run Slop Court judicial trial."""
    allowed, err = check_role_permission("court_trial")
    if not allowed:
        return err

    cmd = [
        str(python_executable()),
        str(SCRIPTS / "workshop_court.py"),
        "trial",
        path,
    ]
    if staged:
        cmd.append("--staged")
    if not strict:
        cmd.append("--lenient")

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    return proc.stdout or proc.stderr

@server_decorator.tool(
    name="court_council",
    description="Summon the Universal Supreme Council for adversarial multi-persona debate over any strategic proposal, software architecture, pitch, business model, or complex decision.",
)
def court_council(topic: str, domain: str = "general", seats: int = 4, rounds: int = 2) -> str:
    """Run Universal Supreme Council deliberation."""
    allowed, err = check_role_permission("court_council")
    if not allowed:
        return err

    cmd = [
        str(python_executable()),
        str(SCRIPTS / "workshop_council.py"),
        topic,
        "--domain", str(domain),
        "--seats", str(seats),
        "--rounds", str(rounds),
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    return proc.stdout or proc.stderr





@server_decorator.tool(

    name="graphify_query",

    description="Query the codebase AST knowledge graph (graphify) to analyze dependencies, module paths, or architectural flows.",

)

def graphify_query(question: str) -> str:

    """Query AST knowledge graph."""

    allowed, err = check_role_permission("graphify_query")

    if not allowed:

        return err



    proc = subprocess.run(

        [

            str(python_executable()),

            str(SCRIPTS / "workshop.py"),

            "graphify",

            "query",

            question,

        ],

        capture_output=True,

        text=True,

        cwd=str(ROOT),

    )

    return proc.stdout or proc.stderr





# ==============================================================================

# 4. RESOURCES (CANONICAL PROTOCOLS)

# ==============================================================================





@server_decorator.resource("workshop://protocol")

def get_protocol() -> str:

    """Canonical Workshop OS Protocol."""

    proto_file = ROOT / "WORKSHOP_PROTOCOL.md"

    return proto_file.read_text(encoding="utf-8", errors="replace")





@server_decorator.resource("workshop://vault/tasks")

def get_tasks() -> str:

    """Current autonomous task queue and session handoffs."""

    tasks_file = (

        VAULT / "04 - Tasks & Sprints" / "Autonomous Task Queue & Session Handoffs.md"

    )

    if tasks_file.exists():

        return tasks_file.read_text(encoding="utf-8", errors="replace")

    return "Task queue file not found."





# ==============================================================================

# 5. MCP PROMPTS (SLASH COMMANDS)

# ==============================================================================





@server_decorator.prompt(

    name="recon",

    description="Execute stage 1: deep reconnaissance across project AST, specifications, and telemetry.",

)

def prompt_recon(target: str = "project") -> str:

    return f"""Execute rigorous Stage 1 RECON for target: {target}

1. Scan project file tree and AST using `graphify` or direct file inspection.

2. Search relevant domain skills via `skill_search`.

3. Check error post-mortems in `memory_recall` to avoid known pitfalls.

4. State findings and irreducible axioms before drafting code.

"""





@server_decorator.prompt(

    name="plan",

    description="Execute stage 2: draft type-safe architecture, state machines, and verification gates.",

)

def prompt_plan(feature: str) -> str:

    return f"""Draft architecture and execution plan for: {feature}

1. Define invariants, computational complexity, and failure modes.

2. Outline modular file changes and type definitions.

3. Establish deterministic verification criteria for every milestone.

4. Request review with `critique` before modifying files.

"""





@server_decorator.prompt(

    name="verify",

    description="Execute stage 5: deterministic verification and pre-flight quality checks.",

)

def prompt_verify(scope: str = "current-changes") -> str:

    return f"""Run deterministic verification for: {scope}

1. Execute unit and integration tests via `verify`.

2. Run `antislop_audit` to ensure zero AI slop, clichés, or lazy comments.

3. If errors occurred, document the fix in memory via `memory_write(kind='postmortem')`.

"""





@server_decorator.prompt(

    name="handoff",

    description="Prepare a multi-session handoff record to persist progress in the Second Brain.",

)

def prompt_handoff(summary: str) -> str:

    return f"""Synthesize session handoff for: {summary}

1. Detail completed milestones, altered state, and pending next actions.

2. Save directly into the Obsidian Vault using `memory_write(kind='handoff')`.

3. Ensure next session can resume with zero loss of context.

"""





# ==============================================================================

# SERVER ENTRYPOINT

# ==============================================================================



if __name__ == "__main__":
    if server is None:
        print("[!] Error: MCP SDK not installed. Run 'uv pip install mcp' or 'pip install mcp'.", file=sys.stderr)
        sys.exit(1)
    server.run("stdio")
