---
source: "https://github.com/Nebutra/MinerU-Skill"
name: mineru-skill
description: "Use when the user needs to parse PDF, Office documents, or images into clean Markdown with LaTeX formulas and tables. Zero-dependency CLI that works with Claude Code, Cursor, and other AI agents. Triggers: 'MinerU', 'PDF to markdown', 'document parser', 'OCR PDF', 'parse PDF', 'convert PDF to markdown', 'MinerU skill'."
risk: unknown
---

# MinerU Skill

[GitHub](https://github.com/Nebutra/MinerU-Skill) · ⭐ 108 · Python · MIT

AI-Native document parser: PDF, Office & images → clean Markdown with LaTeX, tables & OCR. Zero-dependency CLI & skill for Claude Code, Cursor & AI agents.

## Install

```bash
# No pip install needed for basic usage!
# The script uses Python stdlib only with free Agent API
git clone https://github.com/Nebutra/MinerU-Skill.git
cd MinerU-Skill
```

## When to Use

- User needs to **convert PDF to Markdown** for RAG or AI consumption
- User wants to **parse Office documents** (DOCX, XLSX, PPTX) to Markdown
- User needs **OCR on scanned documents** or images
- User wants **LaTeX formula extraction** from academic papers
- User needs to **export to Obsidian, Notion, Logseq** or other PKM tools
- Use when `pdf` skill's pypdf/PyMuPDF approaches aren't sufficient for complex layouts

## Quick Start

```bash
# Parse a PDF (no token needed — uses free Agent API)
python scripts/mineru.py https://example.com/doc.pdf --stdout

# Parse with JSON output
python scripts/mineru.py document.pdf --json

# Parse local file
python scripts/mineru.py report.pdf --stdout > report.md

# With uv (managed Python, zero install)
uv run scripts/mineru.py paper.pdf --stdout

# Parallel batch with resume support
python scripts/mineru.py batch.txt --workers 4 --resume

# Export directly to Obsidian vault
python scripts/mineru.py docs/ --obsidian /path/to/vault
```

## Commands

```bash
# Single file
python scripts/mineru.py <input> [--stdout] [--json] [--output <file>]

# Batch mode
python scripts/mineru.py <file_or_dir> \
  --workers 4 \
  --resume \
  --obsidian /path/to/vault

# Options
--stdout          # Print Markdown to stdout
--json            # Print status as JSON
--output FILE     # Write to file
--workers N       # Parallel workers
--resume          # Resume interrupted batch
--obsidian PATH   # Export directly to Obsidian vault
--logseq PATH     # Export to Logseq
--notion PATH     # Export to Notion
--confluence PATH # Export to Confluence
```

## Supported Input Formats

| Format | OCR | Formulas | Tables | Notes |
|--------|-----|----------|--------|-------|
| PDF | ✅ | ✅ | ✅ | Born-digital & scanned |
| DOCX | ✅ | ✅ | ✅ | Rich formatting preserved |
| XLSX | ✅ | ✅ | ✅ | Charts as images |
| PPTX | ✅ | ✅ | ✅ | Slides as separate docs |
| Images (PNG/JPG) | ✅ | ⚠️ | ⚠️ | OCR only |
| HTML | ✅ | ✅ | ✅ | Structure preserved |

## 17 Delivery Sinks

| Sink | Command Flag |
|------|-------------|
| Obsidian | `--obsidian /path` |
| Logseq | `--logseq /path` |
| SiYuan | `--siyuan /path` |
| Notion | `--notion /path` |
| Confluence | `--confluence /path` |
| OneNote | `--onenote /path` |
| Coda | `--coda /path` |
| Yuque | `--yuque /path` |
| Lark | `--lark /path` |
| Slack | `--slack /path` |
| DingTalk | `--dingtalk /path` |
| WeCom | `--wecom /path` |
| TickTick | `--ticktick /path` |
| Linear | `--linear /path` |
| Airtable | `--airtable /path` |
| Roam Research | `--roam /path` (optional) |
| WPS | `--wps /path` (optional) |

## API Tiers

| Tier | Token Required | Max File | Max Pages | Features |
|------|---------------|----------|-----------|----------|
| **Agent (Free)** | ❌ No | 10 MB | 20 pages | Basic parsing |
| **Standard** | ✅ `MINERU_TOKEN` | 200 MB | 200 pages | Parallel batch, all formats |

```bash
# Upgrade to Standard API
export MINERU_TOKEN=your_token_here
python scripts/mineru.py large_document.pdf --stdout
```

## Comparison Matrix

| Tool | Token-Free | Zero-Install | Offline | Accuracy | Best For |
|------|-----------|--------------|---------|----------|----------|
| **MinerU Skill** | ✅ | ✅ | ⚠️ local option | 90.67 OmniDocBench | Agent workflows, 17 sinks |
| MinerU engine | ✅ | ❌ multi-GB | ✅ | 90.67-95.69 | Maximum accuracy |
| Marker | ✅ | ❌ 3.5-5GB | ✅ | 76.1 olmOCR | Self-hosted |
| Docling (IBM) | ✅ | ⚠️ pip+258M | ✅ | Strong | RAG pipelines |
| LlamaParse | ❌ key | ⚠️ pip | ❌ cloud | Top GenAI | RAG indexes |
| Mathpix | ❌ $19.99 | ✅ | ❌ cloud | Best math | Formula OCR |

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Large files (>10MB) on free tier | Export `MINERU_TOKEN` for Standard API |
| Scanned PDFs slow | Use `--workers 4` for parallel processing |
| Chinese documents | Add `--lang zh` if supported |
| Batch interruption | Use `--resume` to continue from where it left off |
| Formula quality | For complex math, consider Mathpix as fallback |

## Resources

- **GitHub**: https://github.com/Nebutra/MinerU-Skill
- **MinerU Engine**: https://github.com/opendatalab/MinerU
- **Smithery**: https://smithery.ai/skills/nebutra/mineru-skill
