#!/usr/bin/env python3
"""
Workshop skill catalog: discovery, frontmatter parsing, tiering, linting.

Agent Skills spec (agentskills.io / Anthropic): a skill is a directory holding
SKILL.md whose YAML frontmatter has `name` and `description`. Harnesses inject
name+description for every registered skill, so the registered set must stay
small (Tier 0). Everything else is served on demand via skill_search/skill_load.

Usage:
    uv run python scripts/workshop_skills.py stats
    uv run python scripts/workshop_skills.py lint [--json]
    uv run python scripts/workshop_skills.py core
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workshop_paths import ROOT  # noqa: E402

SKILL_ROOTS: tuple[Path, ...] = (
    ROOT / "skills",
    ROOT / "open-design",
    ROOT / "ai-agents-handbook",
    ROOT / "agent-skills" / "skills",
    ROOT / "claude-plugins-official",
    ROOT / "claude-mem",
    ROOT / "openclaw" / "skills",
    ROOT / "open-seo",
    ROOT / "strix" / "skills",
    ROOT / "hyperframes" / "skills",
    ROOT / "browser-use" / "skills",
    ROOT / "ponytail",
)

SKIP_DIRS = {".git", ".venv", ".venv_old", "node_modules", "__pycache__", ".workshop_state", ".ruff_cache", "dist", "build"}

FRONTMATTER_RE = re.compile(r"^\ufeff?---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
MAX_DESCRIPTION = 1024


@dataclass
class Skill:
    name: str
    description: str
    path: Path
    root: Path
    frontmatter: dict = field(default_factory=dict)
    error: str | None = None

    @property
    def dir(self) -> Path:
        return self.path.parent

    def to_dict(self) -> dict:
        d = asdict(self)
        d["path"] = str(self.path).replace("\\", "/")
        d["root"] = str(self.root).replace("\\", "/")
        d.pop("frontmatter", None)
        return d


def parse_frontmatter(text: str) -> tuple[dict, str, str | None]:
    """Return (frontmatter, body, error). Handles folded/literal YAML scalars."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text, "missing YAML frontmatter"
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return {}, text[m.end():], f"invalid YAML: {str(e).splitlines()[0]}"
    if not isinstance(data, dict):
        return {}, text[m.end():], "frontmatter is not a mapping"
    return data, text[m.end():], None


def load_skill(skill_md: Path, root: Path) -> Skill:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, _body, err = parse_frontmatter(text)
    name = str(fm.get("name") or skill_md.parent.name).strip()
    desc = " ".join(str(fm.get("description") or "").split())
    if not err and not desc:
        err = "missing description"
    return Skill(name=name, description=desc, path=skill_md, root=root, frontmatter=fm, error=err)


def _iter_skill_mds(root: Path):
    """Fast recursive walk for SKILL.md files pruning hidden/heavy directories."""
    import os
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if not d.startswith((".", "_")) and d not in SKIP_DIRS
        )
        if "SKILL.md" in filenames:
            yield Path(dirpath) / "SKILL.md"


@lru_cache(maxsize=1)
def discover() -> tuple[Skill, ...]:
    """All skills across roots (including nested skill packs); first root wins on exact name collisions."""
    seen: dict[str, Skill] = {}
    for root in SKILL_ROOTS:
        if not root.is_dir():
            continue
        # 1. Direct children first (highest priority)
        for d in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if not d.is_dir() or d.name.startswith((".", "_")) or d.name in SKIP_DIRS:
                continue
            md = d / "SKILL.md"
            if md.is_file():
                s = load_skill(md, root)
                seen.setdefault(s.name.lower(), s)
        # 2. Nested skill packs (e.g. anthropic-cybersecurity-skills, OpenMontage, ecc, open-design)
        for md in _iter_skill_mds(root):
            s = load_skill(md, root)
            key = s.name.lower()
            if key in seen and seen[key].path != md:
                # Disambiguate nested skill collisions by prefixing parent pack name
                rel_parts = md.relative_to(root).parts
                if len(rel_parts) >= 3:
                    qualified_key = f"{rel_parts[0].lower()}/{key}"
                    seen.setdefault(qualified_key, s)
            else:
                seen.setdefault(key, s)
    return tuple(seen.values())


def by_name(name: str) -> Skill | None:
    key = name.strip().lower()
    for s in discover():
        if s.name.lower() == key or s.dir.name.lower() == key:
            return s
    return None


def lint(skills: tuple[Skill, ...] | None = None) -> list[dict]:
    issues: list[dict] = []
    for s in skills or discover():
        problems = []
        if s.error:
            problems.append(s.error)
        if not NAME_RE.match(s.name):
            problems.append(f"name '{s.name}' violates ^[a-z0-9][a-z0-9-]{{0,63}}$")
        if s.name != s.dir.name:
            problems.append(f"name '{s.name}' != directory '{s.dir.name}'")
        if len(s.description) > MAX_DESCRIPTION:
            problems.append(f"description {len(s.description)} chars > {MAX_DESCRIPTION}")
        if problems:
            issues.append({"skill": s.name, "path": str(s.path).replace("\\", "/"), "problems": problems})
    # Directories that look like skills but lack SKILL.md
    for root in SKILL_ROOTS[:1]:
        for d in root.iterdir():
            if d.is_dir() and not d.name.startswith((".", "_")) and not (d / "SKILL.md").is_file():
                issues.append({"skill": d.name, "path": str(d).replace("\\", "/"), "problems": ["missing SKILL.md"]})
    return issues


def metadata_tokens(skills) -> int:
    """Approximate tokens a harness spends listing these skills (~4 chars/token)."""
    return sum(len(s.name) + len(s.description) + 8 for s in skills) // 4


def core_skills(names: list[str]) -> tuple[list[Skill], list[str]]:
    found, missing = [], []
    for n in names:
        s = by_name(n)
        (found.append(s) if s else missing.append(n))
    return found, missing


MANIFEST_PATH = ROOT / "skills" / "manifest.sha256"


def generate_manifest() -> Path:
    """Generate cryptographic SHA-256 manifest of all discovered skill files (LF normalized)."""
    skills = discover()
    entries: list[str] = []
    for s in sorted(skills, key=lambda x: str(x.path)):
        try:
            rel = s.path.relative_to(ROOT).as_posix()
            content = s.path.read_bytes().replace(b"\r\n", b"\n")
            digest = hashlib.sha256(content).hexdigest()
            entries.append(f"{digest}  {rel}")
        except (OSError, IOError):  # @court-exempt: unreadable file skipped
            pass
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return MANIFEST_PATH


def verify_manifest() -> tuple[bool, int, list[str]]:
    """Verify all skills against cryptographic SHA-256 manifest (LF normalized)."""
    if not MANIFEST_PATH.exists():
        return False, 0, [f"Manifest file not found: {MANIFEST_PATH}"]
    lines = MANIFEST_PATH.read_text(encoding="utf-8").strip().splitlines()
    mismatches: list[str] = []
    verified = 0
    for line in lines:
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        expected_hash, rel_path = parts
        fpath = ROOT / rel_path
        if not fpath.exists():
            mismatches.append(f"Missing file: {rel_path}")
            continue
        content = fpath.read_bytes().replace(b"\r\n", b"\n")
        current_hash = hashlib.sha256(content).hexdigest()
        if current_hash != expected_hash:
            mismatches.append(f"Hash mismatch: {rel_path}")
        else:
            verified += 1
    return len(mismatches) == 0, verified, mismatches


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Workshop skill catalog tools")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats")
    p_lint = sub.add_parser("lint")
    p_lint.add_argument("--json", action="store_true")
    sub.add_parser("core", help="Show Tier 0 skills from the manifest and their context cost")
    p_man = sub.add_parser("manifest", help="Generate or verify cryptographic SHA-256 manifest of all skills")
    p_man.add_argument("--verify", action="store_true", help="Verify integrity against existing manifest")
    args = ap.parse_args()

    if args.cmd == "stats":
        skills = discover()
        print(f"skills discovered : {len(skills)}")
        print(f"metadata tokens   : ~{metadata_tokens(skills):,} (cost if all were registered natively)")
        for root in SKILL_ROOTS:
            n = sum(1 for s in skills if s.root == root)
            if n:
                print(f"  {n:4}  {root.relative_to(ROOT)}")
    elif args.cmd == "lint":
        issues = lint()
        if args.json:
            print(json.dumps(issues, indent=2))
        else:
            for i in issues:
                print(f"[{i['skill']}] {'; '.join(i['problems'])}\n    {i['path']}")
            print(f"\n{len(issues)} skill(s) with issues")
        sys.exit(1 if issues else 0)
    elif args.cmd == "core":
        from workshop_sync import load_manifest
        names = load_manifest()["skills"]["core"]
        found, missing = core_skills(names)
        for s in found:
            print(f"  {s.name:40} {len(s.description):5} chars")
        print(f"\nTier 0: {len(found)} skills, ~{metadata_tokens(found):,} tokens")
        if missing:
            print(f"MISSING: {', '.join(missing)}")
            sys.exit(1)
    elif args.cmd == "manifest":
        if args.verify:
            ok, verified, mismatches = verify_manifest()
            print(f"Verified {verified} skill(s) against manifest.")
            if not ok:
                print(f"[!] Integrity check failed ({len(mismatches)} mismatches):", file=sys.stderr)
                for m in mismatches[:10]:
                    print(f"   • {m}", file=sys.stderr)
                sys.exit(1)
            print("[✓] All skills verified clean against SHA-256 manifest.")
        else:
            p = generate_manifest()
            print(f"[✓] Generated cryptographic manifest: {p}")


if __name__ == "__main__":
    main()
