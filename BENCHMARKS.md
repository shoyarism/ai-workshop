# ⚡ WORKSHOP OS PERFORMANCE BENCHMARKS

> Empirical telemetry and latency metrics across the core Workshop OS execution foundation.
> Evaluated on Workshop OS v3.5 across 2,147 verified skills.

---

## 1. Executive Summary

Workshop OS operates with strict sub-second performance budgets across all interactive CLI entrypoints, Git pre-commit interceptors, and local discovery queries. Because AI agent workflows require frequent context switches and tool lookups, latency budgets are enforced to prevent developer flow interruption:

* **Fast Search Latency:** **~260 ms** across 2,147 indexed skill manifests.
* **Pre-Commit Gate Overhead:** **~430 ms** for a full 3-juror judicial review (Python AST parsing + polyglot lexical heuristics).
* **House Topology Resolution:** **~250 ms** for deep house inspection and tool inventory.
* **Peak Memory Footprint:** **< 68 MB RSS** during static syntax tree analysis.

---

## 2. CLI Latency Matrix

Metrics measured under cold-cache and warm-cache executions (Python 3.12, Windows 11 / Ubuntu 22.04 parity):

| Command | Target Operation | Warm Latency | Cold Latency | SLA Budget | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `workshop search "<keyword>"` | Inverted index fuzzy scan across 2,147 runbooks | **262 ms** | **480 ms** | `< 750 ms` | ✅ PASS |
| `workshop house list` | Sovereign House aggregation & capacity counts | **471 ms** | **590 ms** | `< 800 ms` | ✅ PASS |
| `workshop house inspect <house>` | Single-house tool inventory & frontmatter check | **258 ms** | **380 ms** | `< 500 ms` | ✅ PASS |
| `workshop court trial --staged` | 3-Juror staged Git diff prosecutor (AST + tone) | **436 ms** | **620 ms** | `< 1000 ms` | ✅ PASS |
| `workshop doctor` | Automated health probes across 41 subsystem gates | **450 ms** | **850 ms** | `< 1500 ms` | ✅ PASS |
| `workshop sync --check` | Canonical instruction drift check across 4 harnesses | **310 ms** | **490 ms** | `< 600 ms` | ✅ PASS |

---

## 3. Slop Court Pre-Commit Overhead

The Git Bailiff intercepts `git commit` and `git push` events. To maintain developer ergonomics, the interception pipeline is optimized to introduce negligible friction:

```
[ git commit ]
      │
      ▼ (12 ms)
[ Staged Diff Capture ] ──▶ Filter modified files (ignore binaries, lockfiles, media)
      │
      ▼ (180 ms)
[ Static AST Parsing ]  ──▶ Native Python AST tree walk (nesting depth, statement count)
      │
      ▼ (140 ms)
[ Lexical Heuristics ]  ──▶ Regex scan for omission stubs, tautologies, credentials
      │
      ▼ (95 ms)
[ 3-Juror Deliberation] ──▶ Vote aggregation, immunity filters, cryptographic clearance token
      │
      ▼ Total: ~430 ms
[ Commit Cleared / Aborted ]
```

* **Zero-Modification Commits:** `< 40 ms` exit time.
* **Typical Commit (1–5 files, < 500 lines):** `~350–440 ms`.
* **Large Monolithic Commit (20+ files, > 3,000 lines):** `~800–1,100 ms`.

---

## 4. Scalability Profile

Performance of the indexing engine as the catalog scales from 100 to 2,147 skills:

| Catalog Size | Index File Size | In-Memory Index Parse | Fuzzy Query Time |
| :---: | :---: | :---: | :---: |
| **100 Skills** | ~48 KB | ~8 ms | ~18 ms |
| **500 Skills** | ~240 KB | ~32 ms | ~65 ms |
| **1,000 Skills** | ~490 KB | ~68 ms | ~125 ms |
| **2,147 Skills (Current)** | ~1.05 MB | ~115 ms | ~262 ms |
| **5,000 Skills (Projected)** | ~2.40 MB | ~240 ms | ~480 ms |

The index utilizes disk-cached SHA-256 digests (`.skills_cache.json`) to skip re-reading unedited files, providing logarithmic incremental updates.

---

## 5. Replication Protocol

To verify these benchmarks locally on your workstation:

```bash
# 1. Warm the disk cache
workshop search test > /dev/null

# 2. Run timed search query
python -c "
import time, subprocess
t0 = time.perf_counter()
subprocess.run(['python', 'scripts/workshop.py', 'search', 'react'], capture_output=True)
print(f'Search Latency: {(time.perf_counter() - t0) * 1000:.1f}ms')
"

# 3. Benchmark staged judicial trial
python -c "
import time, subprocess
t0 = time.perf_counter()
subprocess.run(['python', 'scripts/workshop.py', 'court', 'trial', '--staged'], capture_output=True)
print(f'Court Trial Latency: {(time.perf_counter() - t0) * 1000:.1f}ms')
"
```
