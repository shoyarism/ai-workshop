---
name: diagram-design
description: "Universal diagram and visual hierarchy engine. Produces publication-grade Mermaid, SVG, and conceptual diagrams with strict visual rhythm and anti-slop clarity."
userFacing: true
---

# 📐 Diagram Design: Visual Hierarchy & Systems Cartography

> **Purpose:** Transforms abstract ideas, control loops, execution graphs, and protocol state machines into visually compelling, crystal-clear architectural diagrams.

---

## 1. Supported Diagram Typologies

| Type | Best Used For | Format |
|---|---|---|
| **Directed Flowcharts** | Decision logic, build pipelines, agent loops | Mermaid (`flowchart TD` / `flowchart LR`) |
| **Sequence Diagrams** | Multi-agent handoffs, network protocols, API requests | Mermaid (`sequenceDiagram`) |
| **State Machine Graphs**| Task lifecycles, connection states, circuit breakers | Mermaid (`stateDiagram-v2`) |
| **Entity-Relationship**| Database schemas, foreign key mappings | Mermaid (`erDiagram`) |
| **High-Precision SVG** | Complex system topologies, custom hardware/network layouts | Raw Scalable Vector Graphics (`.svg`) |

---

## 2. Mermaid Anti-Slop Rules

1. **Quote Complex Node Labels:** Always wrap labels containing parentheses, brackets, or code symbols in double quotes:
   `id["Task Queue (FIFO)"]` instead of `id[Task Queue (FIFO)]`.
2. **Cluster Grouping:** Use `subgraph` blocks to visually demarcate service boundaries, trust perimeters, or execution tiers.
3. **Intentional Edge Labeling:** Every critical edge must specify the transport and payload (`-->|HTTPS JSON|` or `-->|Event Stream|`).
4. **Restrained Color Palettes:** In SVG or styled Mermaid, limit fills to neutral darks (`#18181b`, `#27272a`), muted borders (`#3f3f46`), and a single deliberate accent (`#3b82f6` or `#10b981`).
