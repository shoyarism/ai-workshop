#!/usr/bin/env python3
"""
Secrets Scanner for Workshop OS
===============================
Scans repository, vault, scratch/, and skills for high-entropy API key patterns.
STRICT SAFETY RULE: Reports file locations, line numbers, and pattern names ONLY.
NEVER prints, logs, or exposes secret values. Never inspects .env, credential stores, or freeapi.db.
Exits with code 1 on ANY unauthorized secret detection outside explicit test allowlists.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Windows UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent

# Key patterns to detect
SECRET_PATTERNS = {
    "openai_key": re.compile(r"\bsk-[a-zA-Z0-9_-]{20,}\b"),
    "anthropic_key": re.compile(r"\bsk-ant-[a-zA-Z0-9_-]{20,}\b"),
    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z-_]{35}\b"),
    "github_token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}\b|\bgithub_pat_[a-zA-Z0-9_]{50,}\b"),
    "huggingface_token": re.compile(r"\bhf_[a-zA-Z0-9]{34,}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[0-9a-zA-Z]{10,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private_key_header": re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"),
}

# Directories/files to strictly skip per security rules
SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", ".pnpm-store", "__pycache__",
    ".idea", ".vscode", "dist", "build"
}

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".mp4", ".mp3",
    ".zip", ".tar", ".gz", ".7z", ".asar", ".exe", ".dll", ".so", ".dylib",
    ".woff", ".woff2", ".ttf", ".eot", ".parquet", ".pdf"
}

# Explicitly forbidden files to open per Hard Rule 1
FORBIDDEN_FILES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "freeapi.db", "freellmapi.db", "credentials.json"
}

# Explicit allowlist of test files containing synthetic/trap keys
ALLOWLIST_FILES = {
    "evals/reasoning/task_08_privacy_leak_trap/oracle.py",
    "scripts/workshop_reasoning_eval.py",
    "tests/test_court.py",
}


def is_allowlisted(file_path: Path) -> bool:
    try:
        rel = file_path.relative_to(ROOT_DIR).as_posix()
        return rel in ALLOWLIST_FILES
    except ValueError:
        return False


def should_scan_file(file_path: Path) -> bool:
    if is_allowlisted(file_path):
        return False
    name = file_path.name.lower()
    if name in FORBIDDEN_FILES or name.startswith(".env"):
        return False
    if file_path.suffix.lower() in SKIP_EXTENSIONS:
        return False
    if name.endswith(".db") or name.endswith(".sqlite") or name.endswith(".sqlite3"):
        return False
    try:
        if file_path.stat().st_size > 5 * 1024 * 1024:
            return False
    except OSError:
        return False
    return True


def scan_file(file_path: Path) -> List[Tuple[int, str]]:
    """Scan a single file for secrets. Returns list of (line_num, pattern_name)."""
    detections: List[Tuple[int, str]] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for idx, line in enumerate(f, 1):
                # Ignore obvious documentation examples or false positive indicators
                lower = line.lower()
                if "your-api-key" in lower or "dummy" in lower or "example" in lower:
                    continue
                for name, pattern in SECRET_PATTERNS.items():
                    if pattern.search(line):
                        detections.append((idx, name))
    except (IOError, OSError):
        pass
    return detections


def _record_file_hits(fpath: Path, summary: Dict[str, int], file_reports: List[Dict[str, Any]]) -> bool:
    """Helper to audit a single file and record hits. Keeps nesting depth shallow."""
    hits = scan_file(fpath)
    if not hits:
        return False
    for _, pat in hits:
        summary[pat] += 1
    rel_path = str(fpath.relative_to(ROOT_DIR) if fpath.is_relative_to(ROOT_DIR) else fpath)
    file_reports.append({
        "path": rel_path,
        "hits": [{"line": l, "pattern": p} for l, p in hits]
    })
    return True


def run_secrets_scan(target_paths: List[Path]) -> Dict[str, Any]:
    summary: Dict[str, int] = {k: 0 for k in SECRET_PATTERNS.keys()}
    file_reports: List[Dict[str, Any]] = []
    total_files_scanned = 0

    for base_path in target_paths:
        if not base_path.exists():
            continue

        if base_path.is_file():
            if should_scan_file(base_path):
                total_files_scanned += 1
                _record_file_hits(base_path, summary, file_reports)
            continue

        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".git")]
            for file in files:
                fpath = Path(root) / file
                if not should_scan_file(fpath):
                    continue
                total_files_scanned += 1
                _record_file_hits(fpath, summary, file_reports)

    total_hits = sum(summary.values())
    return {
        "total_files_scanned": total_files_scanned,
        "total_hits": total_hits,
        "pattern_summary": summary,
        "file_reports": file_reports,
    }


def main():
    parser = argparse.ArgumentParser(description="Scan Workshop OS for exposed secrets.")
    parser.add_argument("--json", action="store_true", help="Output JSON results")
    parser.add_argument("--include-brain", action="store_true", help="Also scan external assistant brain logs")
    args = parser.parse_args()

    # Targets to scan: repo runtime and execution targets
    scan_targets = [
        ROOT_DIR / "scripts",
        ROOT_DIR / "evals",
        ROOT_DIR / "prompts",
        ROOT_DIR / "vault",
        ROOT_DIR / "scratch",
    ]

    if args.include_brain:
        userprofile = os.environ.get("USERPROFILE", "")
        brain_logs = Path(userprofile) / ".gemini" / "antigravity" / "brain"
        if brain_logs.exists():
            scan_targets.append(brain_logs)

    result = run_secrets_scan(scan_targets)

    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print("=======================================================")
        print(" [*] WORKSHOP SECRETS SCAN REPORT")
        print("=======================================================")
        print(f" Total Files Scanned : {result['total_files_scanned']}")
        print(f" Total Pattern Hits  : {result['total_hits']}")
        print(" Pattern Breakdown   :")
        for pat, count in result["pattern_summary"].items():
            print(f"   • {pat:<22}: {count}")

        if result["file_reports"]:
            print("\n [!] UNMASKED SECRETS DETECTED:")
            for rep in result["file_reports"]:
                print(f"   -> {rep['path']}")
                for hit in rep["hits"]:
                    print(f"      [Line {hit['line']}] Matched: {hit['pattern']}")
            print("=======================================================")
            print(" [FAIL] Security violation: Plaintext secrets found in repository.")
            sys.exit(1)
        else:
            print("\n [OK] Clean: Zero unmasked key patterns detected.")
            print("=======================================================")
            sys.exit(0)


if __name__ == "__main__":
    main()
