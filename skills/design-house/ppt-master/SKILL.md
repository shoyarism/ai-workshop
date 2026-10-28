---
name: ppt-master
description: "Generates native, editable PowerPoint (.pptx) presentation decks with professional visual hierarchy, master slide layouts, custom typographic pairings, and data-backed charts."
userFacing: true
---

# 📊 PPT Master: Professional Slide Deck & Presentation Engine

> **Purpose:** Transforms briefs, technical specs, executive memos, and research papers into high-impact, editable PowerPoint presentations (`.pptx`) utilizing master templates, strong typographic hierarchy, and structured visual content blocks.

---

## 1. Editorial Presentation Philosophy

- **Zero Boring Bullet Walls:** Never dump 7 consecutive bullet points onto a plain slide.
- **Content-to-Form Mapping:**
  - 3-Column structured comparison cards for trade-offs and options.
  - Asymmetric split-screen (40% big typography / key metric + 60% structured explanation).
  - Horizontal milestone timeline for roadmaps and deployment phases.
  - Big stat cards with prominent numeric callouts (`+340%`, `0.0ms`) and label subtext.
- **Typographic Scale:**
  - Slide Title: 32–40pt Bold (Tight tracking)
  - Section Header: 20–24pt Medium
  - Body Text: 14–16pt Regular
  - Captions/Metadata: 10–12pt Muted

---

## 2. Technical Execution Pipeline

When generating slides:
1. **Outline Synthesis:** Generate a slide-by-slide narrative structure (Hook $\rightarrow$ Problem $\rightarrow$ Architecture / Solution $\rightarrow$ Data & Benchmarks $\rightarrow$ Next Steps).
2. **Python `python-pptx` Scripting:** Author deterministic Python scripts utilizing `python-pptx` to build the presentation:
   - Configure widescreen 16:9 aspect ratio (`prs.slide_width = Inches(13.333)`, `prs.slide_height = Inches(7.5)`).
   - Define custom color constants (Primary, Neutral Dark, Accent, Muted Gray).
   - Use shapes (`MSO_SHAPE.RECTANGLE`, `MSO_SHAPE.ROUNDED_RECTANGLE`) with clean fills and zero border strokes for structured cards.
3. **Execution & Delivery:**
   - Execute the script to generate the `.pptx` file.
   - Save to workspace or brain directory and surface clickable links.
