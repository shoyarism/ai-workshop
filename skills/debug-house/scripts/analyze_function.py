#!/usr/bin/env python3
"""
Adversarial Debugging Analyzer
==============================
Analyzes Python functions for adversarial failure modes, boundary conditions,
and tail risks that standard testing might miss.

Usage:
    python scripts/analyze_function.py <function_path> [--mode MODE]
    python scripts/analyze_function.py myapp.handlers.process_payment --mode full-spectrum
"""

import ast
import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception as recon_error:
        sys.stderr.write(f"[debug] UTF-8 reconfigure skipped: {recon_error}\n")


class AdversarialAnalyzer(ast.NodeVisitor):
    """AST-based analysis of potential failure modes."""

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.issues: List[Dict[str, Any]] = []
        self.dangerous_patterns: List[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Analyze function for adversarial vulnerabilities."""
        issues = []

        # Check for missing type hints
        has_return_hint = node.returns is not None
        if not has_return_hint:
            issues.append({
                "type": "MISSING_RETURN_TYPE",
                "severity": "LOW",
                "message": f"Function '{node.name}' lacks return type annotation",
                "line": node.lineno
            })

        # Check for bare except
        for child in ast.walk(node):
            if isinstance(child, ast.ExceptHandler):
                if child.type is None:
                    issues.append({
                        "type": "BAREExcept",
                        "severity": "HIGH",
                        "message": "Bare 'except:' catches all exceptions - should log and re-raise",
                        "line": child.lineno
                    })

        # Check for mutable default arguments
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                issues.append({
                    "type": "MUTABLE_DEFAULT",
                    "severity": "MEDIUM",
                    "message": f"Mutable default argument in '{node.name}'",
                    "line": default.lineno
                })

        # Check for if/else chains with potential dead code
        if_stats = []
        for child in ast.walk(node):
            if isinstance(child, ast.If):
                if_stats.append(child)

        if len(if_stats) > 3:
            issues.append({
                "type": "POSSIBLE_DEAD_CODE",
                "severity": "MEDIUM",
                "message": f"Deep if/else chain may hide dead code paths",
                "line": node.lineno
            })

        self.issues.extend(issues)
        self.generic_visit(node)


def analyze_source_file(file_path: Path) -> Dict[str, Any]:
    """Analyze a Python source file for adversarial issues."""
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

    # Parse AST
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"error": f"Syntax Error: {e}"}

    analyzer = AdversarialAnalyzer(source)
    analyzer.visit(tree)

    return {
        "file": str(file_path),
        "lines": len(source.splitlines()),
        "issues_found": len(analyzer.issues),
        "issues": analyzer.issues,
        "risk_score": compute_risk_score(analyzer.issues)
    }


def compute_risk_score(issues: List[Dict[str, Any]]) -> float:
    """Compute adversarial debugging risk score (0-100)."""
    severity_weights = {"HIGH": 10, "MEDIUM": 3, "LOW": 1}
    total = sum(severity_weights.get(i["severity"], 1) for i in issues)
    return min(100.0, total * 2.5)  # Scale to 0-100


def main():
    parser = argparse.ArgumentParser(
        description="Adversarial Debugging Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "target",
        help="Function path (module.function) or Python file path"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["basic", "full-spectrum", "boundary-smash"],
        default="basic",
        help="Analysis mode"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON"
    )

    args = parser.parse_args()
    target = args.target

    # Resolve path
    target_path = Path(target)
    if not target_path.exists():
        # Try as module.function path
        parts = target.split(".")
        if len(parts) >= 2:
            module_path = Path("/".join(parts[:-1] + ["__init__.py"]))
            if module_path.exists():
                target_path = module_path
            else:
                print(f"[!] Path not found: {target}")
                sys.exit(1)
        else:
            print(f"[!] Invalid target: {target}")
            sys.exit(1)

    result = analyze_source_file(target_path)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    if "error" in result:
        print(f"[!] {result['error']}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print(" ⚔️  ADVERSARIAL DEBUGGING ANALYSIS REPORT")
    print("=" * 70)
    print(f" File: {result['file']}")
    print(f" Lines: {result['lines']}")
    print(f" Risk Score: {result['risk_score']:.1f}/100")
    print("-" * 70)

    if result["issues_found"] == 0:
        print(" [✓] No adversarial vulnerabilities detected.")
        print("     (This is rare - run with --mode full-spectrum)")
    else:
        print(f" [!] Found {result['issues_found']} potential issues:\n")
        for issue in result["issues"]:
            sev_icon = "🔴" if issue["severity"] == "HIGH" else ("🟠" if issue["severity"] == "MEDIUM" else "🟡")
            print(f"  {sev_icon} [{issue['severity']}] {issue['type']}")
            print(f"      Line {issue['line']}: {issue['message']}\n")

    print("=" * 70)
    print("\n Recommended Actions:")
    if result["risk_score"] > 50:
        print("  - HIGH RISK: Implement defensive type hints and input validation")
        print("  - Add circuit breakers for external calls")
        print("  - Run property-based testing with Hypothesis")
    elif result["risk_score"] > 20:
        print("  - Run boundary condition tests with edge cases")
        print("  - Add structured logging for error paths")
    else:
        print("  - Good baseline, consider chaos monkey testing")
    print("=" * 70)


if __name__ == "__main__":
    main()