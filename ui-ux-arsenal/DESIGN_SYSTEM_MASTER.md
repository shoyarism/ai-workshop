# UI/UX Master Design System & Architectural Standard

Welcome to the **Workshop UI/UX Design Arsenal**. This guide establishes the visual grammar, spatial geometry, typographic hierarchies, color science, and motion principles for all user interfaces crafted within the Workshop.

---

## 1. Visual Aesthetics & Design Archetypes

### A. Clean Modern SaaS (Linear / Raycast Style)
- **Backgrounds**: Deep neutral darks (`#0a0c10`, `#11141a`) or pristine light (`#f8fafc`, `#ffffff`).
- **Borders**: Hairline 1px borders with subtle alpha (`rgba(255, 255, 255, 0.08)` or `border-zinc-800`).
- **Typography**: Clean geometric grotesk (`Inter`, `Geist Sans`, `Plus Jakarta Sans`).
- **Accents**: Single vibrant neon or high-chroma primary (Electric Indigo `#6366f1`, Emerald `#10b981`, Cyber Cyan `#06b6d4`).

### B. Dark Glassmorphism & Depth
- **Surface Material**: `backdrop-blur-md bg-white/[0.04] border border-white/[0.08] shadow-2xl`.
- **Gradients**: Subtle radial background glows (`bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/30 via-slate-950 to-black`).
- **Elevation**: Multi-layered shadows with ambient light.

### C. Industrial / Neu-Brutalism
- **Borders**: Sharp 2px solid black or high-contrast borders (`border-2 border-black dark:border-white`).
- **Shadows**: Hard-edge unblurred drop shadows (`shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]`).
- **Palette**: High saturation pops (Safety Yellow `#facc15`, Acid Lime `#84cc16`, Hot Coral `#f43f5e`).
- **Typography**: Monospace and bold sans-serif (`Space Grotesk`, `JetBrains Mono`).

---

## 2. Spatial Geometry & The 4/8pt Grid System

All layouts, margins, paddings, and component sizes MUST adhere to the 4pt / 8pt scale:

| Token | Pixels | Tailwind Equivalent | Primary Usage |
| :--- | :--- | :--- | :--- |
| **`space-1`** | 4px | `p-1`, `gap-1` | Tight badge padding, micro-spacing |
| **`space-2`** | 8px | `p-2`, `gap-2` | Icon button padding, chip gaps |
| **`space-3`** | 12px | `p-3`, `gap-3` | Compact card padding, form field vertical padding |
| **`space-4`** | 16px | `p-4`, `gap-4` | Standard card internal padding, standard gaps |
| **`space-6`** | 24px | `p-6`, `gap-6` | Section padding, container gaps |
| **`space-8`** | 32px | `p-8`, `gap-8` | Modal padding, major section dividers |
| **`space-12`**| 48px | `p-12`, `gap-12` | Hero section vertical spacing |

---

## 3. Typographic Hierarchy & Scale

```
Display Large : 48px / 1.1 line-height / font-bold tracking-tight
Heading 1     : 36px / 1.2 line-height / font-bold tracking-tight
Heading 2     : 24px / 1.3 line-height / font-semibold tracking-tight
Heading 3     : 18px / 1.4 line-height / font-semibold
Body Regular  : 14px / 1.5 line-height / font-normal text-muted-foreground
Body Small    : 12px / 1.5 line-height / font-normal
Caption/Code  : 11px / 1.4 line-height / font-mono uppercase tracking-wider
```

---

## 4. Motion Physics & Animation Curves

Use **spring-based physics** or smooth cubic-beziers for natural feel:

- **Hover Transitions**: `transition-all duration-150 ease-out`
- **Modal / Drawer Enter**: `cubic-bezier(0.16, 1, 0.3, 1)` (Duration: 300ms)
- **Scale Feedback**: Active button click `active:scale-[0.98]`
- **Framer Motion Preset**:
  ```tsx
  export const springPreset = {
    type: "spring",
    stiffness: 400,
    damping: 30
  };
  
  export const fadeInSlideUp = {
    initial: { opacity: 0, y: 12 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -8 },
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] }
  };
  ```

---

## 5. Accessibility (WCAG 2.1 AA / AAA Standards)

1. **Color Contrast**: Normal text must achieve at least **4.5:1** contrast against its background. Large text (>=18px) requires **3.0:1**.
2. **Focus Rings**: Always provide distinct keyboard focus indicators (`focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-500`).
3. **Screen Readers**: Provide `aria-label`, `aria-expanded`, and semantic HTML tags (`<main>`, `<nav>`, `<header>`, `<article>`).
