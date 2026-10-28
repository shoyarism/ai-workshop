import sqlite3
from pathlib import Path

conn = sqlite3.connect(str(Path.home() / ".omniroute" / "storage.sqlite"))
c = conn.cursor()

c.execute("PRAGMA table_info(combos)")
print("Columns in combos:", [r[1] for r in c.fetchall()])

c.execute("SELECT * FROM combos LIMIT 5")
print("Sample rows:", c.fetchall())

conn.close()
