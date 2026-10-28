---
name: deep-tutor
description: >
  Lifelong personalized tutoring system. Connects tutoring, problem solving, quiz generation,
  research, visualization, and mastery practice. Use when user mentions "tutor", "learn",
  "study", "quiz", "personalized learning", "knowledge base", "RAG learning".
  Reference: https://github.com/HKUDS/DeepTutor
---

# DeepTutor — Lifelong Personalized Tutoring

DeepTutor is an agent-native learning workspace connecting tutoring, problem solving, quiz generation, research, visualization, and mastery practice.

## Quick Install

```bash
# Install from PyPI
pip install -U deeptutor

# Initialize
deeptutor init

# Start the app
deeptutor start
```

## Usage

```bash
# Interactive chat
deeptutor chat

# With knowledge base
deeptutor chat --capability deep_solve --tool rag --kb my-kb

# Run specific capability
deeptutor run chat "Explain Fourier transform"

# Create knowledge base
deeptutor kb create my-kb --doc textbook.pdf

# Show memory
deeptutor memory show
```

## Key Features

- **Connected learning context** - KB, books, Co-Writer, notebooks across workflows
- **Subagents and Partners** - Live Claude Code, Codex, Gemini, Antigravity, Kimi, opencode
- **Multi-engine knowledge** - LlamaIndex, PageIndex, GraphRAG, LightRAG
- **Extensible tools** - MCP servers, CLI apps, image/video/voice generation
- **Inspectable memory** - L1 traces, L2 summaries, L3 synthesis with evidence graph

## Docker Deployment

```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

## Configuration

After `deeptutor init`, configure:
- LLM provider (OpenAI, Anthropic, Ollama, etc.)
- Embedding provider (optional)
- Search provider (optional)

Default frontend: http://127.0.0.1:3782
