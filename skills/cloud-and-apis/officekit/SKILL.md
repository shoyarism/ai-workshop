---
source: "https://github.com/dream-zjk/officekit"
name: officekit
description: "Use when the user needs a friendly Python library and CLI for reading, creating, editing, and filling Office documents (.docx, .xlsx, .pptx). Offers path-based addressing, atomic batch edits, structured JSON output, and an MCP server. Triggers: 'officekit', 'office document automation', 'Python Office CLI', 'atomic batch edit document'."
risk: low
---

# OfficeKit Skill

[GitHub](https://github.com/dream-zjk/officekit) · ⭐ 110 · Python · MIT

A friendly toolkit to read, create, edit, and fill Office documents — built for humans and AI agents alike. Pure-Python on top of `python-docx` / `openpyxl` / `python-pptx`. No Office install needed.

## Install

```bash
pip install officekit
# With MCP server support:
pip install "officekit[mcp]"
```

## When to Use

- User wants a **Python library** for Office automation (not just CLI)
- User needs **MCP server** integration for AI agents
- User wants **atomic batch edits** with automatic rollback on failure
- User prefers **path-based addressing** (`/slides[1]/shapes[2]`)
- Use when OfficeCLI is unavailable or a lighter Python-native alternative is preferred

## Quick Start

```bash
# Read document text
officekit text report.docx

# View structure
officekit view report.docx --mode outline
officekit view report.docx --mode stats
officekit view report.docx --mode issues

# Query elements
officekit query deck.pptx "/slides[1]/shapes[2]"

# Set properties
officekit set deck.pptx "/slides[1]/shapes[1]" --value "New Title"

# Add elements
officekit add deck.pptx slide --value "Second Slide"

# Remove elements
officekit remove deck.pptx "/slides[2]"

# Create new document
officekit create docx invoice.docx --title "Invoice"

# Merge/fill template
officekit merge invoice-template.docx out.docx \
  --data '{"client":"Acme","amount":"$1,200"}'

# Import tabular data
officekit import book.xlsx People data.csv --header
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `text <file>` | Extract all visible text |
| `view <file> --mode <outline\|stats\|issues>` | Inspect document structure |
| `query <file> <path>` | Get element at path (JSON) |
| `set <file> <path> --value <text>` | Set element value |
| `add <file> <type> --value <text>` | Add new element |
| `remove <file> <path>` | Remove element |
| `create <format> <file> [--title <text>]` | Create new document |
| `merge <template> <output> --data <json>` | Fill template with data |
| `import <xlsx> <csv> --header` | Import CSV into Excel |
| `info <file>` | Document metadata |
| `validate <file>` | Validate against schema |

## Python API

```python
from officekit import OfficeKit

kit = OfficeKit()

# Read
text = kit.text("report.docx")
outline = kit.view("report.docx", mode="outline")

# Write
kit.set("deck.pptx", "/slides[1]/shapes[1]", value="Q4 Report")
kit.add("deck.pptx", "slide", value="Next Slide")

# Batch (atomic)
kit.batch("data.xlsx", [
    {"op": "set", "path": "/sheets[1]/A1", "value": "Name"},
    {"op": "set", "path": "/sheets[1]/B1", "value": "Score"},
    {"op": "set", "path": "/sheets[1]/A2", "value": "Alice"},
])
# If any op fails, entire batch rolls back

# Template merge
kit.merge("template.docx", "out.docx", data={
    "client": "Acme Corp",
    "date": "2026-09-01",
    "amount": "$5,000"
})
```

## MCP Server

```bash
# Start MCP server for AI agent integration
officekit mcp

# Or in Python:
from officekit.mcp import create_server
create_server().run()
```

## Comparison with OfficeCLI

| Feature | officekit | OfficeCLI |
|---------|-----------|-----------|
| Language | Python | Rust binary |
| Install | `pip install` | Download binary |
| Office dependency | None | None |
| Batch atomicity | ✅ Rollback on failure | ✅ Atomic |
| MCP server | ✅ Built-in | ✅ Built-in |
| Path addressing | ✅ | ✅ |
| Charts | Basic | Advanced |
| Pivot tables | ❌ | ✅ |
| Morph animations | ❌ | ✅ |
| Watch/live preview | ❌ | ✅ |
| Complexity | Lightweight | Full-featured |

Use **officekit** when you want a simple Python library with MCP support. Use **OfficeCLI** for advanced features (charts, pivots, morph, live preview).

## Resources

- **GitHub**: https://github.com/dream-zjk/officekit
- **PyPI**: https://pypi.org/project/officekit/
