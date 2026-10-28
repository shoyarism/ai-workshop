---
name: heroui-v3-design-system
description: "Guidelines, component primitives, tokens, and aesthetic principles for crafting modern, accessible web applications using HeroUI v3 (formerly NextUI) with glassmorphism and styled tokens."
---

# HeroUI v3 (NextUI) Design System & Architectural Skill

## Overview
HeroUI (formerly NextUI) v3 provides guidelines, component primitives, tokens, and aesthetic principles for crafting modern, accessible, high-performance web applications with stunning visual depth, glassmorphic surfaces, animated segmented controls, and customizable themes.

## Key Design Principles of HeroUI v3

### 1. Visual Aesthetics & Material Depth
- **Translucent Surfaces**: Surface containers use backdrop blur and subtle opacity (ackdrop-blur-md bg-surface/75 border border-default-200/50).
- **Glow & Radiant Highlights**: Subtle radial glow meshes behind key hero headers or primary CTA cards (
adial-gradient(ellipse at top, rgba(primary, 0.15), transparent 70%)).
- **Curvature & Radii**: Generous corner radii (
ounded-2xl to 
ounded-3xl for cards, 
ounded-full for chips and pill tabs).

### 2. Core Component Primitives & Styling Tokens

| Primitive | HeroUI v3 Pattern | Key CSS Classes / Properties |
|---|---|---|
| **Card** | Elevated container with header, body, footer slots | heroui-card, 
ounded-2xl, p-6, order border-default-100, shadow-medium, hover:scale-[1.01] |
| **Chip / Badge** | Status indicators with dot or avatar | heroui-chip, 
ounded-full, px-3 py-1, ont-semibold text-xs (variants: solid, lat, dot, ordered) |
| **Tabs / Segment** | Pill-shaped tab bar with elevated active indicator | heroui-tabs, g-default-100 p-1.5 rounded-full flex gap-1, heroui-tab-active: bg-surface shadow-sm text-primary |
| **Button** | High-energy tactile buttons with ripple and scale physics | heroui-btn, ctive:scale-95, ont-bold, 
ounded-xl, 	ransition-all (colors: primary, danger, success) |
| **Input / Search** | Floating label or inset pill search input | heroui-input, g-default-100 focus:bg-surface border focus:border-primary rounded-xl px-4 py-2.5 |
| **Slider** | Fluid track with distinct rounded thumb | heroui-slider, accent color with live value badge |
| **Table** | Striped / clean rows with rounded header bar | heroui-table, 
ounded-2xl overflow-hidden, 	h: bg-default-100 text-default-600 font-bold uppercase |
| **Modal** | Blurred backdrop with smooth spring scale | heroui-modal, ackdrop-blur-md bg-black/40, card: rounded-3xl shadow-2xl scale-100 |

### 3. Theme & Contrast Rules
- **Light Theme**: Bright, clean backgrounds (#FAFAFA / #F4F4F5), crisp text (#11181C), soft border lines (#E4E4E7).
- **Dark Theme**: Deep void slate (#000000 / #0C0E14), high contrast text (#ECEDEE), radiant colored glows (primary-500: #090EFB, danger-500: #FC0C04).
- **Accessibility**: All text and interactive controls must adhere to WCAG 2.1 AA (contrast ratio >= 4.5:1).
