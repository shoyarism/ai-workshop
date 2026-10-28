import sqlite3
import json
import time
from pathlib import Path

db_path = str(Path.home() / ".omniroute" / "storage.sqlite")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Insert real 2M / 1M context limits
overrides = [
    ("auto", "auto/best-coding", 2000000),
    ("auto", "auto/best-reasoning", 2000000),
    ("auto", "auto/claude-opus", 1000000),
    ("auto", "auto/best-fast", 1000000),
    ("anthropic", "claude-3-7-sonnet-20250219", 1000000),
    ("anthropic", "claude-3-5-sonnet-20241022", 1000000),
    ("gemini", "gemini-2.5-pro", 2000000),
    ("gemini", "gemini-2.5-flash", 1000000),
    ("antigravity", "gemini-2.5-pro", 2000000),
    ("antigravity", "gemini-2.5-flash", 1000000)
]

for prov, m_id, ctx in overrides:
    try:
        c.execute("""
            INSERT OR REPLACE INTO model_context_overrides (provider, model_id, real_context, source, refreshed_at)
            VALUES (?, ?, ?, 'manual', ?)
        """, (prov, m_id, ctx, int(time.time())))
        print(f"Set {ctx:,} token context window for: {m_id}")
    except Exception as e:
        print(f"Error overriding {m_id}:", e)

conn.commit()
conn.close()
print("Context override configuration complete.")
