---
name: ios-forensics
description: Complete forensic acquisition, offline database carving, keychain analysis, geospatial mapping, and pattern-of-life reconstruction for Apple iOS devices (iOS 10–18, A10+ checkm8).
risk: medium
source: iseeyou-dfir
date_added: 2026-09-25
---

# iOS Digital Forensics, Carving & Incident Response

## Overview
The `ios-forensics` skill provides deterministic protocols, tool integrations, and analysis pipelines for acquiring, decrypting, and parsing Apple iOS devices. Grounded in NIST SP 800-101 Rev 1, ISO/IEC 27037:2012, and SWGDE standards, this methodology covers encrypted logical backups, checkm8/Blackbird SEP exploitation, SQLite freelist/WAL carving, and cross-application intelligence.

<!-- provenance: [NIST SP 800-101 Rev 1, SANS FOR585 Advanced Smartphone Forensics, DFRWS WALRUS Protocol 2026] -->

---

## Foundational Axioms & Critical Realities

1. **File-Based Encryption (FBE) Renders Traditional Carving Obsolete**:
   iOS destroys per-file cryptographic keys upon deletion. Raw NAND dumps and unallocated block carving (e.g. searching for JPEG `FFD8` headers) produce unreadable entropy. All data recovery must target **Database Freelist Carving** (`0x0D` leaf pages) and SQLite WAL journal analysis.
2. **Encrypted Acquisition is Mandatory for Protected Artifacts**:
   Unencrypted iOS backups strip out Apple HealthKit (`healthdb_secure.sqlite`), Wi-Fi credentials, VPN profiles, and Safari AutoFill. Enabling backup encryption forces the device to derive SEP Class A keys and export the complete iOS Keychain.
3. **The WALRUS Protocol (DFRWS)**:
   - **NEVER** run `PRAGMA wal_checkpoint` directly on evidence files in `00_Evidence/`.
   - **ALWAYS** clone the `.db`, `-wal`, and `-shm` files together into a quarantined working directory.
   - Carve orphaned records from raw unallocated pages before checkpointing working copies.
4. **Windows NTFS Colon Restriction Bypass**:
   iOS domains often contain colons (`::`) in file paths. Standard tools (`pymobiledevice3 unback`) fail on Windows NTFS. The pipeline must unpack entries by reading `Manifest.db` directly, sanitizing characters (`::` $\rightarrow$ `_`), and streaming files by `fileID`.

---

## Standard 7-Phase Execution Pipeline

```
[ Phase 0: Encrypted Acquisition ]
       │  pymobiledevice3 / usbmuxd encrypted backup (passcode derivation)
       ▼
[ Phase 1: Cryptographic Preservation ]
       │  Dual SHA-256 + MD5 baseline hashing; Set evidence to READ-ONLY
       ▼
[ Phase 2: Filesystem & Domain Mapping ]
       │  Parse Manifest.db, map AppDomains, CameraRoll, and System Domains
       ▼
[ Phase 3: Core Database & Keychain Parsing ]
       │  Apply WALRUS protocol; Parse sms.db, CallHistory, AddressBook, Keychain
       ▼
[ Phase 4: Media & Live Photo Extraction ]
       │  Extract DCIM; Match HEIC/MOV pairs via Apple ContentIdentifier tag
       ▼
[ Phase 5: Deep-Dive SQLite Freelist Carving ]
       │  Inspect B-tree gaps for deleted records and revoked WhatsApp messages
       ▼
[ Phase 6: Geospatial & Pattern of Life ]
       │  Correlate EXIF GPS + HealthKit telemetry into interactive KML/Leaflet maps
       ▼
[ Phase 7: Daubert-Compliant Reporting ]
       │  Generate self-contained HTML/PDF dossier with unbroken chain of custody
```

---

## Artifact Reference Matrix

| Artifact Domain | Database / Storage Path | Evidentiary Value |
|---|---|---|
| **iMessage & SMS** | `Library/SMS/sms.db` | Message bodies, service type, sender handles, deleted sync remnants |
| **Call History** | `Library/CallHistoryDB/CallHistory.storedata` | Call duration, direction, answered state, contact numbers |
| **HealthKit Telemetry**| `Health/healthdb_secure.sqlite` | Granular GPS tracks, daily step cadence, walking speed asymmetry |
| **iOS Keychain** | `keychain-backup.plist` | Saved WPA Wi-Fi keys, VPN tokens, Safari web passwords, auth secrets |
| **WhatsApp Chats** | `AppDomainGroup-group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite` | Full chat logs, group memberships, revoked message references (`Status 5`) |
| **WhatsApp Revoked**| `ZWAMESSAGE` / `ZWAMEDIAITEM` | Preserved audio `.opus` voice notes and images even after "Delete for Everyone" |
| **Instagram Pando** | `AppDomain-com.burbn.instagram/shared_bootstraps.plist` | Binary plist trees decoding mutual contacts, user PKs, and cached handles |
| **TikTok Contacts** | `AppDomain-com.ss.iphone.ugc.Ame/Documents/AwemeIM.db` | Direct messaging contacts, follower statistics, and interaction metadata |
| **Pattern of Life** | `Library/CoreDuet/Knowledge/knowledgeC.db` | App launch history, device unlock states, battery usage curves |

---

## Automated Verification & Delivery Checklist

- [ ] All evidence files hashed with SHA-256 and MD5 prior to any analytical inspection.
- [ ] Evidence directory set to read-only (`attrib +R "00_Evidence\*.*" /S`).
- [ ] Working database copies inspected without modifying original WAL files.
- [ ] All timestamps normalized to ISO-8601 UTC with Apple Cocoa offset applied (`unix_time = cocoa_time + 978307200`).
- [ ] Network relationship graph compiled connecting telecom, social, and financial entities.
- [ ] Geospatial master ledger cross-verified against physical photograph EXIF data.
- [ ] Case dossier compiled with signed chain-of-custody audit logs.
