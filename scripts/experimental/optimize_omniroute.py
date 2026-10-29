import sqlite3
from pathlib import Path

db_path = Path.home() / ".omniroute" / "storage.sqlite"
conn = sqlite3.connect(str(db_path))
c = conn.cursor()

# 1. Disable connections missing credentials or with expired/unrefreshable OAuth tokens
c.execute("""
    UPDATE provider_connections
    SET is_active = 0
    WHERE (
        (api_key IS NULL OR api_key = '')
        AND (access_token IS NULL OR access_token = '')
        AND provider != 'pollinations'
    )
    OR test_status IN ('expired', 'invalid', 'unavailable', 'unsupported', 'rate_limited', 'error')
""")

# 2. Disable providers with known billing/auth blocks or dead endpoints
blocked_providers = [
    'trae', 'deepseek', 'anthropic', 'cline', 'kilocode',
    'bazaarlink', 'api-airforce', 'vertex-partner', 'vercel-ai-gateway',
    'perplexity-agent', 'llm7', 'tokenrouter', 'groq', 'venice',
    'gemini-cli', 'cursor', 'claude', 'qoder'
]
for p in blocked_providers:
    c.execute("UPDATE provider_connections SET is_active = 0 WHERE provider = ?", (p,))

# 3. Enable verified working providers that have valid credentials
verified_providers = [
    'gemini', 'kiro', 'codex', 'poolside', 'cohere',
    'openrouter', 'kilo-gateway', 'morph', 'exa-search', 'firecrawl'
]
for p in verified_providers:
    c.execute("""
        UPDATE provider_connections
        SET is_active = 1
        WHERE provider = ?
          AND ((api_key IS NOT NULL AND api_key != '') OR (access_token IS NOT NULL AND access_token != ''))
          AND COALESCE(test_status, '') NOT IN ('expired', 'invalid', 'unavailable', 'unsupported', 'error')
    """, (p,))

# Clear tripped circuit breakers & stale LKGP cache
c.execute("DELETE FROM domain_circuit_breakers")
c.execute("DELETE FROM key_value WHERE namespace = 'lkgp'")

conn.commit()

# 4. Verify active providers
c.execute("SELECT provider, name, priority, is_active FROM provider_connections WHERE is_active = 1 ORDER BY priority ASC, provider ASC")
active = c.fetchall()
print(f"\n--- Total Active & Healthy Connections: {len(active)} ---")
for r in active:
    print(f"  {r[0]:<16} | {str(r[1]):<24} | Priority: {r[2]}")

conn.close()
print("\nOmniRoute provider database optimization complete!")

