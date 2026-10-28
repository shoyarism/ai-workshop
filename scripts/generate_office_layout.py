#!/usr/bin/env python3
"""
Pixel Agents Master Office Layout Generator (Clean Architectural Build)
======================================================================
Generates a polished 4-room corporate studio with clean wall geometry,
flush aligned doorways, zero texture glitches, and rich functional furniture.
"""

import json

def generate_clean_office():
    cols = 23
    rows = 21
    
    # 0 = Wall, 255 = Void, 1-8 = Floor types
    tiles = [255] * (cols * rows)
    tile_colors = [None] * (cols * rows)
    
    def set_tile(c, r, tile_type, color=None):
        if 0 <= c < cols and 0 <= r < rows:
            idx = r * cols + c
            tiles[idx] = tile_type
            tile_colors[idx] = color

    # Refined subtle color palettes
    c_wall = {"h": 215, "s": 25, "b": -90, "c": -60}        # Dark architectural perimeter wall
    c_tech_floor = {"h": 215, "s": 15, "b": -30, "c": -70}   # Sleek slate for engineering (North-West)
    c_boardroom = {"h": 28, "s": 35, "b": -15, "c": -60}     # Executive oak for boardroom (North-East)
    c_devpod = {"h": 220, "s": 12, "b": -25, "c": -70}       # Modern studio floor for dev pods (South-West)
    c_lounge = {"h": 210, "s": 30, "b": -20, "c": -50}       # Velvet indigo for cafe lounge (South-East)
    c_corridor = {"h": 215, "s": 10, "b": -15, "c": -40}     # Polished walkway connecting rooms

    # --- 1. FLOORS ---
    # North-West Room (Cols 1-10, Rows 1-9)
    for r in range(1, 10):
        for c in range(1, 11):
            set_tile(c, r, 7, c_tech_floor)
            
    # North-East Room (Cols 12-21, Rows 1-9)
    for r in range(1, 10):
        for c in range(12, 22):
            set_tile(c, r, 4, c_boardroom)
            
    # South-West Room (Cols 1-10, Rows 11-19)
    for r in range(11, 20):
        for c in range(1, 11):
            set_tile(c, r, 7, c_devpod)
            
    # South-East Room (Cols 12-21, Rows 11-19)
    for r in range(11, 20):
        for c in range(12, 22):
            set_tile(c, r, 1, c_lounge)

    # Central Walkways:
    # North-South corridor (Col 11, Rows 1-19)
    for r in range(1, 20):
        set_tile(11, r, 6, c_corridor)
        
    # East-West corridor / Divider row (Row 10, Cols 1-21)
    for c in range(1, 22):
        set_tile(c, 10, 6, c_corridor)

    # --- 2. PERIMETER OUTER WALLS ---
    for c in range(0, 23):
        set_tile(c, 0, 0, c_wall)   # Top boundary wall
        set_tile(c, 20, 0, c_wall)  # Bottom boundary wall
    for r in range(0, 21):
        set_tile(0, r, 0, c_wall)   # Left boundary wall
        set_tile(22, r, 0, c_wall)  # Right boundary wall

    # --- 3. HORIZONTAL ROOM SEPARATOR (Row 10) ---
    # Draw top wall for southern rooms with wide open central archways
    for c in range(1, 22):
        if c in [4, 5, 6, 11, 16, 17, 18]:
            # Walkable open archways between North & South
            set_tile(c, 10, 6, c_corridor)
        else:
            set_tile(c, 10, 0, c_wall)

    # --- 4. FURNITURE PLACEMENT (Zero Collision, Spacious & Clean) ---
    furniture = [
        # ==========================================
        # ROOM 1: EXECUTIVE COMMAND (North-West)
        # ==========================================
        # Wall fixtures (Row 0)
        {"uid": "f-r1-bs1", "type": "DOUBLE_BOOKSHELF", "col": 1, "row": 0},
        {"uid": "f-r1-hp1", "type": "HANGING_PLANT", "col": 3, "row": 0},
        {"uid": "f-r1-wb", "type": "WHITEBOARD", "col": 5, "row": 0},
        {"uid": "f-r1-clk", "type": "CLOCK", "col": 8, "row": 0},
        {"uid": "f-r1-bs2", "type": "DOUBLE_BOOKSHELF", "col": 9, "row": 0},
        
        # Lead Desk 1 (West)
        {"uid": "f-r1-d1", "type": "DESK_FRONT", "col": 2, "row": 3},
        {"uid": "f-r1-pc1", "type": "PC_FRONT_OFF", "col": 3, "row": 3},
        {"uid": "f-r1-ch1", "type": "CUSHIONED_CHAIR_BACK", "col": 3, "row": 5},
        {"uid": "f-r1-cof1", "type": "COFFEE", "col": 2, "row": 4},
        
        # Lead Desk 2 (East)
        {"uid": "f-r1-d2", "type": "DESK_FRONT", "col": 7, "row": 3},
        {"uid": "f-r1-pc2", "type": "PC_FRONT_OFF", "col": 8, "row": 3},
        {"uid": "f-r1-ch2", "type": "CUSHIONED_CHAIR_BACK", "col": 8, "row": 5},
        
        # Greenery & Bin
        {"uid": "f-r1-plt1", "type": "LARGE_PLANT", "col": 1, "row": 6},
        {"uid": "f-r1-plt2", "type": "PLANT_2", "col": 10, "row": 6},
        {"uid": "f-r1-bin", "type": "BIN", "col": 1, "row": 4},

        # ==========================================
        # ROOM 2: STRATEGIC BOARDROOM (North-East)
        # ==========================================
        # Wall fixtures (Row 0)
        {"uid": "f-r2-bs", "type": "DOUBLE_BOOKSHELF", "col": 12, "row": 0},
        {"uid": "f-r2-hp", "type": "HANGING_PLANT", "col": 14, "row": 0},
        {"uid": "f-r2-wb", "type": "WHITEBOARD", "col": 16, "row": 0},
        {"uid": "f-r2-art", "type": "LARGE_PAINTING", "col": 19, "row": 0},
        {"uid": "f-r2-clk", "type": "CLOCK", "col": 21, "row": 0},

        # Grand Conference Table
        {"uid": "f-r2-tbl", "type": "TABLE_FRONT", "col": 15, "row": 4},
        {"uid": "f-r2-ch1", "type": "CUSHIONED_CHAIR_SIDE", "col": 14, "row": 4},
        {"uid": "f-r2-ch2", "type": "CUSHIONED_CHAIR_SIDE", "col": 14, "row": 6},
        {"uid": "f-r2-ch3", "type": "CUSHIONED_CHAIR_SIDE:left", "col": 18, "row": 4},
        {"uid": "f-r2-ch4", "type": "CUSHIONED_CHAIR_SIDE:left", "col": 18, "row": 6},
        {"uid": "f-r2-cof1", "type": "COFFEE", "col": 15, "row": 5},
        {"uid": "f-r2-cof2", "type": "COFFEE", "col": 17, "row": 5},
        {"uid": "f-r2-plt", "type": "LARGE_PLANT", "col": 20, "row": 6},

        # ==========================================
        # ROOM 3: COLLABORATIVE DEV PODS (South-West)
        # ==========================================
        # Wall fixtures (Row 10)
        {"uid": "f-r3-hp", "type": "HANGING_PLANT", "col": 1, "row": 10},
        {"uid": "f-r3-wb", "type": "WHITEBOARD", "col": 2, "row": 10},
        {"uid": "f-r3-art", "type": "SMALL_PAINTING", "col": 8, "row": 10},

        # Workstation Pod 1
        {"uid": "f-r3-d1", "type": "DESK_FRONT", "col": 2, "row": 12},
        {"uid": "f-r3-pc1", "type": "PC_FRONT_OFF", "col": 3, "row": 12},
        {"uid": "f-r3-ch1", "type": "CUSHIONED_CHAIR_BACK", "col": 3, "row": 14},

        # Workstation Pod 2
        {"uid": "f-r3-d2", "type": "DESK_FRONT", "col": 7, "row": 12},
        {"uid": "f-r3-pc2", "type": "PC_FRONT_OFF", "col": 8, "row": 12},
        {"uid": "f-r3-ch2", "type": "CUSHIONED_CHAIR_BACK", "col": 8, "row": 14},

        # Central Pair-Programming Island
        {"uid": "f-r3-tbl", "type": "TABLE_FRONT", "col": 4, "row": 15},
        {"uid": "f-r3-pc3", "type": "PC_SIDE", "col": 4, "row": 15},
        {"uid": "f-r3-pc4", "type": "PC_SIDE", "col": 4, "row": 17},
        {"uid": "f-r3-pc5", "type": "PC_SIDE:left", "col": 6, "row": 15},
        {"uid": "f-r3-pc6", "type": "PC_SIDE:left", "col": 6, "row": 17},
        {"uid": "f-r3-ch3", "type": "WOODEN_CHAIR_SIDE", "col": 3, "row": 15},
        {"uid": "f-r3-ch4", "type": "WOODEN_CHAIR_SIDE", "col": 3, "row": 17},
        {"uid": "f-r3-ch5", "type": "WOODEN_CHAIR_SIDE:left", "col": 7, "row": 15},
        {"uid": "f-r3-ch6", "type": "WOODEN_CHAIR_SIDE:left", "col": 7, "row": 17},

        # Decor & Bin
        {"uid": "f-r3-plt1", "type": "PLANT", "col": 1, "row": 17},
        {"uid": "f-r3-bin", "type": "BIN", "col": 10, "row": 18},

        # ==========================================
        # ROOM 4: CAFE LOUNGE & ZEN OASIS (South-East)
        # ==========================================
        # Wall fixtures (Row 10)
        {"uid": "f-r4-art1", "type": "LARGE_PAINTING", "col": 13, "row": 10},
        {"uid": "f-r4-art2", "type": "SMALL_PAINTING_2", "col": 19, "row": 10},
        {"uid": "f-r4-hp", "type": "HANGING_PLANT", "col": 21, "row": 10},

        # Center Plush Sofa Suite
        {"uid": "f-r4-ctbl", "type": "COFFEE_TABLE", "col": 15, "row": 14},
        {"uid": "f-r4-s1", "type": "SOFA_FRONT", "col": 15, "row": 13},
        {"uid": "f-r4-s2", "type": "SOFA_BACK", "col": 15, "row": 16},
        {"uid": "f-r4-s3", "type": "SOFA_SIDE", "col": 14, "row": 14},
        {"uid": "f-r4-s4", "type": "SOFA_SIDE:left", "col": 17, "row": 14},
        {"uid": "f-r4-cof1", "type": "COFFEE", "col": 15, "row": 15},
        {"uid": "f-r4-cof2", "type": "COFFEE", "col": 16, "row": 14},

        # Refreshment Coffee Bar & Bench (East)
        {"uid": "f-r4-bar", "type": "SMALL_TABLE_FRONT", "col": 19, "row": 13},
        {"uid": "f-r4-cof3", "type": "COFFEE", "col": 19, "row": 13},
        {"uid": "f-r4-cct", "type": "CACTUS", "col": 20, "row": 13},
        {"uid": "f-r4-bnch", "type": "WOODEN_BENCH", "col": 19, "row": 15},

        # Zen Botanical Oasis (South)
        {"uid": "f-r4-lplt", "type": "LARGE_PLANT", "col": 19, "row": 17},
        {"uid": "f-r4-plt1", "type": "PLANT", "col": 13, "row": 18},
        {"uid": "f-r4-plt2", "type": "PLANT_2", "col": 17, "row": 18},
        {"uid": "f-r4-pot", "type": "POT", "col": 18, "row": 19}
    ]

    return {
        "version": 1,
        "cols": cols,
        "rows": rows,
        "layoutRevision": 15,
        "tiles": tiles,
        "tileColors": tile_colors,
        "furniture": furniture
    }

if __name__ == "__main__":
    layout = generate_clean_office()
    
    active_path = r"~\.pixel-agents\layout.json"
    bundled_path = r"~\.vscode\extensions\pablodelucca.pixel-agents-1.4.1\dist\webview\assets\default-layout-1.json"
    
    with open(active_path, "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)
    print(f"Applied clean office to active layout: {active_path}")

    with open(bundled_path, "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)
    print(f"Applied clean office to bundled template: {bundled_path}")
