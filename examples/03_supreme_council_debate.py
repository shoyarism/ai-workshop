"""
Example 03: Programmatic Supreme Council Invocation
Workshop OS // Universal Supreme Council Dialectic API

Demonstrates how to convene a 4-persona adversarial deliberation panel
programmatically to stress-test an architectural decision before committing.
"""

import sys
from pathlib import Path

# Insert scripts root into sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from workshop_council import UniversalCouncil, render_council_transcript


def main() -> None:
    topic = "Should we migrate from SQLite to distributed PostgreSQL for our 10k DAU backend?"
    domain = "architecture"

    print("=" * 70)
    print(" 🏛️  WORKSHOP OS // UNIVERSAL SUPREME COUNCIL PROGRAMMATIC RUN")
    print(f" Topic  : {topic}")
    print(f" Domain : {domain.upper()}")
    print("=" * 70)

    # 1. Initialize Council for the target domain
    council = UniversalCouncil(domain=domain, seats=4)

    # 2. Convene adversarial deliberation
    session = council.convene(topic=topic, rounds=2)

    # 3. Inspect deliberation results
    print(f"\n[DOCKET] Case Number : {session.case_number}")
    print(f"[BENCH] Seated Personas ({len(session.seated_personas)}):")
    for persona in session.seated_personas:
        print(f"  • {persona.name} ({persona.title}) — [{persona.bias_posture}]")

    print(f"\n[ARGUMENTS EXCHANGED]: {len(session.arguments)}")
    for arg in session.arguments[:2]:
        print(f"  [{arg.persona.name} - {arg.stance} ({arg.conviction}/10)]: {arg.thesis[:80]}...")

    print(f"\n[VOTING OUTCOME]: {session.majority_vote}")
    print(f"  AYE: {session.votes_aye} | NAY: {session.votes_nay} | AMEND: {session.votes_amend}")

    print("\n[MAGISTRATE DECREE]:")
    print(f"  {session.magistrate_decree[:140]}...")

    if session.actionable_injunctions:
        print("\n[ACTIONABLE INJUNCTIONS]:")
        for inj in session.actionable_injunctions:
            print(f"  ✓ {inj}")

    print("\n" + "=" * 70)
    print(" Complete Council Session generated successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
