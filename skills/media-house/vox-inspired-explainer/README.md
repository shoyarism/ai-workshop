# Vox-Inspired Editorial Explainer Video Production Skill Pack

A comprehensive, production-grade AI agent skill package for orchestrating **editorial documentary and newsroom-style explainer videos** inspired by Vox's signature investigative video series (e.g. *How wildlife trade is linked to coronavirus*, YouTube `TPpoJGYlW54`).

---

## 📦 Package Contents

```
vox-inspired-explainer/
├── SKILL.md                   # Core instruction manual & agent protocols
├── style-spec.yaml            # Machine-readable style lock (colors, fonts, camera, audio, QC gates)
├── storyboard.schema.json     # Strict JSON schema for deterministic storyboard generation
├── EXAMPLE_STORYBOARD.json    # Full reference storyboard deconstructing the Vox Coronavirus investigation
├── README.md                  # Package overview and architectural principles
├── templates/
│   ├── master-agent-prompt.md # System prompt establishing the Newsroom Director persona
│   └── scene-prompt.md        # Per-beat animation code and asset prompt generator
└── tools/
    └── README.md              # Documentation of Edge-TTS, ElevenLabs, Playwright, Remotion, and FFmpeg
```

---

## 🎯 The Vox Grammar vs. Generic AI Slop

| Feature | Generic AI Video Generator | Vox Newsroom Explainer Protocol |
| :--- | :--- | :--- |
| **Philosophy** | "Make a cool cinematic video about X" | Narration-driven investigative journalism: every shot has an explicit `visual_job` |
| **Aesthetic** | Cyberpunk gradients, dark glowing UI cards, floating 3D balls | Warm archival paper (`#F5F2EA`), declassified scans, tactile photo cutouts, felt highlighter |
| **Visual Taxonomy** | Random AI landscape cuts | 11 strict functional modes: `ARCHIVAL`, `INTERVIEW`, `PHOTO`, `DOCUMENT`, `MAP`, `TIMELINE`, `CHART`, `DIAGRAM`, `DATA CARD`, `RECONSTRUCTION`, `GRAPHIC TITLE` |
| **Motion** | Constant bouncy eases, dizzying zoom transitions | Restrained Ken Burns camera push, mechanical line draws, highlighter wipes synchronized to spoken words |
| **Evidence** | Hallucinated visuals treated as reality | Primary source provenance cited per beat; AI recreations transparently tagged `RECONSTRUCTION` |

---

## 🚀 Autonomous Pipeline

Agents follow a deterministic 8-step pipeline:

$$\text{Research} \longrightarrow \text{Evidence Table} \longrightarrow \text{Script} \longrightarrow \text{Beat Sheet (JSON)} \longrightarrow \text{Asset Manifest} \longrightarrow \text{Audio Sync} \longrightarrow \text{Assembly} \longrightarrow \text{Render}$$

1. Ingest topic or source document.
2. Build an Evidence Table of verified facts, dates, statutes, and figures.
3. Write voiceover narration structured by the 9-stage narrative arc.
4. Output schema-valid `storyboard.json` using `storyboard.schema.json`.
5. Prepare authentic cutouts, blueprints, and signage assets.
6. Synthesize studio voiceover with millisecond word timestamps.
7. Assemble web-native motion graphics or Remotion timeline.
8. Direct-pipe render 1080p @ 24fps via headless browser to FFmpeg stdin.
