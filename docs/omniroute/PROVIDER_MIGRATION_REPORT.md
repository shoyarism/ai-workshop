# FreeLLMAPI Provider Migration Report
**Date:** 2026-09-11
**Source:** `.\Backup\omniroute\exports\providers_and_accounts.json`
**Target:** `~\AppData\Roaming\FreeLLMAPI\freeapi.db`

## Summary
- **Total OmniRoute connections:** 101
- **Compatible providers (keyed API only, active):** 24
- **Keys successfully imported:** 24
- **Safety backup created:** `~\AppData\Roaming\FreeLLMAPI\freeapi.db.bak`
- **Migration script:** `.\Backup\migrate_keys_to_freellm.py`

## Imported Platforms & Labels
1. **agnes** (5 keys: Key 1–5)
2. **aion** (5 keys: Key 1–5)
3. **bazaarlink** (1 key: main)
4. **cohere** (1 key: main)
5. **google** (1 key: main)
6. **groq** (2 keys: main, main2)
7. **kilo** (1 key: main)
8. **llm7** (2 keys: main, main2)
9. **mistral** (3 keys: main, main2, main3)
10. **nvidia** (1 key: main)
11. **ollama** (1 key: main)
12. **openrouter** (1 key: main)
13. **cloudflare** (1 key: main)
14. **bazaarlink** (1 key: main)
15. **vertex-partner** (1 key: main)

## Excluded Platforms
The following OmniRoute providers were excluded due to incompatible auth or mapping:
- **OAuth-only providers:** cline, clinepass, codebuddy-intl, codex, gemini-cli, github, grok-cli, kilocode, kimchi, kimi, kiro, trae, xai
- **Unsupported platforms:** api-airforce, byteplus, cerebras, chutes, commandcode, exa-search, firecrawl, hyperbolic, morph, opencode-go, perplexity-agent, poolside, siliconflow, tokenrouter, vercel-ai-gateway, xiaomi-mimo
- **Inactive/standby:** cloudflare-ai (was standby)

## Technical Notes
- OmniRoute encryption uses `AES-256-GCM` with static salt `omniroute-field-encryption-v1`
- FreeLLMAPI encryption uses `AES-256-GCM` with per-key random 16-byte IV
- Migration script handles platform name mapping and re-encryption
- All keys were re-encrypted with FreeLLMAPI's local `.encryption-key`

## Post-Migration
- FreeLLMAPI should auto-detect the new keys on next startup
- Keys will be health-checked and auto-enabled
- Existing catalog (368 models, 24 platforms) remains intact
