"""
Slop Court code quality tribunal and Git Bailiff interceptor.
"""
from scripts.workshop_court import (
    Prosecutor,
    SlopCourtMagistrate,
    Bailiff,
    Verdict,
    Indictment,
    render_trial_report,
    main,
)

__all__ = [
    "Prosecutor",
    "SlopCourtMagistrate",
    "Bailiff",
    "Verdict",
    "Indictment",
    "render_trial_report",
    "main",
]

if __name__ == "__main__":
    main()
