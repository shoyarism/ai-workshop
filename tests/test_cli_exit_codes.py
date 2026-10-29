"""
Tests to verify CLI failure propagation and exit code contracts.
Demonstrates that child-process failures and invalid command arguments
propagate non-zero exit codes to parent processes and CI.
"""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI_PATH = ROOT / "scripts" / "workshop.py"


class TestCLIExitCodeContracts(unittest.TestCase):
    """Verify that workshop.py adheres to strict exit status contracts."""

    def test_help_exits_zero(self):
        res = subprocess.run([sys.executable, str(CLI_PATH), "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Centralized Workshop Master CLI", res.stdout)

    def test_unknown_subsystem_info_exits_nonzero(self):
        res = subprocess.run(
            [sys.executable, str(CLI_PATH), "info", "completely_nonexistent_subsystem_xyz_999"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(res.returncode, 0, "CLI info query for nonexistent subsystem must exit non-zero")
        self.assertIn("not found", res.stdout.lower() + res.stderr.lower())

    def test_unknown_mcp_server_start_exits_nonzero(self):
        res = subprocess.run(
            [sys.executable, str(CLI_PATH), "mcp", "start", "nonexistent_mcp_server_abc_123"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(res.returncode, 0, "CLI mcp start for unknown server must exit non-zero")
        self.assertIn("unknown mcp server", res.stdout.lower() + res.stderr.lower())


if __name__ == "__main__":
    unittest.main()
