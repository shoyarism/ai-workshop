#!/usr/bin/env python3
"""
Unit tests for Slop Court statutes, prosecutor, and AST analysis.
"""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from workshop_court import Prosecutor, STATUTES


class TestSlopCourt(unittest.TestCase):
    def setUp(self):
        self.prosecutor = Prosecutor(root_dir=SCRIPTS_DIR.parent)

    def test_fel04_fake_stats_regex(self):
        """Verify FEL-04 catches unverified metric claims including trailing non-word chars."""
        samples = [
            ("Our platform supports 10M+ users across Europe.", True),
            ("Guaranteed 99.9% uptime SLA.", True),
            ("Benchmarked across 100M+ tokens processed.", True),
            ("Trusted by 500+ Fortune 500 enterprises.", True),
            ("Standard processing time is 10ms with 5% variance.", False),
            ("Clean technical documentation without claims.", False),
        ]
        statute_found = False
        for text, should_flag in samples:
            charges = self.prosecutor.scan_file(Path("test_snippet.md"), text)
            fel04_charges = [c for c in charges if c.statute_code == "FEL-04"]
            if should_flag:
                self.assertTrue(
                    len(fel04_charges) > 0,
                    f"Expected FEL-04 violation for: '{text}'"
                )
            else:
                self.assertEqual(
                    len(fel04_charges), 0,
                    f"Unexpected FEL-04 violation for: '{text}'"
                )

    def test_fel03_naked_except(self):
        """Verify FEL-03 flags silent error blackholes."""
        code_bad = """
def process():
    try:
        do_work()
    except Exception:
        pass
"""
        charges = self.prosecutor.scan_file(Path("test_snippet.py"), code_bad)
        fel03_charges = [c for c in charges if c.statute_code == "FEL-03" and not c.exempted]
        self.assertTrue(len(fel03_charges) > 0, "Expected FEL-03 for naked except: pass")

    def test_mis06_nesting_depth(self):
        """Verify MIS-06 catches control flow nesting depth > 5."""
        code_deep = """
def deeply_nested():
    if a:
        for b in c:
            while d:
                try:
                    with e:
                        if f:
                            do_something()
                finally:
                    cleanup()
"""
        charges = self.prosecutor.scan_file(Path("test_snippet.py"), code_deep)
        mis06_charges = [c for c in charges if c.statute_code == "MIS-06"]
        self.assertTrue(len(mis06_charges) > 0, "Expected MIS-06 for >5 levels of nesting")

    def test_fel06_secrets(self):
        """Verify FEL-06 catches raw tokens and API keys."""
        code_secret = "GITHUB_PAT = 'ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'"
        charges = self.prosecutor.scan_file(Path("config.py"), code_secret)
        fel06_charges = [c for c in charges if c.statute_code == "FEL-06"]
        self.assertTrue(len(fel06_charges) > 0, "Expected FEL-06 for exposed token")

    def test_mis05_wildcard_import(self):
        """Verify MIS-05 catches wildcard imports in Python."""
        code_wildcard = "from os.path import *"
        charges = self.prosecutor.scan_file(Path("module.py"), code_wildcard)
        mis05_charges = [c for c in charges if c.statute_code == "MIS-05"]
        self.assertTrue(len(mis05_charges) > 0, "Expected MIS-05 for wildcard import")

    def test_fel02_ast_stub_detection(self):
        """Verify AST flags truncated function stubs with pass or Ellipsis."""
        code_stub1 = "def do_calculation():\n    pass\n"
        code_stub2 = "def fetch_records():\n    ...\n"
        code_valid = "def calculate():\n    return 42\n"

        charges1 = self.prosecutor.scan_file(Path("test_stub1.py"), code_stub1)
        self.assertTrue(any(c.statute_code == "FEL-02" and not c.exempted for c in charges1))

        charges2 = self.prosecutor.scan_file(Path("test_stub2.py"), code_stub2)
        self.assertTrue(any(c.statute_code == "FEL-02" and not c.exempted for c in charges2))

        charges_valid = self.prosecutor.scan_file(Path("test_valid.py"), code_valid)
        self.assertFalse(any(c.statute_code == "FEL-02" for c in charges_valid))

    def test_courtprobe_directory_not_exempt(self):
        """Regression test for P0-1: A file inside a directory containing 'court' in its name must still be judged."""
        bad_code = """
def unfinished_logic():
    pass

try:
    crash()
except Exception:
    pass
"""
        charges = self.prosecutor.scan_file(Path("courtprobe/handler.py"), bad_code)
        active_felonies = [c for c in charges if not c.exempted and c.gravity == "FELONY"]
        self.assertGreaterEqual(
            len(active_felonies), 2,
            "courtprobe directory must NOT grant blanket immunity to code violations"
        )

    def test_fel07_dangerous_execution_ast(self):
        """Verify FEL-07 flags eval, exec, pickle.loads, and subprocess shell=True."""
        code_eval = "result = eval(user_input)\n"
        code_pickle = "import pickle\ndata = pickle.loads(payload)\n"
        code_shell = "import subprocess\nsubprocess.run(cmd, shell=True)\n"

        charges_eval = self.prosecutor.scan_file(Path("eval_test.py"), code_eval)
        self.assertTrue(any(c.statute_code == "FEL-07" and not c.exempted for c in charges_eval), "Expected FEL-07 for eval()")

        charges_pickle = self.prosecutor.scan_file(Path("pickle_test.py"), code_pickle)
        self.assertTrue(any(c.statute_code == "FEL-07" and not c.exempted for c in charges_pickle), "Expected FEL-07 for pickle.loads()")

        charges_shell = self.prosecutor.scan_file(Path("shell_test.py"), code_shell)
        self.assertTrue(any(c.statute_code == "FEL-07" and not c.exempted for c in charges_shell), "Expected FEL-07 for shell=True")

    def test_fel08_sql_injection_ast(self):
        """Verify FEL-08 flags dynamic SQL formatting via % and f-strings in execute()."""
        code_sql_mod = "cursor.execute('SELECT * FROM users WHERE name = %s' % username)\n"
        code_sql_fstr = "cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')\n"

        charges_mod = self.prosecutor.scan_file(Path("sql_mod.py"), code_sql_mod)
        self.assertTrue(any(c.statute_code == "FEL-08" and not c.exempted for c in charges_mod), "Expected FEL-08 for SQL % formatting")

        charges_fstr = self.prosecutor.scan_file(Path("sql_fstr.py"), code_sql_fstr)
        self.assertTrue(any(c.statute_code == "FEL-08" and not c.exempted for c in charges_fstr), "Expected FEL-08 for SQL f-string")

    def test_expanded_secrets_detection(self):
        """Verify FEL-06 catches sk-live tokens and hardcoded passwords."""
        code_sk = "API_KEY = 'sk-live-9876543210abcdef9876543210'\n"
        code_pwd = "password = 'SuperSecretDbPassword2026!'\n"

        charges_sk = self.prosecutor.scan_file(Path("secrets_sk.py"), code_sk)
        self.assertTrue(any(c.statute_code == "FEL-06" and not c.exempted for c in charges_sk), "Expected FEL-06 for sk-live token")

        charges_pwd = self.prosecutor.scan_file(Path("secrets_pwd.py"), code_pwd)
        self.assertTrue(any(c.statute_code == "FEL-06" and not c.exempted for c in charges_pwd), "Expected FEL-06 for hardcoded password")

    def test_clean_code_acquittal(self):
        """Verify clean, idiomatic code is acquitted with 0 charges."""
        clean_code = """
def add(a: int, b: int) -> int:
    \"\"\"Return the sum of two integers.\"\"\"
    return a + b
"""
        charges = self.prosecutor.scan_file(Path("clean.py"), clean_code)
        active_charges = [c for c in charges if not c.exempted]
        self.assertEqual(len(active_charges), 0, f"Expected 0 charges, got: {active_charges}")


if __name__ == "__main__":
    unittest.main()
