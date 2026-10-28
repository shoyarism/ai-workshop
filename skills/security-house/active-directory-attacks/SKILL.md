---
name: active-directory-attacks
description: "Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, lateral movement, privilege escalation, and domain dominance for red team operations and penetration testing."
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> AUTHORIZED USE ONLY: Use this skill only for authorized security assessments, defensive validation, or controlled educational environments.

<!-- security-allowlist: credential-extraction, kerberos-attacks -->

# Active Directory Attacks

## Purpose

Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, lateral movement, privilege escalation, and domain dominance for red team operations and penetration testing.

## Inputs/Prerequisites

- Kali Linux or Windows attack platform
- Domain user credentials (for most attacks)
- Network access to Domain Controller
- Tools: Impacket, Mimikatz, BloodHound, Rubeus, CrackMapExec

## Outputs/Deliverables

- Domain enumeration data
- Extracted credentials and hashes
- Kerberos tickets for impersonation
- Domain Administrator access
- Persistent access mechanisms

---

## Essential Tools

| Tool | Purpose |
|------|---------|
| BloodHound | AD attack path visualization |
| Impacket | Python AD attack tools |
| Mimikatz | Credential extraction |
| Rubeus | Kerberos attacks |
| CrackMapExec | Network exploitation |
| PowerView | AD enumeration |
| Responder | LLMNR/NBT-NS poisoning |

---

## Core Workflow

### Step 1: Kerberos Clock Sync

Kerberos requires clock synchronization (±5 minutes):

```bash
# Detect clock skew
nmap -sT 10.10.10.10 -p445 --script smb2-time

# Fix clock on Linux
sudo date -s "14 APR 2024 18:25:16"

# Fix clock on Windows
net time /domain /set

# Fake clock without changing system time
faketime -f '+8h' <command>
```