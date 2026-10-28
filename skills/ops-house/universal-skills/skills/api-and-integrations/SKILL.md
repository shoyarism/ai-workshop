---
name: api-and-integrations
description: Use when calling APIs, LLM endpoints or connecting tools.
---

# Api And Integrations

1. Read the official docs for auth, base URL, parameters and limits.
2. Test with the smallest request first. Print the status code and body on failure.
3. Handle rate limits: respect retry-after, back off, cap retries.
4. Keep keys in environment variables. Never log them.
5. OpenAI-compatible endpoints: set base URL and key, pick the model name, pass messages, tools only if the model supports tool calls. Test tool calling per model.
6. Set timeouts. Validate responses before using them.
7. Free tiers: expect caps and changes. Do not send private data.
