#!/usr/bin/env python3
"""
Unit tests for skills supply chain cryptographic manifest verification.
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import workshop_skills


class TestSkillsManifest(unittest.TestCase):
    def test_skills_manifest_exists(self):
        """Manifest file must exist in skills directory."""
        self.assertTrue(workshop_skills.MANIFEST_PATH.exists(), "skills/manifest.sha256 must exist")

    def test_skills_manifest_integrity(self):
        """All skills must match cryptographic SHA-256 hashes in manifest."""
        ok, verified, mismatches = workshop_skills.verify_manifest()
        self.assertTrue(ok, f"Manifest verification failed with mismatches: {mismatches}")
        self.assertGreaterEqual(verified, 2140, "Expected at least 2,140 verified skills")


if __name__ == "__main__":
    unittest.main()
