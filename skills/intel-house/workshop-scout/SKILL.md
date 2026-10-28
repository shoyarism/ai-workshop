---
name: workshop-scout
description: Proactively inspects the Workshop arsenal to discover, evaluate, and dynamically select the most relevant skills, MCP tools, templates, and frameworks for the user's project.
---

# Workshop Scout — Autonomous Arsenal Selector & Resource Router

Use this skill at the beginning of ANY project, feature request, or complex task to scan the Workshop arsenal (`Workshop/skills/` or via `uv run python Workshop/scripts/workshop.py search "<keyword>"`) and select the optimal tools, skills, and reference code.

---

## 1. The Autonomous Scouting Protocol

When starting a project or receiving a prompt:

1. **Analyze Project Domain & Requirements**:
   - Determine core needs: Frontend/UI, Backend/API, Motion/Video, Web Scraping/Stealth, Multi-Agent Swarm, Database/Cloud, AI Pipelines.

2. **Scan the Workshop Matrix**:
   - **Frontend UI & Anti-Slop Design**: Load `skills/design-taste-frontend/SKILL.md`, `skills/impeccable/SKILL.md`, `skills/uiux-designer/SKILL.md`, `skills/frontend-design/SKILL.md`. Enforce zero purple gradients, zero generic layouts, and audit against 38 Anti-Slop rules.
   - **Video & Motion Graphics**: Activate `hyperframes/skills/` (including `hyperframes-core`, `hyperframes-animation`, `faceless-explainer`, `pr-to-video`) and reference `Workshop/hyperframes`.
   - **Stealth Browsing & Web Automation**: Activate `camofox` MCP (`http://localhost:9377`) for anti-detect scraping + `browser-use/skills/` + `stagehand` / `Scrapling`.
   - **Architecture & Code Quality**: Activate `skills/improve-codebase-architecture`, `ponytail/skills`, and `skills/systematic-debugging`.
   - **Generative AI & Model Pipelines**: Reference `Workshop/open-generative-ai` or `open-image-models`.
   - **Autonomous Agents & Characters**: Reference `Workshop/eliza` or `openai-agents-sdk` or `google-adk`.
   - **Internet & Social Research**: Activate `Workshop/skills/agent-reach` for multi-platform web intelligence.
   - **Domain Skills Catalog**: Search the 990+ skills via `uv run python Workshop/scripts/workshop.py search "<query>"`.

3. **Announce Selected Arsenal**:
   Briefly state the selected tools to the user:
   > *"🎯 Workshop Arsenal Selected for this Task:*
   > *- Skills: [Skill A, Skill B]*
   > *- MCP Tools: [Tool A, Tool B]*
   > *- Reference Repo: [Repo Name]"*

4. **Execute using the Loaded Directives**.
