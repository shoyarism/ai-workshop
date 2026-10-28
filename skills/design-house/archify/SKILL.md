---
name: archify
description: "Generates interactive, validated, self-contained HTML architecture, sequence, and component diagrams from codebases, PRDs, and systems design prompts."
userFacing: true
---

# 📐 Archify: Interactive Architecture Diagram Engine

> **Purpose:** Transforms complex software architectures, module boundaries, network flows, and database relations into interactive, self-contained HTML diagrams that can be inspected, panned, zoomed, and embedded directly into documentation.

---

## 1. Core Operating Flow

```
┌──────────────────┐     ┌───────────────────────┐     ┌──────────────────────┐
│ Codebase / PRD   │ ──> │ AST & Dependency Flow │ ──> │ Self-Contained HTML  │
│ Architecture Doc │     │ Boundary Extraction   │     │ Interactive Canvas   │
└──────────────────┘     └───────────────────────┘     └──────────────────────┘
```

When invoked:
1. **Reconnaissance:** Scan files, directories, imports, and interface definitions to extract components, boundaries, and communication protocols (HTTP, gRPC, WebSocket, EventBus).
2. **Topology Synthesis:** Determine the optimal diagram topology:
   - **System Architecture:** High-level component boxes, services, queues, and gateways.
   - **Sequence Diagram:** Chronological interaction flow between agents/services.
   - **Data Flow Graph:** Pipeline from raw ingestion to persistent storage.
3. **Interactive HTML Generation:** Emit a clean, self-contained single-file HTML artifact (`.html`) featuring:
   - Dark-mode responsive canvas styling.
   - SVG-based pan and zoom controls.
   - Clickable nodes displaying component metadata, file paths, and interface contracts.
   - Export buttons (SVG / PNG snapshot).

---

## 2. Invariants & Output Requirements

- **Self-Contained:** Zero external stylesheet dependencies that require network access; embed CSS and lightweight SVG pan/zoom scripts inline.
- **Hierarchy Clarity:** Use distinct colors and borders to group subsystems into logical containers (e.g. Client Layer, API Gateway, Microservices, Storage Layer).
- **Directional Grounding:** Label every arrow with its protocol and data payload (e.g., `POST /v1/chat -> JSON {message}`).
- **Artifact Output:** Save interactive diagrams to `<appDataDir>\brain\<conversation-id>\architecture_<topic>.html` and provide clickable links in the conversation.
