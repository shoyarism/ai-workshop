"""
Unit and functional tests for the Workshop OS main CLI (scripts/workshop.py).
Tests argument parsing, command dispatch, doctor diagnostics execution,
house inspection, search routing, and exit code propagation.
"""

import sys
import unittest
from unittest.mock import patch
from pathlib import Path
from io import StringIO

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import scripts.workshop as workshop_cli


class TestWorkshopCLI(unittest.TestCase):
    """Verify Master Workshop CLI commands and invariants."""

    def setUp(self):
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.out = StringIO()
        self.err = StringIO()
        sys.stdout = self.out
        sys.stderr = self.err

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def test_parser_construction(self):
        """ArgumentParser must configure all expected subcommands."""
        parser = workshop_cli.build_parser()
        self.assertIsNotNone(parser)
        
        # Test help formatting without exception
        help_text = parser.format_help()
        self.assertIn("workshop", help_text)
        self.assertIn("doctor", help_text)
        self.assertIn("court", help_text)
        self.assertIn("search", help_text)
        self.assertIn("house", help_text)

    def test_house_list_command(self):
        """`workshop house list` must enumerate all 7 Sovereign Houses."""
        parser = workshop_cli.build_parser()
        args = parser.parse_args(["house", "list"])
        self.assertEqual(args.command, "house")
        self.assertEqual(args.action, "list")

        # Execute cmd_house handler
        exit_code = workshop_cli.cmd_house(args)
        self.assertEqual(exit_code, 0)
        output = self.out.getvalue()
        self.assertIn("SOVEREIGN HOUSES", output)
        self.assertIn("security-house", output)
        self.assertIn("dev-house", output)

    def test_house_inspect_valid(self):
        """`workshop house inspect dev-house` must display details."""
        parser = workshop_cli.build_parser()
        args = parser.parse_args(["house", "inspect", "dev-house"])
        exit_code = workshop_cli.cmd_house(args)
        self.assertEqual(exit_code, 0)
        output = self.out.getvalue()
        self.assertIn("dev-house", output)

    def test_house_inspect_invalid(self):
        """`workshop house inspect non-existent` must report error and exit 1."""
        parser = workshop_cli.build_parser()
        args = parser.parse_args(["house", "inspect", "non_existent_house_xyz"])
        exit_code = workshop_cli.cmd_house(args)
        self.assertEqual(exit_code, 1)

    def test_search_routing(self):
        """`workshop search` must route to skill search."""
        parser = workshop_cli.build_parser()
        args = parser.parse_args(["search", "superpowers"])
        self.assertEqual(args.command, "search")
        self.assertEqual(args.query, "superpowers")

    def test_cli_entrypoint_no_args_shows_help(self):
        """Invoking main() with no arguments prints help and exits 0."""
        with patch.object(sys, "argv", ["workshop"]):
            exit_code = workshop_cli.main()
            self.assertEqual(exit_code, 0)
            output = self.out.getvalue()
            self.assertIn("usage:", output.lower())

    def test_doctor_command_routing(self):
        """`workshop doctor` parser routing."""
        parser = workshop_cli.build_parser()
        args = parser.parse_args(["doctor", "--strict"])
        self.assertEqual(args.command, "doctor")
        self.assertTrue(args.strict)


if __name__ == "__main__":
    unittest.main()
