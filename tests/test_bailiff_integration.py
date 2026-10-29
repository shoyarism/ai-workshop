#!/usr/bin/env python3
"""
Integration test for Slop Court Git Bailiff hook gatekeeper.
Verifies that pre-commit intercepts and aborts commits containing felony slop violations.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from workshop_court import Bailiff


class TestBailiffIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_dir = Path(self.temp_dir.name)

        # Initialize temporary git repository
        subprocess.run(
            ["git", "init"],
            cwd=self.repo_dir,
            capture_output=True,
            check=True,
            text=True,
        )
        # Configure local git user to enable commits
        subprocess.run(
            ["git", "config", "user.email", "bailiff-test@workshop.local"],
            cwd=self.repo_dir,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Bailiff Test Agent"],
            cwd=self.repo_dir,
            capture_output=True,
            check=True,
        )

        # Copy scripts directory into temp repo so the hook can execute workshop_court.py
        shutil.copytree(
            SCRIPTS_DIR,
            self.repo_dir / "scripts",
            ignore=shutil.ignore_patterns(".skills_cache.json", "__pycache__", ".*"),
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_bailiff_blocks_felony_slop_commit(self):
        """Bailiff pre-commit hook must intercept and abort git commit on FEL-03 naked pass."""
        ok, msg = Bailiff.install_hooks(self.repo_dir)
        self.assertTrue(ok, f"Failed to install hooks: {msg}")

        # 1. Clean commit should succeed
        clean_file = self.repo_dir / "clean_module.py"
        clean_file.write_text(
            'def calculate_total(items: list[float]) -> float:\n    """Return the arithmetic sum of item prices."""\n    return sum(items)\n',
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "clean_module.py", "scripts/"], cwd=self.repo_dir, capture_output=True, check=True)
        res_clean = subprocess.run(
            ["git", "commit", "-m", "chore: initial clean commit"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(res_clean.returncode, 0, f"Clean commit failed unexpectedly: {res_clean.stderr}\n{res_clean.stdout}")

        # 2. Felony slop (FEL-03 naked except pass) must be blocked by the Bailiff
        slop_file = self.repo_dir / "slop_module.py"
        slop_file.write_text(
            "def broken_network_call():\n    try:\n        import urllib.request\n        urllib.request.urlopen('http://127.0.0.1:9999')\n    except:\n        pass\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "slop_module.py"], cwd=self.repo_dir, capture_output=True, check=True)
        res_slop = subprocess.run(
            ["git", "commit", "-m", "feat: introduce illegal error blackhole"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        self.assertNotEqual(
            res_slop.returncode,
            0,
            "Bailiff failed to abort commit containing FEL-03 naked error blackhole!",
        )
        combined_output = (res_slop.stdout + res_slop.stderr).lower()
        self.assertTrue(
            "contempt of court" in combined_output or "fel-03" in combined_output or "aborted" in combined_output,
            f"Expected contempt of court rejection, got: {res_slop.stdout}\n{res_slop.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
