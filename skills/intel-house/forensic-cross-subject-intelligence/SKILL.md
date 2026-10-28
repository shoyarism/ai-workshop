---
name: forensic-cross-subject-intelligence
description: Cross-subject forensic investigation, multi-source evidence correlation, timeline reconstruction, and entity resolution across digital footprints, telemetry, Git histories, and network artifacts.
risk: low
source: workshop-arsenal
date_added: 2026-09-14
---

# Forensic Cross-Subject Intelligence & Investigation

## Overview
Forensic Cross-Subject Intelligence provides methodologies and automated procedures for reconstructing events, resolving entities across disparate digital systems, verifying cryptographic chains of custody, and correlating multi-source investigative evidence.

When analyzing security incidents, git history anomalies, compromised environments, or multi-identity operations, evidence is rarely localized to a single log. This skill defines deterministic protocols for aggregating, normalizing, and cross-correlating traces across heterogeneous systems.

---

## Core Invariants & Axioms

1. **Evidence Immutability & Hashing**: Every examined artifact must be hashed immediately upon acquisition (SHA-256) to establish baseline integrity prior to analysis.
2. **Deterministic Timeline Synchronization**: All timestamps must be normalized to UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SS.sssZ`) with explicit drift offsets recorded.
3. **Multi-Source Triangulation**: No attribution or causal conclusion may rely on a single source of telemetry. A minimum of two orthogonal corroborating artifacts (e.g., Git author signature + SSH key log + network egress IP) is required for high-confidence linkage.
4. **Graph-Based Entity Resolution**: Entities (emails, usernames, public keys, IP addresses, user-agent fingerprints) must be modeled as nodes in an undirected bipartite graph connected by observed co-occurrences.

---

## Investigation Workflows

### 1. Multi-Artifact Correlation Matrix
Construct an evidence matrix mapping temporal events across distinct telemetry vectors:

| Timestamp (UTC) | Source Vector | Subject Identifier | Event Description | Cryptographic Hash |
| :--- | :--- | :--- | :--- | :--- |
| `2026-09-14T10:15:22Z` | Git Log | `author@domain.com` | GPG-signed commit `a1b2c3d` | `sha256:...` |
| `2026-09-14T10:15:45Z` | Egress Proxy | `198.51.100.24` | HTTP POST to API endpoint | `sha256:...` |
| `2026-09-14T10:16:01Z` | Syslog Auth | `developer-session` | Sudo elevation / privilege check | `sha256:...` |

### 2. Digital Fingerprinting & Behavioral Consistency
Analyze cross-subject consistency across technical indicators:
* **Commit Timezone & Activity Cadence**: Fourier analysis of timestamp distributions to establish probable working time zones and sleep cycles.
* **Compiler & Runtime Flags**: Cross-matching build environments, Node/Python minor versions, and PATH variables embedded in compiled binaries or logs.
* **Stylometric Profiling**: Code comment habits, indentation quirks, variable naming taxonomies, and commit message semantics.

### 3. Verification & Reporting Gate
Every forensic report must conclude with:
1. **Confidence Score**: Quantitative metric ($[0.0, 1.0]$) derived from corroborating edge count in the entity graph.
2. **Alternative Hypotheses**: Explicit consideration of spoofing, shared credentials, VPN hopping, or automated bot activities.
3. **Remediation & Hardening Recommendations**: Concrete patches, key revocations, or perimeter rules.
