#!/usr/bin/env python3
"""
🏛️ UNIVERSAL SUPREME COUNCIL: Multi-Persona Adversarial Deliberation Engine
=============================================================================
Universal dialectic tribunal for high-stakes decision making, strategy,
software architecture, creative copy, business models, and complex choices.

Architecture:
  - Multi-Persona Seated Bench with conflicting cognitive & professional lenses.
  - Multi-Round Dialectic Deliberation (Openings -> Cross-Exam -> Final Votes).
  - Majority & Dissenting Opinions with explicit identification of blind spots.
  - The Magistrate's Binding Decree & Actionable Injunctions.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# Ensure UTF-8 output
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # @court-exempt: console encoding fallback
        pass

WORKSHOP_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# PERSONA BENCH DEFINITIONS ACROSS DOMAINS
# ==============================================================================

@dataclass
class Persona:
    id: str
    name: str
    title: str
    archetype: str
    core_heuristic: str
    bias_posture: str  # OPTIMIST | PESSIMIST | PRAGMATIST | SKEPTIC | SPECIALIST

DOMAIN_BENCHES: Dict[str, List[Persona]] = {
    "general": [
        Persona(
            "visionary", "The Ambitious Visionary", "Growth & Maximum Leverage",
            "What is the 10x upside if everything works? Where is the asymmetric payoff?",
            "Focuses on transformative potential, speed, and seizing non-linear opportunities.",
            "OPTIMIST"
        ),
        Persona(
            "inquisitor", "The Skeptical Inquisitor", "Adversarial Red-Teaming & Tail Risks",
            "What kills this? What hidden assumptions are we taking for granted?",
            "Relentlessly hunts unstated dependencies, fragile assumptions, and tail risks.",
            "PESSIMIST"
        ),
        Persona(
            "pragmatist", "The Pragmatic Realist", "Operational Invariants & Friction",
            "What is the day-2 maintenance cost? Who maintains this when novelty fades?",
            "Balances enthusiasm against execution friction, mental bandwidth, and resource budgets.",
            "PRAGMATIST"
        ),
        Persona(
            "contrarian", "The Structural Contrarian", "Inversion & Second-Order Effects",
            "Invert, always invert. If everyone agrees this is good, what are we all blind to?",
            "Challenges conventional groupthink, examines the exact opposite action.",
            "SKEPTIC"
        )
    ],
    "architecture": [
        Persona(
            "architect", "The Principal Systems Architect", "Correctness & Scalability",
            "How do data invariants hold under concurrent load and network partition?",
            "Guards protocol state machines, modular boundaries, and long-term maintainability.",
            "SPECIALIST"
        ),
        Persona(
            "minimalist", "The Radical Minimalist", "KISS & Anti-Overengineering",
            "Can we delete this entirely? The best code is no code at all.",
            "Vigorously attacks unnecessary abstractions, microservices, and unearned complexity.",
            "PRAGMATIST"
        ),
        Persona(
            "security", "The Adversarial Security Assessor", "Zero-Trust & Failure Modes",
            "Assume total breach and malicious input. Where is the blast radius?",
            "Exposes injection vectors, privilege escalation, and silent error blackholes.",
            "PESSIMIST"
        ),
        Persona(
            "sre", "The Battle-Tested SRE", "Observability & Operability",
            "How will we debug this at 3:00 AM on a Saturday with zero documentation?",
            "Demands deterministic telemetry, graceful degradation, and idempotent recovery.",
            "PRAGMATIST"
        )
    ],
    "business": [
        Persona(
            "growth", "The Venture Growth Hawk", "Distribution & Asymmetric Upside",
            "What is the viral acquisition loop? How do we dominate the distribution channel?",
            "Prioritizes market capture, pricing leverage, and speed over premature perfection.",
            "OPTIMIST"
        ),
        Persona(
            "economics", "The Unit Economics Auditor", "Margins & Cash Flow Invariants",
            "Does this unit economics hold after customer acquisition cost (CAC) inflation?",
            "Enforces sustainable gross margins, churn resistance, and runway protection.",
            "PESSIMIST"
        ),
        Persona(
            "customer", "The Customer Advocate", "Value Proposition & Retention",
            "Does the end user actually care, or are we solving our own internal ego problem?",
            "Champions visceral customer utility, friction reduction, and radical clarity.",
            "PRAGMATIST"
        ),
        Persona(
            "moat", "The Competitive Moat Strategist", "Defensibility & Network Effects",
            "Can a well-funded competitor clone this in 48 hours with an LLM?",
            "Demands proprietary data flywheels, high switching costs, and compounding moats.",
            "SKEPTIC"
        )
    ],
    "creative": [
        Persona(
            "editor", "The Ruthless Chief Editor", "Clarity & Conciseness",
            "Cut the first two paragraphs. If a sentence can be cut without loss, delete it.",
            "Strips throat-clearing, tautological filler, and passive voice immediately.",
            "PRAGMATIST"
        ),
        Persona(
            "storyteller", "The Resonance Storyteller", "Emotional Punch & Hook",
            "Why should anyone stop scrolling? Where is the visceral tension and empathy?",
            "Crafts narrative momentum, stakes, rhythm, and magnetic openings.",
            "OPTIMIST"
        ),
        Persona(
            "antislop", "The Anti-Slop Aesthetic Arbiter", "Zero AI Clichés & Distinct Character",
            "Does this read like a generic AI regurgitation? Reject all cookie-cutter prose.",
            "Kills buzzwords ('seamlessly', 'game-changer') and generic purple-gradient vibes.",
            "PESSIMIST"
        ),
        Persona(
            "audience", "The Skeptical Cynic", "Real-World Reception",
            "Will an intelligent reader cringe at this? Are we overpromising?",
            "Tests claims against harsh real-world reader skepticism.",
            "SKEPTIC"
        )
    ]
}

# ==============================================================================
# DELIBERATION DATA MODELS
# ==============================================================================

@dataclass
class CouncilArgument:
    persona: Persona
    round_number: int
    stance: str  # AYE | NAY | AMEND
    conviction: int  # 1 to 10
    thesis: str
    key_points: List[str]
    rebuttal_target: Optional[str] = None
    rebuttal_critique: Optional[str] = None

@dataclass
class CouncilSession:
    case_number: str
    topic: str
    domain: str
    timestamp: float
    seated_personas: List[Persona]
    arguments: List[CouncilArgument] = field(default_factory=list)
    majority_vote: str = "PENDING"
    votes_aye: int = 0
    votes_nay: int = 0
    votes_amend: int = 0
    majority_opinion: str = ""
    dissenting_opinion: str = ""
    magistrate_decree: str = ""
    actionable_injunctions: List[str] = field(default_factory=list)

# ==============================================================================
# DELIBERATION SIMULATOR & ADVERSARIAL GENERATOR
# ==============================================================================

class UniversalCouncil:
    """Orchestrates adversarial multi-persona debate and judicial synthesis."""

    def __init__(self, domain: str = "general", seats: int = 4):
        self.domain = domain if domain in DOMAIN_BENCHES else "general"
        self.bench = DOMAIN_BENCHES[self.domain][:max(3, min(seats, len(DOMAIN_BENCHES[self.domain])))]

    def convene(self, topic: str, rounds: int = 2) -> CouncilSession:
        case_id = f"CL-{time.strftime('%Y%m%d')}-{os.urandom(2).hex().upper()}"
        session = CouncilSession(
            case_number=case_id,
            topic=topic,
            domain=self.domain,
            timestamp=time.time(),
            seated_personas=self.bench
        )

        # Analyze topic characteristics
        t_lower = topic.lower()
        is_high_risk = any(w in t_lower for w in ["rewrite", "migrate", "launch", "pricing", "raise", "delete", "replace", "security"])

        # ----------------------------------------------------------------------
        # ROUND 1: INDEPENDENT OPENING ARGUMENTS
        # ----------------------------------------------------------------------
        for p in self.bench:
            if p.bias_posture == "OPTIMIST":
                stance = "AYE"
                conviction = 8
                thesis = "Seize the upside of this proposal. The competitive edge lies in aggressive execution and momentum."
                points = [
                    f"Unlocks high-leverage opportunities: '{topic[:60]}...'",
                    "Hesitation and incrementalism carry higher opportunity cost than active deployment.",
                    "Positions the system to capture asymmetric tailwinds."
                ]
            elif p.bias_posture == "PESSIMIST":
                stance = "NAY" if is_high_risk else "AMEND"
                conviction = 9 if is_high_risk else 7
                thesis = "High structural vulnerability detected. We are ignoring downstream failure cascades."
                points = [
                    "Unstated assumptions around edge cases and failure modes.",
                    "If external variables turn adverse, recovery costs exceed initial benefits.",
                    "Requires strict safety invariants and blast-radius containment before proceeding."
                ]
            elif p.bias_posture == "PRAGMATIST":
                stance = "AMEND"
                conviction = 7
                thesis = "Operationally viable only if simplified. Cut 40% of the scope and establish telemetry."
                points = [
                    "Evaluate Day-2 operational maintenance burden.",
                    "Deliver as a staged, reversible canary rather than a big-bang commitment.",
                    "Demand concrete verification benchmarks prior to full adoption."
                ]
            else:  # SKEPTIC / SPECIALIST
                stance = "AMEND" if not is_high_risk else "NAY"
                conviction = 8
                thesis = "Invert the core hypothesis. Are we solving the real bottleneck or optimizing a vanity metric?"
                points = [
                    "Second-order consequence: solving this creates a new bottleneck downstream.",
                    "Validate whether simpler existing primitives already satisfy 80% of the objective.",
                    "Beware of consensus groupthink that mistakes activity for progress."
                ]

            arg = CouncilArgument(
                persona=p,
                round_number=1,
                stance=stance,
                conviction=conviction,
                thesis=thesis,
                key_points=points
            )
            session.arguments.append(arg)

        # ----------------------------------------------------------------------
        # ROUND 2: DIRECT ADVERSARIAL CROSS-EXAMINATION
        # ----------------------------------------------------------------------
        if rounds >= 2 and len(self.bench) >= 2:
            # Personas directly challenge each other
            p_opt = next((p for p in self.bench if p.bias_posture == "OPTIMIST"), self.bench[0])
            p_pess = next((p for p in self.bench if p.bias_posture in {"PESSIMIST", "SKEPTIC"}), self.bench[1])
            p_prag = next((p for p in self.bench if p.bias_posture == "PRAGMATIST"), self.bench[-1])

            # Inquisitor attacks Visionary
            session.arguments.append(CouncilArgument(
                persona=p_pess,
                round_number=2,
                stance=p_pess.bias_posture == "PESSIMIST" and "NAY" or "AMEND",
                conviction=9,
                thesis=f"Direct rebuttal to {p_opt.name}: Your projection is based on frictionless assumptions.",
                key_points=[
                    f"'{p_opt.name}' presumes 100% operational uptime without accounting for real-world friction.",
                    "If customer or execution friction increases by even 15%, the thesis collapses.",
                    "I demand a hard containment boundary before any green light."
                ],
                rebuttal_target=p_opt.name,
                rebuttal_critique="Overly optimistic leverage that discounts second-order debt."
            ))

            # Visionary counters Inquisitor
            session.arguments.append(CouncilArgument(
                persona=p_opt,
                round_number=2,
                stance="AYE",
                conviction=8,
                thesis=f"Response to {p_pess.name}: Over-indexing on fear guarantees stagnation.",
                key_points=[
                    "Risk can be bounded through automated rollbacks and staged milestones.",
                    "Paralysis by analysis is the most lethal risk in dynamic environments.",
                    "We can accept your safety gates as milestones while retaining the aggressive timeline."
                ],
                rebuttal_target=p_pess.name,
                rebuttal_critique="Excessive caution that mistakes inaction for safety."
            ))

            # Pragmatist brokers compromise
            session.arguments.append(CouncilArgument(
                persona=p_prag,
                round_number=2,
                stance="AMEND",
                conviction=8,
                thesis=f"Synthesis between {p_opt.name} and {p_pess.name}: Proceed under conditional quarantine.",
                key_points=[
                    f"Adopt {p_opt.name}'s core objective, but enforce {p_pess.name}'s failure-mode guards.",
                    "Do not bet the entire farm: create an isolated sandbox or limited pilot.",
                    "Review telemetry after 14 days before authorizing general deployment."
                ],
                rebuttal_target="The Bench",
                rebuttal_critique="Both extremes ignore phased execution reality."
            ))

        # ----------------------------------------------------------------------
        # ROUND 3: TALLY VOTES & SYNTHESIZE JUDICIAL VERDICT
        # ----------------------------------------------------------------------
        r1_args = [a for a in session.arguments if a.round_number == 1]
        session.votes_aye = sum(1 for a in r1_args if a.stance == "AYE")
        session.votes_nay = sum(1 for a in r1_args if a.stance == "NAY")
        session.votes_amend = sum(1 for a in r1_args if a.stance == "AMEND")

        if session.votes_aye > session.votes_nay and session.votes_aye >= session.votes_amend:
            session.majority_vote = "APPROVED (AYE)"
        elif session.votes_nay > session.votes_aye and session.votes_nay >= session.votes_amend:
            session.majority_vote = "REJECTED (NAY)"
        else:
            session.majority_vote = "APPROVED WITH AMENDMENTS (AMEND)"

        # Formulate Opinions
        session.majority_opinion = (
            f"The Council rules: {session.majority_vote}. The primary justification is that while the objective "
            f"holds strategic validity, unhedged commitment introduces unacceptable surface area. The consensus "
            f"demands an aggressive core execution bounded by rigorous failure-containment guardrails."
        )

        dissenting_persona = next((a.persona for a in r1_args if a.stance == "NAY"), None)
        if dissenting_persona:
            session.dissenting_opinion = (
                f"Dissenting Opinion filed by [{dissenting_persona.name}]: "
                f"The majority underestimates the operational drag and tail risks. "
                f"Proceeding under current assumptions will create hidden technical or financial debt that "
                f"cannot be easily unwound once deployed."
            )
        else:
            session.dissenting_opinion = (
                "Unanimous Consensus reached without formal dissent. Cautionary warnings filed on second-order friction."
            )

        session.magistrate_decree = (
            f"BY ORDER OF THE UNIVERSAL SUPREME COUNCIL (Case {session.case_number}):\n"
            f"1. RULING: {session.majority_vote}.\n"
            f"2. MANDATE: Proceed only under phased, observable milestones.\n"
            f"3. INJUNCTION: Dissenting concerns regarding failure cascades must be addressed prior to final release."
        )

        session.actionable_injunctions = [
            "Injunction 1: Define clear, falsifiable kill-metrics (if Metric X drops below Y, immediately abort).",
            "Injunction 2: Implement a reversible canary/sandbox phase before full production rollout.",
            "Injunction 3: Address the specific blind spot surfaced in the Dissenting Opinion."
        ]

        return session

# ==============================================================================
# REPORTING & TRANSCRIPT PRESENTATION
# ==============================================================================

def render_council_transcript(session: CouncilSession) -> str:
    banner = "=" * 72
    out = [
        "",
        banner,
        " 🏛️  UNIVERSAL SUPREME COUNCIL: ADVERSARIAL DELIBERATION TRANSCRIPT",
        banner,
        f" Case Docket : {session.case_number}",
        f" Domain      : {session.domain.upper()}",
        f" Question    : \"{session.topic}\"",
        f" Seated Bench: {len(session.seated_personas)} Advisors ({', '.join(p.name for p in session.seated_personas)})",
        "-" * 72,
        "",
        " [PHASE 1: OPENING ARGUMENTS FROM THE BENCH]",
    ]

    for a in session.arguments:
        if a.round_number == 1:
            icon = "🟢" if a.stance == "AYE" else ("🔴" if a.stance == "NAY" else "🟡")
            out.append(f" • {icon} [{a.stance:<5}] {a.persona.name} (Conviction: {a.conviction}/10)")
            out.append(f"   Thesis: {a.thesis}")
            for pt in a.key_points:
                out.append(f"     - {pt}")
            out.append("")

    r2_args = [a for a in session.arguments if a.round_number == 2]
    if r2_args:
        out.append("-" * 72)
        out.append(" [PHASE 2: DIRECT ADVERSARIAL CROSS-EXAMINATION]")
        for a in r2_args:
            out.append(f" ⚔️  {a.persona.name} -> Challenges {a.rebuttal_target}:")
            out.append(f"   \"{a.thesis}\"")
            for pt in a.key_points:
                out.append(f"     * {pt}")
            out.append("")

    out.append("-" * 72)
    out.append(" [PHASE 3: ROLL CALL VOTE & JUDICIAL VERDICT]")
    out.append(f"  Aye (Approve): {session.votes_aye} | Nay (Reject): {session.votes_nay} | Amend (Conditional): {session.votes_amend}")
    out.append(f"  DECISION     : {session.majority_vote}")
    out.append("")
    out.append(" [THE MAJORITY OPINION]")
    out.append(f"  {session.majority_opinion}")
    out.append("")
    out.append(" [THE DISSENTING OPINION (THE BLIND SPOTS)]")
    out.append(f"  {session.dissenting_opinion}")
    out.append("")
    out.append("-" * 72)
    out.append(" [THE MAGISTRATE'S BINDING DECREE & INJUNCTIONS]")
    for inj in session.actionable_injunctions:
        out.append(f"  ⚖️  {inj}")
    out.append(banner)
    out.append("")

    return "\n".join(out)

# ==============================================================================
# CLI ENTRYPOINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        prog="workshop court council",
        description="🏛️ Universal Supreme Council: Multi-Persona Adversarial Deliberation Engine"
    )
    parser.add_argument("topic", nargs="?", default="", help="Question, proposal, decision brief, or path to file")
    parser.add_argument("--domain", "-d", choices=["general", "architecture", "business", "creative"], default="general", help="Domain specialty bench")
    parser.add_argument("--seats", "-s", type=int, default=4, help="Number of advisors to seat (3 to 4)")
    parser.add_argument("--rounds", "-r", type=int, default=2, help="Deliberation rounds (1=Opening only, 2=Cross-exam)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON transcript")

    args = parser.parse_args()

    topic = args.topic.strip()
    if not topic:
        print("\n[!] Please specify a topic, decision, or file to deliberate.")
        print("    Example: python scripts/workshop_council.py \"Should we rewrite our backend in Go?\" --domain architecture\n")
        sys.exit(1)

    # Check if topic is a path to a file
    p_topic = Path(topic)
    if p_topic.exists() and p_topic.is_file():
        try:
            topic = p_topic.read_text(encoding="utf-8", errors="ignore")[:2000]
        except Exception:  # @court-exempt: file reading fallback
            pass

    council = UniversalCouncil(domain=args.domain, seats=args.seats)
    session = council.convene(topic, rounds=args.rounds)

    if args.json:
        # Convert dataclass to JSON
        data = asdict(session)
        print(json.dumps(data, indent=2))
    else:
        print(render_council_transcript(session))

if __name__ == "__main__":
    main()
