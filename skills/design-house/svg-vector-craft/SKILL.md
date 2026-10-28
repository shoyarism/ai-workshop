---
name: svg-vector-craft
description: Precision vector SVG engineering, text containment mathematics, resolution-independent layout, and technical illustration. Use when designing SVG banners, architecture diagrams, technical charts, or visual assets that must never clip or overflow across devices.
---

# SVG Vector Craft & Precision Layout Engineering

## 1. Core Principles: Vector Geometry vs Raster Habits

Designing in SVG requires strict mathematical discipline. Unlike HTML DOM elements, SVG elements do **not** reflow, wrap text automatically, or manage their own margins. Every coordinate is an absolute Cartesian point in space:

* **Aspect Ratio Invariants:** Always specify an explicit `viewBox="0 0 W H"` attribute. Never rely on naked `width` and `height` without a `viewBox`.
* **Zero Subpixel Blur:** To render razor-sharp 1px lines on standard screens, offset 1px vertical or horizontal strokes by `0.5px` (e.g. `x1="20.5" x2="20.5"`), or use even coordinates with an explicit `stroke-width="1.2"`.

---

## 2. The SVG Text Containment Calculus

The number one defect in AI-generated SVG diagrams is **text spilling out of bounding boxes**. 

### The Math of Character Width Estimation
In SVG, the browser computes character widths at render time using whichever system font is locally available. Because letter widths vary by OS (Windows vs macOS vs Linux), you must calculate maximum bounding limits conservatively:

$$\text{Estimated Line Width} \approx \text{Character Count} \times (\text{Font Size} \times K)$$

* For **Standard Sans-Serif** (`Helvetica`, `Arial`, `-apple-system`): $K \approx 0.62$
* For **Monospaced Fonts** (`Consolas`, `SF Mono`, `Courier`): $K \approx 0.65$

### The Hard Multi-line Wrapping Rule
SVG `<text>` tags will render on a single continuous horizontal line forever unless explicitly segmented into `<tspan>` nodes.

```xml
<!-- WRONG: Text will spill past 240px container -->
<text x="16" y="24" font-size="12">This is a long sentence that will spill completely out of the box in SVG.</text>

<!-- CORRECT: Mathematically wrapped with vertical line rhythm -->
<text x="16" y="24" font-size="12">
  <tspan x="16" dy="0">This is a long sentence</tspan>
  <tspan x="16" dy="18">that is safely contained</tspan>
  <tspan x="16" dy="18">within the bounding box.</tspan>
</text>
```

### Text Anchoring Strategy
* **Left-Aligned Text:** Use `text-anchor="start"`. Set `x` at least 16–20px inside the left container border.
* **Centered Data:** Use `text-anchor="middle"`. Set `x` at the exact geometric midpoint of the container ($X = \text{BoxLeft} + \frac{\text{Width}}{2}$).
* **Right-Aligned Data:** Always use `text-anchor="end"`. Set `x` at $\text{BoxRight} - 16\text{px}$. This makes it mathematically impossible for text to spill past the right border regardless of client font scaling.

---

## 3. Human Detailing: Optical Calibration Marks

Human technical design features functional registration and measurement details that give vector assets tactile quality:

### A. Screenprint Registration Targets
```xml
<g stroke="#eb5e28" stroke-width="1" opacity="0.8">
  <circle cx="20" cy="20" r="4" fill="none"/>
  <line x1="12" y1="20" x2="28" y2="20"/>
  <line x1="20" y1="12" x2="20" y2="28"/>
</g>
```

### B. Precision Dimension Ticks
```xml
<g stroke="#252730" stroke-width="1">
  <line x1="20" y1="260" x2="30" y2="260"/>
  <line x1="1130" y1="260" x2="1140" y2="260"/>
</g>
```

---

## 4. Pre-Flight SVG Audit Checklist

Before releasing any SVG diagram or hero banner:
- [ ] **Boundary Containment:** Does every text element have at least a 16px buffer from the nearest container wall?
- [ ] **Multi-Line Check:** Are any strings longer than 32 characters in a narrow column without `<tspan>` wrapping?
- [ ] **Right-Margin Anchor:** Are all right-aligned labels anchored with `text-anchor="end"`?
- [ ] **ViewBox Consistency:** Does the `viewBox` width and height match the intended canvas aspect ratio?
- [ ] **Zero Competing Accents:** Is there only one primary chromatic accent hue in the entire graphic?
