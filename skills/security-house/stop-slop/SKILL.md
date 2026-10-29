---
name: stop-slop
description: >
  Remove AI tells from prose. Detects and fixes: throat-clearing openers, emphatic crutches,
  business jargon, all adverbs, vague declaratives, binary contrasts, staccato fragmentation,
  false agency, narrator-from-a-distance voice, passive voice.
  Reference: https://github.com/hardikpandya/stop-slop
---

# Stop Slop — Remove AI Writing Traces

Teach AI to catch and remove predictable writing patterns that make text sound robotic.

## What It Catches

### Banned Phrases
- Throat-clearing openers ("It is important to note that...")
- Emphatic crutches ("really", "very", "truly")
- Business jargon ("leverage", "utilize", "delve")
- All adverbs
- Vague declaratives
- Meta-commentary

### Structural Clichés
- Binary contrasts ("not X, but Y")
- Negative listings
- Dramatic fragmentation
- Rhetorical setups
- False agency
- Narrator-from-a-distance voice
- Passive voice

## Scoring

Rate 1-10 on each dimension:
- **Directness**: Statements or announcements?
- **Rhythm**: Varied or metronomic?
- **Trust**: Respects reader intelligence?
- **Authenticity**: Sounds human?
- **Density**: Anything cuttable?

Below 35/50: revise.

## Usage

Copy `SKILL.md` and reference files into your agent's skill directory:

```bash
# Clone stop-slop
git clone https://github.com/hardikpandya/stop-slop.git

# Add to Claude Code
cp -r stop-slop ~/.claude/skills/stop-slop
```
