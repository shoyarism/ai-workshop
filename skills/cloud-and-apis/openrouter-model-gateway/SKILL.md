---
name: openrouter-model-gateway
description: Real-time model discovery, pricing analysis, and free-tier inspection across 445+ commercial and open-source models on OpenRouter. Use when selecting cost-effective LLMs, finding 100% free models, or inspecting context window limits.
---

# OpenRouter Model Gateway Skill

This skill provides operational patterns, invariants, and CLI commands for leveraging **OpenRouter** (`https://openrouter.ai`)—the universal API gateway aggregating over 445+ frontier and open-weights models.

---

## 1. Interface & Commands

```bash
# 1. List all 25+ completely free models (zero billing)
uv run python scripts/workshop.py openrouter free

# 2. Search models by keyword, family, or task
uv run python scripts/workshop.py openrouter search "deepseek" --limit 10
uv run python scripts/workshop.py openrouter search "claude" --limit 10
uv run python scripts/workshop.py openrouter search "coder" --limit 10

# 3. Inspect detailed context windows, token pricing, and modalities
uv run python scripts/workshop.py openrouter inspect deepseek/deepseek-r1
uv run python scripts/workshop.py openrouter inspect anthropic/claude-3.7-sonnet

# 4. Find the lowest cost models meeting a context threshold
uv run python scripts/workshop.py openrouter cheapest --min-context 64000 --limit 5
```

---

## 2. Invariants & Best Practices

1. **Free-Tier Suffix Convention**:
   - Models ending in `:free` (e.g. `deepseek/deepseek-r1:free`, `meta-llama/llama-3.3-70b-instruct:free`, `google/gemini-2.0-flash-exp:free`) incur zero monetary cost. Ideal for continuous CI/CD evaluation and agent testing.
2. **OpenAI Compatibility**:
   - OpenRouter uses the standard OpenAI API structure (`https://openrouter.ai/api/v1/chat/completions`) with `Authorization: Bearer $OPENROUTER_API_KEY`.
3. **Automatic Fallback Routing**:
   - In production code, configure fallback arrays so if a primary provider rate-limits, the request automatically cascades to secondary providers without throwing an exception.
