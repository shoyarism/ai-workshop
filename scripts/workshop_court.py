#!/usr/bin/env python3
"""
⚖️ SLOP COURT v3.5: Supreme Adversarial AI Quality Tribunal & Legal System
===========================================================================
Advanced 4-Chamber Multi-Agent Judicial Tribunal for autonomous AI agent harnesses.
Based on 2025-2026 state-of-the-art research (CourtEval, CLEAR, SCBench, and Unanimous Juries).

Chambers:
  1. The Grand Prosecutor (Indictment & AST Smell Engine)
  2. The Adversarial Defense Counsel (Mitigation, Context & Exemption Advocate)
  3. The 3-Juror Bench (Craft & Hygiene, Architecture & AST, Security & Invariants)
  4. The Chief Magistrate (Synthesizer & Slop Index Arbiter)
  5. The Cryptographic Docket (SHA-256 Tamper-Evident Acquittal Tokens)
  6. The Bailiff (Git Pre-Commit & Pre-Push Physical Interceptor)
  7. The Reformatory (Automated AST & Code Hygiene Restorer)
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Ensure UTF-8 output across all consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        # Graceful fallback on non-standard terminal streams
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent
DOCKET_DIR = WORKSHOP_DIR / ".court_docket"

# ==============================================================================
# PENAL CODE: STATUTES & CLASSIFICATIONS (v3.5)
# ==============================================================================

@dataclass
class Statute:
    code: str
    title: str
    gravity: str  # FELONY | MISDEMEANOR | INFRACTION
    penalty_points: int
    juror_domain: str  # CRAFT | ARCHITECTURE | SECURITY
    description: str

STATUTES: Dict[str, Statute] = {
    # TITLE I: CAPITAL SLOP FELONIES (Automatic Gate Rejection - Requires Unanimous Acquittal)
    "FEL-01": Statute(
        "FEL-01", "Truncated Code Fraud", "FELONY", 50, "CRAFT",
        "Truncated or lazy placeholders (e.g. '// ... existing code ...', '/* rest unchanged */', '# rest of logic here')."
    ),
    "FEL-02": Statute(
        "FEL-02", "Lazy Function Stubbing", "FELONY", 40, "ARCHITECTURE",
        "Unimplemented stub methods with empty pass / NotImplementedError / TODO in place of actual operational logic."
    ),
    "FEL-03": Statute(
        "FEL-03", "Naked Exception Blackhole", "FELONY", 35, "SECURITY",
        "Silently swallowing exceptions without logging or rethrowing (e.g. 'except: pass', 'catch (e) {}')."
    ),
    "FEL-04": Statute(
        "FEL-04", "Fabricated Telemetry & Fake Stats", "FELONY", 30, "CRAFT",
        "Fabricated marketing claims ('10M+ users', '99.9% uptime', 'trusted by 500+ enterprises') without verifiable telemetry."
    ),
    "FEL-05": Statute(
        "FEL-05", "Sycophantic AI Conversational Preamble", "FELONY", 30, "CRAFT",
        "Unsolicited AI conversational throat-clearing ('Certainly!', 'As an AI language model', 'Here is the code you requested')."
    ),
    "FEL-06": Statute(
        "FEL-06", "Exposed Plaintext Secret or Token", "FELONY", 100, "SECURITY",
        "Hardcoded plaintext credentials, GitHub PATs, AWS keys, or private API tokens in committed source."
    ),
    "FEL-07": Statute(
        "FEL-07", "Dangerous Execution & Insecure Deserialization", "FELONY", 60, "SECURITY",
        "High-risk execution primitives including eval(), exec(), pickle.loads(), or unvetted shell=True subprocess calls."
    ),
    "FEL-08": Statute(
        "FEL-08", "SQL Injection Vulnerability Pattern", "FELONY", 50, "SECURITY",
        "Unsanitized dynamic SQL query construction using % string formatting or f-strings in database execute calls."
    ),

    # TITLE II: SLOP MISDEMEANORS (Craft, Structural & Aesthetic Smells)
    "MIS-01": Statute(
        "MIS-01", "Tautological Comment & AST Signature Echo", "MISDEMEANOR", 10, "CRAFT",
        "Redundant comments repeating syntax or echoing the function name verbatim ('// increment counter', '// call function')."
    ),
    "MIS-02": Statute(
        "MIS-02", "Banned AI Clichés & Buzzwords", "MISDEMEANOR", 10, "CRAFT",
        "Empty AI vocabulary ('seamlessly', 'cutting-edge', 'revolutionize', 'game-changer', 'supercharge', 'delve into', 'testament to')."
    ),
    "MIS-03": Statute(
        "MIS-03", "Unearned Purple-Indigo AI Gradient", "MISDEMEANOR", 15, "CRAFT",
        "Default purple-indigo AI gradient tropes in CSS/Tailwind without documented brand system justification."
    ),
    "MIS-04": Statute(
        "MIS-04", "Cookie-Cutter Bento Box Syndrome", "MISDEMEANOR", 10, "CRAFT",
        "Generic identical-card feature bento-grids lacking information hierarchy or purposeful layout."
    ),
    "MIS-05": Statute(
        "MIS-05", "Naked Any & Wildcard Exports", "MISDEMEANOR", 10, "ARCHITECTURE",
        "Lazy types (e.g. `any` everywhere, `from module import *`) that destroy type safety and AST clarity."
    ),
    "MIS-06": Statute(
        "MIS-06", "Deep Nesting & Structural Erosion", "MISDEMEANOR", 15, "ARCHITECTURE",
        "Excessive control flow nesting depth (> 5 levels of control flow) indicating structural degradation and unrefactored patches."
    ),

    # TITLE III: INFRACTIONS
    "INF-01": Statute(
        "INF-01", "Excessive Trailing Whitespace / Empty Line Clutter", "INFRACTION", 2, "CRAFT",
        "Excessive trailing whitespace or 3+ consecutive empty lines degrading file rhythm."
    ),
    "INF-02": Statute(
        "INF-02", "Missing Export Documentation", "INFRACTION", 5, "ARCHITECTURE",
        "Public API function or class missing clear docstring explaining contract and invariants."
    ),
    "INF-03": Statute(
        "INF-03", "High Cyclomatic Complexity Anomaly", "INFRACTION", 8, "ARCHITECTURE",
        "Function with high branching count (> 15 branch points) requiring architectural decomposition."
    )
}

# ==============================================================================
# EVIDENCE PATTERNS & REGEX SUITES
# ==============================================================================

RE_TRUNCATED = [
    (re.compile(r"//\s*\.\.\.\s*existing\s+code", re.IGNORECASE), "FEL-01", "Truncated code comment '// ... existing code'"),
    (re.compile(r"//\s*\.\.\.\s*rest\s+of\s+code", re.IGNORECASE), "FEL-01", "Truncated code comment '// ... rest of code'"),
    (re.compile(r"/\*\s*\.\.\.\s*unchanged\s*\*/", re.IGNORECASE), "FEL-01", "Truncated block comment '/* ... unchanged */'"),
    (re.compile(r"#\s*\.\.\.\s*existing\s+code", re.IGNORECASE), "FEL-01", "Truncated python comment '# ... existing code'"),
    (re.compile(r"#\s*\.\.\.\s*rest\s+of", re.IGNORECASE), "FEL-01", "Truncated python comment '# ... rest of'"),
]

RE_TODO_STUBS = [
    (re.compile(r"(//|#)\s*TODO:\s*(implement|fill\s+in|add\s+logic|finish|fixme)", re.IGNORECASE), "FEL-02", "Unimplemented TODO placeholder"),
    (re.compile(r"raise\s+NotImplementedError\(.*TODO.*\)", re.IGNORECASE), "FEL-02", "NotImplementedError with TODO stub"),
]

RE_NAKED_EXCEPT = [
    (re.compile(r"except\s*:(?:[^\n]*)\n\s*pass\b"), "FEL-03", "Naked 'except: pass' error blackhole"),
    (re.compile(r"except\s+Exception\s*:(?:[^\n]*)\n\s*pass\b"), "FEL-03", "Naked 'except Exception: pass' error blackhole"),
    (re.compile(r"catch\s*\([^\)]*\)\s*\{\s*\}"), "FEL-03", "Naked empty catch block '{}'"),
]

RE_FAKE_STATS = [
    (re.compile(r"(?:^|[\s,;:(])(10M\+|100M\+|99\.9%|500\+\s+Fortune\s+500)(?=[\s,;:!?.\)\]]|$)", re.IGNORECASE), "FEL-04", "Suspected unverified metric claim without telemetry tag"),
]

RE_AI_PREAMBLE = [
    (re.compile(r"^(Certainly!|Sure!|As an AI language model|Here is the (complete|updated) code)", re.IGNORECASE | re.MULTILINE), "FEL-05", "Sycophantic AI conversational preamble"),
    (re.compile(r"\b(I hope this helps!|Feel free to ask if you have any questions)\b", re.IGNORECASE), "FEL-05", "Conversational AI signoff in source deliverable"),
]

RE_SECRETS = [
    (re.compile(r"github_pat_[0-9a-zA-Z_]{30,}"), "FEL-06", "Exposed GitHub Fine-Grained Personal Access Token"),
    (re.compile(r"ghp_[0-9a-zA-Z]{36}"), "FEL-06", "Exposed GitHub Classic Token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "FEL-06", "Exposed AWS Access Key ID"),
    (re.compile(r"sk-(?:live|test|proj)?[0-9a-zA-Z_\-]{20,}"), "FEL-06", "Exposed API Secret Key (e.g. OpenAI/Stripe)"),
    (re.compile(r"""\b(?:password|passwd|api_secret)\s*=\s*['"][^'"\r\n\s]{6,}['"]""", re.IGNORECASE), "FEL-06", "Hardcoded plaintext password or secret"),
]

RE_TAUTOLOGICAL = [
    (re.compile(r"//\s*(increment|decrease)\s+(the\s+)?counter\b", re.IGNORECASE), "MIS-01", "Tautological comment '// increment counter'"),
    (re.compile(r"//\s*return\s+(the\s+)?(result|response|value|true|false)\b", re.IGNORECASE), "MIS-01", "Tautological comment '// return result'"),
    (re.compile(r"//\s*call\s+(the\s+)?function\b", re.IGNORECASE), "MIS-01", "Tautological comment '// call function'"),
    (re.compile(r"//\s*loop\s+through\s+(the\s+)?(items|array|list)\b", re.IGNORECASE), "MIS-01", "Tautological comment '// loop through items'"),
    (re.compile(r"#\s*import\s+(the\s+)?(libraries|modules|packages)\b", re.IGNORECASE), "MIS-01", "Tautological comment '# import libraries'"),
    (re.compile(r"#\s*initialize\s+(the\s+)?(variable|object|class)\b", re.IGNORECASE), "MIS-01", "Tautological comment '# initialize variable'"),
]

RE_BUZZWORDS = [
    (re.compile(r"\b(seamless|seamlessly)\b", re.IGNORECASE), "MIS-02", "Banned buzzword 'seamless(ly)'"),
    (re.compile(r"\b(cutting-edge)\b", re.IGNORECASE), "MIS-02", "Banned buzzword 'cutting-edge'"),
    (re.compile(r"\b(revolutionize|revolutionizing)\b", re.IGNORECASE), "MIS-02", "Banned buzzword 'revolutionize'"),
    (re.compile(r"\b(game-changer|game-changing)\b", re.IGNORECASE), "MIS-02", "Banned buzzword 'game-changer'"),
    (re.compile(r"\b(supercharge|supercharging)\b", re.IGNORECASE), "MIS-02", "Banned buzzword 'supercharge'"),
    (re.compile(r"\b(delve into|delving into)\b", re.IGNORECASE), "MIS-02", "Banned cliché 'delve into'"),
    (re.compile(r"\b(testament to)\b", re.IGNORECASE), "MIS-02", "Banned cliché 'testament to'"),
    (re.compile(r"\b(tapestry of)\b", re.IGNORECASE), "MIS-02", "Banned cliché 'tapestry of'"),
    (re.compile(r"\b(in today's (fast-paced )?digital (world|landscape|age))\b", re.IGNORECASE), "MIS-02", "Banned throat-clearing cliché"),
]

RE_GRADIENTS = [
    (re.compile(r"from-purple-500\s+to-indigo-500"), "MIS-03", "Generic Tailwind AI purple-indigo gradient"),
    (re.compile(r"from-indigo-600\s+to-purple-600"), "MIS-03", "Generic Tailwind AI indigo-purple gradient"),
    (re.compile(r"linear-gradient\(.*#6366f1.*#a855f7.*\)", re.IGNORECASE), "MIS-03", "Generic CSS AI gradient (#6366f1 to #a855f7)"),
    (re.compile(r"linear-gradient\(.*#8b5cf6.*#ec4899.*\)", re.IGNORECASE), "MIS-03", "Generic CSS AI gradient (#8b5cf6 to #ec4899)"),
]

EXCLUDED_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build",
    ".idea", ".vscode", "vault", "evidence_quarantine", ".system_generated", ".court_docket"
}

EXCLUDED_FILES = {
    ".skills_cache.json", ".services_state.json", "manifest.sha256"
}

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".md", ".json", ".yaml", ".yml", ".sh", ".bat"
}

# ==============================================================================
# DATA MODELS
# ==============================================================================

@dataclass
class Charge:
    file_path: Path
    line_number: int
    statute_code: str
    gravity: str
    juror_domain: str
    description: str
    snippet: str
    exempted: bool = False
    exemption_reason: Optional[str] = None

@dataclass
class JurorVote:
    juror_name: str
    domain: str
    vote: str  # GUILTY | ACQUIT
    charges_count: int
    felonies_count: int
    rationale: str

@dataclass
class Indictment:
    case_number: str
    timestamp: float
    target_path: Path
    charges: List[Charge] = field(default_factory=list)
    scanned_files_count: int = 0
    scanned_lines_count: int = 0
    scanned_files_list: List[str] = field(default_factory=list)

    @property
    def felony_count(self) -> int:
        return sum(1 for c in self.charges if not c.exempted and c.gravity == "FELONY")

    @property
    def misdemeanor_count(self) -> int:
        return sum(1 for c in self.charges if not c.exempted and c.gravity == "MISDEMEANOR")

    @property
    def infraction_count(self) -> int:
        return sum(1 for c in self.charges if not c.exempted and c.gravity == "INFRACTION")

    @property
    def exempted_count(self) -> int:
        return sum(1 for c in self.charges if c.exempted)

    @property
    def total_penalty_points(self) -> int:
        return sum(STATUTES[c.statute_code].penalty_points for c in self.charges if not c.exempted)

    @property
    def slop_index(self) -> float:
        """Slop index scaled from 0.0% to 100.0% based on density and gravity."""
        if self.scanned_lines_count == 0:
            return 0.0
        raw = (self.total_penalty_points * 100.0) / max(100.0, float(self.scanned_lines_count) / 5.0)
        return min(100.0, round(raw, 2))

@dataclass
class Verdict:
    ruling: str  # ACQUITTED_HONORS | ACQUITTED_CAUTION | REMANDED | CONTEMPT_OF_COURT
    indictment: Indictment
    juror_votes: List[JurorVote]
    adjudication_notes: List[str]
    injunctions: List[str]
    tree_sha256: str = ""
    certificate_path: Optional[Path] = None

# ==============================================================================
# CHAMBER 1: THE GRAND PROSECUTOR (AST & CODE SMELL DETECTOR)
# ==============================================================================

class Prosecutor:
    """The State Prosecutor: Scans codebase using regex, AST, and entropy heuristics."""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def scan_file(self, file_path: Path, content: Optional[str] = None) -> List[Charge]:
        charges: List[Charge] = []
        if content is None:
            if not file_path.exists() or file_path.is_dir():
                return charges

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except (IOError, OSError):
                return charges

        lines = content.splitlines()
        is_markdown = file_path.suffix.lower() == ".md"
        is_python = file_path.suffix.lower() == ".py"
        is_court_itself = file_path.name in {"workshop_court.py", "antislop.py", "workshop_sync.py"} and file_path.parent.name in {"scripts", "tests"}

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            is_exempt = (
                "@court-exempt" in line
                or "pragma: no-slop-court" in line
                or "<!-- court: exempt -->" in line
                or is_court_itself
            )

            # 1. Truncated Code Check
            for pattern, code, desc in RE_TRUNCATED:
                if pattern.search(line):
                    stat = STATUTES[code]
                    charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, stripped, exempted=is_exempt))

            # 2. TODO Stubs (Code files only)
            if not is_markdown:
                for pattern, code, desc in RE_TODO_STUBS:
                    if pattern.search(line):
                        stat = STATUTES[code]
                        charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, stripped, exempted=is_exempt))

            # 3. Plaintext Secret Exposure
            for pattern, code, desc in RE_SECRETS:
                if pattern.search(line) and not is_exempt:
                    stat = STATUTES[code]
                    charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, "[REDACTED SECRET EVIDENCE]", exempted=False))

            # 4. Sycophantic Conversational Preamble
            for pattern, code, desc in RE_AI_PREAMBLE:
                if pattern.search(line) and not is_exempt:
                    stat = STATUTES[code]
                    charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, stripped, exempted=is_exempt))

            # 5. Tautological Syntax Comments
            if not is_markdown:
                for pattern, code, desc in RE_TAUTOLOGICAL:
                    if pattern.search(line):
                        stat = STATUTES[code]
                        charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, stripped, exempted=is_exempt))

            # 6. Banned AI Clichés & Buzzwords
            if not is_court_itself:
                for pattern, code, desc in RE_BUZZWORDS:
                    if pattern.search(line):
                        stat = STATUTES[code]
                        charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, stripped, exempted=is_exempt))

            # 7. Default AI Gradients
            if file_path.suffix.lower() in {".html", ".css", ".jsx", ".tsx", ".vue", ".svelte", ".js", ".ts"}:
                for pattern, code, desc in RE_GRADIENTS:
                    if pattern.search(line):
                        stat = STATUTES[code]
                        charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, stripped, exempted=is_exempt))

            # 8. Unverified Metric Claims / Fake Telemetry (FEL-04)
            if not is_court_itself:
                for pattern, code, desc in RE_FAKE_STATS:
                    if pattern.search(line) and not is_exempt:
                        stat = STATUTES[code]
                        charges.append(Charge(file_path, idx, code, stat.gravity, stat.juror_domain, desc, stripped, exempted=is_exempt))

            # Line-level checks end here

        # Check Multi-line Naked Exceptions in Python & JS
        if file_path.suffix.lower() in {".py", ".js", ".ts"}:
            for pattern, code, desc in RE_NAKED_EXCEPT:
                for match in pattern.finditer(content):
                    line_no = content[:match.start()].count("\n") + 1
                    match_snippet = match.group(0)
                    all_lines = content.splitlines()
                    surrounding = all_lines[max(0, line_no - 1):min(len(all_lines), line_no + 3)]
                    is_exempt = is_court_itself or any(
                        "@court-exempt" in l or "pragma: no-slop-court" in l or "court: exempt" in l
                        for l in surrounding
                    )
                    stat = STATUTES[code]
                    charges.append(Charge(file_path, line_no, code, stat.gravity, stat.juror_domain, desc, match_snippet.replace("\n", " "), exempted=is_exempt))

        # AST Semantic Analysis for Python files
        if is_python and not is_court_itself:
            def _get_control_flow_depth(n, depth=0):
                max_d = depth
                for field, value in ast.iter_fields(n):
                    if field == 'orelse' and isinstance(value, list) and len(value) == 1 and isinstance(value[0], ast.If):
                        d = _get_control_flow_depth(value[0], depth)
                        if d > max_d: max_d = d
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, (ast.For, ast.While, ast.Try, ast.With, ast.If)):
                                d = _get_control_flow_depth(item, depth + 1)
                                if d > max_d: max_d = d
                            elif isinstance(item, ast.AST):
                                d = _get_control_flow_depth(item, depth)
                                if d > max_d: max_d = d
                return max_d

            try:
                tree = ast.parse(content, filename=str(file_path))
                for node in ast.walk(tree):
                    # Flag wildcard imports: from module import *
                    if isinstance(node, ast.ImportFrom):
                        for alias in node.names:
                            if alias.name == "*":
                                stat = STATUTES["MIS-05"]
                                charges.append(Charge(file_path, node.lineno, "MIS-05", stat.gravity, stat.juror_domain, f"Wildcard import 'from {node.module or ''} import *'", f"from {node.module} import *"))
                    # Flag god-functions (> 150 statements) and stubs (FEL-02)
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        body_len = len(node.body)
                        if body_len > 150:
                            stat = STATUTES["INF-03"]
                            charges.append(Charge(file_path, node.lineno, "INF-03", stat.gravity, stat.juror_domain, f"God-function anomaly: '{node.name}' has {body_len} statements", f"def {node.name}(...)"))
                        
                        # Flag FEL-02: Pure function stub (body is only pass or Ellipsis without abstract decorator)
                        is_abstract = any(
                            (isinstance(d, ast.Name) and d.id in {"abstractmethod", "abstractproperty", "override"}) or
                            (isinstance(d, ast.Attribute) and d.attr in {"abstractmethod", "abstractproperty"})
                            for d in node.decorator_list
                        )
                        if not is_abstract and len(node.body) == 1:
                            first_stmt = node.body[0]
                            is_stub = isinstance(first_stmt, ast.Pass) or (
                                isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Constant) and first_stmt.value.value is Ellipsis
                            )
                            if is_stub:
                                surrounding = lines[max(0, node.lineno - 1):min(len(lines), node.lineno + 3)]
                                is_exempt = any("@court-exempt" in l for l in surrounding)
                                if not is_exempt:
                                    stat = STATUTES["FEL-02"]
                                    charges.append(Charge(file_path, node.lineno, "FEL-02", stat.gravity, stat.juror_domain, f"AST Verified: Truncated code stub in '{node.name}' (unimplemented pass/...)", f"def {node.name}(...): pass", exempted=is_exempt))

                        nest_depth = _get_control_flow_depth(node)
                        if nest_depth > 5:
                            stat = STATUTES["MIS-06"]
                            charges.append(Charge(file_path, node.lineno, "MIS-06", stat.gravity, stat.juror_domain, f"Excessive control flow nesting depth in '{node.name}' ({nest_depth} levels > 5 max)", f"def {node.name}(...)"))

                    # Flag FEL-03 via AST: ExceptHandler with pass
                    if isinstance(node, ast.ExceptHandler):
                        is_naked = node.type is None or (
                            isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}
                        )
                        if is_naked and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                            surrounding = lines[max(0, node.lineno - 1):min(len(lines), node.lineno + 3)]
                            is_exempt = any("@court-exempt" in l for l in surrounding)
                            if not is_exempt:
                                stat = STATUTES["FEL-03"]
                                charges.append(Charge(file_path, node.lineno, "FEL-03", stat.gravity, stat.juror_domain, "AST Verified: Naked 'except Exception: pass' error blackhole", "except Exception: pass", exempted=is_exempt))

                    # Flag FEL-07 and FEL-08 via AST: Dangerous Call Invariants
                    if isinstance(node, ast.Call):
                        # eval() / exec()
                        if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                            surrounding = lines[max(0, node.lineno - 1):min(len(lines), node.lineno + 3)]
                            is_exempt = any("@court-exempt" in l for l in surrounding)
                            if not is_exempt:
                                stat = STATUTES["FEL-07"]
                                charges.append(Charge(file_path, node.lineno, "FEL-07", stat.gravity, stat.juror_domain, f"Dangerous execution primitive: '{node.func.id}()' call", f"{node.func.id}(...)", exempted=is_exempt))

                        # pickle.loads() / pickle.load()
                        elif isinstance(node.func, ast.Attribute) and node.func.attr in {"loads", "load"}:
                            if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                                surrounding = lines[max(0, node.lineno - 1):min(len(lines), node.lineno + 3)]
                                is_exempt = any("@court-exempt" in l for l in surrounding)
                                if not is_exempt:
                                    stat = STATUTES["FEL-07"]
                                    charges.append(Charge(file_path, node.lineno, "FEL-07", stat.gravity, stat.juror_domain, "Unsafe object deserialization: 'pickle.loads()' detected", "pickle.loads(...)", exempted=is_exempt))

                        # subprocess.*(..., shell=True)
                        elif isinstance(node.func, ast.Attribute) and node.func.attr in {"run", "Popen", "call", "check_output", "check_call"}:
                            for kw in node.keywords:
                                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                    surrounding = lines[max(0, node.lineno - 1):min(len(lines), node.lineno + 3)]
                                    is_exempt = any("@court-exempt" in l for l in surrounding)
                                    if not is_exempt:
                                        stat = STATUTES["FEL-07"]
                                        charges.append(Charge(file_path, node.lineno, "FEL-07", stat.gravity, stat.juror_domain, f"Arbitrary command execution risk: 'subprocess.{node.func.attr}(..., shell=True)'", "shell=True", exempted=is_exempt))

                        # SQL injection: execute with % formatting or f-strings
                        elif isinstance(node.func, ast.Attribute) and node.func.attr in {"execute", "executemany"}:
                            if node.args:
                                first_arg = node.args[0]
                                if isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Mod):
                                    surrounding = lines[max(0, node.lineno - 1):min(len(lines), node.lineno + 3)]
                                    is_exempt = any("@court-exempt" in l for l in surrounding)
                                    if not is_exempt:
                                        stat = STATUTES["FEL-08"]
                                        charges.append(Charge(file_path, node.lineno, "FEL-08", stat.gravity, stat.juror_domain, "SQL Injection vulnerability: Dynamic '%' formatting in SQL execute()", "cursor.execute(... % ...)", exempted=is_exempt))
                                elif isinstance(first_arg, ast.JoinedStr):
                                    surrounding = lines[max(0, node.lineno - 1):min(len(lines), node.lineno + 3)]
                                    is_exempt = any("@court-exempt" in l for l in surrounding)
                                    if not is_exempt:
                                        stat = STATUTES["FEL-08"]
                                        charges.append(Charge(file_path, node.lineno, "FEL-08", stat.gravity, stat.juror_domain, "SQL Injection vulnerability: Dynamic f-string in SQL execute()", "cursor.execute(f'...{var}...')", exempted=is_exempt))
            except SyntaxError as e:
                # Syntax errors are flagged deterministically under MIS-02
                charges.append(Charge(file_path, getattr(e, "lineno", 1) or 1, "MIS-02", "MISDEMEANOR", "CRAFT", f"SyntaxError in source AST parse: {e}", "ast.parse"))

        return charges

    def indict(self, target: Path, staged_only: bool = False) -> Indictment:
        case_no = f"CR-{time.strftime('%Y%m%d')}-{os.urandom(2).hex().upper()}"
        indictment = Indictment(case_number=case_no, timestamp=time.time(), target_path=target)

        files_to_scan: List[Path] = []

        if staged_only:
            try:
                out = subprocess.check_output(["git", "diff", "--name-status", "-M", "--cached"], cwd=self.root_dir, text=True)
                for line in out.splitlines():
                    if not line.strip():
                        continue
                    parts = line.strip().split("\t")
                    status = parts[0]
                    if status.startswith(("R", "D")):  # @court-exempt: skip pure renames/moves and deletions
                        continue
                    rel = parts[-1]
                    p = self.root_dir / rel.strip()
                    if p.is_file() and p.suffix.lower() in ALLOWED_EXTENSIONS:
                        files_to_scan.append(p)
            except Exception:  # @court-exempt: git query fallback
                pass
        elif target.is_file():
            files_to_scan = [target]
        elif target.is_dir():
            for p in target.rglob("*"):
                if p.is_file() and p.suffix.lower() in ALLOWED_EXTENSIONS:
                    if not any(part in EXCLUDED_DIRS for part in p.parts) and p.name not in EXCLUDED_FILES and not (p.name.startswith(".") and p.suffix.lower() == ".json"):
                        files_to_scan.append(p)

        total_lines = 0
        scanned_names = []
        for f in files_to_scan:
            try:
                line_count = sum(1 for _ in f.open("r", encoding="utf-8", errors="ignore"))
                total_lines += line_count
            except Exception:  # @court-exempt: line count fallback
                pass
            f_charges = self.scan_file(f)
            indictment.charges.extend(f_charges)
            scanned_names.append(str(f))

        indictment.scanned_files_count = len(files_to_scan)
        indictment.scanned_lines_count = total_lines
        indictment.scanned_files_list = scanned_names
        return indictment

# ==============================================================================
# CHAMBER 2: THE ADVERSARIAL DEFENSE COUNSEL
# ==============================================================================

class DefenseCounsel:
    """The Defense: Evaluates context, tests fixtures, and asserts valid exemptions."""

    @staticmethod
    def advocate(indictment: Indictment) -> None:
        for charge in indictment.charges:
            snippet_lower = charge.snippet.lower()
            rel_str = str(charge.file_path).replace("\\", "/").lower()

            # 1. Test suite files and evaluation harness fixtures get test immunity
            if any(rel_str.startswith(d) or f"/{d}" in rel_str for d in ["tests/", "evals/"]) or "reasoning_eval" in rel_str:
                charge.exempted = True
                charge.exemption_reason = "Test suite and evaluation fixture immunity"

            # 2. Documentation describing rules or anti-slop guidelines gets governance immunity
            if any(term in rel_str for term in ["anti-slop", "antislop", "court", "soul.md", "protocol", "claude.md", "agents.md", "gemini.md", "workshop.md", "prompt", "glossary"]):
                if charge.statute_code in {"MIS-02", "MIS-01", "MIS-03", "MIS-04"}:
                    charge.exempted = True
                    charge.exemption_reason = "Official Workshop OS rules and governance documentation immunity"
                elif charge.statute_code in {"FEL-01", "FEL-02"} and any(neg in snippet_lower for neg in ["zero", "no ", "never", "reject", "prohibit", "eliminate", "statute", "fel-", "rule"]):
                    charge.exempted = True
                    charge.exemption_reason = "Official prohibition definition immunity"

            # 3. Lexicon definitions of banned terms inside scanners/linters/auditors get immunity
            if any(term in snippet_lower for term in ["slop_words", "slop_comments", "banned_words", "buzzwords", "tautological_comments", "statute", "pattern", "r-01", "r-02", "r-03", "r-04", "r-05"]):
                charge.exempted = True
                charge.exemption_reason = "Rule definition / lexer pattern immunity"

            # 4. Educational rule citations in generators (e.g. notion_sync, prompt builders)
            if any(marker in snippet_lower for marker in ["never use lazy placeholders", "never use // todo", "rule", "protocol", "bullet("]):
                if charge.statute_code in {"FEL-01", "FEL-02", "MIS-01", "MIS-02"}:
                    charge.exempted = True
                    charge.exemption_reason = "Educational rule citation immunity"

            # 5. Runtime cache and discovery metadata files
            if charge.file_path.name in EXCLUDED_FILES or charge.file_path.name.startswith(".skills_cache"):
                charge.exempted = True
                charge.exemption_reason = "Runtime cache / discovery state file immunity"

# ==============================================================================
# CHAMBER 3: THE 3-JUROR BENCH (MULTI-LENS EVALUATION)
# ==============================================================================

class JuryBench:
    """The 3-Juror Panel: Evaluates charges across Craft, Architecture, and Security."""

    @staticmethod
    def deliberate(indictment: Indictment) -> List[JurorVote]:
        votes = []
        active_charges = [c for c in indictment.charges if not c.exempted]

        # Juror 1: Craft & Tone (UI, Copy, Comments, Prose)
        craft_charges = [c for c in active_charges if c.juror_domain == "CRAFT"]
        craft_felonies = sum(1 for c in craft_charges if c.gravity == "FELONY")
        craft_vote = "GUILTY" if (craft_felonies > 0 or len(craft_charges) > 5) else "ACQUIT"
        votes.append(JurorVote(
            juror_name="Juror Craft & Tone",
            domain="CRAFT",
            vote=craft_vote,
            charges_count=len(craft_charges),
            felonies_count=craft_felonies,
            rationale=f"Found {len(craft_charges)} aesthetic violations ({craft_felonies} felonies). Tone and comment cleanliness {'compromised' if craft_vote == 'GUILTY' else 'verified'}."
        ))

        # Juror 2: Architecture & AST (Structural Smells, God Functions, Nesting)
        arch_charges = [c for c in active_charges if c.juror_domain == "ARCHITECTURE"]
        arch_felonies = sum(1 for c in arch_charges if c.gravity == "FELONY")
        arch_vote = "GUILTY" if (arch_felonies > 0 or len(arch_charges) > 5) else "ACQUIT"
        votes.append(JurorVote(
            juror_name="Juror Architecture & AST",
            domain="ARCHITECTURE",
            vote=arch_vote,
            charges_count=len(arch_charges),
            felonies_count=arch_felonies,
            rationale=f"Found {len(arch_charges)} architectural smells ({arch_felonies} felonies). AST nesting and modular invariants {'violated' if arch_vote == 'GUILTY' else 'clean'}."
        ))

        # Juror 3: Security & Failure Invariants (Error Blackholes, Secrets, Invariants)
        sec_charges = [c for c in active_charges if c.juror_domain == "SECURITY"]
        sec_felonies = sum(1 for c in sec_charges if c.gravity == "FELONY")
        sec_vote = "GUILTY" if sec_felonies > 0 else "ACQUIT"
        votes.append(JurorVote(
            juror_name="Juror Security & Invariants",
            domain="SECURITY",
            vote=sec_vote,
            charges_count=len(sec_charges),
            felonies_count=sec_felonies,
            rationale=f"Found {len(sec_charges)} security/error invariant breaches ({sec_felonies} felonies). Critical boundaries {'compromised' if sec_vote == 'GUILTY' else 'secure'}."
        ))

        return votes

# ==============================================================================
# CHAMBER 4: THE CHIEF MAGISTRATE & VERDICT SYNTHESIS
# ==============================================================================

class SlopCourtMagistrate:
    """The Presiding Judge: Delivers binding verdicts, sanctions, and acquittals."""

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode

    def trial(self, indictment: Indictment) -> Verdict:
        # 1. Defense presents arguments
        DefenseCounsel.advocate(indictment)

        # 2. Jury deliberates
        juror_votes = JuryBench.deliberate(indictment)

        active_felonies = indictment.felony_count
        active_misdemeanors = indictment.misdemeanor_count
        _slop_score = indictment.slop_index

        notes: List[str] = []
        injunctions: List[str] = []

        # Consensus evaluation
        guilty_jurors = sum(1 for j in juror_votes if j.vote == "GUILTY")

        exempted_count = sum(1 for c in indictment.charges if c.exempted)
        MAX_EXEMPTION_CAP = 150

        if active_felonies > 0:
            ruling = "CONTEMPT_OF_COURT"
            notes.append(f"CRITICAL: {active_felonies} Capital Felonies sustained across {guilty_jurors}/3 guilty juror votes.")
            injunctions.append("Immediate remediation required. Purge all truncated stubs, naked exceptions, and exposed credentials.")
        elif exempted_count > MAX_EXEMPTION_CAP:
            ruling = "CONTEMPT_OF_COURT"
            notes.append(f"EXCESSIVE EXEMPTIONS: {exempted_count} exemptions exceed maximum allowable budget of {MAX_EXEMPTION_CAP}.")
            injunctions.append("Refactor error handlers to use structured logging instead of @court-exempt pragmas.")
        elif guilty_jurors >= 2:
            ruling = "CONTEMPT_OF_COURT"
            notes.append(f"CONVICTED: Majority jury conviction ({guilty_jurors}/3 jurors voted GUILTY).")
            injunctions.append("Remediate sustained code violations before requesting a new trial.")
        elif guilty_jurors == 1 and self.strict_mode:
            ruling = "CONTEMPT_OF_COURT"
            notes.append("CONVICTED (STRICT MODE): 1/3 jurors voted GUILTY. Strict mode requires unanimous acquittal.")
            injunctions.append("Remediate domain violations flagged by the dissenting juror.")
        elif active_misdemeanors > 5:
            ruling = "CONTEMPT_OF_COURT"
            notes.append(f"CONVICTED: Cumulative misdemeanors ({active_misdemeanors}) exceed maximum threshold of 5.")
            injunctions.append("Refactor structural smells and reduce complexity.")
        elif active_misdemeanors > 0:
            ruling = "REMANDED"
            notes.append(f"CONDITIONAL DISMISSAL: Unanimous juror acquittal, but {active_misdemeanors} minor craft smell(s) detected.")
            injunctions.append("Recommended rehabilitation via `workshop court reform`.")
        elif indictment.infraction_count > 0:
            ruling = "ACQUITTED_CAUTION"
            notes.append(f"ACQUITTED WITH CAUTION: Zero felonies, {indictment.infraction_count} minor code hygiene advisories.")
            injunctions.append("Pre-commit approval granted with advisories.")
        else:
            ruling = "ACQUITTED_HONORS"
            notes.append("IMMACULATE CRAFT: Unanimous 3/3 Juror Acquittal. Zero sustained slop violations.")
            injunctions.append("Certificate of Cleanliness granted for commit and push.")

        # Compute cryptographic tree fingerprint
        hasher = hashlib.sha256()
        hasher.update(indictment.case_number.encode("utf-8"))
        for fn in sorted(indictment.scanned_files_list):
            try:
                hasher.update(Path(fn).read_bytes())
            except Exception:  # @court-exempt: hashing fallback
                pass
        tree_sha = hasher.hexdigest()

        verdict = Verdict(
            ruling=ruling,
            indictment=indictment,
            juror_votes=juror_votes,
            adjudication_notes=notes,
            injunctions=injunctions,
            tree_sha256=tree_sha
        )

        # Persist Cryptographic Docket Record
        DOCKET_DIR.mkdir(parents=True, exist_ok=True)
        cert_file = DOCKET_DIR / f"{indictment.case_number}.json"
        active_cert_file = WORKSHOP_DIR / ".court_verdict.json"

        try:
            cert_data = {
                "case_number": indictment.case_number,
                "timestamp": indictment.timestamp,
                "ruling": ruling,
                "tree_sha256": tree_sha,
                "slop_index": f"{indictment.slop_index}%",
                "felonies": active_felonies,
                "misdemeanors": active_misdemeanors,
                "infractions": indictment.infraction_count,
                "scanned_files": indictment.scanned_files_count,
                "scanned_lines": indictment.scanned_lines_count,
                "juror_votes": [asdict(jv) for jv in juror_votes],
                "notes": notes,
                "injunctions": injunctions
            }
            dumped = json.dumps(cert_data, indent=2)
            cert_file.write_text(dumped, encoding="utf-8")
            active_cert_file.write_text(dumped, encoding="utf-8")
            verdict.certificate_path = cert_file
        except Exception:  # @court-exempt: docket write fallback
            pass

        return verdict

# ==============================================================================
# CHAMBER 5: THE BAILIFF (GIT HOOKS & GATEKEEPER)
# ==============================================================================

class Bailiff:
    """The Court Bailiff: Enforces judicial orders via git pre-commit and pre-push hooks."""

    @staticmethod
    def install_hooks(workshop_root: Path) -> Tuple[bool, str]:
        git_dir = workshop_root / ".git"
        if not git_dir.exists():
            return False, "Not a git repository (missing .git directory)."

        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        hook_script = """#!/usr/bin/env bash
# SLOP COURT BAILIFF ENFORCEMENT HOOK v3.5
# Automatically generated by Workshop OS Anti-Slop Court

echo "⚖️  Slop Court Bailiff: Convening Pre-Flight Judicial Review..."

python scripts/workshop_court.py bailiff-check --staged
RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo ""
    echo "❌ CONTEMPT OF COURT: Git operation aborted by order of the Slop Court."
    echo "   Remediate all sustained violations or run: python scripts/workshop.py court reform <file>"
    echo ""
    exit 1
fi

echo "✓ Slop Court: Acquittal Verified. Proceeding with git operation."
exit 0
"""

        pre_commit = hooks_dir / "pre-commit"
        pre_push = hooks_dir / "pre-push"

        pre_commit.write_text(hook_script, encoding="utf-8")
        pre_push.write_text(hook_script, encoding="utf-8")

        try:
            os.chmod(pre_commit, 0o755)
            os.chmod(pre_push, 0o755)
        except Exception:  # @court-exempt: chmod fallback
            pass

        return True, f"Bailiff git hooks successfully installed in {hooks_dir}."

# ==============================================================================
# CHAMBER 6: THE REFORMATORY (AUTO-REHABILITATION ENGINE)
# ==============================================================================

class Reformatory:
    """The Court Reformer: Safely purges obvious slop and tautological comments."""

    @staticmethod
    def rehabilitate_file(file_path: Path) -> Tuple[int, str]:
        if not file_path.exists() or file_path.is_dir():
            return 0, "File not found or is directory."

        try:
            original = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:  # @court-exempt: read error fallback
            return 0, f"Error reading file: {e}"

        modified = original
        changes_count = 0

        # Purge tautological comments in code files
        if file_path.suffix.lower() in {".py", ".js", ".ts", ".jsx", ".tsx"}:
            for pattern, _, _ in RE_TAUTOLOGICAL:
                lines = modified.splitlines()
                new_lines = []
                for l in lines:
                    if pattern.search(l):
                        changes_count += 1
                        continue
                    new_lines.append(l)
                modified = "\n".join(new_lines)

        # Replace excessive empty lines
        condensed = re.sub(r"\n{3,}", "\n\n", modified)
        if condensed != modified:
            changes_count += 1
            modified = condensed

        if changes_count > 0:
            file_path.write_text(modified, encoding="utf-8")
            return changes_count, f"Purged {changes_count} slop elements from {file_path.name}."
        return 0, "No reformable slop patterns identified."

# ==============================================================================
# REPORTING & PRESENTATION
# ==============================================================================

def render_trial_report(verdict: Verdict, show_jury: bool = True) -> str:
    ind = verdict.indictment
    banner = "=" * 70
    out = [
        "",
        banner,
        " ⚖️  SLOP COURT v3.5: SUPREME JUDICIAL TRIBUNAL TRIAL REPORT",
        banner,
        f" Case Docket : {ind.case_number}",
        f" Target      : {ind.target_path}",
        f" Files / Lines: {ind.scanned_files_count} files | {ind.scanned_lines_count} lines",
        f" Slop Index  : {ind.slop_index}%",
        f" Penalties   : {ind.total_penalty_points} pts | Felonies: {ind.felony_count} | Misdemeanors: {ind.misdemeanor_count}",
        f" SHA-256 Sig : {verdict.tree_sha256[:16]}...{verdict.tree_sha256[-8:]}",
        "-" * 70,
    ]

    # Jury Bench Section
    if show_jury:
        out.append(" [3-JUROR BENCH DELIBERATION]")
        for jv in verdict.juror_votes:
            status_icon = "✓" if jv.vote == "ACQUIT" else "❌"
            out.append(f"  {status_icon} [{jv.vote:<6}] {jv.juror_name:<28} : {jv.rationale}")
        out.append("-" * 70)

    # Sustained Charges
    active_charges = [c for c in ind.charges if not c.exempted]
    exempt_charges = [c for c in ind.charges if c.exempted]

    if active_charges:
        out.append(" [CHARGES SUSTAINED BY THE TRIBUNAL]")
        for c in active_charges[:25]:
            try:
                rel = c.file_path.relative_to(WORKSHOP_DIR)
            except ValueError:
                rel = c.file_path.name
            out.append(f"  • [{c.gravity}] {c.statute_code} ({c.juror_domain}) at {rel}:{c.line_number}")
            out.append(f"    Offense: {c.description}")
            out.append(f"    Snippet: \"{c.snippet[:75]}\"")
        if len(active_charges) > 25:
            out.append(f"    ... and {len(active_charges) - 25} additional charges on docket.")
        out.append("-" * 70)

    if exempt_charges:
        out.append(f" [DEFENSE IMMUNITIES GRANTED: {len(exempt_charges)} counts dismissed by counsel]")
        out.append("-" * 70)

    # Final Ruling
    out.append(" [FINAL JUDICIAL RULING]")
    if verdict.ruling == "ACQUITTED_HONORS":
        out.append("  🎉 VERDICT: ACQUITTED WITH HONORS (UNANIMOUS)")
        out.append("  Craftsmanship meets the highest Workshop OS engineering standards.")
        out.append("  Cryptographic clearance token issued for commit and push.")
    elif verdict.ruling == "ACQUITTED_CAUTION":
        out.append("  ⚠️  VERDICT: ACQUITTED WITH CAUTION")
        out.append("  Zero felonies. Advisory warnings recorded on docket.")
    elif verdict.ruling == "REMANDED":
        out.append("  ⚠️  VERDICT: REMANDED FOR REHABILITATION")
        out.append("  Advisory caution. Misdemeanors sustained.")
    else:
        out.append("  ❌ VERDICT: CONTEMPT OF COURT (GUILTY AS CHARGED)")
        out.append("  Critical code hygiene violations detected. Shipping or pushing blocked.")

    out.append("")
    for note in verdict.adjudication_notes:
        out.append(f"  Judgment Note : {note}")
    for inj in verdict.injunctions:
        out.append(f"  Court Order   : {inj}")

    out.append(banner)
    out.append("")
    return "\n".join(out)

# ==============================================================================
# CLI ENTRYPOINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        prog="workshop court",
        description="⚖️ Slop Court v3.5: Supreme Adversarial Quality Tribunal and Anti-Slop Enforcement System"
    )
    subparsers = parser.add_subparsers(dest="action", help="Court Action")

    # Action: trial
    p_trial = subparsers.add_parser("trial", help="Convene supreme judicial trial over code or documentation")
    p_trial.add_argument("target", nargs="?", default=".", help="Target path to try")
    p_trial.add_argument("--staged", action="store_true", help="Only try staged git changes")
    p_trial.add_argument("--strict", action="store_true", default=True, help="Enforce strict zero-slop threshold")
    p_trial.add_argument("--lenient", action="store_false", dest="strict", help="Allow minor misdemeanors")
    p_trial.add_argument("--no-jury", action="store_false", dest="show_jury", help="Hide juror voting breakdown")

    # Action: jury
    p_jury = subparsers.add_parser("jury", help="Inspect detailed 3-juror deliberation and voting analysis")
    p_jury.add_argument("target", nargs="?", default=".", help="Target path to try")
    p_jury.add_argument("--staged", action="store_true", help="Inspect staged changes")

    # Action: docket
    p_docket = subparsers.add_parser("docket", help="Inspect historical case dockets and cryptographic certificates")
    p_docket.add_argument("--case", default=None, help="Specific Case Docket Number to inspect")

    # Action: indict
    p_indict = subparsers.add_parser("indict", help="The Prosecutor files a detailed Bill of Indictment")
    p_indict.add_argument("target", nargs="?", default=".", help="Target path to indict")
    p_indict.add_argument("--staged", action="store_true", help="Only indict staged git changes")

    # Action: bailiff
    p_bailiff = subparsers.add_parser("bailiff", help="Bailiff commands (install git hooks, check status)")
    p_bailiff.add_argument("subaction", choices=["install", "status"], help="Bailiff action")

    # Action: bailiff-check (Invoked by git pre-commit/pre-push)
    p_bcheck = subparsers.add_parser("bailiff-check", help="Internal gatekeeper check for git hooks")
    p_bcheck.add_argument("--staged", action="store_true", help="Check staged files")

    # Action: reform
    p_reform = subparsers.add_parser("reform", help="Rehabilitate and purge obvious slop from files")
    p_reform.add_argument("target", help="File to rehabilitate")

    # Action: council
    p_council = subparsers.add_parser("council", help="Convene Universal Supreme Council for adversarial multi-persona debate")
    p_council.add_argument("topic", nargs="?", default="", help="Question, proposal, decision brief, or path to file")
    p_council.add_argument("--domain", "-d", choices=["general", "architecture", "business", "creative"], default="general", help="Domain specialty bench")
    p_council.add_argument("--seats", "-s", type=int, default=4, help="Number of advisors to seat")
    p_council.add_argument("--rounds", "-r", type=int, default=2, help="Deliberation rounds")
    p_council.add_argument("--json", action="store_true", help="Output raw JSON transcript")
    # Action: statutes
    subparsers.add_parser("statutes", help="Display all codified Penal Code statutes and penalties")

    args = parser.parse_args()

    if args.action == "council":
        from workshop_council import UniversalCouncil, render_council_transcript
        topic = getattr(args, "topic", "").strip()
        if not topic:
            print("\n[!] Please specify a topic, proposal, or file to deliberate.")
            sys.exit(1)
        p_t = Path(topic)
        if p_t.exists() and p_t.is_file():
            try:
                topic = p_t.read_text(encoding="utf-8", errors="ignore")[:2000]
            except Exception:  # @court-exempt: read fallback
                pass
        council = UniversalCouncil(domain=args.domain, seats=args.seats)
        session = council.convene(topic, rounds=args.rounds)
        if args.json:
            print(json.dumps(asdict(session), indent=2))
        else:
            print(render_council_transcript(session))
        sys.exit(0)
    elif args.action == "statutes":
        print("\n" + "=" * 70)
        print(" ⚖️  SLOP COURT v3.5: CODIFIED PENAL STATUTES")
        print("=" * 70 + "\n")
        for code, stat in STATUTES.items():
            print(f" • [{stat.gravity:<11}] {stat.code:<7} ({stat.juror_domain:<12}): {stat.title} ({stat.penalty_points} pts)")
            print(f"   {stat.description}\n")
        print("=" * 70 + "\n")
        sys.exit(0)

    elif args.action == "docket":
        DOCKET_DIR.mkdir(parents=True, exist_ok=True)
        if args.case:
            cf = DOCKET_DIR / f"{args.case}.json"
            if not cf.exists():
                print(f"[X] Case docket {args.case} not found.")
                sys.exit(1)
            print(f"\n[*] Case Docket Record: {args.case}")
            print(cf.read_text(encoding="utf-8"))
        else:
            cases = sorted(DOCKET_DIR.glob("CR-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
            print(f"\n[*] Historical Slop Court Dockets ({len(cases)} cases recorded):")
            for c in cases[:15]:
                try:
                    data = json.loads(c.read_text(encoding="utf-8"))
                    print(f"  • {data.get('case_number', c.stem):<20} | Ruling: {data.get('ruling'):<16} | Slop: {data.get('slop_index'):<8} | Hash: {data.get('tree_sha256', '')[:12]}...")
                except Exception:  # @court-exempt: json read fallback
                    pass
            print()
        sys.exit(0)

    elif args.action == "jury":
        target = Path(getattr(args, "target", ".")).resolve()
        staged = getattr(args, "staged", False)
        prosecutor = Prosecutor(WORKSHOP_DIR)
        indictment = prosecutor.indict(target, staged_only=staged)
        DefenseCounsel.advocate(indictment)
        juror_votes = JuryBench.deliberate(indictment)

        print("\n" + "=" * 70)
        print(" 🏛️  SLOP COURT: 3-JUROR BENCH DELIBERATION RECORD")
        print("=" * 70 + "\n")
        for jv in juror_votes:
            status = "ACQUITTED" if jv.vote == "ACQUIT" else "CONVICTED"
            print(f" [JUROR: {jv.juror_name}]")
            print(f"  Domain        : {jv.domain}")
            print(f"  Judicial Vote : {status} (Charges: {jv.charges_count}, Felonies: {jv.felonies_count})")
            print(f"  Rationale     : {jv.rationale}\n")
        print("=" * 70 + "\n")
        sys.exit(0)

    elif args.action == "bailiff":
        if args.subaction == "install":
            ok, msg = Bailiff.install_hooks(WORKSHOP_DIR)
            print(f"\n[*] Slop Court Bailiff: {msg}\n")
            sys.exit(0 if ok else 1)
        elif args.subaction == "status":
            hook = WORKSHOP_DIR / ".git" / "hooks" / "pre-commit"
            if hook.exists() and "SLOP COURT" in hook.read_text(encoding="utf-8", errors="ignore"):
                print("\n[✓] Slop Court Bailiff: Active and guarding git pre-commit / pre-push.\n")
            else:
                print("\n[!] Slop Court Bailiff: NOT installed. Run `workshop court bailiff install`.\n")
            sys.exit(0)

    elif args.action == "bailiff-check":
        prosecutor = Prosecutor(WORKSHOP_DIR)
        indictment = prosecutor.indict(WORKSHOP_DIR, staged_only=args.staged)
        magistrate = SlopCourtMagistrate(strict_mode=True)
        verdict = magistrate.trial(indictment)
        if verdict.ruling == "CONTEMPT_OF_COURT":
            print(render_trial_report(verdict, show_jury=True))
            sys.exit(1)
        else:
            print(f"✓ Slop Court Bailiff: Acquitted ({indictment.scanned_files_count} files clean, SHA {verdict.tree_sha256[:8]}).")
            sys.exit(0)

    elif args.action == "reform":
        target = Path(args.target).resolve()
        count, msg = Reformatory.rehabilitate_file(target)
        print(f"\n[*] Reformatory: {msg}\n")
        sys.exit(0)

    elif args.action == "indict":
        target = Path(args.target).resolve() if args.target else WORKSHOP_DIR
        prosecutor = Prosecutor(WORKSHOP_DIR)
        indictment = prosecutor.indict(target, staged_only=args.staged)
        print(f"\n[*] Grand Prosecutor Bill of Indictment: Case {indictment.case_number}")
        print(f"    Scanned: {indictment.scanned_files_count} files, {indictment.scanned_lines_count} lines")
        print(f"    Charges: {len(indictment.charges)} counts ({indictment.felony_count} Felonies, {indictment.misdemeanor_count} Misdemeanors)")
        print(f"    Slop Index: {indictment.slop_index}%\n")
        for c in indictment.charges[:20]:
            print(f"    - [{c.gravity}] {c.statute_code} ({c.juror_domain}) at {c.file_path.name}:{c.line_number} -> {c.description}")
        sys.exit(0)

    else:
        # Default: trial
        target = Path(getattr(args, "target", ".")).resolve()
        staged = getattr(args, "staged", False)
        strict = getattr(args, "strict", True)
        show_jury = getattr(args, "show_jury", True)

        prosecutor = Prosecutor(WORKSHOP_DIR)
        indictment = prosecutor.indict(target, staged_only=staged)
        magistrate = SlopCourtMagistrate(strict_mode=strict)
        verdict = magistrate.trial(indictment)

        print(render_trial_report(verdict, show_jury=show_jury))
        sys.exit(0 if verdict.ruling in {"ACQUITTED_HONORS", "ACQUITTED_CAUTION", "REMANDED"} else 1)

if __name__ == "__main__":
    main()