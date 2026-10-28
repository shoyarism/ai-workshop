---
name: digital-forensics-and-recovery
description: Professional digital forensics, data recovery, filesystem triage, signature carving, memory forensics, and court-admissible evidence reporting via TSK, TestDisk, PhotoRec, Dissect, and Volatility 3.
risk: low
source: workshop-arsenal
date_added: 2026-09-21
---

# Digital Forensics & Data Recovery Engine

## Overview
The Digital Forensics & Data Recovery Engine equips AI agents to perform digital forensics, incident response triage, and data recovery across physical disks, disk images (`.raw`, `.dd`, `.img`, `.E01`), virtual disk formats (`VMDK`, `VHD`), and memory dumps.

It integrates:
- **The Sleuth Kit (TSK 4.15.0)**: Low-level partition layout (`mmls`), filesystem structures (`fsstat`), deleted file listings (`fls`), and inode-based targeted file extraction (`icat`).
- **CGSecurity TestDisk & PhotoRec 7.3**: Partition table repair, boot sector reconstruction (FAT/NTFS/EXT/HFS), and non-destructive signature-based file carving.
- **Fox-IT Dissect**: Enterprise incident response framework for dissecting disk targets, NTFS `$MFT`, `$LogFile`, `$UsnJrnl`, Registry hives, and Windows Event Logs.
- **Volatility 3**: Memory forensics for triage of RAM dumps.
- **Evidence Integrity Verification**: Cryptographic hashing (MD5, SHA-1, SHA-256) and ISO/IEC 27037 compliant audit reporting.

---

## Capabilities & Commands

All commands can be executed from any directory via Python/`uv`:

```bash
# Set workshop root
$W = "."

# 🛡️ 1. Arsenal Health & Tool Availability Check
uv run python $W\scripts\workshop.py forensic status

# 🔒 2. Evidence Integrity & Chain of Custody Hashing (MD5, SHA1, SHA256)
uv run python $W\scripts\workshop.py forensic hash "C:\evidence\disk.raw" [--json]

# 📐 3. Partition Table Discovery (mmls)
uv run python $W\scripts\workshop.py forensic partitions "C:\evidence\disk.raw"

# 📊 4. Filesystem Statistics & Cluster Geometry (fsstat)
uv run python $W\scripts\workshop.py forensic fsstat "C:\evidence\disk.raw" --offset 2048

# 🗑️ 5. List Deleted Files & Unallocated Inodes (fls)
uv run python $W\scripts\workshop.py forensic list-deleted "C:\evidence\disk.raw" --offset 2048

# 🎯 6. Targeted File Recovery by Inode / MFT Record (icat)
uv run python $W\scripts\workshop.py forensic recover "C:\evidence\disk.raw" <inode_num> "C:\recovered\secret.docx" --offset 2048

# ⛏️ 7. Deep Signature-Based File Carving (PhotoRec)
uv run python $W\scripts\workshop.py forensic carve "C:\evidence\disk.raw" "C:\carved_output"

# 📜 8. Forensic Printable Strings Extraction
uv run python $W\scripts\workshop.py forensic strings "C:\evidence\memory.dmp" --min 6 --grep "password"

# 🔍 9. Dissect Container & Virtual Target Analysis (Fox-IT)
uv run python $W\scripts\workshop.py forensic dissect "C:\evidence\server.vmdk" --query info
```

---

## Operational Directives & Invariants

1. **Zero-Modification Policy (Rule #1 of DFIR)**:
   * **NEVER** perform in-place writes, defragmentation, `chkdsk`, or `fsck` on original physical disks or primary evidence images.
   * Conduct all investigations on bit-stream forensic copies or with write-blockers / copy-on-write (CoW) overlays.
2. **Cryptographic Verification**:
   * Calculate SHA-256 before opening evidence, and verify identical hashes after extraction or analysis.
3. **Deterministic Carving**:
   * Never speculate or generate hallucinated binary payloads for damaged files. Leverage PhotoRec or TSK `icat` to extract authentic byte structures.
