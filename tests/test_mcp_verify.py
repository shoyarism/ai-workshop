#!/usr/bin/env python3
"""
Unit tests for workshop_mcp verify tool command safety and execution.
"""

import os
import sys
import unittest
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import workshop_mcp


class TestMCPVerifyTool(unittest.TestCase):
    def setUp(self):
        # Set agent role to architect so verify tool is permitted
        self.old_role = os.environ.get("WORKSHOP_ROLE")
        os.environ["WORKSHOP_ROLE"] = "architect"

    def tearDown(self):
        if self.old_role is not None:
            os.environ["WORKSHOP_ROLE"] = self.old_role
        else:
            os.environ.pop("WORKSHOP_ROLE", None)

    def test_verify_allowed_python_command(self):
        """Allowed executable with clean arguments should succeed."""
        result = workshop_mcp.verify("python -c \"print('VERIFY_PASSED')\"")
        self.assertIn("VERIFY_PASSED", result)
        self.assertIn("Status: SUCCESS", result)

    def test_verify_allowed_git_command(self):
        """Allowed git command should run cleanly."""
        result = workshop_mcp.verify("git status --short")
        self.assertIn("Status: SUCCESS", result)

    def test_verify_blocked_executable_not_in_allowlist(self):
        """Executables not in ALLOWED_VERIFY_EXECUTABLES should be blocked."""
        forbidden_commands = [
            "powershell -Command Get-Process",
            "cmd /c dir",
            "bash -c 'ls -la'",
            "curl http://127.0.0.1:8080/test",
            "wget http://127.0.0.1:8080/test",
            "cat sensitive_file.txt",
        ]
        for cmd in forbidden_commands:
            result = workshop_mcp.verify(cmd)
            self.assertIn("[BLOCKED BY SAFETY GATE]", result, f"Expected '{cmd}' to be blocked.")

    def test_verify_blocked_env_leak_pattern(self):
        """Commands attempting to access .env should be blocked by safety gate."""
        leak_attempts = [
            "git diff .env",
            "git log -p .env",
        ]
        for cmd in leak_attempts:
            result = workshop_mcp.verify(cmd)
            self.assertIn("[BLOCKED BY SAFETY GATE]", result, f"Expected '{cmd}' to be blocked.")

    def test_verify_default_deny_when_unauthorized_role(self):
        """Default-deny should reject execution when no role or spectator role is active."""
        os.environ["WORKSHOP_ROLE"] = "spectator"
        result = workshop_mcp.verify("git status")
        self.assertIn("default-deny active", result)


if __name__ == "__main__":
    unittest.main()
