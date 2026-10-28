---
name: editorial-graphic-design
description: Master human graphic design, Swiss grid systems, typographic scale, and editorial layout architecture. Use when designing posters, brand boards, digital artifacts, web layouts, and book or editorial spreads with zero generic AI slop.
---

# Editorial Graphic Design & Layout Architecture

## 1. Core Philosophy: The Human Designer's Eye

Generic AI design defaults to three predictable clichés:
1. Symmetrical rounded cards floating with soft drop shadows.
2. Clashing high-saturation hazard colors (neon yellow + neon orange on pure black).
3. Monotonous, uncalibrated scale where headers, body copy, and metadata blur together.

Human graphic design—grounded in the lineage of **Josef Müller-Brockmann**, **Armin Hofmann**, **Wim Crouwel**, and **Massimo Vignelli**—treats layout as **spatial tension, typographic mass, and mathematical rhythm**.

---

## 2. The Master Grid Systems

### A. The Swiss Modular Grid
* **The Unit Matrix:** Divide the canvas into an explicit grid (e.g. 12 or 16 columns by 8 or 12 rows).
* **Zero Accidental Positions:** Every edge, baseline, line break, and graphic container must snap directly to a grid coordinate.
* **Asymmetrical Balance:** Balance a massive, heavy typographic anchor on one quadrant with active, purposeful negative space and delicate micro-metadata on the opposing quadrant.

### B. Proportional Margin Ratios (Van de Graaf Canon)
* When designing single-page posters or editorial spreads:
  * Top Margin: $1.0\times$
  * Left/Right Margins: $1.2\times$
  * Bottom Margin: $1.6\times$ (gives the layout gravitational weight and prevents elements from appearing to slide off the bottom).

---

## 3. Typographic Hierarchy & Scale Calculus

### A. The Typographic Scale
Never pick arbitrary font sizes. Use a musical / geometric scale based on a consistent ratio:

| Scale Ratio | Factor | Display Use Cases |
| :--- | :--- | :--- |
| **Major Third** | $1.25$ | High-density technical interfaces, dashboards |
| **Perfect Fourth** | $1.333$ | Editorial articles, books, documentation |
| **Golden Ratio** | $1.618$ | Exhibition posters, architectural monographs, hero covers |

Example 1.333 Scale (Base 12px):
`12px` (Caption/Meta) $\rightarrow$ `16px` (Body) $\rightarrow$ `21px` (H3) $\rightarrow$ `28px` (H2) $\rightarrow$ `38px` (H1) $\rightarrow$ `50px` (Hero Title) $\rightarrow$ `67px` (Monumental Display).

### B. Optical Tracking & Kerning Discipline
* **Display (> 48px):** Tighten tracking ($-20$ to $-40$ units / $-0.02\text{em}$ to $-0.04\text{em}$). Display typography needs architectural density so letters form cohesive wordmarks.
* **Body (14px–18px):** Neutral tracking ($0\text{em}$ to $+0.01\text{em}$).
* **Micro-Data / Captions (< 12px):** Open tracking ($+0.08\text{em}$ to $+0.15\text{em}$). Small uppercase text becomes illegible without generous breathing room between glyphs.

---

## 4. Text Containment & Anti-Spillover Invariants

### The Column Capacity Rule
* **Reading Comfort Window:** 45 to 75 characters per line for body prose.
* **Card & Column Containers:** In narrow multi-column layouts (width $< 300\text{px}$), strictly cap line lengths at **22 to 32 characters**.
* **SVG Hard Constraint:** SVG text elements never wrap automatically. Break multi-line copy into explicit `<tspan>` nodes with calibrated vertical offsets (`dy="18"` or explicit `y` values).
* **Right-Aligned Labels:** Always anchor right-aligned data with `text-anchor="end"` to mathematically eliminate container wall collisions.

---

## 5. Pre-Flight Visual Audit Checklist

Before finalizing any graphic layout or layout artifact:
- [ ] **Grid Locking:** Are all bounding edges aligned to a defined column or row axis?
- [ ] **No Accidental Centering:** Is centering used strictly for monumental symmetrical statements, or did the design default to lazy center-alignment?
- [ ] **Containment Audit:** Does every line of text have at least 16–24px of breathing margin from its surrounding bounding border?
- [ ] **Typographic Mass:** Is there a bold, unmistakable ratio (at least $4:1$ in font size) between the dominant display headline and the body copy?
- [ ] **Negative Space Integrity:** Does the empty space feel active, structural, and deliberate rather than like a forgotten gap?
