"""
Tests to mechanically verify that all relative documentation links across
the repository root and docs/ directory resolve to valid paths on disk.
Prevents front-door 404 regressions.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestDocumentationLinks(unittest.TestCase):
    """Mechanically audits markdown links to guarantee zero broken references."""

    MD_FILES = [
        ROOT / "README.md",
        ROOT / "WORKSHOP_PROTOCOL.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "SECURITY.md",
        ROOT / "AUTHORS.md",
        ROOT / "docs" / "README.md",
    ]

    LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def test_all_markdown_relative_links_resolve(self):
        broken_links = []
        checked_count = 0

        for md_path in self.MD_FILES:
            if not md_path.exists():
                broken_links.append(f"Missing core document: {md_path}")
                continue

            content = md_path.read_text(encoding="utf-8", errors="ignore")
            matches = self.LINK_PATTERN.findall(content)

            for anchor_text, link_target in matches:
                link_clean = link_target.strip()
                if (
                    link_clean.startswith("http://")
                    or link_clean.startswith("https://")
                    or link_clean.startswith("mailto:")
                    or link_clean.startswith("#")
                ):
                    continue

                # Strip anchor fragments (e.g. #section)
                file_target = link_clean.split("#")[0]
                if not file_target:
                    continue

                # Resolve target relative to the directory containing the markdown file
                resolved_path = (md_path.parent / file_target).resolve()

                checked_count += 1
                if not resolved_path.exists():
                    broken_links.append(
                        f"[{anchor_text}]({link_clean}) in {md_path.relative_to(ROOT)} -> {file_target} does not exist"
                    )

        self.assertGreater(checked_count, 10, "Sanity check: expected to verify multiple docs links")
        self.assertEqual(
            broken_links,
            [],
            f"Detected {len(broken_links)} broken relative documentation link(s):\n" + "\n".join(broken_links),
        )


if __name__ == "__main__":
    unittest.main()
