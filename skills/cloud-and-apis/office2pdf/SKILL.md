---
source: "https://github.com/developer0hye/office2pdf"
name: office2pdf
description: "Use when the user needs to convert DOCX, XLSX, or PPTX files to PDF. Pure-Rust CLI with zero external dependencies — no LibreOffice, no Chromium, no Docker. Single binary powered by Typst. Supports PDF/A-2b archival output. Triggers: 'convert to PDF', 'DOCX to PDF', 'PPTX to PDF', 'XLSX to PDF', 'office to PDF'."
risk: low
---

# office2pdf

[GitHub](https://github.com/developer0hye/office2pdf) · ⭐ 108 · Rust · MIT

Pure-Rust library and CLI for converting DOCX, XLSX, and PPTX files to PDF. No LibreOffice, no Chromium, no Docker — just a single binary powered by Typst.

## Install

```bash
# Pre-built binary (recommended)
# Download from: https://github.com/developer0hye/office2pdf/releases

# Cargo install
cargo install office2pdf-cli

# Or use with uv
uvx office2pdf
```

## When to Use

- User wants to **convert Office documents to PDF** quickly
- User needs **PDF/A-2b archival compliance**
- User wants **no external dependencies** (no LibreOffice, no Docker)
- User needs to convert in **CI/CD or containerized environments**
- Use instead of `libreoffice --headless --convert-to pdf` for faster, dependency-free conversion

## Quick Start

```bash
# Convert DOCX to PDF
office2pdf input.docx output.pdf

# Convert PPTX to PDF
office2pdf presentation.pptx slides.pdf

# Convert XLSX to PDF
office2pdf spreadsheet.xlsx report.pdf

# PDF/A-2b archival output
office2pdf --pdf-a report.docx archival.pdf

# Batch convert
for f in *.docx; do office2pdf "$f" "${f%.docx}.pdf"; done
```

## CLI Reference

```bash
office2pdf [OPTIONS] <input> [output]

# Positional arguments
<input>    # Input file (DOCX, XLSX, or PPTX)
<output>   # Output PDF file (optional, defaults to <input>.pdf)

# Options
--pdf-a          # Generate PDF/A-2b archival compliant PDF
--help, -h       # Show help
--version, -v    # Show version
```

## Supported Features by Format

### DOCX → PDF

- ✅ Paragraphs with formatting (bold/italic/underline/color)
- ✅ Tables with borders and shading
- ✅ Images (inline and floating)
- ✅ Ordered and nested lists
- ✅ Syntax-highlighted code blocks
- ✅ Headers and footers
- ✅ Page setup (margins, orientation)
- ✅ Embedded fonts

### XLSX → PDF

- ✅ Multiple sheets (one page per sheet)
- ✅ Chartsheets (full-page charts)
- ✅ Cell formatting (colors, fonts, borders)
- ✅ Merged cells
- ✅ Column widths and row heights
- ✅ Excel tables (banding, header rules, bold headers)
- ✅ Conditional formatting (DataBar, IconSet, formula rules)

### PPTX → PDF

- ✅ Slides with text and shapes
- ✅ Tables with theme-based styling
- ✅ Images
- ✅ Slide masters
- ✅ Speaker notes
- ✅ Gradient backgrounds
- ✅ Shadow/reflection effects
- ✅ Embedded fonts (auto-extracted and deobfuscated)

## macOS Office Font Discovery

```bash
# Auto-discovers fonts from macOS Office installations
# Word/PowerPoint/Excel bundled fonts are searched automatically
# For mutable Office cloud caches, provide explicit path:
office2pdf --font-path /Applications/Microsoft\ Word.app/Contents/Resources/Fonts input.docx
```

## WASM / Browser Usage

```javascript
// In browser or Node.js
import { convert } from 'office2pdf-wasm';

const pdf = await convert(docxBuffer, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
```

## Comparison with LibreOffice

| Feature | office2pdf | LibreOffice |
|---------|-----------|-------------|
| Install | Single binary (~10MB) | ~300MB+ suite |
| Dependencies | None | Java, X11, fonts |
| Docker needed | ❌ No | ✅ Usually |
| Speed | Fast (Typst engine) | Slow (full UI) |
| PDF/A | ✅ Native | ✅ With flags |
| Charts | ✅ | ✅ |
| Complex formatting | ✅ | ✅ |
| Macro support | ❌ No | ✅ Yes |

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Chinese characters missing | Ensure font is embedded in source document |
| Large PPTX slow | Convert slide-by-slide for huge files |
| XLSX charts look different | Chart rendering depends on source formatting |
| Custom fonts not embedded | Use `--font-path` on macOS |

## Resources

- **GitHub**: https://github.com/developer0hye/office2pdf
- **Releases**: https://github.com/developer0hye/office2pdf/releases
- **Docs.rs**: https://docs.rs/office2pdf
