# Original User Request

## Initial Request — 2026-07-30T20:13:23+07:00

Craft an advanced, production-grade AI System Prompt and Operational Spec designed for AI coding agents to autonomously browse, scrape, reverse-engineer, and synthesize every detail of any target website (architecture, client-side logic, API endpoints, state management, resources, data workflows, and documentation) into structured, AI-readable technical blueprints.

Working directory: C:\Users\Ideapad\.gemini\antigravity\scratch\website_recon_prompt
Integrity mode: development

## Requirements

### R1. Complete System Prompt & Execution Framework
Develop a modular, step-by-step System Prompt for AI agents detailing how to perform website reconnaissance, crawl execution, dynamic network analysis, JavaScript bundle parsing, and architectural mapping.

### R2. Systematic Extraction & Reverse-Engineering Methodology
Incorporate explicit directives for:
- Static analysis: DOM hierarchy, asset extraction, JS AST/bundle inspection, hidden route detection.
- Dynamic analysis: Network telemetry interception, API schema inference, auth token flows, WebSocket/SSE mapping.
- Documentation & resource aggregation: Scraping embedded docs, OpenAPI spec reconstruction, metadata mapping.

### R3. AI-Optimized Data Output Formats
Define standardized Markdown and JSON schema specifications for output artifacts (e.g., Endpoint Catalogs, Component Graphs, State Machine Flowcharts, Data Model Specs) formatted specifically for high context density and zero-ambiguity AI comprehension.

### R4. Verification & Testing Matrix
Provide concrete evaluation rubrics and benchmark criteria to test an agent's execution of this prompt against sample complex web applications (e.g. SPAs, SSR apps, protected APIs).

## Acceptance Criteria

### Prompt Completeness & Clarity
- [ ] Includes an explicit 6-phase operational workflow (Discovery, Scraping, Telemetry, Reverse-Engineering, Synthesis, Output).
- [ ] Contains comprehensive extraction guidelines for frontend logic, API contracts, state management, and asset dependencies.
- [ ] Defines structured Markdown & JSON output schemas tailored for direct ingestion into AI context windows.
- [ ] Includes edge-case handling guidelines (anti-bot, dynamic rendering, obfuscation, rate-limiting).
