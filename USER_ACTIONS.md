# 🛡️ USER_ACTIONS.md — Manual User Actions & Key Rotation Checklist
**Workshop OS (Hermes-First)** | **Date:** 2026-10-05

Per strict security boundaries, AI agents **NEVER** rotate credentials automatically. The user must manually rotate any keys that may have appeared in prior session history, transcripts, or `.env` files.

---

## 1. Provider Keys to Rotate Immediately

The automated secrets scan detected pattern matches in historical session transcripts (`brain/` logs from earlier conversations). You should rotate the following API keys from their respective provider dashboards:

| Provider | Service / Type | Reason | Action URL |
| :--- | :--- | :--- | :--- |
| **OpenAI** | API Key (`sk-...`) | Flagged in historical agent logs | [OpenAI API Keys](https://platform.openai.com/api-keys) |
| **Anthropic** | API Key (`sk-ant-...`) | Flagged in historical agent logs | [Anthropic Console](https://console.anthropic.com/settings/keys) |
| **GitHub** | Personal Access Token (`ghp_...`) | Flagged in historical agent logs | [GitHub Tokens](https://github.com/settings/tokens) |
| **FreeLLMAPI** | Local Gateway Key | Stored in User Env `FREELLMAPI_API_KEY` | FreeLLMAPI Desktop UI -> Settings |

> [!IMPORTANT]
> After rotating these keys:
> 1. Update your User Environment variables (`setx FREELLMAPI_API_KEY "<new-key>"`).
> 2. Update your local Hermes credential store if you use persistent direct provider credentials.
> 3. Do **not** post or paste raw keys into chat prompts.

---

## 2. FreeLLMAPI Dashboard Fallback Chain (Action Items)

Empirical fitness benchmarking evaluated candidate free models across 4 criteria (Basic Reply, 1-Tool schema, 3-Tool disambiguation, and 20k context recall).

### Recommended Fallback Chain (Apply in FreeLLMAPI Dashboard -> Fallback Chains):
1. **Primary**: `codestral-latest` (Score: 100/100, 646.6 ms latency, flawless multi-tool calling & 20k context)
2. **Secondary**: `codestral` (Score: 100/100, 1803.4 ms latency, reliable backup)
3. **Tertiary**: `command-r` (Score: 100/100, 2213.2 ms latency, 128k context, solid tool compliance)

### Models to Disable / Drop from Fallback Chains:
- `command-r-plus-08-2024`: Frequent upstream 429 rate-limiting on free tiers.
- `openai-gpt-4o-mini`: Upstream provider out-of-credits / HTTP 502 Bad Gateway.
- `gemini-2.5-flash`: Upstream model not found (404) / routed provider failures.
- `mistral-small-3-2-24b-instruct`: HTTP 503 (missing upstream provider API key).
- `hyperbolic-llama-3.3-70b`: HTTP 404 / 502 provider connection failures.
- `qwen-3.8-27b`: Upstream Cloudflare Workers AI credentials missing.

---

## 3. Secondary Harness Verification Commands (To Be Populated in Task 5)
*(Will be updated following Hermes role isolation compilation)*
