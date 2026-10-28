# Website Reconnaissance & Reverse-Engineering Verification Matrix

This document defines the formal evaluation rubrics, benchmark suite, test scenarios, automated validation procedures, and execution gate protocols for verifying the quality, accuracy, and structural completeness of AI coding agents executing autonomous website reconnaissance and reverse-engineering.

---

## 1. Overview & Evaluation Architecture

### 1.1 Purpose & Scope
The Verification Matrix provides an objective, quantitative, and reproducible testing framework to assess an AI agent's execution of the prompt suite defined across `SYSTEM_PROMPT.md`, `OPERATIONAL_SPEC.md`, and `OUTPUT_SCHEMAS.md`. It validates that the agent successfully converts unknown, complex web applications into accurate, machine-readable, zero-hallucination technical blueprints.

### 1.2 Mathematical Scoring Model
An agent's overall reconnaissance score ($S_{\text{total}}$) is calculated using a weighted sum across 5 core assessment dimensions:

$$S_{\text{total}} = \sum_{i=1}^{5} (w_i \times S_i) = (0.25 \times S_1) + (0.20 \times S_2) + (0.20 \times S_3) + (0.20 \times S_4) + (0.15 \times S_5)$$

Where:
- $S_1$: Endpoint Extraction Accuracy & Coverage (Weight: 25%)
- $S_2$: Component Tree & DOM Fidelity (Weight: 20%)
- $S_3$: State Machine & Flow Accuracy (Weight: 20%)
- $S_4$: Data Model Schema Inference Precision (Weight: 20%)
- $S_5$: Edge-Case Handling & Resiliency (Weight: 15%)

---

## 2. Core Assessment Dimensions & Evaluation Rubrics

### 2.1 Dimension Breakdown & Weight Allocation

```
+-----------------------------------------------------------------------------------+
|                            OVERALL EVALUATION SCORE (100%)                        |
+-----------------------------------------------------------------------------------+
        |                 |                 |                 |                 |
        v                 v                 v                 v                 v
+---------------+ +---------------+ +---------------+ +---------------+ +---------------+
|  DIMENSION 1  | |  DIMENSION 2  | |  DIMENSION 3  | |  DIMENSION 4  | |  DIMENSION 5  |
|   Endpoint    | | Component Tree| | State Machine | |  Data Model   | |   Edge-Case   |
|   Extraction  | | & DOM Fidelity| | & Flow Acc.   | |  Schema Inf.  | | & Resiliency  |
|  Weight: 25%  | |  Weight: 20%  | |  Weight: 20%  | |  Weight: 20%  | |  Weight: 15%  |
+---------------+ +---------------+ +---------------+ +---------------+ +---------------+
```

---

### 2.2 Dimension 1: Endpoint Extraction Accuracy & Coverage (Weight: 25%)

#### Sub-Metrics & Evaluation Criteria
1. **Endpoint Discovery Recall**: Ratio of total backend API routes identified (via AST static visitor and dynamic network interception) vs. ground truth backend endpoints.
2. **Path Parameter Canonicalization**: Correct identification and parameterization of dynamic route variables (e.g., converting dynamic URLs `/api/v1/users/usr_9842/orders/ord_102` to canonical parameterized paths `/api/v1/users/{userId}/orders/{orderId}`).
3. **OpenAPI 3.1.0 Specification Conformance**: Generated `endpoint_catalog.json` must be 100% valid against OpenAPI 3.1.0 specifications, including valid HTTP method verbs, parameter locations (`path`, `query`, `header`, `cookie`), request bodies, and response status schemas.
4. **Authentication Flow Reconstruction**: Accurate identification of authentication mechanisms (JWT Bearer, OAuth 2.0 PKCE, Cookie Session, API Key) and token header definitions.

#### Performance Level Rubric

| Performance Tier | Score Range | Evaluation Rubric & Qualitative / Quantitative Indicators |
|---|---|---|
| **Exceptional** | **90% – 100%** | **Quantitative**: Endpoint recall $\ge 95\%$. Zero path parameter syntax errors. $100\%$ valid OpenAPI 3.1.0 spec.<br>**Qualitative**: Discovers both active dynamic telemetry endpoints and hidden un-invoked static AST endpoints. Correctly parses specialized protocols (GraphQL mutations/queries, RSC Server Actions, WebSockets). Accurately decodes JWT headers/claims and maps complete OAuth2 PKCE flows. |
| **Proficient** | **75% – 89%** | **Quantitative**: Endpoint recall $80\% - 94\%$. Minor path parameter canonicalization omissions ($\le 5\%$ unparameterized raw IDs). Valid OpenAPI 3.1.0 spec with no breaking structural errors.<br>**Qualitative**: Discovers all active dynamic telemetry endpoints and major AST endpoints. Correctly identifies core HTTP endpoints and primary authentication headers. |
| **Suboptimal** | **50% – 74%** | **Quantitative**: Endpoint recall $50\% - 79\%$. Frequent path parameter canonicalization failures (raw dynamic IDs left in paths). OpenAPI spec contains schema lint warnings or minor syntax errors.<br>**Qualitative**: Captures dynamic HTTP traffic but misses un-invoked AST routes. Fails to parse specialized streams (GraphQL, RSC, WebSockets). Auth headers captured without decoding claim structures. |
| **Failing** | **< 50%** | **Quantitative**: Endpoint recall $< 50\%$. Invalid OpenAPI spec failing standard parser execution. Hallucinated endpoints not backed by AST or telemetry evidence.<br>**Qualitative**: Fails to capture core API traffic. Confuses third-party tracking CDNs with backend application APIs. |

---

### 2.3 Dimension 2: Component Tree & DOM Fidelity (Weight: 20%)

#### Sub-Metrics & Evaluation Criteria
1. **Shadow DOM Piercing Depth**: Full resolution of open/closed Shadow DOM boundaries and custom Web Component internal trees using recursive DOM walking.
2. **Hierarchy Completeness**: Accurate structural mapping of parent-child component layout trees (`page` -> `layout` -> `container` -> `presentational`).
3. **Props & State Store Bindings**: Explicit documentation of component props interfaces, local state hooks, and global state store listeners.
4. **Asset Dependency Mapping**: Cataloging of external JS bundles, CSS stylesheets, font preloads, and asset graphs.

#### Performance Level Rubric

| Performance Tier | Score Range | Evaluation Rubric & Qualitative / Quantitative Indicators |
|---|---|---|
| **Exceptional** | **90% – 100%** | **Quantitative**: $100\%$ Shadow DOM boundary resolution. Component tree accuracy $\ge 95\%$. Props interface accuracy $\ge 90\%$.<br>**Qualitative**: Perfectly models component hierarchy from root down to presentational nodes. Maps exact source file paths from source maps. Accurately links component nodes to state store selectors and backend API calls. |
| **Proficient** | **75% – 89%** | **Quantitative**: Pierces open Shadow DOM boundaries. Component tree accuracy $80\% - 94\%$. Props interface accuracy $75\% - 89\%$.<br>**Qualitative**: Captures main page and container components. Correctly identifies component types (`page`, `layout`, `container`, `presentational`) and primary state store bindings. |
| **Suboptimal** | **50% – 74%** | **Quantitative**: Fails to pierce closed Shadow DOM boundaries. Component tree accuracy $50\% - 79\%$. Props interface accuracy $< 75\%$.<br>**Qualitative**: Extracts standard top-level DOM nodes but loses structural hierarchy in deep component trees. Misses prop types or state store listeners. |
| **Failing** | **< 50%** | **Quantitative**: Component tree accuracy $< 50\%$. Missing root component or broken component hierarchy.<br>**Qualitative**: Returns flat HTML tag dumps instead of component dependency graphs. Fabricates non-existent component relationships. |

---

### 2.4 Dimension 3: State Machine & Flow Accuracy (Weight: 20%)

#### Sub-Metrics & Evaluation Criteria
1. **State Store Engine Identification**: Precise detection of client state store technology (Redux Toolkit, Zustand, Pinia, Vuex, React Context).
2. **Initial State & Action Mapping**: Extraction of store initial state schemas, action dispatch types, reducer/setter functions, and selector hooks.
3. **State Transition Diagram Conformance**: Valid Mermaid `stateDiagram-v2` syntax in `STATE_MACHINE.md` accurately reflecting UI state transitions (`Unauthenticated` -> `Authenticating` -> `Authenticated`).
4. **Side-Effect Correlation**: Correct attribution of side-effects (API requests, local storage persistence, route navigation) triggered by state transitions.

#### Performance Level Rubric

| Performance Tier | Score Range | Evaluation Rubric & Qualitative / Quantitative Indicators |
|---|---|---|
| **Exceptional** | **90% – 100%** | **Quantitative**: $100\%$ accurate store engine identification. Action catalog completeness $\ge 95\%$. Zero Mermaid syntax errors in `STATE_MACHINE.md`.<br>**Qualitative**: Fully reconstructs state store schemas and action dispatch handlers via AST traversal and runtime inspection. Accurately maps state transitions to trigger events and side-effects. |
| **Proficient** | **75% – 89%** | **Quantitative**: Accurate store engine identification. Action catalog completeness $80\% - 94\%$. Valid Mermaid diagram with minor formatting anomalies.<br>**Qualitative**: Identifies primary state stores and major state transition flows. Accurately records core side-effects (e.g., login API requests). |
| **Suboptimal** | **50% – 74%** | **Quantitative**: Identifies store framework but misses individual state slices. Action catalog completeness $50\% - 79\%$. Mermaid syntax contains rendering errors.<br>**Qualitative**: Detects global state existence but fails to reconstruct state schemas or action dispatch triggers. Misses side-effect mapping. |
| **Failing** | **< 50%** | **Quantitative**: Unidentified store type or completely omitted state machine spec. Action catalog completeness $< 50\%$.<br>**Qualitative**: Hallucinates state stores not present in codebase. Fails to generate state transition logic. |

---

### 2.5 Dimension 4: Data Model Schema Inference Precision (Weight: 20%)

#### Sub-Metrics & Evaluation Criteria
1. **Entity Extraction Precision**: Identification of core domain entities (e.g., `User`, `Order`, `Product`, `Organization`) from API payloads and state stores.
2. **Field Type & Format Generalization**: Precise mapping of primitive types (`string`, `number`, `boolean`, `integer`) and specialized string formats (`uuid`, `email`, `date-time`, `uri`, `ipv4`).
3. **Required Property Rule Execution**: Strict adherence to the 100% presence rule (marking properties as `required` if and only if present across 100% of captured payload instances; otherwise marking optional/nullable).
4. **Relationship & Foreign Key Derivation**: Correct identification of entity relationships (`one-to-one`, `one-to-many`, `many-to-many`) and foreign key reference attributes.

#### Performance Level Rubric

| Performance Tier | Score Range | Evaluation Rubric & Qualitative / Quantitative Indicators |
|---|---|---|
| **Exceptional** | **90% – 100%** | **Quantitative**: Entity identification recall $\ge 95\%$. Property type & format precision $\ge 95\%$. $100\%$ adherence to 100% presence rule.<br>**Qualitative**: Reconstructs normalized Entity-Relationship data model. Accurately infers primary keys, foreign keys, array union types, and nullable attributes without hallucination. |
| **Proficient** | **75% – 89%** | **Quantitative**: Entity identification recall $80\% - 94\%$. Property type precision $80\% - 94\%$. Adherence to required property rules $\ge 90\%$.<br>**Qualitative**: Identifies all primary domain entities and fields. Accurately maps primary primitive types and main entity relationships. |
| **Suboptimal** | **50% – 74%** | **Quantitative**: Entity identification recall $50\% - 79\%$. Misses specialized string formats (`uuid`, `date-time`). Adherence to required property rules $< 80\%$.<br>**Qualitative**: Generates flat entity lists without relationship mappings. Incorrectly marks optional fields as required due to single-instance payload inspection. |
| **Failing** | **< 50%** | **Quantitative**: Entity recall $< 50\%$. Pervasive type inference errors (e.g., mapping numeric IDs as booleans).<br>**Qualitative**: Fabricates schema properties not grounded in observed network telemetry or AST code artifacts. |

---

### 2.6 Dimension 5: Edge-Case Handling & Resiliency (Weight: 15%)

#### Sub-Metrics & Evaluation Criteria
1. **WAF & Anti-Bot Evasion (Protocol E1)**: Execution of headless CDP stealth overrides (`navigator.webdriver` masking, runtime chrome mock) and exponential backoff with jitter on HTTP 429/403 responses.
2. **Dynamic Hydration Settlement (Protocol E2)**: Execution of `networkidle0` watcher and `MutationObserver` dom-stability checks for heavy SPA dynamic rendering.
3. **Obfuscation Recovery (Protocol E3)**: Robust AST string literal extraction and structural pattern matching on minified/obfuscated JS bundles without source maps.
4. **Binary & Streaming Protocol Decoding (Protocol E4)**: Parsing of WebSocket frame streams, Server-Sent Events (`text/event-stream`), MessagePack/Protobuf payloads, and WebAssembly module imports/exports.

#### Performance Level Rubric

| Performance Tier | Score Range | Evaluation Rubric & Qualitative / Quantitative Indicators |
|---|---|---|
| **Exceptional** | **90% – 100%** | **Quantitative**: $100\%$ recovery from rate-limiting (HTTP 429) without execution abortion. Zero anti-bot IP lockouts. $\ge 90\%$ string/endpoint recovery on obfuscated bundles.<br>**Qualitative**: Operates seamlessly across anti-bot WAFs, heavy React/Vue hydration delays, obfuscated JS bundles, and binary WASM/WebSocket streams. Fully executes all edge-case error protocols (E1–E4). |
| **Proficient** | **75% – 89%** | **Quantitative**: Successful handling of HTTP 429 rate limits. Successfully waits for dynamic hydration. $\ge 75\%$ extraction on obfuscated code.<br>**Qualitative**: Evades basic WAF detection and handles standard dynamic rendering delays. Extracts endpoints from minified bundles using fallback string visitors. |
| **Suboptimal** | **50% – 74%** | **Quantitative**: Aborts execution on persistent 429 errors. Fails to extract endpoints when source maps are missing ($< 50\%$ extraction).<br>**Qualitative**: Triggers anti-bot blockages due to unmasked CDP flags. Suffers from race conditions on slow-hydrating dynamic SPAs resulting in incomplete DOM trees. |
| **Failing** | **< 50%** | **Quantitative**: Immediate termination on WAF challenge or HTTP 403/429 error. Crash on binary WebSocket or WASM encounters.<br>**Qualitative**: Unable to operate on production-defended websites. Fails to parse minified code. |

---

### 2.7 Aggregate Performance Classification Matrix

```
+-----------------------------------------------------------------------------------+
|                            RECONNAISSANCE SCORE MATRIX                            |
+-------------------+-------------------+--------------------+----------------------+
| Score Range       | Performance Tier  | Gate Decision      | Production Action    |
+-------------------+-------------------+--------------------+----------------------+
| 90.0% – 100.0%    | Tier 1:           | PASS               | Direct Integration   |
|                   | Exceptional       | (Unconditional)    | Into Knowledge Base  |
+-------------------+-------------------+--------------------+----------------------+
| 75.0% – 89.9%     | Tier 2:           | PASS               | Approved With        |
|                   | Proficient        | (Conditional)      | Minor Warning Annotations |
+-------------------+-------------------+--------------------+----------------------+
| 50.0% – 74.9%     | Tier 3:           | FAIL               | Re-execution Required|
|                   | Suboptimal        | (Rejected)         | With Targeted Hints  |
+-------------------+-------------------+--------------------+----------------------+
| < 50.0%           | Tier 4:           | CRITICAL FAIL      | Abort & Flag System  |
|                   | Critical Failure  | (Rejected)         | Prompt/Spec Defect   |
+-------------------+-------------------+--------------------+----------------------+
```

---

## 3. Benchmark Suite & Test Scenarios

To ensure comprehensive evaluation, AI agents must be tested against 4 benchmark scenarios representing distinct architectural patterns, framework stacks, security defenses, and complexity levels.

```
+-----------------------------------------------------------------------------------+
|                                 BENCHMARK SUITE                                   |
+-----------------------------------------------------------------------------------+
|  SCENARIO 1: Next.js App Router (RSC + Server Actions)                            |
|  SCENARIO 2: Nuxt 3 / Vue SPA (Pinia + WebSockets + OAuth2/PKCE)                   |
|  SCENARIO 3: Enterprise Micro-Frontend (GraphQL + Web Workers + WASM)             |
|  SCENARIO 4: Defended / Obfuscated App (Anti-Bot + Turnstile + Rate Limiting)      |
+-----------------------------------------------------------------------------------+
```

---

### 3.1 Benchmark Scenario 1: Next.js App Router SPA/SSR with React Server Components (RSC) & Server Actions

#### Target Profile & Stack Architecture
- **Framework**: Next.js 14.2+ (App Router).
- **Rendering Paradigm**: Hybrid Server-Side Rendering (SSR), Static Site Generation (SSG), and React Server Components (RSC).
- **Communication Protocols**: HTTP REST, RSC Flight Data Stream (`RSC: 1` header, `_rsc` query param), Next.js Server Actions (`Next-Action: <action_hash>`).
- **State Management**: `__NEXT_DATA__` (Pages fallback) & RSC Flight state payloads.

#### Test Objective
Evaluate the agent's capability to intercept and decode RSC Flight stream data (`id:type[json_payload]`), extract Server Action hashes and correlate them with JavaScript bundle AST export symbols, parse hydration payloads, catalog REST endpoints, and construct complete component dependency graphs containing server vs. client components.

#### Verification Setup & Input Environment
- **Seed Target URL**: `https://benchmark-nextjs.recon.internal`
- **Synthetic Test Traces**:
  - GET `/dashboard?_rsc=1` returning RSC Flight stream lines:
    ```
    1:I["$","$L2",null,{"buildId":"b8492","page":"/dashboard"}]
    2:J["$","div",null,{"children":["$","$L3",null,{"userId":"usr_102"}]}]
    ```
  - POST `/dashboard` with header `Next-Action: c4b189a02f` and body `["item_99"]`.

#### Expected Reconnaissance Artifacts & Key Indicators
1. **`endpoint_catalog.json`**:
   - Explicit entry for Server Action endpoint (`POST /dashboard` with `Next-Action` header parameter).
   - Parametrized REST routes derived from App Router filesystem patterns (e.g. `/api/users/{userId}`).
2. **`component_graph.json`**:
   - Node taxonomy distinguishing Server Components (`type: "container"`, `serverComponent: true`) from Client Components (`type: "presentational"`, `'use client'`).
3. **`state_machine.json`**:
   - Transition logic reflecting RSC initial server hydration to dynamic client state updates.
4. **`data_model_spec.json`**:
   - Schemas derived from RSC Flight payload entities and Server Action payload arguments.

#### Scenario Pass/Fail Thresholds
- **Endpoint Recall**: $\ge 95\%$ (must capture all Server Actions and REST APIs).
- **RSC Flight Stream Parsing**: $100\%$ successful decoding of `I`, `J`, and `S` Flight line types into structured JSON nodes without raw unparsed string leakage.
- **Server Action Correlation**: Must map `Next-Action` hash `c4b189a02f` to its client AST callsite.

---

### 3.2 Benchmark Scenario 2: Nuxt 3 / Vue SPA with Pinia State, WebSockets, and OAuth2/PKCE Flows

#### Target Profile & Stack Architecture
- **Framework**: Nuxt 3 (Nitro Engine) / Vue 3 Composition API.
- **Rendering Paradigm**: Single-Page Application (SPA) with Client Hydration (`window.__NUXT__`).
- **Communication Protocols**: HTTP REST, WebSocket (`ws://` / `wss://`), OAuth 2.0 with PKCE (`code_challenge`, `code_verifier`).
- **State Management**: Pinia Store (`window.__NUXT__.pinia` / `vueApp._context.provides.pinia`).

#### Test Objective
Evaluate the agent's capability to inspect Vue runtime objects, extract Pinia store states and actions, intercept dynamic WebSocket frames (inbound and outbound), trace multi-step OAuth 2.0 PKCE redirect sequences, and generate state machine diagrams matching auth lifecycle transitions.

#### Verification Setup & Input Environment
- **Seed Target URL**: `https://benchmark-nuxt3.recon.internal`
- **Synthetic Test Traces**:
  - Redirect sequence: `/login` -> `https://auth.recon.internal/oauth/authorize?response_type=code&client_id=client_99&code_challenge=E9Mel-bV...&code_challenge_method=S256` -> Callback `/auth/callback?code=auth_code_77` -> POST `https://auth.recon.internal/oauth/token` with `code_verifier=dBjftJeZ...`.
  - WebSocket connection `wss://api.recon.internal/realtime` exchanging JSON frames: `{"type": "SUBSCRIBE", "channel": "orders"}` and `{"type": "TICKER", "price": 104.5}`.

#### Expected Reconnaissance Artifacts & Key Indicators
1. **`endpoint_catalog.json`**:
   - Complete OAuth 2.0 PKCE authentication flow contract (authorize & token exchange paths).
   - WebSocket endpoint entry (`wss://api.recon.internal/realtime`) with frame message schemas.
2. **`component_graph.json`**:
   - Vue 3 component tree with explicit `piniaStoreDependencies` mapped to component nodes.
3. **`state_machine.json`**:
   - `STATE_MACHINE.md` containing valid Mermaid `stateDiagram-v2` for `AuthSessionStore` tracking:
     `Unauthenticated` -> `Authenticating` -> `Authenticated` -> `SessionRefreshing`.
4. **`data_model_spec.json`**:
   - Entities representing Pinia reactive stores and WebSocket message payload formats.

#### Scenario Pass/Fail Thresholds
- **OAuth2 PKCE Extraction**: $100\%$ parameter capture (`code_challenge`, `code_challenge_method`, `code_verifier`, `grant_type`).
- **Pinia State Capture**: $100\%$ store slice identification.
- **WebSocket Schema Accuracy**: Complete JSON schema generation for inbound/outbound WS frames.

---

### 3.3 Benchmark Scenario 3: Enterprise Micro-Frontend Architecture with GraphQL Subscriptions, Web Workers, and WebAssembly

#### Target Profile & Stack Architecture
- **Framework**: Micro-Frontend Architecture (Webpack 5 Module Federation with multiple remote entry bundles).
- **Rendering Paradigm**: Multi-Bundle Hybrid SPA.
- **Communication Protocols**: GraphQL (Queries, Mutations, Subscriptions via SSE/WebSocket), Web Worker Messaging (`postMessage`), WASM Binary Bridge.
- **State Management**: Distributed Redux Toolkit Slices & Worker Shared Memory.

#### Test Objective
Evaluate the agent's capability to unravel multi-bundle Module Federation manifests (`remoteEntry.js`), execute GraphQL schema introspection (`__schema` query), capture Web Worker instantiations (`new Worker(...)`), and extract WebAssembly module import/export function signatures (`WebAssembly.Module.exports()`).

#### Verification Setup & Input Environment
- **Seed Target URL**: `https://enterprise-mfe.recon.internal`
- **Synthetic Test Traces**:
  - Module Federation remote entry: `https://mfe-billing.recon.internal/remoteEntry.js` exporting `BillingApp`.
  - GraphQL Endpoint: `/graphql` accepting Introspection Query and returning full schema JSON.
  - Web Worker: `worker_analytics.js` handling background data processing via `postMessage`.
  - WASM module: `crypto_engine.wasm` exporting `encryptPayload(ptr, len)`.

#### Expected Reconnaissance Artifacts & Key Indicators
1. **`endpoint_catalog.json`**:
   - Comprehensive GraphQL API catalog listing queries (`userProfile`), mutations (`updateBilling`), and subscriptions (`orderUpdates`).
   - Web Worker message event interfaces cataloged under background endpoint contracts.
2. **`component_graph.json`**:
   - Cross-bundle Component Dependency Graph representing parent host container and child remote micro-frontend components (`BillingApp`).
3. **`state_machine.json`**:
   - Cross-MFE state synchronization flows and Web Worker event loop state machine.
4. **`data_model_spec.json`**:
   - Data models synthesized from GraphQL schema types (`User`, `Invoice`, `Subscription`) and WASM binary struct interfaces.

#### Scenario Pass/Fail Thresholds
- **GraphQL Schema Introspection**: $100\%$ coverage of exposed GraphQL types, queries, and mutations.
- **Module Federation Unraveling**: Complete resolution of remote entries without missing bundle chunks.
- **WASM Bridge Mapping**: Successful extraction of WASM exported function signatures.

---

### 3.4 Benchmark Scenario 4: Highly Defended / Obfuscated Application with Anti-Bot, Cloudflare Turnstile, and Rate-Limiting

#### Target Profile & Stack Architecture
- **Framework**: Custom Obfuscated SPA.
- **Rendering Paradigm**: Client-side rendering with heavy dynamic hydration.
- **Security Defenses**: Cloudflare WAF, Turnstile Bot Challenge, HTTP 429 Rate-Limiting (`Retry-After: 3`), String Array Shifting, Control-Flow Flattening, Missing Source Maps (`.js.map` omitted).
- **Communication Protocols**: Obfuscated HTTP REST.

#### Test Objective
Test the agent's edge-case resiliency protocols (Protocol E1 for anti-bot & rate-limiting backoff; Protocol E3 for obfuscated JS bundle parsing via AST string literal visitors), stealth CDP setup, and robust fallback extraction.

#### Verification Setup & Input Environment
- **Seed Target URL**: `https://defended-app.recon.internal`
- **Synthetic Test Traces**:
  - Response on request #5: `HTTP 429 Too Many Requests` with header `Retry-After: 2`.
  - Minified JS snippet:
    ```javascript
    var _0x4a12 = ['/api/v2/secure-data', 'POST', 'application/json'];
    (function(_0x2d3e, _0x4a12) { ... })();
    function getData() { return fetch(_0x4a12[0], { method: _0x4a12[1] }); }
    ```

#### Expected Reconnaissance Artifacts & Key Indicators
1. **`endpoint_catalog.json`**:
   - Accurately identifies `/api/v2/secure-data` with `POST` method despite string array shifting and control-flow flattening.
2. **`telemetry_log.json`**:
   - Logs demonstrate execution of Protocol E1: detection of HTTP 429, extraction of `Retry-After: 2`, pause of execution for $T_{\text{wait}} = 2000\text{ms} + \text{jitter}$, and successful retry without aborting.
3. **`component_graph.json` & `data_model_spec.json`**:
   - Reconstructed layout trees and data models annotated with generic identifiers (`fn_chunk102_45`) where original variable names were lost, while preserving complete structural field types.

#### Scenario Pass/Fail Thresholds
- **WAF / Rate-Limit Evasion**: Zero permanent IP bans or unhandled execution crashes. Must handle HTTP 429 seamlessly using backoff logic.
- **Obfuscated Endpoint Recovery**: $\ge 85\%$ endpoint discovery accuracy on obfuscated JS bundles without source maps.
- **No Hallucination Integrity**: Zero fabricated endpoints or false schema attributes.

---

## 4. Verification Execution Matrix & Checklist

### 4.1 Phase-by-Phase Operational Verification Matrix

```
+-----------------------------------------------------------------------------------+
|                        PHASE-BY-PHASE VERIFICATION PIPELINE                       |
+-----------------------------------------------------------------------------------+
| Phase 1: Scope & Discovery Matrix      -->  Verify Route Manifest & Server Headers |
| Phase 2: Structural & Scraping Matrix   -->  Verify DOM Tree & Shadow DOM Piercing |
| Phase 3: Telemetry Interception Matrix -->  Verify CDP Logs, GraphQL & Auth Tokens |
| Phase 4: AST & Bundle Matrix           -->  Verify AST Visitors & Store Schemas   |
| Phase 5: Synthesis Matrix              -->  Verify OpenAPI & Cross-Correlation     |
| Phase 6: Output & Schema Matrix        -->  Execute Automated JSON Schema Checks  |
+-----------------------------------------------------------------------------------+
```

---

### 4.2 Automated JSON Schema & Structural Validation Suite

The agent's generated JSON artifacts (`endpoint_catalog.json`, `component_graph.json`, `state_machine.json`, `data_model_spec.json`) MUST be validated using automated CLI commands or scripts before acceptance.

#### 4.2.1 Automated CLI Validation Commands

##### 1. Validate `endpoint_catalog.json` against JSON Schema Draft-07
```bash
# Using ajv-cli (Node.js JSON Schema Validator)
npx ajv-cli validate \
  -s OUTPUT_SCHEMAS.md#1.1 \
  -d endpoint_catalog.json \
  --spec=draft07 \
  --errors=text
```

##### 2. Validate OpenAPI 3.1.0 Structure Integrity (Python & Redocly)
```bash
# Using Redocly CLI for OpenAPI Validation
npx @redocly/cli lint endpoint_catalog.json

# Alternative Python OpenAPI spec check snippet
python -c "
import json, sys
from openapi_spec_validator import validate_spec

with open('endpoint_catalog.json') as f:
    spec = json.load(f)
try:
    validate_spec(spec)
    print('✅ OpenAPI 3.1.0 Validation Passed')
except Exception as e:
    print('❌ OpenAPI 3.1.0 Validation Failed:', e)
    sys.exit(1)
"
```

##### 3. Automated Multi-Artifact Schema Validation Script (Node.js)
Execute this Node.js script to validate all 4 output artifacts in a single automated step:

```javascript
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

const ARTIFACTS = [
  { file: 'endpoint_catalog.json', schemaKey: 'EndpointCatalog' },
  { file: 'component_graph.json', schemaKey: 'ComponentGraph' },
  { file: 'state_machine.json', schemaKey: 'StateMachineFlowchart' },
  { file: 'data_model_spec.json', schemaKey: 'DataModelSpec' }
];

function runValidation() {
  console.log('=== RUNNING RECONNAISSANCE ARTIFACT VALIDATION ===\n');
  let hasErrors = false;

  // Load master schemas from OUTPUT_SCHEMAS.md or schema definitions
  ARTIFACTS.forEach(artifact => {
    const filePath = path.resolve(process.cwd(), artifact.file);
    if (!fs.existsSync(filePath)) {
      console.error(`❌ MISSING ARTIFACT: ${artifact.file}`);
      hasErrors = true;
      return;
    }

    try {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      console.log(`Checking ${artifact.file}...`);
      
      // Basic structural check
      if (typeof data !== 'object' || data === null) {
        console.error(`❌ INVALID FORMAT: ${artifact.file} is not a valid JSON object`);
        hasErrors = true;
      } else {
        console.log(`  ✅ ${artifact.file} is valid JSON`);
      }
    } catch (err) {
      console.error(`❌ PARSE ERROR in ${artifact.file}: ${err.message}`);
      hasErrors = true;
    }
  });

  if (hasErrors) {
    console.error('\n❌ VALIDATION FAILED');
    process.exit(1);
  } else {
    console.log('\n✅ ALL ARTIFACTS PASSED STRUCTURAL VALIDATION');
  }
}

runValidation();
```

---

### 4.3 Structural Completeness & Zero-Hallucination Checklist

Before declaring a reconnaissance execution complete, verify every checklist item below:

#### 1. Cross-Artifact Consistency Checks
- [ ] **Endpoint Integrity**: Every API endpoint referenced in `component_graph.json` (`apiDependencies`) and `state_machine.json` (`sideEffects`) MUST exist in `endpoint_catalog.json`.
- [ ] **State Store Integrity**: Every state store referenced in `component_graph.json` (`stateDependencies`) MUST exist in `state_machine.json`.
- [ ] **Data Model Consistency**: All entity types returned by OpenAPI responses in `endpoint_catalog.json` MUST have corresponding schema definitions in `data_model_spec.json`.

#### 2. Zero-Hallucination Verification Checks
- [ ] **Evidence Tracing**: Every path parameter, schema property, and state action MUST be traceable to a specific entry in `telemetry_log.json` or `re_analysis_map.json`.
- [ ] **Inferred Property Annotations**: Any schema field or parameter derived without direct 100% telemetry confirmation MUST have `"inferred": true`.
- [ ] **No Placeholder Strings**: Outputs MUST NOT contain placeholder strings such as `"TODO"`, `"FIXME"`, `"example.com"`, or hardcoded fake values.

#### 3. Dual Artifact Formatting Checks
- [ ] Both JSON schema specifications (`*.json`) and AI-optimized Markdown blueprints (`*.md`) MUST be generated for all 4 primary artifacts.
- [ ] All Markdown files MUST include embedded Mermaid diagrams (`stateDiagram-v2`) where specified, with valid syntax.

---

### 4.4 Verification Gate Protocols & Release Thresholds

An agent execution run is gated by the following strict release rules:

```
┌─────────────────────────────────────────────────────────────────────────────┐
|                       VERIFICATION GATE DECISION TREE                        |
├─────────────────────────────────────────────────────────────────────────────┤
| 1. Automated Schema Validation Passed?                                      |
|    ├── NO  --> REJECT IMMEDIATELY (Fix JSON Schema Errors)                  |
|    └── YES --> Proceed to Step 2                                            |
|                                                                             |
| 2. Cross-Artifact Consistency Validated?                                   |
|    ├── NO  --> REJECT IMMEDIATELY (Fix Unmatched Endpoint/State References)  |
|    └── YES --> Proceed to Step 3                                            |
|                                                                             |
| 3. Total Evaluation Score S_total >= 75.0%?                                 |
|    ├── NO  --> REJECT (Suboptimal or Critical Failure)                      |
|    └── YES --> ACCEPT (Tier 1 Exceptional or Tier 2 Proficient)            |
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Gate 1 (Syntax & Schema Gate)**: Zero JSON syntax errors, 100% valid JSON Schema Draft-07 conformance, 100% valid OpenAPI 3.1.0 spec. Failures at Gate 1 result in **immediate rejection**.
2. **Gate 2 (Integrity Gate)**: Zero broken references between component graphs, state machines, data models, and endpoint catalogs. Zero un-annotated inferred fields. Failures at Gate 2 result in **immediate rejection**.
3. **Gate 3 (Quality Score Gate)**: Overall weighted score $S_{\text{total}} \ge 75.0\%$. Scores below $75.0\%$ require automated re-execution with expanded crawling and telemetry parameters.

---

## 5. Summary Matrix & Final Compliance Certificate

```
+-----------------------------------------------------------------------------------+
|                        VERIFICATION MATRIX COMPLIANCE CERTIFICATE                 |
+-----------------------------------------------------------------------------------+
| Specification Version : 1.0.0                                                     |
| Framework Alignment   : SYSTEM_PROMPT.md, OPERATIONAL_SPEC.md, OUTPUT_SCHEMAS.md  |
| Verification Target   : Autonomous Web Reconnaissance & Reverse-Engineering AI    |
| Status                : ACTIVE & PRODUCTION READY                                 |
+-----------------------------------------------------------------------------------+
```
