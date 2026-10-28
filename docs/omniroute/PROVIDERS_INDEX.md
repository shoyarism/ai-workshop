# OmniRoute Providers & Keys — Master Index
**Source:** `.\Backup\omniroute\exports\providers_and_accounts.json`
**Total Connections:** 101
**Last Exported:** 2026-09-02

## Provider Inventory

### API Key Providers (Compatible with FreeLLMAPI)
| Provider | Keys | Status | FreeLLMAPI Platform |
|----------|------|--------|---------------------|
| agnes | 5 | Active | agnes |
| aion | 5 | Active | aion |
| bazaarlink | 1 | Active | bazaarlink |
| cloudflare-ai | 1 | Standby | cloudflare |
| cohere | 1 | Active | cohere |
| gemini | 1 | Active | google |
| groq | 2 | Active | groq |
| kilo-gateway | 1 | Active | kilo |
| llm7 | 2 | Active | llm7 |
| mistral | 3 | Active | mistral |
| nvidia | 1 | Active | nvidia |
| ollama | 1 | Active | ollama |
| openai | 4 | Standby | google |
| opencode-go | 6 | Standby | opencode |
| openrouter | 1 | Active | openrouter |
| vertex-partner | 1 | Active | google |

**Total API Key Providers:** 16 platforms, ~34 keys

### OAuth Providers (Not importable to FreeLLMAPI)
| Provider | Email | Status |
|----------|-------|--------|
| cline | voruebergehend.past@gmail.com | Active |
| clinepass | voruebergehend.past@gmail.com | Standby |
| codebuddy-intl | Account 1 | Active (error) |
| codex | ariya.digitalmarketing.rsuimb@gmail.com | Active |
| gemini-cli | ariya.digitalmarketing.rsuimb@gmail.com | Active (error) |
| github | Voruebergehend | Standby |
| grok-cli | ariya.digitalmarketing.rsuimb@gmail.com | Standby (error) |
| kilocode | ariya.digitalmarketing.rsuimb@gmail.com | Active |
| kimchi | voruebergehend.past@gmail.com | Active (error) |
| kimi | Account 1 | Active (error) |
| kiro | Account 1 | Standby |
| trae | Voruebergehend | Active (error) |
| xai | ariya.digitalmarketing.rsuimb@gmail.com | Standby (error) |

**Total OAuth Providers:** 13

### Other Providers (Special Auth)
| Provider | Notes |
|----------|-------|
| api-airforce | API key |
| byteplus | API key |
| cerebras | API key |
| chutes | API key |
| commandcode | API key (error) |
| exa-search | 4 API keys |
| firecrawl | 5 API keys (1 error) |
| hyperbolic | 3 API keys |
| morph | 4 API keys (standby) |
| perplexity-agent | API key (error) |
| poolside | API key (error) |
| siliconflow | 3 API keys |
| tokenrouter | 4 API keys |
| vercel-ai-gateway | 3 API keys |
| venice | 3 API keys |
| xiaomi-mimo | 13 API keys (standby) |

## Encryption Details
- **OmniRoute Format:** `enc:v1:<16-byte-IV>:<ciphertext>:<16-byte-tag>`
- **Algorithm:** AES-256-GCM
- **Key Derivation:** scrypt (N=16384, r=8, p=1) with static salt `omniroute-field-encryption-v1`
- **Secret:** `STORAGE_ENCRYPTION_KEY` from `.env`

## FreeLLMAPI Integration
- **Script:** `migrate_keys_to_freellm.py`
- **Result:** 24 keys imported to `freeapi.db`
- **Backup:** `freeapi.db.bak` created before migration
