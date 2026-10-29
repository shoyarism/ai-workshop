# AI Engineering Agent — Verification Matrix

This document defines the formal evaluation rubrics, benchmark suite, validation procedures, and release gate protocols for verifying the quality, accuracy, and structural completeness of the **AI Engineering Agent**'s deliveries.

> Adapted and generalized from the original reconnaissance verification matrix (`prompts/VERIFICATION_MATRIX.md`).

---

## 1. Overview & Evaluation Architecture

### 1.1 Purpose & Scope
The Verification Matrix provides an objective, quantitative, and reproducible framework to assess an agent execution — from pre-execution planning through implementation, testing, and handoff. It validates that the agent converts a task into accurate, evidence-backed, zero-hallucination deliverables that conform to the output schemas in `02-OUTPUT-SCHEMAS.md`.

### 1.2 Mathematical Scoring Model
An execution's overall delivery score ($S_{\text{total}}$) is a weighted sum across 5 core assessment dimensions:

$$S_{\text{total}} = \sum_{i=1}^{5} (w_i \times S_i) = (0.25 \times S_1) + (0.20 \times S_2) + (0.20 \times S_3) + (0.20 \times S_4) + (0.15 \times S_5)$$

Where:
- $S_1$: Architecture & Scope Fidelity (Weight: 25%)
- $S_2$: Implementation Correctness & Code Quality (Weight: 20%)
- $S_3$: Data & State Integrity (Weight: 20%)
- $S_4$: Testing & Validation Coverage (Weight: 20%)
- $S_5$: Edge-Case Handling & Resiliency (Weight: 15%)

---

## 2. Core Assessment Dimensions & Evaluation Rubrics

### 2.1 Dimension Breakdown

```
+-----------------------------------------------------------------------------------+
|                            OVERALL EVALUATION SCORE (100%)                        |
+-----------------------------------------------------------------------------------+
        |                 |                 |                 |                 |
        v                 v                 v                 v                 v
+---------------+ +---------------+ +---------------+ +---------------+ +---------------+
|  DIMENSION 1  | |  DIMENSION 2  | |  DIMENSION 3  | |  DIMENSION 4  | |  DIMENSION 5  |
| Architecture  | |  Implemen-    | |  Data & State | |  Testing &    | |  Edge-Case    |
| & Scope Fid.  | |  tation       | |  Integrity    | |  Validation   | |  & Resiliency |
|  Weight: 25%  | |  Weight: 20%  | |  Weight: 20%  | |  Weight: 20%  | |  Weight: 15%  |
+---------------+ +---------------+ +---------------+ +---------------+ +---------------+
```

### 2.2 Dimension 1: Architecture & Scope Fidelity (Weight: 25%)

#### Sub-Metrics
1. **Scope Adherence:** All work stays inside the declared in-scope boundary; no out-of-scope modifications.
2. **Stack Appropriateness:** Selected tech stack matches project constraints and is justified in the plan.
3. **Contract Completeness:** Data model, API contracts, component architecture, and state design are complete and internally consistent.
4. **Path/Route Canonicalization:** Dynamic routes correctly parameterized (e.g. `/users/{userId}`), no raw IDs left in path patterns.

#### Performance Level Rubric

| Tier | Range | Indicators |
|---|---|---|
| **Exceptional** | 90–100% | Scope 100% honored. Contracts complete and consistent. Zero path syntax errors. Full dependency-order planning. |
| **Proficient** | 75–89% | Scope honored with minor clarifications. Contracts complete. Minor canonicalization omissions (≤5%). |
| **Suboptimal** | 50–74% | Scope drift or incomplete contracts. Frequent canonicalization failures. Missing architecture artifacts. |
| **Failing** | <50% | Out-of-scope changes, missing design artifacts, or fabricated architecture. |

### 2.3 Dimension 2: Implementation Correctness & Code Quality (Weight: 20%)

#### Sub-Metrics
1. **Compilation & Type Safety:** Builds cleanly; zero type errors.
2. **Convention Conformance:** Follows project lint rules, naming, and directory structure.
3. **Code Clarity & Efficiency:** Clean, maintainable code; appropriate abstraction; no dead code.
4. **Security Hygiene:** No secrets committed; input validation present; no obvious injection/XSS risks.

#### Performance Level Rubric

| Tier | Range | Indicators |
|---|---|---|
| **Exceptional** | 90–100% | Zero lint/type/build errors. Full convention conformance. Clean idiomatic code. Security best practices applied. |
| **Proficient** | 75–89% | Zero fatal errors, minor style warnings. Conventions mostly followed. Sound security hygiene. |
| **Suboptimal** | 50–74% | Lint/type warnings, some dead code, partial convention conformance. |
| **Failing** | <50% | Build breaks, pervasive anti-patterns, or exposed secrets. |

### 2.4 Dimension 3: Data & State Integrity (Weight: 20%)

#### Sub-Metrics
1. **Schema Accuracy:** Entities, fields, and types accurately reflect requirements/observed payloads.
2. **Required-Property Discipline:** Properties marked required only with 100% evidence; otherwise optional.
3. **Relationship Derivation:** Correct one-to-one / one-to-many / many-to-many mappings and foreign keys.
4. **State Machine Accuracy:** Store engine identified correctly; transitions and side-effects accurately mapped.

#### Performance Level Rubric

| Tier | Range | Indicators |
|---|---|---|
| **Exceptional** | 90–100% | 100% adherence to evidence rules. Accurate entities, types, relationships, and state transitions. |
| **Proficient** | 75–89% | Identifies all core entities/fields. ≥90% adherence to required-property rules. Accurate main relationships. |
| **Suboptimal** | 50–74% | Misses formats (uuid/date-time), marks optional fields required, flat lists without relationships. |
| **Failing** | <50% | Fabricated fields, wrong types, or invented state stores. |

### 2.5 Dimension 4: Testing & Validation Coverage (Weight: 20%)

#### Sub-Metrics
1. **Static Checks:** Lint and typecheck pass with evidence captured.
2. **Test Coverage:** Unit/integration/E2E tests cover critical paths, validation schemas, and API handlers.
3. **Validation Accuracy:** Test results actually verify behavior (no trivial/skipped tests passing silently).
4. **Accessibility & Performance Checks:** Documented where applicable.

#### Performance Level Rubric

| Tier | Range | Indicators |
|---|---|---|
| **Exceptional** | 90–100% | Full static + test pass with evidence. Critical paths covered. Accessibility/perf checks documented. |
| **Proficient** | 75–89% | Static checks pass; core tests present and passing. Some gaps in edge coverage. |
| **Suboptimal** | 50–74% | Tests present but shallow; static checks pass with warnings; evidence incomplete. |
| **Failing** | <50% | No tests, broken tests, or "done" claimed without running verification. |

### 2.6 Dimension 5: Edge-Case Handling & Resiliency (Weight: 15%)

#### Sub-Metrics
1. **Error Recovery (Protocol E1):** Build/install/network failures handled via backoff and recovery, not aborts.
2. **Dynamic Environments (Protocol E2):** Correct readiness waits for slow/dynamic environments.
3. **Unknown/Obfuscated Code (Protocol E3):** Structural extraction succeeds on minified/generated code.
4. **Binary & Streaming Protocols (Protocol E4):** WS/SSE/WASM handled without crashing.

#### Performance Level Rubric

| Tier | Range | Indicators |
|---|---|---|
| **Exceptional** | 90–100% | All edge protocols executed; zero abort crashes; ≥90% recovery on hostile inputs. |
| **Proficient** | 75–89% | Handles common failures; retries rate limits; extracts from minified bundles via fallbacks. |
| **Suboptimal** | 50–74% | Aborts on persistent failures; fails without source maps; race conditions on dynamic SPAs. |
| **Failing** | <50% | Immediate termination on any challenge; crashes on binary/streaming content. |

### 2.7 Aggregate Performance Classification Matrix

```
+-----------------------------------------------------------------------------------+
|                            DELIVERY SCORE MATRIX                                   |
+-------------------+-------------------+--------------------+----------------------+
| Score Range       | Performance Tier  | Gate Decision      | Production Action    |
+-------------------+-------------------+--------------------+----------------------+
| 90.0% – 100.0%    | Tier 1:           | PASS               | Direct Integration   |
|                   | Exceptional       | (Unconditional)    |                     |
+-------------------+-------------------+--------------------+----------------------+
| 75.0% – 89.9%     | Tier 2:           | PASS               | Approved With Minor  |
|                   | Proficient        | (Conditional)      | Warning Annotations  |
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

To ensure comprehensive evaluation, the agent should be exercised against the following benchmark scenarios covering distinct architectural patterns, framework stacks, and difficulty levels.

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

### 3.1 Scenario 1: Next.js App Router (RSC + Server Actions)
- **Objective:** Intercept and decode RSC Flight stream data (`id:type[json_payload]`), extract Server Action hashes and correlate them with bundle export symbols, parse hydration payloads, catalog REST endpoints, and construct component graphs distinguishing server vs. client components.
- **Key Trace:** `GET /dashboard?_rsc=1` → `1:I["$","$L2",null,{...}]` lines; `POST /dashboard` with `Next-Action: c4b189a02f`.
- **Pass Thresholds:** Endpoint recall ≥95%; 100% RSC line decoding (`I`, `J`, `S` types); Server Action hash correlated to AST callsite.

### 3.2 Scenario 2: Nuxt 3 / Vue SPA (Pinia + WebSockets + OAuth2/PKCE)
- **Objective:** Inspect Vue runtime objects, extract Pinia store states/actions, intercept WebSocket frames, trace OAuth 2.0 PKCE redirect sequences, and generate state machine diagrams for the auth lifecycle.
- **Key Trace:** `/login` → `/oauth/authorize?...code_challenge=...` → callback `?code=...` → token exchange with `code_verifier`; `wss://.../realtime` JSON frames.
- **Pass Thresholds:** 100% PKCE parameter capture; 100% Pinia store slice identification; complete WS frame schemas.

### 3.3 Scenario 3: Enterprise Micro-Frontend (GraphQL + Workers + WASM)
- **Objective:** Unravel Module Federation manifests (`remoteEntry.js`), execute GraphQL introspection, capture Web Worker instantiations, and extract WASM import/export signatures.
- **Pass Thresholds:** 100% GraphQL schema coverage; complete remote entry resolution; WASM bridge mapping extracted.

### 3.4 Scenario 4: Highly Defended / Obfuscated App
- **Objective:** Execute edge-case resiliency protocols — rate-limit backoff (Protocol E1), stealth CDP setup, and structural extraction on obfuscated bundles (Protocol E3).
- **Key Trace:** `HTTP 429` with `Retry-After: 2`; minified JS with string-array shifting hiding `/api/v2/secure-data`.
- **Pass Thresholds:** Zero permanent bans/aborts; ≥85% endpoint recovery on obfuscated bundles; zero fabricated endpoints.

---

## 4. Verification Execution Matrix & Checklist

### 4.1 Phase-by-Phase Verification Pipeline

```
+-----------------------------------------------------------------------------------+
|                        PHASE-BY-PHASE VERIFICATION PIPELINE                       |
+-----------------------------------------------------------------------------------+
| Phase 1: Discovery & Scope     -->  Verify scope map, stack fingerprint, inventory |
| Phase 2: Architecture & Design -->  Verify schema, API contracts, state design     |
| Phase 3: Implementation        -->  Verify code correctness, conventions, security |
| Phase 4: Testing & QA          -->  Verify lint/typecheck/tests with captured output|
| Phase 5: Verification & Gates  -->  Execute Gate 1/2/3, schema & cross-artifact    |
| Phase 6: Delivery & Handoff    -->  Verify deployment, docs, changelog, rollback   |
+-----------------------------------------------------------------------------------+
```

### 4.2 Automated Validation Suite

```bash
# Validate endpoint catalog against JSON Schema Draft-07
npx ajv-cli validate -s data_model_spec.json -d endpoint_catalog.json --spec=draft07 --errors=text

# Validate OpenAPI 3.1.0 structure
npx @redocly/cli lint endpoint_catalog.json
```

See `02-OUTPUT-SCHEMAS.md` Section 6 for the full multi-artifact validation script.

### 4.3 Structural Completeness & Zero-Hallucination Checklist

#### Cross-Artifact Consistency
- [ ] Every API endpoint referenced in `component_graph.json` and `state_machine.json` EXISTS in `endpoint_catalog.json`.
- [ ] Every state store referenced in `component_graph.json` EXISTS in `state_machine.json`.
- [ ] All entity types returned by API responses have corresponding definitions in `data_model_spec.json`.

#### Zero-Hallucination Verification
- [ ] Every path parameter, schema property, and state action traces to evidence (code, telemetry, or execution output).
- [ ] Any field derived without direct 100% confirmation is annotated `(inferred)`.
- [ ] No placeholder strings (`TODO`, `FIXME`, `example.com`, fake values) emitted as if real.

#### Dual Artifact Formatting
- [ ] JSON + Markdown generated for all applicable artifacts.
- [ ] Markdown includes valid Mermaid `stateDiagram-v2` where specified.

### 4.4 Verification Gate Protocols & Release Thresholds

```
+----------------------------------------------------------------------------+
|                       VERIFICATION GATE DECISION TREE                        |
+----------------------------------------------------------------------------+
| 1. Automated Schema/Static Validation Passed?                              |
|    NO  --> REJECT IMMEDIATELY (fix lint/type/schema errors)                |
|    YES --> Proceed to Step 2                                                |
|                                                                             |
| 2. Cross-Artifact Consistency Validated?                                   |
|    NO  --> REJECT IMMEDIATELY (fix unmatched references)                   |
|    YES --> Proceed to Step 3                                                |
|                                                                             |
| 3. Total Evaluation Score S_total >= 75.0%?                                |
|    NO  --> REJECT (re-execute with targeted effort)                        |
|    YES --> ACCEPT (Tier 1 Exceptional or Tier 2 Proficient)                |
+----------------------------------------------------------------------------+
```

1. **Gate 1 (Syntax & Schema):** Zero lint/type/build errors; artifacts valid against schemas. Failures → immediate rejection.
2. **Gate 2 (Integrity):** Zero broken cross-references; zero un-annotated inferred fields. Failures → immediate rejection.
3. **Gate 3 (Quality Score):** $S_{\text{total}} \ge 75.0\%$. Below → re-execution of targeted phases.

---

## 5. Summary Matrix & Final Compliance Certificate

```
+-----------------------------------------------------------------------------------+
|                        VERIFICATION MATRIX COMPLIANCE CERTIFICATE                 |
+-----------------------------------------------------------------------------------+
| Specification Version : 2.0.0                                                     |
| Framework Alignment   : 00-MASTER-PROMPT.md, 01-OPERATIONAL-SPEC.md,               |
|                          02-OUTPUT-SCHEMAS.md                                     |
| Verification Target   : AI Engineering Agent (Full-Stack Delivery + Analysis)     |
| Status                : ACTIVE & PRODUCTION READY                                 |
+-----------------------------------------------------------------------------------+
```
