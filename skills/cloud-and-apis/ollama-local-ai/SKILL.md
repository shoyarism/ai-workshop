---
name: ollama-local-ai
description: Manage and run local LLMs with Ollama — pull models, serve endpoints, chat completions, embeddings, model libraries, and local fine-tuning. Use when the user wants to run AI models offline on their own machine without cloud APIs, needs local model selection (Llama, Qwen, Codestral, Mistral, etc.), or wants to build privacy-first AI workflows. Triggers on: ollama, local LLM, run model locally, pull model, local embeddings, llamafile, LM Studio alternative, private AI, offline AI, local inference, serve model.
---

# Ollama Local AI

Run large language models entirely on your own hardware via Ollama. This skill covers the full local-AI lifecycle: installation, model management, the Ollama REST API, chat completions, embeddings, model libraries, and basic local fine-tuning with Modelfiles.

## When to trigger

- User wants to run an LLM without sending data to a cloud provider
- User mentions Ollama, llamafile, LM Studio, local inference, or offline AI
- User needs embeddings or chat completions from a locally-served model
- User wants to customize a model's behavior with a Modelfile (system prompt, parameters, template)

## Core capabilities

### 1. Install & serve Ollama

- Verify Ollama is installed: `ollama --version`
- Start the server: `ollama serve` (runs on `http://localhost:11434`)
- Confirm the API is up: `curl http://localhost:11434/api/tags`

### 2. Model management

- List installed models: `ollama list`
- Pull a model: `ollama pull <model>` (e.g., `llama3.2`, `qwen2.5-coder:7b`, `codestral`, `mistral-nemo`, `nomic-embed-text`)
- Remove a model: `ollama rm <model>`
- Copy a model: `ollama cp <source> <destination>`
- Show model details: `ollama show <model>`

### 3. Chat completions (REST API)

Endpoint: `POST http://localhost:11434/api/chat`

Request body:
```json
{
  "model": "llama3.2",
  "messages": [
    {"role": "user", "content": "Explain RAG in two sentences."}
  ],
  "stream": false,
  "options": {
    "temperature": 0.7,
    "num_predict": 512
  }
}
```

Streaming: set `"stream": true` and read newline-delimited JSON chunks.

### 4. Embeddings

Endpoint: `POST http://localhost:11434/api/embeddings`

Request body:
```json
{
  "model": "nomic-embed-text",
  "prompt": "Text to embed"
}
```

### 5. Modelfiles (local model customization)

Example `Modelfile`:
```dockerfile
FROM llama3.2
PARAMETER temperature 0.3
PARAMETER num_predict 256
SYSTEM """You are a concise code-review assistant. Reply only with actionable findings."""
TEMPLATE """{{ .System }} {{ .Prompt }}"""
```

Create and run:
```bash
ollama create code-reviewer -f Modelfile
ollama run code-reviewer "Review this function for bugs..."
```

### 6. Python client (optional)

Install: `pip install ollama`

```python
import ollama

# Chat
response = ollama.chat(model="llama3.2", messages=[
    {"role": "user", "content": "Why is the sky blue?"}
])
print(response["message"]["content"])

# Embeddings
emb = ollama.embeddings(model="nomic-embed-text", prompt="Hello world")
print(emb["embedding"])
```

## Model selection guide

| Use case | Recommended model |
|---|---|
| General chat | `llama3.2:3b` or `llama3.1:8b` |
| Code generation | `qwen2.5-coder:7b` or `codestral` |
| Embeddings | `nomic-embed-text` or `mxbai-embed-large` |
| Long context | `llama3.1:8b` (128k context) |
| Low RAM (<8GB) | `llama3.2:1b` or `phi3:mini` |

## Safety & privacy

- Models run entirely locally; no data leaves the machine
- Model files are stored in `~/.ollama/models`
- Always verify model provenance before pulling from the Ollama library

## Example workflows

**Quick local chat:**
```bash
ollama pull llama3.2
ollama run llama3.2 "Draft a polite email declining a meeting."
```

**Local embeddings for RAG:**
```bash
ollama pull nomic-embed-text
curl -X POST http://localhost:11434/api/embeddings -d '{"model":"nomic-embed-text","prompt":"Your document text here"}'
```

**Custom code-review model:**
```bash
ollama create reviewer -f Modelfile
ollama run reviewer "Find security issues in: <paste code>"
```

## Related Workshop skills

- `rag-pipeline-builder` — combine local embeddings with a vector store for RAG
- `mcp-builder` — expose your local Ollama models as MCP tools
