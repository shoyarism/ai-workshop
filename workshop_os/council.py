"""
Universal Supreme Council multi-persona dialectic engine.
"""
from scripts.workshop_council import (
    UniversalCouncil,
    Persona,
    CouncilSession,
    CouncilArgument,
    render_council_transcript,
    main,
)

__all__ = [
    "UniversalCouncil",
    "Persona",
    "CouncilSession",
    "CouncilArgument",
    "render_council_transcript",
    "main",
]

if __name__ == "__main__":
    main()
