---
name: design-taste-frontend
description: "Anti-slop frontend design engine by Leon Lin. Enforces intentional aesthetic families, mandatory Design Read, strict color limits, and dials for Variance, Motion Intensity, and Visual Density."
userFacing: true
---

# 🎨 Design Taste Frontend: The Anti-Slop Engine

> **Rule:** Never jump straight to generating code. Always execute a mandatory **Design Read** to select an intentional aesthetic family, calibrate liveliness dials, and ban generic AI design tropes.

---

## 1. The Mandatory Design Read Protocol

Before writing or editing any frontend component, the agent must output a **Design Read**:

```markdown
### 📐 DESIGN READ
- **Aesthetic Family:** [Brutalist | High-End Editorial | Warm Organic Minimalist | Cyber-Terminal | Neo-Corporate]
- **Target Persona:** [Who uses this, and what emotional register do they expect?]
- **Typography Pairing:** [Display Serif + Technical Sans | Clean Grotesk + Monospace | Bold Geometric]
- **Color Discipline:** 1 Base Canvas, 1 Dominant Neutral, Max 1 Accent (<80% saturation). Zero generic saturated purple/blue neon.
- **Liveliness Dials:**
  - *Variance (1-5):* [1 = Conservative Corporate ... 5 = Unconventional Editorial]
  - *Motion Intensity (1-5):* [1 = Instant Snap ... 5 = Fluid Spring Choreography]
  - *Visual Density (1-5):* [1 = Airy Spacious Canvas ... 5 = High-Information Compact Grid]
```

---

## 2. Absolute Banned AI Slop Patterns

1. **The AI Gradient Badge:** Never wrap random pills in `bg-gradient-to-r from-purple-500 to-indigo-500`. Badges must be purposeful, flat, or subtly bordered.
2. **The 3-Card Symmetrical SaaS Grid:** Never default to three equal-width rounded cards with glowing borders and centered generic icons. Vary hierarchy: feature one primary hero block, balance with asymmetrical columns.
3. **The Unearned Glassmorphism:** Never slap `backdrop-blur-md bg-white/10` without an underlying physical z-index layering rationale.
4. **Vague Marketing Clichés:** Banish hollow buzzwords, empty marketing jargon, and unearned abstractions. Use concrete, functional engineering copy.

---

## 3. Typography & Spacing Invariants

- **Fluid Type Scales:** Use proportional steps (`text-xs`, `text-sm`, `text-base`, `text-xl`, `text-3xl`, `text-5xl`). Display headers must feature tight tracking (`tracking-tight` or `-0.02em`).
- **Mathematical Spacing:** Anchor all margins and padding to standard 4px/8px increments (`p-2`, `p-4`, `p-6`, `p-8`, `p-12`).
- **Micro-Interactions:** Buttons must provide tactile feedback (e.g. `active:scale-[0.98]`, subtle shadow shifts, crisp border-color transitions `duration-150`).

---

## 4. Pre-Flight Delivery Checklist

Before marking frontend tasks complete:
- [ ] Contrast ratio verified (WCAG AA $\ge$ 4.5:1 for body, 3:1 for large display headers).
- [ ] Keyboard navigation: explicit `focus-visible:ring-2` on all interactive triggers.
- [ ] Mobile responsive breakpoint verified (`sm:`, `md:`, `lg:`).
- [ ] Zero unearned purple/indigo gradients.
