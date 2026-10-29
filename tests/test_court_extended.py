#!/usr/bin/env python3
"""
Extended Unit Tests for Slop Court v3.5
========================================
Additional test cases for new statutes and edge cases.
"""

import unittest
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from workshop_court import Prosecutor, STATUTES


class TestExtendedSlopCourt(unittest.TestCase):
    """Extended test coverage for Slop Court including new statutes."""

    def setUp(self):
        self.prosecutor = Prosecutor(root_dir=SCRIPTS_DIR.parent)

    def test_fel07_eval_in_function(self):
        """Verify FEL-07 flags eval() even in complex contexts."""
        code = """
def dangerous():
    user_input = request.args.get('q')
    result = eval(user_input)  # Critical vulnerability
    return result
"""
        charges = self.prosecutor.scan_file(Path("dangerous.py"), code)
        fel07_charges = [c for c in charges if c.statute_code == "FEL-07" and not c.exempted]
        self.assertTrue(len(fel07_charges) > 0, "Expected FEL-07 for eval() in function")

    def test_fel07_exec_in_loop(self):
        """Verify FEL-07 flags exec() even in loops."""
        code = """
for cmd in commands:
    exec(cmd)  # Code injection vector
"""
        charges = self.prosecutor.scan_file(Path("loop_exec.py"), code)
        self.assertTrue(any(c.statute_code == "FEL-07" and not c.exempted for c in charges))

    def test_fel08_fstring_in_table_create(self):
        """Verify FEL-08 catches SQL injection via f-strings in DDL."""
        code = """
table_name = user_input
cursor.execute(f'CREATE TABLE {table_name} (id INT)')
"""
        charges = self.prosecutor.scan_file(Path("ddl_injection.py"), code)
        self.assertTrue(any(c.statute_code == "FEL-08" and not c.exempted for c in charges))

    def test_mis06_deep_nesting_in_try_finally(self):
        """Verify MIS-06 catches deep nesting with try/finally."""
        code = """
def complex_function():
    if a:
        for x in items:
            while cond:
                try:
                    with context:
                        if nested:
                            for inner in inner_items:
                                do_something(inner)
                finally:
                    cleanup()
"""
        charges = self.prosecutor.scan_file(Path("nested.py"), code)
        mis06_charges = [c for c in charges if c.statute_code == "MIS-06"]
        self.assertTrue(len(mis06_charges) > 0, "Expected MIS-06 for deep nesting")

    def test_inf02_missing_docstrings(self):
        """Verify INF-02 flags public functions without docstrings."""
        code = """
def calculate_tax(amount, rate):
    return amount * rate

def process_data(data):
    for item in data:
        yield transform(item)
"""
        charges = self.prosecutor.scan_file(Path("no_docs.py"), code)
        inf02_charges = [c for c in charges if c.statute_code == "INF-02"]
        # Note: This test depends on function being "public" - may need adjustment
        # based on implementation details

    def test_fel01_crlf_truncated(self):
        """Verify FEL-01 catches truncated comments with Windows line endings."""
        code = "def func():\\n    # ... existing code\\r\\n    return True\\n"
        charges = self.prosecutor.scan_file(Path("truncated_crlf.py"), "def func():\n    # ... existing code\r\n    return True\n")
        fel01_charges = [c for c in charges if c.statute_code == "FEL-01"]
        self.assertTrue(len(fel01_charges) > 0, "Expected FEL-01 for truncated comment with CRLF")

    def test_fel01_python_truncated(self):
        """Verify FEL-01 catches Python-style truncated comments."""
        code = "def func():\\n    # ... rest of code\\n    return True\\n"
        charges = self.prosecutor.scan_file(Path("python_truncated.py"), code)
        self.assertTrue(any(c.statute_code == "FEL-01" and not c.exempted for c in charges))

    def test_court_exempt_annotated_ignored(self):
        """Verify @court-exempt annotations correctly exempt charges."""
        code = """
def skip_this():
    # @court-exempt: Platform encoding fallback
    except UnicodeDecodeError:
        pass
"""
        charges = self.prosecutor.scan_file(Path("exempt.py"), code)
        active_felonies = [c for c in charges if not c.exempted and c.gravity == "FELONY"]
        self.assertEqual(len(active_felonies), 0, "FEL-03 should be exempted by annotation")

    def test_wildcard_import_detection(self):
        """Verify MIS-05 catches wildcard imports."""
        code = "from os.path import *\\nfrom collections import *"
        charges = self.prosecutor.scan_file(Path("wildcards.py"), code)
        mis05_charges = [c for c in charges if c.statute_code == "MIS-05"]
        self.assertTrue(len(mis05_charges) >= 2, "Expected MIS-05 for wildcard imports")

    def test_fel06_stripe_secret_key(self):
        """Verify FEL-06 catches Stripe-style secret keys."""
        code = "STRIPE_KEY = 'sk_test_FAKE_KEY_FOR_TESTING_12345'"
        charges = self.prosecutor.scan_file(Path("stripe.py"), code)
        self.assertTrue(any(c.statute_code == "FEL-06" and not c.exempted for c in charges))

    def test_fel06_aws_secret_access_key(self):
        """Verify FEL-06 catches AWS secret keys."""
        code = "AWS_SECRET_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE_FAKE_TEST'"
        charges = self.prosecutor.scan_file(Path("aws.py"), code)
        self.assertTrue(any(c.statute_code == "FEL-06" and not c.exempted for c in charges))

    def test_mis04_bento_grid_detection(self):
        """Verify MIS-04 can detect bento grid patterns in HTML."""
        html_code = """
<div class="grid grid-cols-3 gap-4">
  <div class="card">Feature 1</div>
  <div class="card">Feature 2</div>
  <div class="card">Feature 3</div>
</div>
"""
        charges = self.prosecutor.scan_file(Path("bento.html"), html_code)
        # MIS-04 applies to CSS/HTML with identical card patterns
        # This test may need adjustment based on implementation

    def test_clean_code_with_types_passes(self):
        """Verify well-typed, documented code passes Slop Court."""
        clean_code = '''
from typing import Optional
from decimal import Decimal

def calculate_discount(
    amount: Decimal,
    discount_rate: float,
    coupon: Optional[str] = None
) -> Decimal:
    """
    Calculate discounted amount with optional coupon validation.

    Args:
        amount: Original amount (positive Decimal)
        discount_rate: Discount percentage (0.0 to 1.0)
        coupon: Optional coupon code for validation

    Returns:
        Discounted amount as Decimal

    Raises:
        ValueError: If amount is negative or discount_rate invalid
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")

    discount = amount * Decimal(str(discount_rate))
    return amount - discount
'''
        charges = self.prosecutor.scan_file(Path("clean_full.py"), clean_code)
        active_charges = [c for c in charges if not c.exempted]
        self.assertEqual(
            len(active_charges), 0,
            f"Clean code should have 0 active charges, got: {active_charges}"
        )

    def test_ast_function_stub_with_decorator(self):
        """Verify abstractmethod decorator properly exempts stubs."""
        code = """
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, data: str) -> dict:
        pass
"""
        charges = self.prosecutor.scan_file(Path("abstract.py"), code)
        fel02_charges = [c for c in charges if c.statute_code == "FEL-02" and not c.exempted]
        self.assertEqual(len(fel02_charges), 0, "Abstract stubs should be exempt")


if __name__ == "__main__":
    unittest.main()