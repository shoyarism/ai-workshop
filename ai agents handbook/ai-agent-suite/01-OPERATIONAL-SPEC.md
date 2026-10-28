# AI Engineering Agent — Operational Specification

This document defines the exact technical execution protocols for the **AI Engineering Agent**: codebase fingerprinting, website/application reconnaissance, browser automation, dynamic hydration parsing, JavaScript AST analysis, network telemetry hooks, authentication decoding, and error recovery strategies.

> This is the operational companion to `00-MASTER-PROMPT.md`. The reconnaissance material here is adapted and generalized from the original website-reconnaissance suite (`prompts/SYSTEM_PROMPT.md`, `prompts/OPERATIONAL_SPEC.md`).

---

## 1. System Architecture & Operational Pipeline

```
+----------------------------------------------------------------------------+
|                ANALYSIS ENGINE (CODEBASE / HEADLESS BROWSER / CDP)         |
|  - Repository & Manifest Inspection                                        |
|  - CDP Session Hooks (Fetch.enable, Network.enable)                        |
|  - Runtime Injected Monkey-Patches (Fetch, XHR, WebSocket, EventSource)    |
+----------------------------------------------------------------------------+
        |                                         |
        v                                         v
+----------------------------------+     +------------------------------------+
|   STATIC & STRUCTURAL ENGINE     |     |   DYNAMIC TELEMETRY INTERCEPT       |
|  - Codebase/Manifest Fingerprint |     |  - XHR/Fetch Payload Sniffer        |
|  - DOM Tree / Shadow DOM Piercer |     |  - WS/SSE Message Log               |
|  - Hydration Blob Extractor      |     |  - Auth Header & JWT Token Decoder  |
|  - Asset/Module Graph Builder    |     +------------------------------------+
+----------------------------------+                     |
        |                                                 |
        +----------------------+--------------------------+
                               v
+----------------------------------------------------------------------------+
|               JAVASCRIPT AST & BUNDLE UNRAVELER                            |
|  - Source Map Unpacker (.js.map)                                           |
|  - Webpack Chunk / Vite Import Visitor                                    |
|  - State Store Inspector (Redux, Zustand, Pinia)                           |
|  - Static Route & Endpoint Visitor                                         |
+----------------------------------------------------------------------------+
                               |
                               v
+----------------------------------------------------------------------------+
|                SYNTHESIS & OUTPUT ENGINE                                   |
|  - Route & Endpoint Cross-Correlator                                       |
|  - JSON Schema Type Generalizer                                            |
|  - OpenAPI 3.1.0 Builder                                                   |
|  - Component Graph & State Machine Flowchart Generator                     |
+----------------------------------------------------------------------------+
```

---

## 2. Codebase Fingerprinting & Existing-Project Analysis

Use this protocol during Phase 1 (Discovery) when the task targets an existing repository or application.

### 2.1 Manifest & Config Inventory
1. Read the package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `composer.json`) and extract: runtime, framework, key dependencies, scripts, and package manager lockfile.
2. Read config files that reveal architecture: `next.config.*`, `vite.config.*`, `nuxt.config.*`, `tsconfig.json`, `tailwind.config.*`, `drizzle.config.*`, `prisma/schema.prisma`, `.env.example`.
3. Read `README.md`, `AGENTS.md`, and top-level docs for declared conventions and run commands.
4. Identify the folder/route skeleton: `app/` or `pages/` (Next.js), `src/` conventions, `api/` directories, migration folders.

### 2.2 Fingerprint Signals (External Target)

| Signal | Where to Look | What It Tells You |
|---|---|---|
| `Server`, `X-Powered-By`, `CF-Ray`, `Server-Timing` | Response headers | Runtime, reverse proxy, CDN |
| `<meta name="generator">`, `#root`, `#__next`, `#__nuxt`, `app-root` | HTML root | Framework and mount point |
| `window.__NEXT_DATA__`, `window.__NUXT__`, `window.__remixContext`, `window.React` | Inline scripts | Framework hydration model |
| Manifest & build assets (`manifest.json`, `build-manifest.json`, `remoteEntry.js`) | Document/script tags | Build tooling, micro-frontends |

### 2.3 Route, Endpoint & Data Inventory
1. Enumerate existing routes and pages (filesystem or router config).
2. Enumerate API endpoints (route handlers, server actions, controller files).
3. Enumerate the database schema (migrations/ORM) and state stores (state folder, stores folder, providers).
4. Tag each item as `touched`, `extended`, or `read-only` relative to the task scope.

---

## 3. Web Scraper & Headless Browser Execution Protocol

Use when analyzing a live external target (black-box reconnaissance).

### 3.1 CDP Initialization Parameters
Launch the headless Chrome instance via CDP or Playwright/Puppeteer with the following flags to maximize inspection capability while disabling security isolation features that block cross-origin telemetry analysis:

```bash
google-chrome \
  --remote-debugging-port=9222 \
  --disable-web-security \
  --allow-running-insecure-content \
  --disable-site-isolation-trials \
  --disable-blink-features=AutomationControlled \
  --no-sandbox \
  --disable-setuid-sandbox \
  --window-size=1920,1080 \
  --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
```

### 3.2 Stealth & Evasion Overrides
To prevent anti-bot WAFs (Cloudflare, Akamai, Datadome) from blocking analysis, inject the following stealth script before document initialization (`Page.addScriptToEvaluateOnNewDocument`):

```javascript
// Mask WebDriver Flags
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// Mock Chrome Runtime
window.chrome = {
  runtime: {},
  app: {},
  csi: () => {},
  loadTimes: () => {}
};

// Mock Plugin Array
Object.defineProperty(navigator, 'plugins', {
  get: () => [1, 2, 3, 4, 5]
});

// Mock Languages
Object.defineProperty(navigator, 'languages', {
  get: () => ['en-US', 'en']
});
```

### 3.3 Shadow DOM Piercing Algorithm
`document.querySelector` fails to penetrate open/closed Shadow DOM boundaries. Use the following recursive DOM walker to extract full component trees:

```javascript
function pierceShadowDOM(root = document, depth = 0) {
  const nodes = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);

  let currentNode = walker.currentNode;
  while (currentNode) {
    const nodeData = {
      tagName: currentNode.tagName.toLowerCase(),
      id: currentNode.id || null,
      classList: Array.from(currentNode.classList),
      attributes: Array.from(currentNode.attributes).map(a => ({ name: a.name, value: a.value })),
      shadowRoot: false,
      children: []
    };

    if (currentNode.shadowRoot) {
      nodeData.shadowRoot = true;
      nodeData.shadowChildren = pierceShadowDOM(currentNode.shadowRoot, depth + 1);
    }

    nodes.push(nodeData);
    currentNode = walker.nextNode();
  }
  return nodes;
}
```

### 3.4 Navigation & Hydration Readiness Protocol
1. **Network Idle Detection:** Navigation is considered settled when there are 0 active network connections for at least 500ms (`networkidle0`).
2. **DOM Stability Watcher:** Wait for dynamic rendering using a `MutationObserver` timeout of 2000ms with no new node additions.
3. For infinite-scroll / lazy-loaded pages, execute explicit scroll-to-bottom actions to trigger dynamic imports and deferred requests.

---

## 4. Dynamic Hydration & Framework-Specific Extraction Procedures

### 4.1 Next.js (Pages Router & App Router)

#### 4.1.1 Pages Router Hydration (`__NEXT_DATA__`)
Locate `<script id="__NEXT_DATA__" type="application/json">` and parse the JSON structure:

```typescript
interface NextDataPayload {
  props: {
    pageProps: Record<string, any>;
    __N_SSP?: boolean; // Server-side props flag
    __N_SSG?: boolean; // Static site generation flag
  };
  page: string;         // Current route path (e.g. "/dashboard/[userId]")
  query: Record<string, string>;
  buildId: string;      // Build hash identifier
  runtimeConfig?: Record<string, any>;
  assetPrefix?: string;
}
```

#### 4.1.2 App Router & React Server Components (RSC) Flight Stream Decoding
Next.js App Router transmits server component tree updates using the RSC Flight data format via HTTP requests containing the `RSC: 1` header or `_rsc` query parameter.

**RSC Line Payload Format:** `<id>:<type>[json_payload]`

**RSC Decoder Logic:**
```typescript
function parseRSCStream(rawRSCStream: string) {
  const lines = rawRSCStream.split('\n');
  const rscNodes = [];

  for (const line of lines) {
    if (!line.trim()) continue;
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;

    const id = line.substring(0, colonIndex);
    const rest = line.substring(colonIndex + 1);
    const typeChar = rest[0];
    const payloadRaw = rest.substring(1);

    try {
      if (typeChar === 'I') { // Client Module Import declaration
        rscNodes.push({ id, type: 'module_import', data: JSON.parse(payloadRaw) });
      } else if (typeChar === 'J') { // JSX Component Tree Chunk
        rscNodes.push({ id, type: 'jsx_tree', data: JSON.parse(payloadRaw) });
      } else if (typeChar === 'S') { // Symbol / Action Descriptor
        rscNodes.push({ id, type: 'symbol', data: payloadRaw });
      }
    } catch (e) {
      // Raw string fallback
      rscNodes.push({ id, type: 'raw', data: rest });
    }
  }
  return rscNodes;
}
```

#### 4.1.3 Server Actions Extraction
Server Actions manifest as POST requests with the header `Next-Action: <action_hash>`. Extract `<action_hash>` and match it against JavaScript AST export symbol maps to identify backend execution handlers.

### 4.2 Vue 3 & Nuxt 3 (Nitro Engine)

#### 4.2.1 Nuxt State Hydration (`window.__NUXT__`)
Extract `window.__NUXT__` from inline script execution:

```typescript
interface NuxtStatePayload {
  serverRendered: boolean;
  data: Record<string, any>;      // useAsyncData / useFetch cached payloads
  state: Record<string, any>;     // useState global reactive state
  pinia?: Record<string, any>;    // Pinia store states
  fetch: Record<string, any>;
}
```

#### 4.2.2 Pinia Store Reflection
Execute runtime extraction in the browser context:

```javascript
function extractPiniaStores() {
  if (window.__NUXT__ && window.__NUXT__.pinia) {
    return window.__NUXT__.pinia;
  }
  const vueApp = document.querySelector('[data-v-app]')?.__vue_app__;
  if (vueApp && vueApp._context.provides.pinia) {
    const piniaState = vueApp._context.provides.pinia.state.value;
    return JSON.parse(JSON.stringify(piniaState));
  }
  return null;
}
```

### 4.3 Remix & SvelteKit
- **Remix:** Parse `<script>window.__remixContext = ...;</script>`. Extract `routeModules`, `manifest`, `future`, and `loaderData` for route endpoint signatures.
- **SvelteKit:** Parse `<script>__sveltekit_1... = { env: {}, assets: ..., element: ..., nodes: ... }</script>`. Extract route layout index and static data payloads.

---

## 5. JavaScript AST Parser Configurations & Algorithms

### 5.1 Parser Toolchain Setup
Use `@babel/parser` configured for modern ECMAScript, TypeScript, and JSX parsing:

```javascript
const babelParser = require('@babel/parser');

const PARSER_OPTIONS = {
  sourceType: 'module',
  allowImportExportEverywhere: true,
  allowReturnOutsideFunction: true,
  plugins: [
    'jsx',
    'typescript',
    'classProperties',
    'dynamicImport',
    'exportDefaultFrom',
    'exportNamespaceFrom',
    'nullishCoalescingOperator',
    'optionalChaining',
    'objectRestSpread'
  ]
};
```

### 5.2 AST Visitor Patterns

#### 5.2.1 API Invocation Visitor (Axios / Fetch / Custom Clients)
Scans AST nodes for HTTP invocation patterns:

```javascript
const traverse = require('@babel/traverse').default;

function extractAPIInvocations(ast) {
  const endpoints = [];

  traverse(ast, {
    CallExpression(path) {
      const callee = path.node.callee;

      // Match: fetch("/api/v1/users", { method: "POST" })
      if (callee.name === 'fetch' || (callee.type === 'MemberExpression' && callee.property.name === 'fetch')) {
        const arg0 = path.node.arguments[0];
        if (arg0 && (arg0.type === 'StringLiteral' || arg0.type === 'TemplateLiteral')) {
          endpoints.push({
            url: arg0.type === 'StringLiteral' ? arg0.value : arg0.quasis.map(q => q.value.raw).join('{param}'),
            method: 'UNKNOWN_FETCH',
            location: path.node.loc
          });
        }
      }

      // Match: axios.get("/api/v1/orders"), axios.post(...)
      if (callee.type === 'MemberExpression' && callee.object.name === 'axios') {
        const method = callee.property.name.toUpperCase();
        const arg0 = path.node.arguments[0];
        if (arg0 && (arg0.type === 'StringLiteral' || arg0.type === 'TemplateLiteral')) {
          endpoints.push({
            url: arg0.type === 'StringLiteral' ? arg0.value : arg0.quasis.map(q => q.value.raw).join('{param}'),
            method: method,
            location: path.node.loc
          });
        }
      }
    }
  });

  return endpoints;
}
```

#### 5.2.2 Webpack Chunk Graph Unraveler
Parses minified Webpack chunk push statements to index module dependencies:

```javascript
function extractWebpackModules(ast) {
  const moduleCatalog = new Map();

  traverse(ast, {
    AssignmentExpression(path) {
      // Look for: (self.webpackChunk = self.webpackChunk || []).push(...)
      if (
        path.node.left.type === 'MemberExpression' &&
        path.node.left.property.name === 'webpackChunk'
      ) {
        const rightCall = path.node.right;
        // Traverse push arguments
      }
    },
    CallExpression(path) {
      if (
        path.node.callee.type === 'MemberExpression' &&
        path.node.callee.property.name === 'push' &&
        path.node.arguments.length > 0
      ) {
        const arg = path.node.arguments[0];
        if (arg.type === 'ArrayExpression' && arg.elements.length >= 2) {
          const chunkId = arg.elements[0];
          const modulesObj = arg.elements[1];

          if (modulesObj && modulesObj.type === 'ObjectExpression') {
            modulesObj.properties.forEach(prop => {
              const moduleId = prop.key.value || prop.key.name;
              moduleCatalog.set(String(moduleId), prop.value);
            });
          }
        }
      }
    }
  });

  return moduleCatalog;
}
```

#### 5.2.3 Client State Store Visitor (Redux Toolkit & Zustand)
Identifies state slices and action handlers:

```javascript
function extractStateStores(ast) {
  const stores = [];

  traverse(ast, {
    CallExpression(path) {
      // Redux Toolkit: createSlice({ name: 'user', initialState: {}, reducers: {} })
      if (path.node.callee.name === 'createSlice' && path.node.arguments[0]?.type === 'ObjectExpression') {
        const obj = path.node.arguments[0];
        let sliceName = 'unknown';
        const actions = [];

        obj.properties.forEach(p => {
          if (p.key.name === 'name') sliceName = p.value.value;
          if (p.key.name === 'reducers' && p.value.type === 'ObjectExpression') {
            p.value.properties.forEach(r => actions.push(r.key.name || r.key.value));
          }
        });

        stores.push({ type: 'redux', name: sliceName, actions });
      }

      // Zustand: create((set) => ({ state: ..., action: ... }))
      if (path.node.callee.name === 'create') {
        stores.push({ type: 'zustand', location: path.node.loc });
      }
    }
  });

  return stores;
}
```

#### 5.2.4 Source Map Recovery
- Scan downloaded `.js` files for `//# sourceMappingURL=` comments, or test `.js.map` URL additions.
- If source maps exist, unpack the full client source directory (`sources`, `sourcesContent`) to reconstruct original file paths and TypeScript types.

---

## 6. Telemetry & Network Interception Execution Rules

### 6.1 CDP Telemetry Listener Setup

```javascript
const CDP = require('chrome-remote-interface');

async function attachNetworkTelemetry(client) {
  const { Network, Fetch } = client;

  await Network.enable({ maxTotalBufferSize: 10000000, maxResourceBufferSize: 5000000 });
  await Fetch.enable({ patterns: [{ requestStage: 'Request' }, { requestStage: 'Response' }] });

  Network.requestWillBeSent((params) => {
    console.log(`[REQUEST] ${params.requestId} | ${params.request.method} | ${params.request.url}`);
    // Log headers, auth tokens, POST data
  });

  Network.responseReceived((params) => {
    console.log(`[RESPONSE] ${params.requestId} | ${params.response.status} | ${params.response.mimeType}`);
  });

  Network.webSocketFrameReceived((params) => {
    console.log(`[WS_RECV] ${params.response.opcode} | ${params.response.payloadData}`);
  });

  Network.eventSourceMessageReceived((params) => {
    console.log(`[SSE_RECV] Event: ${params.eventName} | Data: ${params.data}`);
  });
}
```

### 6.2 Browser Runtime Monkey-Patching Snippet
Inject this script into the browser runtime to intercept standard dynamic requests:

```javascript
(function() {
  window.__RECON_TELEMETRY__ = { requests: [], websockets: [] };

  // Intercept Fetch
  const nativeFetch = window.fetch;
  window.fetch = async function(...args) {
    const url = typeof args[0] === 'string' ? args[0] : args[0].url;
    const options = args[1] || {};
    const startTime = Date.now();

    try {
      const response = await nativeFetch.apply(this, args);
      const clone = response.clone();
      const responseBody = await clone.text();

      window.__RECON_TELEMETRY__.requests.push({
        type: 'fetch',
        url: url,
        method: options.method || 'GET',
        headers: options.headers || {},
        requestBody: options.body || null,
        status: response.status,
        responseBody: responseBody,
        duration: Date.now() - startTime
      });

      return response;
    } catch (err) {
      throw err;
    }
  };

  // Intercept WebSocket
  const NativeWebSocket = window.WebSocket;
  window.WebSocket = function(url, protocols) {
    const ws = new NativeWebSocket(url, protocols);
    const wsLog = { url: url, frames: [] };
    window.__RECON_TELEMETRY__.websockets.push(wsLog);

    ws.addEventListener('message', (event) => {
      wsLog.frames.push({ direction: 'inbound', data: event.data, timestamp: Date.now() });
    });

    const nativeSend = ws.send;
    ws.send = function(data) {
      wsLog.frames.push({ direction: 'outbound', data: data, timestamp: Date.now() });
      return nativeSend.apply(this, arguments);
    };

    return ws;
  };
})();
```

### 6.3 GraphQL Introspection Execution
If any request URL contains `/graphql` or a payload contains `query`, issue an introspection request:

```graphql
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      kind
      name
      description
      fields {
        name
        type { name kind ofType { name kind } }
        args { name type { name kind } }
      }
    }
  }
}
```

### 6.4 WebSocket, SSE & Web Worker Capture
- **WebSocket:** Capture the handshake HTTP Upgrade request, subprotocols, and incoming/outgoing frames. Catalog frame message formats (JSON, Binary, SockJS, Socket.io).
- **SSE:** Capture `text/event-stream` connections, event channels, and message payload structures.
- **Workers:** Intercept `new Worker(...)` and `navigator.serviceWorker.register(...)` instantiations.
- **WASM:** Inspect `.wasm` modules via `WebAssembly.Module.exports()` and `WebAssembly.Module.imports()` to document binary bridge functions and memory signatures.

---

## 7. Authentication & Token Lifecycle Management

### 7.1 Authorization Header Inspection
Scan all intercepted request headers for:
- `Authorization: Bearer <JWT_STRING>`
- `Authorization: Basic <BASE64_STRING>`
- `X-API-Key: <KEY_STRING>`
- `X-CSRF-Token` / `X-XSRF-TOKEN`

### 7.2 JWT Claim Decoder
When a Bearer token matches JWT format (`^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+$`), parse header and payload components without secret verification:

```javascript
function decodeJWT(jwtString) {
  const parts = jwtString.split('.');
  if (parts.length !== 3) return null;

  const base64UrlDecode = (str) => {
    let base64 = str.replace(/-/g, '+').replace(/_/g, '/');
    while (base64.length % 4) base64 += '=';
    return JSON.parse(atob(base64));
  };

  return {
    header: base64UrlDecode(parts[0]),
    payload: base64UrlDecode(parts[1]),
    signature: parts[2]
  };
}
```

### 7.3 OAuth 2.0 PKCE Flow Tracing
Trace browser navigation query parameters during login redirects:
1. Capture `code_challenge` and `code_challenge_method` on the authorization request (`/oauth/authorize`).
2. Intercept the POST token exchange request (`/oauth/token`) and record `code_verifier`, `code`, `grant_type: "authorization_code"`.

> **Security note:** The agent may inspect and document auth flows for understanding. It MUST NOT exfiltrate live credentials, and any real tokens captured during analysis should be redacted from committed artifacts.

---

## 8. Error Recovery, Fallbacks & Anti-Obfuscation Engine

### 8.1 Obfuscation Pattern Detection & Recovery

| Pattern | Detection Criteria | Recovery Action |
|---|---|---|
| **String Array Shifting** | Global array of strings referenced via `_0x1a2b[index]` offset function. | Evaluate the string array initialization function in an isolated sandbox VM to build a lookup map. |
| **Control Flow Flattening** | `switch(state)` block inside an infinite `while(true)` loop driven by a state array. | Flatten AST switch states into sequential statements by tracing the state array sequence. |
| **Dead Code Injection** | Conditional blocks evaluated against constant false expressions (`if(false)`). | Prune AST branches where the condition evaluates to a static literal false. |
| **Missing Source Maps** | `.js.map` files absent; minified single-line bundles. | Fall back to structural pattern extraction: string literals, URL regex matches, object property definitions, API client calls. |

### 8.2 Retry Logic & Error Matrix

| Error Code | Root Cause | Recovery Action |
|---|---|---|
| HTTP 429 | Rate limit exceeded | Pause for `max(Retry-After, 2^n * 1000ms + jitter)`. |
| HTTP 403 | WAF / Anti-Bot block | Rotate User-Agent, flush cookies, introduce random delays. |
| AST Timeout | Circular import / huge bundle | Set AST max line limit (50,000 lines), fall back to regex string extractor. |
| Parse Failure | Invalid JS syntax / WASM | Try SWC/Acorn parser with loose parsing options. |
| Build Failure | Dependency/version conflict | Verify lockfile, clear caches, pin versions, check env vars. |
| Test Flake | Timing/dynamic rendering | Apply Protocol E2 (network idle + DOM stability waits). |

---

## 9. Compliance With The Evidence-Based Integrity Mandate

- Every route, parameter, schema field, and state variable in generated artifacts MUST trace to direct observation (code, telemetry, execution output).
- Anything inferred MUST be annotated `(inferred)`.
- Scope boundaries and non-destructive rules from `00-MASTER-PROMPT.md` Section 5 apply at all times during operational execution.
