---
name: auspex-osint-intelligence
description: Deep Open Source Intelligence (OSINT), multi-platform username reconnaissance, email verification, international phone lookup, domain infrastructure, IP geolocation, and Auspex 75-module suite orchestration.
risk: low
source: workshop-arsenal
date_added: 2026-09-21
---

# Auspex OSINT & Intelligence Engine

## Overview
The Auspex OSINT & Intelligence Engine connects AI agents to the Auspex Open Source Intelligence ecosystem (`.\Projects\Auspex`), spanning over 75 specialized reconnaissance modules and 1,500+ global website signatures.

It enables agents to conduct structured, multi-vector investigations across digital identities, infrastructure, telecommunications, and corporate records without manual web search friction.

---

## Capabilities & Commands

Execute from any directory using the Workshop CLI:

```bash
# Set workshop root
$W = "."

# 🌐 1. Intelligence Suite Status & Available Modules
uv run python $W\scripts\workshop.py osint status

# 👤 2. Cross-Platform Username Enumeration
uv run python $W\scripts\workshop.py osint username <username> [--fast] [--json]

# ✉️ 3. Email Reconnaissance (Syntax, MX Verification, Disposable Flagging)
uv run python $W\scripts\workshop.py osint email <target_email> [--json]

# 📱 4. International Phone Intelligence (libphonenumber)
uv run python $W\scripts\workshop.py osint phone "+14155552671" [--json]

# 🏛️ 5. Domain Infrastructure & Certificate Transparency Subdomains (crt.sh, DNS, WHOIS)
uv run python $W\scripts\workshop.py osint domain "targetcompany.com" [--json]

# 🌍 6. IP Geolocation, ASN & Network Host Recon
uv run python $W\scripts\workshop.py osint ip "1.1.1.1" [--json]

# 📄 7. File Forensic Metadata & EXIF Analysis
uv run python $W\scripts\workshop.py osint metadata "C:\path\to\document.pdf" [--json]

# 🚀 8. Launch Auspex Interactive Web/Desktop Console
uv run python $W\scripts\workshop.py osint launch-auspex
```

---

## Auspex Master Inventory Reference (`.\Projects\Auspex\modules`)
Agents can directly import and automate the internal Auspex modules:
* **Identity & Socmint**: `username_checker.py`, `sites_database.py` (1,500+ sites), `whatsmyname_sync.py`, `aliens_eye_osint.py`, `socmint_deep.py`, `people_search_osint.py`, `name_dob_generator.py`.
* **Email & Accounts**: `email_checker.py`, `mail_access_osint.py`, `holehe_email_probe.py`, `behindtheemail.py`.
* **Telecom**: `phone_checker.py`, `phone_intelligence.py`.
* **Domain & Infra**: `infra_recon.py`, `dork_engine.py`.
* **Threat & Darkweb**: `breach_checker.py`, `breachstack.py`, `darkweb_intel.py`, `ahmia_darkweb.py`.
* **Forensics & Exporters**: `file_metadata.py`, `whatsapp_forensics.py`, `forensic_exporter.py`.
