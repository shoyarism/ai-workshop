---
name: vox-inspired-explainer
description: "Newsroom-grade editorial documentary & explainer video production agent skill. Transforms topics into authentic Vox-style investigative explainers using structured evidence, 9-stage narrative arcs, 11 functional visual modes, restrained motion, and machine-readable storyboard schemas."
allowed-tools: Read Write Edit Glob Grep run_command
---

# Vox-Inspired Editorial Explainer Video Production Skill

A deterministic, high-rigor engineering and journalistic pipeline for autonomous AI agents producing broadcast-ready **editorial documentary explainer videos** modeled after Vox's signature investigative format (reference: *How wildlife trade is linked to coronavirus*, YouTube `TPpoJGYlW54`).

<!-- provenance: [Pillar 1: Formal Documentary Journalism & Information Design (Edward Tufte, Richard Saul Wurman), Pillar 2: Upstream Vox Newsroom Explainer Grammar (TPpoJGYlW54), Pillar 3: Web Animations API & GSAP 3.12 / Remotion, Pillar 4: Local Telemetry 1080p@24fps Direct Pipe] -->

---

## 1. CORE OPERATING PRINCIPLE: NEWSROOM EXPLAINER VS. AI SLOP

Most AI video generators mistake the Vox style for "paper collage textures with random sliding cards." **This is false.** 

Real Vox explainer videos are **narrative-driven investigative journalism**:
1. **Narration is King:** The script is written like a lean, forensic podcast or news dispatch. Every visual element exists *only* to advance the viewer's comprehension of the narration.
2. **Every Shot Has a Functional `visual_job`:** Never think *"make a cool cinematic shot of X"*. Always declare: *"This sentence explains geographic distribution $\rightarrow$ use MAP $\rightarrow$ highlight region $\rightarrow$ draw route line at the exact syllable the city is spoken."*
3. **Primary Evidence First:** Authentic declassified documents, hospital blueprints, historical clippings, and empirical charts always take precedence over decorative AI-generated imagery. Any AI recreation must be transparently tagged with a `RECONSTRUCTION` badge.
4. **Restrained, Motivated Motion:** Zero bouncy cartoon easing. Use smooth Ken Burns push-ins (`scale 1.0` to `1.03`), mechanical line draws, ruler reveals, and tactile highlighter swipes.

---

## 2. THE 9-STAGE NARRATIVE ARC

Every Vox-style explainer deconstructs complex topics through this structural trajectory:

```
[ 1. HOOK ] ──▶ [ 2. OBSERVATION ] ──▶ [ 3. QUESTION ] ──▶ [ 4. PRECEDENT ] ──▶ [ 5. MECHANISM ]
                                                                                       │
[ 10. IMPLICATION ] ◀── [ 9. RESPONSE ] ◀── [ 8. CONSEQUENCE ] ◀── [ 7. INCENTIVE / SYSTEM ] ◀─┘
```

1. **HOOK:** A jarring, specific current event or data anomaly that grabs immediate attention without sensationalist clickbait.
2. **OBSERVATION:** Granular inspection of what is happening on the ground (dissecting stereotypes and presenting physical realities).
3. **QUESTION:** The central thesis question that the video promises to systematically solve (e.g., *"Why were wild animals being sold there legally in the first place?"*).
4. **PRECEDENT:** Historical context proving this is part of an ongoing systemic pattern (e.g., the 2002 SARS outbreak).
5. **MECHANISM:** The technical, biological, or physical chain of cause-and-effect (e.g., zoonotic viral transmission pathways).
6. **SYSTEM & POLICY:** The legal statutes, regulations, or institutional architectures that created the condition (e.g., China's 1988 Wildlife Protection Law).
7. **ECONOMIC INCENTIVE:** The money, lobbying power, or economic motivations sustaining the system (e.g., $76 Billion commercial farming lobby).
8. **CONSEQUENCE:** Unintended systemic failures, loopholes, or catastrophic breakdowns.
9. **RESPONSE:** The institutional reaction, emergency decrees, or reform attempts.
10. **IMPLICATION:** The unresolved tension or future systemic vulnerability remaining.

---

## 3. THE 11 FUNCTIONAL VISUAL MODES

Agents must categorize every single beat into one of these 11 mutually exclusive visual modes:

| Visual Mode | Primary `visual_job` | Key Styling & Animation Rules |
| :--- | :--- | :--- |
| `ARCHIVAL` | Historical grounding via newspaper clippings, declassified memos, microfiches. | Paper cutouts (3px white border), subtle multi-layer drop shadows (`0 12px 28px rgba(0,0,0,0.12)`), slight physical rotation ($\pm 1.2^\circ$). |
| `INTERVIEW` | Credible testimony or expert quotation. | Two-line editorial pill lower third with bold uppercase name and muted credentials. |
| `PHOTO` | Direct observation of physical reality. | Slow Ken Burns push (`scale 1.0` to `1.03`), anchoring strictly on focal subject. |
| `DOCUMENT` | Legal statute, policy decree, medical procedure. | Camera pushes into specific clause; translucent yellow felt highlighter animates across critical sentence as spoken. |
| `MAP` | Spatial distribution, vector spread, trade routes. | Muted cream/gray landmass, crisp borders, thin dotted transport lines, red locator pulse. |
| `TIMELINE` | Chronological sequencing and pattern evolution. | Horizontal/vertical thin solid ruler; active year or date scales in with red callout tick. |
| `CHART` | Quantitative comparison or historical trend. | Minimal axes, no decorative 3D slop, direct data labels on bars/lines. |
| `DIAGRAM` | Structural cross-section, biological transmission, technical protocol. | Vector line icons with thin directional flow arrows (`──►`), elevation lines, cross-hatching. |
| `DATA CARD` | High-impact singular statistic. | Massive numeral counter reveal ($0 \to N$) with short context label underneath. |
| `RECONSTRUCTION`| Reenactment or forensic 3D simulation. | **Mandatory:** `RECONSTRUCTION` or `SIMULASI` badge must appear in upper corner. |
| `GRAPHIC TITLE`| Chapter breaks or core thesis question. | Bold grotesque headline on warm paper canvas with highlight wipe. |

---

## 4. END-TO-END PRODUCTION PIPELINE

```
Topic / Source Material
        │
        ▼
[ STEP 1: FORENSIC RESEARCH & EVIDENCE TABLE ]
        │ Extract claims, primary quotes, statutes, statistics, and verifiable dates.
        ▼
[ STEP 2: NARRATIVE SCRIPTING ]
        │ Write 9-stage narrative arc. Time target: ~130-150 words per minute.
        ▼
[ STEP 3: BEAT SHEET SPECIFICATION ]
        │ Generate schema-compliant JSON validating against `storyboard.schema.json`.
        ▼
[ STEP 4: ASSET GATHERING & CUTOUT PREPARATION ]
        │ Gather primary logos, blueprints, official signage, and document scans.
        ▼
[ STEP 5: AUDIO SYNTHESIS & TIMECODE EXTRACTION ]
        │ Synthesize studio VO (Edge-TTS or ElevenLabs) and extract word timestamps via Whisper.
        ▼
[ STEP 6: WEB-NATIVE MOTION GRAPHICS ASSEMBLY ]
        │ Compile into HTML5/GSAP or Remotion project bound to `window.seekToTime(t)`.
        ▼
[ STEP 7: ANTI-SLOP QUALITY GATE (AUDIT) ]
        │ Verify contrast, zero decorative wallpaper, highlighter alignment, and color count.
        ▼
[ STEP 8: HEADLESS DIRECT-PIPE RENDERING ]
        │ Pipe headless Edge frames directly into FFmpeg stdin with AAC master audio.
```

---

## 5. MACHINE-READABLE STYLE SPECIFICATION (`style-spec.yaml`)

All visual styling is governed deterministically by `style-spec.yaml`:
- **Canvas:** 1920x1080 @ 24fps.
- **Ground Background:** Warm Archival Paper (`#F5F2EA`) with fine paper grain and soft edge vignette.
- **Highlighter:** Organic Translucent Yellow Felt Pen (`#FFE500`, alpha: 0.85, blend: multiply).
- **Typography:** Heavy Grotesque Black (Inter / Helvetica Now / Barlow) for headings, Monospaced Uppercase for technical metadata, High-legibility Sans for captions.
- **Audio Standards:** Calm close-mic dialogue (-18 LUFS), ducked documentary music bed (-32 LUFS during speech), restrained analog newsroom SFX (-20 LUFS).

---

## 6. ANTI-SLOP QUALITY CONTROL GATES (MANDATORY AUDIT)

Before any final render is produced, the agent must verify:
- [ ] **Gate 1: Primary Evidence Check:** Are real hospital documents, official signage, or verifiable sources used rather than generic AI art?
- [ ] **Gate 2: Kinetic Synchronicity:** Does the highlighter stroke animate at the *exact second* the highlighted word is vocalized?
- [ ] **Gate 3: Visual Job Purity:** Does every graphic perform a real explanatory task, or is there decorative filler? (Reject any decorative floating shapes).
- [ ] **Gate 4: Color Economy:** Are chromatic colors strictly limited to documentary neutrals plus maximum *two* controlled accents (Yellow marker + Red alert)?
- [ ] **Gate 5: Typography Legibility:** Are on-screen graphics free of wall-of-text paragraphs? (Max 16 words per graphic card).

---

## 7. EXECUTING WITH WORKSHOP CLI

To run the automated production agent for any topic or brief:

```bash
# Ingest brief and generate verified storyboard JSON:
uv run python scripts/vox_production_agent.py storyboard --topic "K3RS Safety Induction" --input "brief.md"

# Synthesize audio and extract exact subtitle timestamps:
uv run python scripts/vox_production_agent.py audio --script "script.txt"

# Assemble web motion graphics and execute headless direct-pipe render:
uv run python scripts/vox_production_agent.py render --storyboard "storyboard.json" --output "output.mp4"
```
