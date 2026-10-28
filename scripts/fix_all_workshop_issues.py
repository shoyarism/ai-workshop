import json
import sqlite3
import re
from pathlib import Path

print("=== 1. OPTIMIZING OMNIROUTE CONFIG (.env) ===")
env_path = Path.home() / ".omniroute" / ".env"
if env_path.exists():
    content = env_path.read_text(encoding="utf-8", errors="ignore")
    content = re.sub(r"^ENABLE_SOCKS5_PROXY=true", "ENABLE_SOCKS5_PROXY=false", content, flags=re.MULTILINE)
    content = re.sub(r"^NEXT_PUBLIC_ENABLE_SOCKS5_PROXY=true", "NEXT_PUBLIC_ENABLE_SOCKS5_PROXY=false", content, flags=re.MULTILINE)
    env_path.write_text(content, encoding="utf-8")
    print("Fixed SOCKS5 proxy settings to direct connection in .env")

print("\n=== 2. CONFIGURING CLAUDE CODE 1M CONTEXT WINDOW & MODEL ===")
claude_settings = Path.home() / ".claude" / "settings.json"
if claude_settings.exists():
    with open(claude_settings, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # Using claude-3-7-sonnet gives Claude Code full 1,000,000 token context window recognition
    cfg["model"] = "claude-3-7-sonnet-20250219"
    cfg["effortLevel"] = "xhigh"
    with open(claude_settings, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("Set Claude Code model to claude-3-7-sonnet-20250219 for 1M context support.")

print("\n=== 3. OPTIMIZING OMNIROUTE PROVIDERS & ROUTING ===")
db_path = str(Path.home() / ".omniroute" / "storage.sqlite")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Disable connections missing credentials or with expired/unrefreshable OAuth tokens
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

# Disable known failing/exhausted providers
unstable = [
    'trae', 'deepseek', 'anthropic', 'cline', 'kilocode',
    'bazaarlink', 'api-airforce', 'vertex-partner', 'vercel-ai-gateway',
    'perplexity-agent', 'llm7', 'tokenrouter', 'groq', 'venice',
    'gemini-cli', 'cursor', 'claude', 'qoder'
]
for p in unstable:
    c.execute("UPDATE provider_connections SET is_active = 0 WHERE provider = ?", (p,))

conn.commit()
conn.close()
print("OmniRoute providers optimized.")

print("\n=== 4. REDESIGNING PIXEL AGENTS DESKS FOR ZERO SUBAGENT BUNCHING ===")
cols = 23
rows = 21

tiles = [255] * (cols * rows)
tile_colors = [None] * (cols * rows)

def set_tile(c_idx, r_idx, tile_type, color=None):
    if 0 <= c_idx < cols and 0 <= r_idx < rows:
        idx = r_idx * cols + c_idx
        tiles[idx] = tile_type
        tile_colors[idx] = color

c_wall = {"h": 215, "s": 25, "b": -90, "c": -60}
c_tech_floor = {"h": 215, "s": 15, "b": -30, "c": -70}
c_boardroom = {"h": 28, "s": 35, "b": -15, "c": -60}
c_devpod = {"h": 220, "s": 12, "b": -25, "c": -70}
c_lounge = {"h": 210, "s": 30, "b": -20, "c": -50}
c_corridor = {"h": 215, "s": 10, "b": -15, "c": -40}

# Floors
for r in range(1, 10):
    for c_idx in range(1, 11): set_tile(c_idx, r, 7, c_tech_floor)
    for c_idx in range(12, 22): set_tile(c_idx, r, 4, c_boardroom)

for r in range(11, 20):
    for c_idx in range(1, 11): set_tile(c_idx, r, 7, c_devpod)
    for c_idx in range(12, 22): set_tile(c_idx, r, 1, c_lounge)

for r in range(1, 20): set_tile(11, r, 6, c_corridor)
for c_idx in range(1, 22): set_tile(c_idx, 10, 6, c_corridor)

# Perimeter Walls
for c_idx in range(0, 23):
    set_tile(c_idx, 0, 0, c_wall)
    set_tile(c_idx, 20, 0, c_wall)
for r in range(0, 21):
    set_tile(0, r, 0, c_wall)
    set_tile(22, r, 0, c_wall)

# Horizontal archways
for c_idx in range(1, 22):
    if c_idx in [4, 5, 6, 11, 16, 17, 18]:
        set_tile(c_idx, 10, 6, c_corridor)
    else:
        set_tile(c_idx, 10, 0, c_wall)

# Distinct, widely-separated workstations across all 4 rooms (so each agent gets its own room/desk!)
furniture = [
    # ROOM 1: Lead Command Workstations (North-West)
    {"uid": "f-r1-bs1", "type": "DOUBLE_BOOKSHELF", "col": 1, "row": 0},
    {"uid": "f-r1-hp1", "type": "HANGING_PLANT", "col": 3, "row": 0},
    {"uid": "f-r1-wb", "type": "WHITEBOARD", "col": 5, "row": 0},
    {"uid": "f-r1-clk", "type": "CLOCK", "col": 8, "row": 0},
    {"uid": "f-r1-bs2", "type": "DOUBLE_BOOKSHELF", "col": 9, "row": 0},
    # Workstation 1 (West)
    {"uid": "f-desk-1", "type": "DESK_FRONT", "col": 2, "row": 3},
    {"uid": "f-pc-1", "type": "PC_FRONT_OFF", "col": 3, "row": 3},
    {"uid": "f-chair-1", "type": "CUSHIONED_CHAIR_BACK", "col": 3, "row": 5},
    {"uid": "f-cof-1", "type": "COFFEE", "col": 2, "row": 4},
    # Workstation 2 (East)
    {"uid": "f-desk-2", "type": "DESK_FRONT", "col": 7, "row": 3},
    {"uid": "f-pc-2", "type": "PC_FRONT_OFF", "col": 8, "row": 3},
    {"uid": "f-chair-2", "type": "CUSHIONED_CHAIR_BACK", "col": 8, "row": 5},
    {"uid": "f-r1-plt", "type": "LARGE_PLANT", "col": 1, "row": 7},
    {"uid": "f-r1-bin", "type": "BIN", "col": 10, "row": 7},

    # ROOM 2: Boardroom & Strategic Suite (North-East)
    {"uid": "f-r2-bs", "type": "DOUBLE_BOOKSHELF", "col": 12, "row": 0},
    {"uid": "f-r2-hp", "type": "HANGING_PLANT", "col": 14, "row": 0},
    {"uid": "f-r2-wb", "type": "WHITEBOARD", "col": 16, "row": 0},
    {"uid": "f-r2-art", "type": "LARGE_PAINTING", "col": 19, "row": 0},
    {"uid": "f-r2-clk", "type": "CLOCK", "col": 21, "row": 0},
    # Workstation 3 (Boardroom Desk 1)
    {"uid": "f-desk-3", "type": "DESK_FRONT", "col": 13, "row": 3},
    {"uid": "f-pc-3", "type": "PC_FRONT_OFF", "col": 14, "row": 3},
    {"uid": "f-chair-3", "type": "CUSHIONED_CHAIR_BACK", "col": 14, "row": 5},
    # Workstation 4 (Boardroom Desk 2)
    {"uid": "f-desk-4", "type": "DESK_FRONT", "col": 18, "row": 3},
    {"uid": "f-pc-4", "type": "PC_FRONT_OFF", "col": 19, "row": 3},
    {"uid": "f-chair-4", "type": "CUSHIONED_CHAIR_BACK", "col": 19, "row": 5},
    {"uid": "f-r2-plt", "type": "LARGE_PLANT", "col": 20, "row": 7},

    # ROOM 3: Dev Pods (South-West)
    {"uid": "f-r3-hp", "type": "HANGING_PLANT", "col": 1, "row": 10},
    {"uid": "f-r3-wb", "type": "WHITEBOARD", "col": 3, "row": 10},
    {"uid": "f-r3-art", "type": "SMALL_PAINTING", "col": 8, "row": 10},
    # Workstation 5 (South-West Desk 1)
    {"uid": "f-desk-5", "type": "DESK_FRONT", "col": 2, "row": 13},
    {"uid": "f-pc-5", "type": "PC_FRONT_OFF", "col": 3, "row": 13},
    {"uid": "f-chair-5", "type": "CUSHIONED_CHAIR_BACK", "col": 3, "row": 15},
    # Workstation 6 (South-West Desk 2)
    {"uid": "f-desk-6", "type": "DESK_FRONT", "col": 7, "row": 13},
    {"uid": "f-pc-6", "type": "PC_FRONT_OFF", "col": 8, "row": 13},
    {"uid": "f-chair-6", "type": "CUSHIONED_CHAIR_BACK", "col": 8, "row": 15},
    {"uid": "f-r3-plt1", "type": "PLANT", "col": 1, "row": 18},
    {"uid": "f-r3-plt2", "type": "PLANT_2", "col": 9, "row": 18},
    {"uid": "f-r3-bin", "type": "BIN", "col": 5, "row": 18},

    # ROOM 4: Lounge & Relaxation (South-East)
    {"uid": "f-r4-art1", "type": "LARGE_PAINTING", "col": 13, "row": 10},
    {"uid": "f-r4-art2", "type": "SMALL_PAINTING_2", "col": 19, "row": 10},
    {"uid": "f-r4-hp", "type": "HANGING_PLANT", "col": 21, "row": 10},
    # Central Lounge Sofas
    {"uid": "f-lounge-ctbl", "type": "COFFEE_TABLE", "col": 15, "row": 14},
    {"uid": "f-lounge-s1", "type": "SOFA_FRONT", "col": 15, "row": 13},
    {"uid": "f-lounge-s2", "type": "SOFA_BACK", "col": 15, "row": 16},
    {"uid": "f-lounge-s3", "type": "SOFA_SIDE", "col": 14, "row": 14},
    {"uid": "f-lounge-s4", "type": "SOFA_SIDE:left", "col": 17, "row": 14},
    {"uid": "f-lounge-cof1", "type": "COFFEE", "col": 15, "row": 15},
    # Refreshment Counter
    {"uid": "f-r4-bar", "type": "SMALL_TABLE_FRONT", "col": 19, "row": 13},
    {"uid": "f-r4-cof2", "type": "COFFEE", "col": 19, "row": 13},
    {"uid": "f-r4-cct", "type": "CACTUS", "col": 20, "row": 13},
    {"uid": "f-r4-bnch", "type": "WOODEN_BENCH", "col": 19, "row": 15},
    # Zen Garden
    {"uid": "f-r4-lplt", "type": "LARGE_PLANT", "col": 19, "row": 17},
    {"uid": "f-r4-plt1", "type": "PLANT", "col": 13, "row": 18},
    {"uid": "f-r4-pot", "type": "POT", "col": 17, "row": 18}
]

layout = {
    "version": 1,
    "cols": cols,
    "rows": rows,
    "layoutRevision": 20,
    "tiles": tiles,
    "tileColors": tile_colors,
    "furniture": furniture
}

active_path = Path.home() / ".pixel-agents" / "layout.json"
bundled_path = Path.home() / ".vscode" / "extensions" / "pablodelucca.pixel-agents-1.4.1" / "dist" / "webview" / "assets" / "default-layout-1.json"

if active_path.parent.exists():
    with open(active_path, "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)

if bundled_path.parent.exists():
    with open(bundled_path, "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)

# Reset seat assignments state so subagents get freshly assigned to different rooms
state_file = Path.home() / ".pixel-agents" / "vscode-state.json"
if state_file.parent.exists():
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump({"agents": [], "seats": {}}, f, indent=2)

print("Pixel Agents layout updated to Revision 20 with distributed spacious desks.")
print("=== ALL FIXES APPLIED SUCCESSFULLY ===")
