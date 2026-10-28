---
name: litellm-proxy-gateway
description: Universal LLM proxy and API gateway routing 100+ AI models (OpenAI, Anthropic, Gemini, DeepSeek, Local Ollama) through standard OpenAI format.
---

# LiteLLM Universal Proxy & Routing Gateway

LiteLLM provides a single, unified interface for calling 100+ LLMs using the standard OpenAI format, featuring automatic load balancing, retries, fallbacks, and cost tracking.

## Usage
`python
from litellm import completion

# Call any model with standard syntax
response = completion(
    model='gemini/gemini-1.5-pro',
    messages=[{'role': 'user', 'content': 'Explain quantum computing'}]
)
print(response.choices[0].message.content)
`
