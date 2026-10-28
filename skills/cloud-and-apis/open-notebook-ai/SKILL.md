---
name: open-notebook-ai
description: Multi-model AI research companion, document grounding, source synthesis, and audio podcast generation with Open Notebook.
---

# Open Notebook AI Research Engine

Open Notebook is an open-source, multi-model alternative to Google NotebookLM. It enables deep grounded document analysis, multi-document synthesis, source citations, notes organization, and audio overview generation using local and cloud LLMs.

## Core Capabilities
- **Document Grounding**: Ingest PDFs, Markdown, websites, and audio transcripts.
- **Strict Evidence Citation**: Responses cite exact source paragraphs and page ranges.
- **Audio Overviews**: Generate two-speaker conversational podcast discussions from source notes.

## Setup & Running
`ash
# Start Open Notebook server
cd open-notebook && python -m open_notebook.server --port 8000
`
