---
name: book-to-skill-converter
description: Distill books, whitepapers, comprehensive PDFs, and large documentation sets into structured, production-grade AI agent skills using Book-to-Skill.
---

# Book-to-Skill Distillation Engine

Book-to-Skill parses entire technical books, manuals, or API documentation collections, extracts core principles, design patterns, rules, and code recipes, and formats them into standardized SKILL.md packages ready for agent execution.

## Core Capabilities
- **Document Chunking & Hierarchy Parsing**: Chapters, sections, and callouts extraction.
- **Pattern & Rule Synthesis**: Isolates anti-patterns, golden rules, and executable code templates.
- **SKILL.md Generation**: Emits YAML frontmatter and modular skill guidelines.

## CLI Usage
`ash
# Distill a PDF book or technical manual into a skill package
python book-to-skill/main.py --input path/to/book.pdf --output skills/distilled-topic-skill/
`
