---
name: hugging-face-hub-explorer
description: Autonomous exploration, telemetry retrieval, searching, and metadata inspection across the Hugging Face Hub (Models, Datasets, Spaces, Daily Papers, Serverless Inference). Use when searching for state-of-the-art models, inspecting Safetensors weights, streaming dataset samples, or tracking AI research papers.
---

# Hugging Face Hub Explorer Skill

This skill provides first-principles operational instructions, invariants, and executable patterns for exploring and interacting with the **Hugging Face Hub** (`https://huggingface.co`)—the planetary registry and deployment ground for open-source machine learning.

---

## 1. Interface & Command Matrix

### Centralized Workshop CLI:
```bash
# 1. Live trending models, spaces, datasets, and research papers
uv run python scripts/workshop.py hf trending [--limit 5]

# 2. Search Hub models, datasets, or spaces
uv run python scripts/workshop.py hf search "deepseek" --type models --limit 10
uv run python scripts/workshop.py hf search "web text" --type datasets --limit 5
uv run python scripts/workshop.py hf search "image generation" --type spaces --limit 5

# 3. Deep inspection of repository metadata and tensor shards
uv run python scripts/workshop.py hf inspect "deepseek-ai/DeepSeek-R1"
uv run python scripts/workshop.py hf inspect "black-forest-labs/FLUX.1-dev"

# 4. Fetch the latest academic preprints and community evaluations
uv run python scripts/workshop.py hf papers --limit 5
```

### Direct Programmatic Python REST Interface:
```python
import urllib.request
import json

def query_hf(endpoint: str, params: dict = None) -> dict:
    url = f"https://huggingface.co/api/{endpoint.lstrip('/')}"
    if params:
        from urllib.parse import urlencode
        url += f"?{urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Workshop-Agent/2.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

# Fetch top models
top_models = query_hf("models", {"limit": 5, "sort": "downloads", "direction": -1})
```

---

## 2. Foundational Invariants & Ground Truths

1. **Structured REST over Raw HTML Scraping**:
   - Never scrape raw HTML or render headless browsers solely to extract model downloads, likes, or card data. The Hugging Face Hub exposes comprehensive public REST endpoints at `https://huggingface.co/api/...`.
2. **Safetensors Over Python Pickles**:
   - Always verify and prioritize `.safetensors` weight files over `.bin` or `.pt` files. Safetensors guarantees zero arbitrary code execution (no unpickling vulnerability) and supports zero-copy memory mapping (`mmap`).
3. **Chunked Streaming & Git-LFS Headers**:
   - Model weights on the Hub are stored via Git-LFS or direct chunked blob storage. To inspect large models, inspect the sibling tree via `https://huggingface.co/api/models/<id>` rather than downloading tens of gigabytes.
4. **Dataset Streaming (Zero-Download Preview)**:
   - Use the Hugging Face Dataset Viewer API (`https://datasets-server.huggingface.co`) to query rows, splits, and schemas using HTTP range requests and Apache Arrow without downloading the entire dataset.
5. **Inference Providers API (Unified Endpoint)**:
   - When executing serverless inference, use the OpenAI-compatible route (`https://api-inference.huggingface.co/v1/chat/completions`) with a Hugging Face user access token (`HF_TOKEN`).

---

## 3. Step-by-Step Execution Trajectories

### Trajectory A: Model Evaluation & Discovery
1. **Search**: Run `workshop.py hf search "<task_or_architecture>" --type models`.
2. **Inspect**: Run `workshop.py hf inspect "<author>/<repo_name>"`.
3. **Analyze**: Check:
   - `pipeline_tag`: task category (e.g. `text-generation`, `image-text-to-text`).
   - `license`: compatibility (e.g. `apache-2.0`, `mit`, `llama3.1`).
   - `safetensors`: number of shards and quantization (`fp8`, `4-bit`, `bf16`).
   - `base_model`: upstream foundation model if fine-tuned.

### Trajectory B: Research Paper Tracking
1. **Fetch**: Run `workshop.py hf papers --limit 5`.
2. **Link Verification**: Each paper includes arXiv ID, discussion threads, project pages, and associated model/dataset cards on the Hub.

---

## 4. Verification Oracle

| Check | Success Condition | Remediation if Failed |
|---|---|---|
| **API Connectivity** | HTTP 200 from `https://huggingface.co/api/models` | Check outbound DNS and network proxy settings. |
| **Model Verification** | Repo ID returns valid JSON with `id`, `tags`, and `siblings` | Verify case sensitivity in author/model slug. |
| **Token Verification** | `https://huggingface.co/api/whoami-v2` returns user object | Set `HF_TOKEN` environment variable. |

---

## 5. Anti-Patterns

- ❌ **Anti-Pattern 1: Scraping HTML with Playwright for Static Stats**: Wastes CPU, memory, and time. Use the native `workshop.py hf` or REST API endpoints.
- ❌ **Anti-Pattern 2: Blind Model Cloning**: Running `git clone https://huggingface.co/...` without LFS exclusions will attempt to pull 100GB+ of weights. Always filter files or use `hf download <repo> --include "*.json"`.
- ❌ **Anti-Pattern 3: Unpickling Untrusted `.bin` Files**: Never execute `torch.load()` on arbitrary Hub `.bin` files; check for `safetensors` files.

---

## 6. Multi-Source Literature Grounding

- **Safetensors Standard**: Patry et al., *Safetensors: Fast and Safe Tensor Storage*, Hugging Face, 2022.
- **TGI Whitepapers**: Hugging Face Systems Team, *Text Generation Inference Architecture & Continuous Batching*, 2023.
- **Apache Arrow Specifications**: In-memory columnar format for flat and hierarchical data, Apache Software Foundation.
