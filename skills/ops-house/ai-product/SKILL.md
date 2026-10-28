---
name: ai-product
description: Every product will be AI-powered. The question is whether you'll
  build it right or ship a demo that falls apart in production.
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# AI Product Development

Every product will be AI-powered. The question is whether you'll build it
right or ship a demo that falls apart in production.

This skill covers LLM integration patterns, RAG architecture, prompt
engineering that scales, AI UX that users trust, and cost optimization
that doesn't bankrupt you.

## Principles

- LLMs are probabilistic, not deterministic | Description: The same input can give different outputs. Design for variance.
Add validation layers. Never trust output blindly. Build for the
edge cases that will definitely happen. | Examples: Good: Validate LLM output against schema, fallback to human review | Bad: Parse LLM response and use directly in database
- Prompt engineering is product engineering | Description: Prompts are code. Version them. Test them. A/B test them. Document them.
One word change can flip behavior. Treat them with the same rigor as code. | Examples: Good: Prompts in version control, regression tests, A/B testing | Bad: Prompts inline in code, changed ad-hoc, no testing
- RAG over fine-tuning for most use cases | Description: Fine-tuning is expensive, slow, and hard to update. RAG lets you add
knowledge without retraining. Start with RAG. Fine-tune only when RAG
hits clear limits. | Examples: Good: Company docs in vector store, retrieved at query time | Bad: Fine-tuned model on company data, stale after 3 months
- Design for latency | Description: LLM calls take 1-30 seconds. Users hate waiting. Stream responses.
Show progress. Pre-compute when possible. Cache aggressively. | Examples: Good: Streaming response with typing indicator, cached embeddings | Bad: Spinner for 15 seconds, then wall of text appears