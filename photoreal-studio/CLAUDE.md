# Agent Instructions & Project Operating Standard

This project adheres strictly to the Centralized Workshop Operating Standards.

1. **Ingest Master System Prompt**: Read and adopt `.\prompts\UNIVERSAL_SYSTEM_PROMPT.md`
2. **Search Workshop Skills & Tools**: Run `python .\scripts\workshop.py search "<keyword>"`
3. **First-Principles & Multi-Source Research**: Ground all architectural decisions in irreducible axioms, peer-reviewed journals, optical physics, and upstream specs.
4. **Design Tokens & Anti-Slop**: Use `.\ui-ux-arsenal\tokens\design_tokens.json` and follow `.\skills\antislop\SKILL.md`.
5. **Notion Second Brain**:
   - Second Brain: https://app.notion.com/p/AI-AGENT-SECOND-BRAIN-3cc6d0c8ba0c80c1980bcd0a2b601008?source=copy_link
   - Workshop Hub: https://app.notion.com/p/AI-AGENT-WORKSHOP-3cc6d0c8ba0c8097a87bc9dd87c4f922?source=copy_link
6. **Rules**: Zero sycophancy, never truncate code (no `// TODO`s), evidence-based reconnaissance first, deterministic verification.

<!-- antislop:start -->
## antislop
For UI, copy, people, mobile layout, or code comments work, read `./anti-slop/antislop.md` (core) and then the skill for the task:
- Core filter: `./skills/antislop/SKILL.md`
- UI / visual: `./skills/antislop-ui/SKILL.md`
- Copy & text: `./skills/antislop-copywriting/SKILL.md`
- People / accessibility: `./skills/antislop-human/SKILL.md`
- Mobile / responsive: `./skills/antislop-layoutmobile/SKILL.md`
- Code comments: `./skills/antislop-code/SKILL.md`
<!-- antislop:end -->
