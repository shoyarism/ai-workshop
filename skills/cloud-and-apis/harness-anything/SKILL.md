---
source: "https://github.com/yb2460/harness-anything"
name: harness-anything
description: "Use when the user needs an AI agent control hub for WPS Office, Microsoft Office, Zotero, Adobe Illustrator, and more. Provides 47 CLI commands and 27 academic skills for Windows. Also use when converting SVG to PPTX, managing Zotero references, or automating academic workflows. Triggers: 'harness anything', 'cli-anything', 'Zotero automation', 'WPS automation', 'Illustrator CLI', 'SVG to PPTX'."
risk: unknown
---

# Harness Anything Skill

[GitHub](https://github.com/yb2460/harness-anything) · ⭐ 1,578 · Python · MIT

An AI agent control hub with 47 CLI commands for WPS/MS Office, Zotero, and Adobe Illustrator on Windows. Includes 27 academic skills.

## Install

```bash
# WPS / Microsoft Office automation
pip install git+https://github.com/yb2460/cli-anything-wps.git

# Zotero academic agent
cli-anything-zotero --help

# Adobe Illustrator harness
cd illustrator-harness/agent-harness && pip install -e .
```

## When to Use

- User needs to **automate WPS Office or Microsoft Office** via CLI
- User wants to **manage Zotero references** programmatically
- User needs to **control Adobe Illustrator** via CLI on Windows
- User wants to **convert SVG to PPTX** automatically
- User needs **academic writing/review pipelines** (7 skill categories)
- User mentions `cli-anything`, `harness`, or Windows COM automation

## Component 1: cli-anything-wps (47 Commands)

```bash
# Writer (Word Processing)
cli-anything-wps writer new report.docx
cli-anything-wps writer add-paragraph --text "Hello" --style Heading1
cli-anything-wps writer add-table --rows 3 --cols 2
cli-anything-wps writer add-image --path logo.png --width 200
cli-anything-wps writer find-replace --find "old" --replace "new"
cli-anything-wps writer export --format pdf report.pdf

# Calc (Spreadsheets)
cli-anything-wps calc new data.xlsx
cli-anything-wps calc set-cell --sheet 1 --cell A1 --value 100
cli-anything-wps calc add-formula --cell B1 --formula "=A1*2"
cli-anything-wps calc merge-cells --range A1:B2

# Impress (Presentations)
cli-anything-wps impress new deck.pptx
cli-anything-wps impress add-slide --title "Slide 1"
cli-anything-wps impress add-shape --type textbox --x 100 --y 100 --text "Hello"
cli-anything-wps impress export --format png slide1.png
```

**Export formats**: DOCX, XLSX, PPTX, PDF, TXT, HTML, CSV, RTF

## Component 2: cli-anything-zotero (27 Academic Skills)

```bash
# List all skills
cli-anything-zotero skills list

# Search literature
cli-anything-zotero skills search "machine learning" --limit 10

# Research pipelines
cli-anything-zotero skills pipeline original_article
cli-anything-zotero skills pipeline meta_analysis

# Journal formatting
cli-anything-zotero skills journal "Nature"
cli-anything-zotero skills journal "Science"
```

**7 Skill Categories:**

| Category | Skills | Purpose |
|----------|--------|---------|
| search | 3 | Quick search, systematic review, deep literature |
| research | 4 | Idea generation, brainstorming, hypotheses, deep research |
| writing | 5 | Paper writing, IMRAD, citations, outlines, revision |
| review | 5 | 5-person peer review, counter-argument analysis |
| visualization | 4 | Slides, diagrams, posters, journal figures |
| analysis | 3 | Exploratory analysis, statistics, evidence evaluation |
| pipeline | 2 | Full research-to-paper workflow |

## Component 3: Illustrator Harness

```bash
# Project management
cli-anything-illustrator project new logo.ai -w 500 -h 500
cli-anything-illustrator project open existing.ai

# Layers
cli-anything-illustrator layers new --name "background"
cli-anything-illustrator layers set-visible --name "background" --visible false

# Shapes
cli-anything-illustrator shapes rect --x 50 --y 50 --w 200 --h 100 --fill "#FF0000"
cli-anything-illustrator shapes ellipse --cx 300 --cy 200 --rx 50 --ry 30
cli-anything-illustrator shapes line --x1 0 --y1 0 --x2 500 --y2 500

# Text
cli-anything-illustrator text add "Brand Name" --x 100 --y 100 --font Arial --size 72 --color "#000000"

# Export
cli-anything-illustrator export png output.png --resolution 300
cli-anything-illustrator export svg output.svg
cli-anything-illustrator export pdf output.pdf
```

**Requirements**: Windows 10/11 + Adobe Illustrator 2023+ + Python 3.10+ + pywin32 + click

## Component 4: SVG to PPTX

```bash
# Convert SVG to PowerPoint slide
cli-anything-wps impress svg-to-pptx --input diagram.svg --output deck.pptx
```

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| COM automation fails | Ensure WPS/Office is closed before running commands |
| Zotero not connected | Start Zotero desktop app first; CLI connects via COM |
| Illustrator commands fail | Run as same user who has Illustrator installed; check COM registration |
| Path issues on Windows | Use forward slashes or raw strings: `C:/path/to/file` |

## Resources

- **GitHub**: https://github.com/yb2460/harness-anything
- **cli-anything-wps**: https://github.com/yb2460/cli-anything-wps
- **Illustrator Harness**: https://github.com/yb2460/illustrator-harness
