---
name: digital-forensic-investigation
description: Digital forensics, disk analysis, and mobile device evidence acquisition protocols for Windows and iOS.
tags: [forensics, ios, tsk, testdisk, hashes, chain-of-custody]
---

# Digital Forensic Investigation & Evidence Acquisition Protocol

This skill codifies deterministic procedures for physical/logical disk forensics, mobile device evidence extraction, and hash-verified chain-of-custody preservation.

---

## 1. Operating Rules & Evidence Invariants

1. **Write-Blocking / Read-Only Guard:** Never mount, write to, or mutate primary evidence files. Always set read-only attributes:
   ```cmd
   attrib +R "evidence\*.*" /S /D
   ```
2. **Cryptographic Provenance:** Compute dual SHA-256 and MD5 hashes immediately upon acquisition:
   ```bash
   uv run python scripts/workshop.py forensic hash "<evidence_path>" --json
   ```
3. **Sequential Device Extraction on Windows:** When acquiring iOS devices via `pymobiledevice3` on Windows, do NOT parallelize extraction commands. Execute commands sequentially to prevent Windows USB stack disconnects.

---

## 2. Core Forensic Workflows

### A. Disk Partition & Volume Inspection
```bash
# Check status and available forensic engines (TSK, TestDisk, Volatility)
uv run python scripts/workshop.py forensic status

# Inspect partition table layout
uv run python scripts/workshop.py forensic partitions "<disk_image.raw>"

# List deleted files at specific sector offset
uv run python scripts/workshop.py forensic list-deleted "<disk_image.raw>" --offset 2048
```

### B. Inode Recovery & File Carving
```bash
# Recover specific deleted file by Inode
uv run python scripts/workshop.py forensic recover "<disk_image.raw>" <inode> "<output_file>" --offset 2048

# Signature-based file carving (PhotoRec / TestDisk)
uv run python scripts/workshop.py forensic carve "<disk_image.raw>" "<output_dir>"
```

### C. iOS Live Extraction & Manifest Parsing
1. **Resumable Extraction:** `backup2 unback` operations are resilient. If interrupted by timeout or cable disconnect, re-running preserves previously extracted domains in `<udid>.unback/`.
2. **Manifest.plist Extraction:** The encrypted `Manifest.db` cannot be parsed with standard SQLite without device keybags. Instead, parse `Manifest.plist` via Python's standard `plistlib`:
   ```python
   import plistlib
   with open("Manifest.plist", "rb") as f:
       manifest = plistlib.load(f)
   apps = manifest.get("Applications", {})
   ```
3. **App Artifact Targeting:** Priority SQLite databases for instant extraction:
   * WhatsApp: `ChatStorage.sqlite`, `CallHistory.sqlite`, `ContactsV2.sqlite`
   * Telegram & Line databases
   * TikTok: `AwemeIM.db`
