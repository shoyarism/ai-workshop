#!/usr/bin/env python3
"""Compose the 6 restyle presets into one 3x2 gallery with labels."""
from PIL import Image, ImageDraw, ImageFont

SS = "/Users/snoo/Documents/Kiwi/Projects/DesignSystem/styleseed/showcase"
OUT = SS + "/style-gallery.png"

items = [
    ("swiss",          "SWISS",          "grid honesty · sharp · red"),
    ("editorial",      "EDITORIAL",      "serif seasoning · airy · oxblood"),
    ("technical",      "TECHNICAL",      "dark · dense · teal signal"),
    ("warm-dtc",       "WARM-DTC",       "pill · warm · terracotta"),
    ("minimal-mono",   "MINIMAL-MONO",   "whitespace · light · one accent"),
    ("brutalist-lite", "BRUTALIST-LITE", "hard borders · bold · cobalt"),
]

TW = 760                       # thumb width
TH = round(TW * 860 / 1240)    # thumb height (keep 1240:860)
PAD = 44
GAP = 24
LABEL_H = 74
TITLE_H = 108
COLS = 3
BG = (18, 18, 20)
FG = (245, 245, 245)
MUTED = (150, 150, 155)
CARD = (30, 30, 34)


def font(sz, bold=False):
    names = ["/System/Library/Fonts/SFNS.ttf", "/System/Library/Fonts/Helvetica.ttc"]
    for n in names:
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


rows = 2
W = PAD * 2 + TW * COLS + GAP * (COLS - 1)
H = TITLE_H + PAD + rows * (TH + LABEL_H) + (rows - 1) * GAP + PAD
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

f_title = font(40, True)
f_sub = font(21)
f_lbl = font(24, True)
f_cap = font(19)

title = "Same product. Six presets. One  /ss-restyle  away."
d.text((PAD, 40), title, font=f_title, fill=FG)
sub = "Each is a coherent coordinate across the dial axes — distinct, never generic. Built with StyleSeed."
d.text((PAD, 40 + 52), sub, font=f_sub, fill=MUTED)

y0 = TITLE_H + PAD
for i, (fn, label, cap) in enumerate(items):
    r, c = divmod(i, COLS)
    x = PAD + c * (TW + GAP)
    y = y0 + r * (TH + LABEL_H + GAP)
    thumb = Image.open(f"{SS}/style-{fn}.png").convert("RGB").resize((TW, TH), Image.LANCZOS)
    # thin frame
    d.rectangle([x - 1, y - 1, x + TW, y + TH], outline=(60, 60, 66), width=1)
    img.paste(thumb, (x, y))
    ly = y + TH + 16
    d.text((x, ly), label, font=f_lbl, fill=FG)
    d.text((x, ly + 30), cap, font=f_cap, fill=MUTED)

img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({W}x{H})")
