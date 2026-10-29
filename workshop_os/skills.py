"""
Workshop OS skills discovery and SHA-256 integrity manifest.
"""
from scripts.workshop_skills import (
    discover,
    generate_manifest,
    verify_manifest,
    list_skills,
    find_skill,
    MANIFEST_PATH,
    Skill,
)

__all__ = [
    "discover",
    "generate_manifest",
    "verify_manifest",
    "list_skills",
    "find_skill",
    "MANIFEST_PATH",
    "Skill",
]
