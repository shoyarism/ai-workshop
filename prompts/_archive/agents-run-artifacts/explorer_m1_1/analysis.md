# Website Reconnaissance System Prompt & Operational Spec: Architectural Research & Blueprint Analysis

**Author:** Explorer Agent (`explorer_m1_1`)  
**Milestone:** M1 — Architectural Blueprint & Research  
**Target Project Directory:** `C:\Users\Ideapad\.gemini\antigravity\scratch\website_recon_prompt`  
**Date:** 2026-07-30  

---

## Executive Summary

This report establishes the technical foundation, operational workflow, extraction strategies, data output schemas, and verification dimensions for building a production-grade AI System Prompt and Operational Spec (`SYSTEM_PROMPT.md`, `OPERATIONAL_SPEC.md`, `OUTPUT_SCHEMAS.md`, and `VERIFICATION_MATRIX.md`).

The system enables AI agents to systematically inspect, scrape, reverse-engineer, and synthesize complex web applications (Single Page Applications, Server-Side Rendered architectures, hybrid micro-frontends) into machine-readable technical specifications, OpenAPI schemas, component dependency graphs, and state flowcharts optimized for direct context ingestion.

---

## Section 1: Detailed Breakdown of Requirements (R1–R4)

### R1. Complete System Prompt & Execution Framework
- **Objective:** Provide a structured, multi-pass instruction framework that guides an AI coding agent through deterministic website analysis without context degradation or infinite looping.
- **Capabilities Required:**
  1. **Autonomous Phase Execution:** Strict progression through 6 operational phases.
  2. **Multi-Pass Context Strategy:** Partitioning extraction into static layout, dynamic network interception, client JS bundle decompilation, and schema synthesis.
  3. **Context Window Density Management:** Outputting compact, zero-redundancy Markdown and JSON specs to avoid context overflow when ingesting large frontend bundles.
  4. **Self-Correction & Fallbacks:** Fallback mechanisms when source maps are missing, APIs are obfuscated, or endpoints block automated probes.

### R2. Systematic Extraction & Reverse-Engineering Methodology
- **Objective:** Codify explicit engineering procedures for both static and dynamic inspection.
- **Scope & Methodologies:**
  1. **Static Analysis:**
     - DOM semantic structure extraction and Shadow DOM traversal.
     - Static asset cataloging (styles, fonts, images, web manifests).
     - JavaScript AST & bundler chunk map reconstruction (Webpack, Vite, Turbopack, Rollup).
     - Routing table discovery (React Router, Next.js App/Pages Router, Vue Router).
  2. **Dynamic Analysis:**
     - Network telemetry logging (Fetch/XHR interception via CDP/Chrome DevTools Protocol or monkey-patching).
     - API schema inference through runtime request/response payload sniffing.
     - Auth stream detection (JWT extraction, OAuth 2.0 PKCE state flow tracing, session cookies).
     - Real-time communication protocol mapping (WebSocket frames, Server-Sent Events).
  3. **Documentation & Resource Aggregation:**
     - Extracting inline Swagger/OpenAPI endpoints, embedded GraphQL schemas (`__schema` introspection), and client-side data stores (`__NEXT_DATA__`, `window.__INITIAL_STATE__`, Pinia/Zustand hydration states).

### R3. AI-Optimized Data Output Formats
- **Objective:** Define strict JSON Schemas and Markdown document standards for 4 core deliverables:
  1. **Endpoint Catalog & OpenAPI Specs:** Fully typed request/response models, auth headers, and route patterns.
  2. **Component Dependency Graphs:** Hierarchy of UI components, props, hooks, and external service calls.
  3. **State Machine Flowcharts:** Visual and structural representation of client-side state transitions, side effects, and state stores.
  4. **Data Model Specifications:** Normalized entity-relationship definitions extracted from client state models and API responses.

### R4. Verification & Testing Matrix
- **Objective:** Establish formal evaluation benchmarks, scoring rubrics (0–100%), and test suites across modern architecture paradigms:
  - React 18/19 (Next.js App Router, React Server Components, Server Actions).
  - Vue 3 / Nuxt 3 (Composition API, Pinia, Nitro server engine).
  - GraphQL APIs (Introspection, persisted queries, batching).
  - WebSockets & SSE (Bi-directional framing, subscription channels).
  - OAuth 2.0 / JWT Streams (Token refresh, bearer propagation).

---

## Section 2: Complete 6-Phase Operational Workflow

```
+-----------------------------------------------------------------------------------+
| PHASE 1: DISCOVERY & SCOPE MAPPING                                                |
| - Seed URL ingest, scope definition, sitemap.xml, robots.txt, route discovery     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 2: STRUCTURAL & ASSET SCRAPING                                              |
| - DOM tree semantics, SSR payload extraction (__NEXT_DATA__), static asset index |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 3: DYNAMIC NETWORK & TELEMETRY INTERCEPTION                                 |
| - CDP network domain hook, XHR/Fetch logging, auth header mapping, WS/SSE streams |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 4: JAVASCRIPT AST & CLIENT-SIDE REVERSE ENGINEERING                          |
| - Source map recovery, chunk graph unraveling, route/store AST parsing, WebWorkers|
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 5: ARCHITECTURAL SYNTHESIS & OPENAPI RECONSTRUCTION                         |
| - Correlate AST routes + Network logs, payload type inference, OpenAPI 3.1 synth |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 6: BLUEPRINT OUTPUT GENERATION                                              |
| - Format JSON schemas, generate AI-optimized Markdown bundles, validate artifacts |
+-----------------------------------------------------------------------------------+
```

### Phase 1: Discovery & Scope Mapping
- **Input:** Target domain / base URL.
- **Operations:**
  1. Fetch and parse `robots.txt`, `sitemap.xml`, `.well-known/openid-configuration`, `security.txt`.
  2. Perform initial HTTP HEAD/GET request to evaluate server headers (Server, X-Powered-By, Content-Security-Policy).
  3. Extract client-side routing definitions from SSR hydration blobs (`__NEXT_DATA__`, `window.__NUXT__`).
  4. Establish target domain boundaries (in-scope hostnames vs. third-party telemetry/CDN endpoints).

### Phase 2: Structural & Asset Scraping
- **Input:** Discovered HTML pages and DOM trees.
- **Operations:**
  1. Parse DOM semantic structure, extracting custom elements, web components, and pierced Shadow DOM nodes.
  2. Extract `<script>`, `<link rel="modulepreload">`, and `<style>` asset tags.
  3. Extract static assets (images, SVGs, web fonts, JSON manifests) into an Asset Catalog.
  4. Isolate inline data scripts (e.g., `application/json`, `application/ld+json`).

### Phase 3: Dynamic Network & Telemetry Interception
- **Input:** Live browser automation / headless session (Puppeteer, Playwright, or CDP).
- **Operations:**
  1. Attach network listener hooks to `Fetch.enable` and `Network.enable`.
  2. Capture request method, target URL, request headers, request body, status code, response headers, and response body.
  3. Record authorization token transmission (Bearer tokens, custom headers `X-Api-Key`, session cookies).
  4. Intercept WebSocket framing (`Network.webSocketFrameSent`, `Network.webSocketFrameReceived`) and SSE event channels (`text/event-stream`).
  5. Intercept GraphQL HTTP POST requests and map `operationName`, `query`, and `variables`.

### Phase 4: JavaScript AST & Client-Side Reverse Engineering
- **Input:** Downloaded `.js` bundle files and `.js.map` source maps.
- **Operations:**
  1. Check for accessible source maps (`.js.map`); if available, unravel original TypeScript/JavaScript source tree structure.
  2. If source maps are missing, parse minified JavaScript into an Abstract Syntax Tree (AST) using Babel parser / SWC / Acorn.
  3. Identify bundler manifest patterns (e.g., `webpackChunk`, Vite dynamic import calls `import()`, Rollup chunk hashes).
  4. Analyze client state stores (Redux `createSlice`, Zustand `create()`, Pinia `defineStore`, Vuex) to extract state shape and action types.
  5. Inspect Web Workers and WebAssembly binaries (`.wasm` export/import functions via binary header parsing).

### Phase 5: Architectural Synthesis & OpenAPI Reconstruction
- **Input:** Consolidated AST route definitions, network telemetry logs, state store schemas.
- **Operations:**
  1. Cross-reference statically discovered endpoints (from JS AST) with dynamically intercepted API traffic (Phase 3).
  2. Generalize concrete payload instances into JSON Schemas (identifying required vs. optional fields, types, enum values).
  3. Synthesize OpenAPI 3.1.0 specification documents for all identified backend endpoints.
  4. Construct Component Dependency Graphs and State Transition Flowcharts.

### Phase 6: Blueprint Output Generation
- **Input:** Synthesized architectural models.
- **Operations:**
  1. Format specifications into standardized JSON Schemas and Markdown technical blueprints.
  2. Perform schema validation to ensure syntactic correctness and structural integrity.
  3. Output artifacts to target files: Endpoint Catalog, Component Graph, State Machine Flowchart, Data Model Spec.

---

## Section 3: Technical Extraction Strategies Deep-Dive

### 1. DOM Tree Extraction & Semantic Mapping
- **Shadow DOM Pierce:** Utilize recursive DOM walkers using `Element.shadowRoot` to inspect closed/open Shadow DOM hierarchies.
- **Custom Element Register:** Query `window.customElements` registry to extract custom Web Component class definitions and observed attributes.
- **Hydration State Harvesting:** Extract script tag payloads:
  - Next.js: `document.getElementById('__NEXT_DATA__')` -> Parse JSON -> Extract `page`, `buildId`, `props.pageProps`.
  - Nuxt.js: `window.__NUXT__` -> Extract state hydration object.
  - Remix: `window.__remixContext` -> Extract route modules and initial load data.

### 2. Bundle Chunk Unraveling & Source Map Recovery
- **Source Map Fetching:** Append `.map` to script URLs or parse `//# sourceMappingURL=` comments.
- **Webpack Chunk Interception:** Hook into `window.webpackChunk` array pushes:
  ```js
  const originalPush = window.webpackChunk.push;
  window.webpackChunk.push = function(chunk) {
    const [chunkId, modules] = chunk;
    console.log("Captured Webpack Chunk:", chunkId, Object.keys(modules));
    return originalPush.apply(this, arguments);
  };
  ```
- **AST Route Traversal:** Search AST nodes for routing patterns:
  - React Router: `path:`, `element:`, `<Route path="..." component={...}>`.
  - Next.js App Router: Directory structural parsing (`page.tsx`, `layout.tsx`, `route.ts`).
  - Axios/Fetch call patterns: Find AST CallExpressions matching `axios.get()`, `axios.post()`, `fetch()`.

### 3. Web Worker & WebAssembly (WASM) Parsing
- **Web Worker Hooking:** Intercept worker instantiation:
  ```js
  const OriginalWorker = window.Worker;
  window.Worker = function(scriptURL, options) {
    console.log("Worker initialized:", scriptURL);
    const worker = new OriginalWorker(scriptURL, options);
    worker.addEventListener("message", e => console.log("Worker -> Main:", e.data));
    return worker;
  };
  ```
- **WASM Exports/Imports Inspection:** Read WASM headers using `WebAssembly.compile` or `WebAssembly.Module.exports(module)` / `WebAssembly.Module.imports(module)` to extract exported functions, imported host bindings, and memory buffer shapes.

### 4. Dynamic Network Interception & Telemetry Mapping
- **Monkey-Patching Runtime Fetch & XHR:**
  ```js
  const nativeFetch = window.fetch;
  window.fetch = async (...args) => {
    const response = await nativeFetch(...args);
    const clone = response.clone();
    console.log("Interception:", args[0], response.status, await clone.text());
    return response;
  };
  ```
- **CDP Telemetry Interception:** Use `Network.requestWillBeSent` and `Network.responseReceived` for lower-level protocol inspection, bypassing JS-level anti-tampering.

### 5. Token & Auth Header Mapping
- **Authorization Flow Extraction:** Monitor outgoing request headers for `Authorization: Bearer <token>`, `X-CSRF-Token`, or custom session headers.
- **JWT Inspection:** Automatically decode JWT header and payload sections (base64url) to extract token claims (`exp`, `iat`, `sub`, `roles`, `iss`, `aud`).
- **OAuth 2.0 State Tracking:** Trace URL query parameters for `code`, `state`, `code_challenge`, and `code_verifier` during redirect sequences.

### 6. State Store Analysis
- **Redux / Toolkit:** Inspect `window.__REDUX_DEVTOOLS_EXTENSION__` state snapshot or hook into store dispatchers.
- **Zustand:** Iterate over initialized Zustand stores attached to component modules or global window objects.
- **Pinia (Vue):** Access `window.__NUXT__.pinia` or Vue app instance root `app._context.provides.pinia.state.value`.

### 7. API Schema Inference Engine
- **JSON Payload Type Generalization:** Merge multiple JSON response instances of an endpoint into a unified schema:
  - Primitive type detection (`string`, `number`, `boolean`, `null`).
  - Array type union (`Array<string | number>`).
  - Required vs. optional property detection (if key is absent in >0 instances, mark as optional).
  - Format inferencing (ISO 8601 timestamps, UUID v4, email formats, URL strings).

---

## Section 4: Structural Design for Output Schemas & Markdown Templates

To ensure zero ambiguity and high context density for downstream AI consumption, deliverables are formatted into strict JSON schemas and corresponding structured Markdown templates.

### 1. Endpoint Catalog & OpenAPI Spec Schema (`endpoint_catalog.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EndpointCatalog",
  "type": "object",
  "required": ["baseUrl", "endpoints"],
  "properties": {
    "baseUrl": { "type": "string", "format": "uri" },
    "authentication": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["bearer", "oauth2", "cookie", "apiKey"] },
        "headerName": { "type": "string" },
        "tokenLocation": { "type": "string" }
      }
    },
    "endpoints": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "method", "parameters", "responses"],
        "properties": {
          "path": { "type": "string" },
          "method": { "type": "string", "enum": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"] },
          "summary": { "type": "string" },
          "source": { "type": "string", "enum": ["ast_discovered", "telemetry_intercepted", "hybrid"] },
          "parameters": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "in": { "type": "string", "enum": ["path", "query", "header", "cookie"] },
                "required": { "type": "boolean" },
                "type": { "type": "string" }
              }
            }
          },
          "requestBody": {
            "type": "object",
            "properties": {
              "contentType": { "type": "string" },
              "schema": { "type": "object" }
            }
          },
          "responses": {
            "type": "object",
            "additionalProperties": {
              "type": "object",
              "properties": {
                "description": { "type": "string" },
                "contentType": { "type": "string" },
                "schema": { "type": "object" }
              }
            }
          }
        }
      }
    }
  }
}
```

### 2. Component Graph Schema (`component_graph.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ComponentGraph",
  "type": "object",
  "required": ["rootComponent", "components"],
  "properties": {
    "rootComponent": { "type": "string" },
    "components": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "children", "stateDependencies", "apiDependencies"],
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "type": { "type": "string", "enum": ["page", "layout", "container", "presentational", "provider"] },
          "props": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "type": { "type": "string" },
                "required": { "type": "boolean" }
              }
            }
          },
          "children": { "type": "array", "items": { "type": "string" } },
          "stateDependencies": { "type": "array", "items": { "type": "string" } },
          "apiDependencies": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

### 3. State Machine Flowchart Schema (`state_machine.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "StateMachineFlowchart",
  "type": "object",
  "required": ["storeName", "initialState", "states", "transitions"],
  "properties": {
    "storeName": { "type": "string" },
    "type": { "type": "string", "enum": ["redux", "zustand", "pinia", "context", "vuex"] },
    "initialState": { "type": "object" },
    "states": { "type": "array", "items": { "type": "string" } },
    "transitions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["from", "to", "action", "sideEffects"],
        "properties": {
          "from": { "type": "string" },
          "to": { "type": "string" },
          "action": { "type": "string" },
          "sideEffects": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

### 4. Data Model Specification Schema (`data_model_spec.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "DataModelSpec",
  "type": "object",
  "required": ["entities"],
  "properties": {
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "fields", "relationships"],
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "fields": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "type"],
              "properties": {
                "name": { "type": "string" },
                "type": { "type": "string" },
                "isPrimaryKey": { "type": "boolean" },
                "isNullable": { "type": "boolean" }
              }
            }
          },
          "relationships": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "targetEntity": { "type": "string" },
                "type": { "type": "string", "enum": ["one-to-one", "one-to-many", "many-to-many"] },
                "foreignKey": { "type": "string" }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Section 5: Key Evaluation Dimensions & Benchmark Matrix

To systematically test an AI agent's execution of the system prompt, a matrix of evaluation dimensions and modern web framework benchmark scenarios is established.

### 1. Framework Evaluation Scenarios

| Framework / Architecture Target | Core Verification Focus | Complexity Indicators |
|---|---|---|
| **React / Next.js (App Router)** | Server vs. Client component boundaries, `__NEXT_DATA__` parsing, React Server Component (RSC) wire format decoding, Server Actions endpoints. | High (Bundled RSC stream payloads, code-split dynamic dynamic import chunks). |
| **Vue 3 / Nuxt 3** | Nitro engine endpoints, Pinia state stores, `__NUXT__` hydration object, Vue Router dynamic route definitions. | Medium-High (Proxy-based reactive state, SSR hydration payload encoding). |
| **GraphQL APIs** | Introspection query (`__schema`) processing, operation name mapping, variable types, persisted query hash matching. | Medium (Single `/graphql` POST endpoint requiring operation body parsing). |
| **WebSockets & SSE** | Event subscription taxonomy, frame payload decoding, heartbeat/ping-pong filtering, SSE event-name to payload mapping. | High (Bi-directional async streams, custom binary/JSON frame specs). |
| **OAuth 2.0 / JWT Auth Streams** | Bearer token interception, PKCE code exchange sequence mapping, refresh token cycle detection, JWT claim parsing. | High (Multi-redirect authorization flows, short-lived tokens, secure cookies). |

### 2. Scoring Rubric Dimensions (0–100%)

1. **Extraction Completeness (Weight: 25%):**
   - Percentage of total client routes discovered.
   - Percentage of total active API endpoints cataloged.
   - Asset and component coverage ratio.
2. **Schema Accuracy & Type Fidelity (Weight: 25%):**
   - Conformance of reconstructed OpenAPI specs to OpenAPI 3.1 standards.
   - Accuracy of inferred JSON types, required/optional property flags, and nested object hierarchies.
3. **Logic Tracing & Flow Depth (Weight: 20%):**
   - Correctness of state machine transition paths (action -> state update -> side effect).
   - Accuracy of component hierarchy and dependency graph connectivity.
4. **Context Window Efficiency (Weight: 15%):**
   - Information density ratio (useful schema tokens vs. verbatim code duplicate tokens).
   - Zero redundancy in final Markdown/JSON outputs.
5. **Edge Case Resilience & Obfuscation Handling (Weight: 15%):**
   - Ability to process bundle files when source maps are absent.
   - Graceful handling of anti-bot protections, rate limits, and dynamically hydrated state payloads.

---

## Section 6: Recommended Implementation Strategy for Milestone 2 & 3

1. **Milestone 2 Deliverables Construction:**
   - `SYSTEM_PROMPT.md`: Implement a modular prompt containing explicit agent system instructions, 6-phase operational workflow, phase transition triggers, and error recovery protocols.
   - `OPERATIONAL_SPEC.md`: Implement the technical execution guide detailing exact DOM query selectors, AST node patterns, monkey-patching scripts, CDP network domain commands, and OpenAPI synthesis algorithms.
   - `OUTPUT_SCHEMAS.md`: Implement ready-to-use JSON Schema definitions and Markdown context templates.
2. **Milestone 3 Deliverable Construction:**
   - `VERIFICATION_MATRIX.md`: Implement detailed benchmark test cases, scoring calculations, pass/fail rubrics, and automated audit checklists.

---
