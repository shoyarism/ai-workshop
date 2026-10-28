---
source: "https://github.com/deckflow/deckprobe"
name: deckprobe
description: "Use when the user needs to inspect document metadata without opening the file — PDF, DOCX, XLSX, PPTX, or Apple iWork files. Returns structured JSON with confidence scores, evidence paths, and measured I/O cost. Rust CLI + WASM SDK. Triggers: 'probe document', 'document metadata', 'deckprobe', 'inspect PDF', 'check PPTX', 'document preflight'."
risk: low
---

# DeckProbe

[GitHub](https://github.com/deckflow/deckprobe) · ⭐ 92 · Rust · MIT

`ffprobe` for documents — probe PDF, Microsoft Office, and Apple iWork files without opening them. Returns structured JSON with confidence, evidence, and measured I/O cost.

## Install

```bash
# Download pre-built binary
# https://github.com/deckflow/deckprobe/releases

# Or via cargo
cargo install deckprobe

# Browser WASM SDK
npm install deckprobe-wasm
```

## When to Use

- User needs to **inspect document metadata** without rendering/opening
- User wants to **determine document type, page count, or structure** before processing
- User needs **confidence scores** for document parsing decisions
- User is building **document routing pipelines** (decide parse → render → reject)
- User mentions `deckprobe`, `document probe`, `ffprobe for documents`, or `preflight`

## Quick Start

```bash
# Get slide count from PPTX
deckprobe --pretty -t slide_count deck.pptx

# Get page count from PDF
deckprobe --pretty -t page_count document.pdf

# Get word count from DOCX
deckprobe --pretty -t word_count report.docx

# Full probe (all targets)
deckprobe --pretty document.pptx
```

## CLI Reference

```bash
deckprobe [OPTIONS] <input>

# Positional
<input>          # Document file path

# Options
-t, --target <target>    # Specific target to probe (can repeat)
--pretty                 # Human-readable JSON output
--json                   # Machine-readable JSON (default)
--confidence <level>     # Minimum confidence: low|medium|high
--cost-limit <bytes>     # Max I/O cost in bytes
--help, -h               # Show help
--version, -v            # Show version
```

## Supported Targets

| Target | Format | Description |
|--------|--------|-------------|
| `page_count` | PDF, PPTX, DOCX | Number of pages/slides |
| `slide_count` | PPTX | Number of slides |
| `word_count` | DOCX | Word count |
| `char_count` | DOCX | Character count |
| `table_count` | DOCX, XLSX | Number of tables |
| `image_count` | DOCX, PPTX | Number of images |
| `chart_count` | XLSX, PPTX | Number of charts |
| `sheet_count` | XLSX | Number of sheets |
| `form_count` | DOCX | Number of form fields |
| `comment_count` | DOCX, XLSX | Number of comments |
| `outline` | DOCX, PPTX | Document outline/headings |
| `format` | All | Document format detection |
| `size` | All | File size |
| `created` | All | Creation timestamp |
| `modified` | All | Last modified timestamp |
| `author` | All | Document author |
| `title` | All | Document title |

## Output Format

```json
{
  "driver": { "id": "powerpoint", "profile": "pptx" },
  "results": {
    "slide_count": {
      "status": "resolved",
      "value": 31,
      "confidence": "high",
      "path": "/ppt/presentation.xml",
      "io_cost": 1024
    },
    "format": {
      "status": "resolved",
      "value": "pptx",
      "confidence": "high"
    }
  },
  "metadata": {
    "total_io_cost": 2048,
    "probes_run": 2,
    "time_ms": 45
  }
}
```

## Decision Logic

DeckProbe helps agents decide what to do with a document:

```bash
# Check if file is valid before full parse
deckprobe -t format document.pdf
# → {"format": {"status": "resolved", "value": "pdf", "confidence": "high"}}

# Check page count to estimate processing time
deckprobe -t page_count large_report.pdf
# → {"page_count": {"status": "resolved", "value": 150, "confidence": "high"}}

# Reject suspicious files
deckprobe -t format suspicious.docx
# → {"format": {"status": "unresolved", "confidence": "low"}}
```

## Runtime Role in DeckFlow

| Engine | Responsibility |
|--------|---------------|
| **DeckProbe** | Inspect and expose bounded preflight signals |
| **DeckParse** | Make document content operable as persistent state |
| **DeckRender** | Produce visual representations |

DeckProbe provides the **evidence** for routing decisions; it does not automatically choose or execute downstream actions.

## Comparison with alternatives

| Tool | Format Support | JSON Output | Confidence | WASM SDK |
|------|---------------|-------------|------------|----------|
| **DeckProbe** | PDF, Office, iWork | ✅ | ✅ | ✅ |
| `file` command | All | ❌ | ❌ | ❌ |
| Python `python-magic` | All | ❌ | ❌ | ❌ |
| PDF metadata tools | PDF only | ✅ | ❌ | ❌ |

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Corrupted files | Check `confidence` field — low confidence may indicate corruption |
| Large files | Use `--cost-limit` to bound I/O |
| Untrusted documents | Probe before opening; never feed untrusted files to renderers without probe |
| iWork files | Ensure macOS or appropriate decoder is available |

## Resources

- **GitHub**: https://github.com/deckflow/deckprobe
- **Installation Guide**: https://github.com/deckflow/deckprobe/blob/main/docs/INSTALLATION.md
- **CLI Reference**: https://github.com/deckflow/deckprobe/blob/main/docs/CLI-REFERENCE.md
