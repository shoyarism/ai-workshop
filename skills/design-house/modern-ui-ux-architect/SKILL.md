---
name: modern-ui-ux-architect
description: Elite UI/UX frontend architecture and design standard. Use when creating modern web applications, landing pages, interactive dashboards, design systems, and animations.
---

# Modern UI/UX Architect Skill

Use this skill to design and implement world-class web applications, landing pages, and component design systems.

## 1. Design System Foundations

Reference: `ui-ux-arsenal/DESIGN_SYSTEM_MASTER.md` & `ui-ux-arsenal/tokens/design_tokens.json`

### Core Aesthetics
1. **Clean Dark Mode & Glassmorphism**: `backdrop-blur-md bg-zinc-900/60 border border-zinc-800 shadow-xl`
2. **Refined Typography**: Modern grotesk (`Inter`, `Geist Sans`, `Plus Jakarta Sans`) with tight letter spacing (`tracking-tight`).
3. **Harmonious Accents**: Subtle gradients, electric indigo/cyan glow effects, and micro-interactions.

## 2. Animation & Spring Physics

Integrate Framer Motion / Motion primitives:
```tsx
import { motion } from "framer-motion";

export function HeroCard({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      className="p-6 rounded-2xl bg-zinc-900/80 border border-zinc-800/80 hover:border-indigo-500/50 transition-colors"
    >
      <h3 className="text-xl font-semibold text-zinc-100">{title}</h3>
      <p className="mt-2 text-sm text-zinc-400">{subtitle}</p>
    </motion.div>
  );
}
```

## 3. Accessibility Standard

- Minimum 4.5:1 text-to-background contrast ratio (WCAG 2.1 AA).
- Explicit focus states (`focus-visible:ring-2 focus-visible:ring-indigo-500`).
- Responsive layouts with mobile-first breakpoints (`sm`, `md`, `lg`, `xl`, `2xl`).
