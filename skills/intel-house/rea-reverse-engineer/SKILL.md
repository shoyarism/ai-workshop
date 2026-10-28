---
name: rea-reverse-engineer
description: "Reverse Engineer Anything (REA). Tools and workflows for binary disassembly, Electron bundle extraction, network protocol sniffing, and undocumented API deconstruction."
userFacing: true
---

# 🕵️ REA: Reverse Engineer Anything

> **Purpose:** Enables AI agents to inspect, unpack, and deconstruct compiled binaries, obfuscated scripts, Electron desktop applications, and undocumented internal network endpoints.

---

## 1. Core Reverse Engineering Domains

### 1. Electron & WebBundles
- Unpack `.asar` archives (`npx asar extract app.asar unpacked/`).
- Beautify obfuscated minified JavaScript/TypeScript bundles (`js-beautify`, `prettier`).
- Locate internal IPC channels (`ipcRenderer.send`, `ipcMain.handle`).

### 2. Network & Private API Sniffing
- Intercept HTTP/WebSocket traffic between client applications and backend servers.
- Extract request schemas, authorization headers, nonces, and payload schemas.
- Reconstruct OpenAPI/Postman specification drafts from observed traffic.

### 3. Native Binaries & Shared Libraries
- Inspect headers and symbols using `dumpbin`, `objdump`, `strings`, and `file`.
- Trace dynamic library dependencies (`ldd`, `Dependencies.exe`).
- Extract embedded strings, cryptographic certificates, and endpoint URLs.

---

## 2. Invariants & Deliverables

- **Evidence-Based Output:** Report exact file offsets, extracted string matches, and decompiled code blocks.
- **Safety Invariant:** Never execute untrusted third-party binaries outside isolated sandboxes or without static inspection first.
- **Synthesized Contract:** Output clean, typed TypeScript or Python interface definitions corresponding to the reverse-engineered APIs.
