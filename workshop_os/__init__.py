"""
Workshop OS — The Irreducible Operating Foundation & Code Quality Gate for AI Agents.
"""

from pathlib import Path
import sys

# Ensure repository root is on sys.path when imported as a package
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import workshop_court as court
from scripts import workshop_council as council
from scripts import workshop_skills as skills
from scripts import workshop as cli

__version__ = "3.5.0"
__all__ = ["court", "council", "skills", "cli", "__version__"]
