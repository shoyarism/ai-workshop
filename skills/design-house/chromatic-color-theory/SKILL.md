---
name: chromatic-color-theory
description: Professional color formulation, chromatic harmony, anodized and tactile palettes, and contrast mathematics. Use when selecting color schemes, building brand palettes, or calibrating UI and graphic color hierarchies for human visual comfort.
---

# Chromatic Color Theory & Palette Architecture

## 1. The Core Law: The 60-30-10 Harmonic Ratio

Uncalibrated designs fail because too many saturated hues compete for the viewer's eye simultaneously. High-craft palettes follow strict mathematical distribution:

* **60% Dominant Ground (Substrate):**
  The canvas foundation. In dark mode, avoid raw `#000000` (causes harsh eye fatigue); use matte anodized carbon, deep slate (`#121316`), or warm espresso graphite (`#141312`). In light mode, avoid blinding `#FFFFFF`; use warm alabaster, bone, or silk paper (`#f4f3ee`).
* **30% Structural Supporting Neutrals:**
  Dividing rails, borders, secondary text, and container backgrounds. Aluminum silver (`#8e919a`), muted titanium, or deep graphite container fill (`#191a22`).
* **10% The Single Functional Spot Color:**
  **One** deliberate, authoritative chromatic accent (e.g. Signal Vermilion `#eb5e28`, International Klein Blue `#002fa7`, or Forest Jade `#107e54`). Used strictly for primary calls-to-action, status alerts, or brand signatures.

---

## 2. Eliminating Chromatic Clashing & Optical Vibration

### The Simultaneous Contrast Trap
Placing two highly saturated complementary colors directly against each other (e.g. saturated hazard yellow `#e2f800` right beside saturated orange `#ff4400`) creates **simultaneous contrast vibration**. The human eye struggles to focus on both wavelengths at the same time, producing visual irritation and a cheap, amateur feel.

### Rules for Harmonic Accent Selection
1. **Never pit two saturated warm accents against each other.** If you choose Vermilion/Orange, pair it with muted, desaturated neutrals, not bright yellow or hot pink.
2. **Temperature Grounding:** If your dominant ground has cool undertones (blue-tinted graphite `#0f1118`), balance it with a warm accent (ochre, amber, vermilion) to create rich chromatic depth.
3. **Munsell Value Separation:** Ensure adjacent colors differ by at least 30% in value (lightness), not just hue. Hue contrast without value contrast is invisible to color-blind viewers and muddy in print.

---

## 3. Curated Anodized & Tactile Palettes

### Archetype A: The Teenage Engineering Industrial Rack
* **Substrate (60%):** `#111215` (Matte Anodized Charcoal)
* **Structure (30%):** `#252730` (Milled Aluminum Rail) & `#8e919a` (Steel Legend Text)
* **Spot Accent (10%):** `#eb5e28` (Safety Vermilion / Warm Ochre)
* **High-Contrast Text:** `#eceae4` (Silk Bone White)

### Archetype B: The Swiss Editorial Broadsheet
* **Substrate (60%):** `#f5f4ef` (Uncoated Book Paper)
* **Structure (30%):** `#323338` (Deep Printer's Ink) & `#787982` (Lead Rules)
* **Spot Accent (10%):** `#d83120` (Swiss Red / Vermilion)

### Archetype C: The Precision Aerospace Instrument
* **Substrate (60%):** `#0c0e14` (Deep Night Carbon)
* **Structure (30%):** `#1e2230` (Titanium Chassis) & `#7d859b` (Telemetry Slate)
* **Spot Accent (10%):** `#2563eb` (Precision Blue)

---

## 4. Mathematical Contrast & Accessibility Ratios

Always verify luminance contrast ratios before finalizing:
* **WCAG 2.2 Level AA:** Minimum $4.5:1$ contrast ratio for regular body text; $3:1$ for large text ($> 18\text{pt}$ or $14\text{pt}$ bold).
* **WCAG 2.2 Level AAA (Recommended):** Minimum $7:1$ contrast ratio for normal text; $4.5:1$ for display text.
* **APCA (Advanced Perceptual Contrast Algorithm):** Minimum $L^c \ge 60$ for body copy and $L^c \ge 45$ for bold headings against dark substrates.
