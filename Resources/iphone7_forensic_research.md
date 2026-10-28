# iPhone 7 Forensic Research Report — Project "iseeyou / Gita"

> Compiled: 2026-09-23 | Sources: 6 parallel research agents | Scope: iPhone 7 (A10 Fusion, iOS 10–15)

---

## Critical Findings That Change Everything

> [!CAUTION]
> These findings fundamentally alter the forensic approach from what was originally planned.

### 1. Traditional File Carving is USELESS on iOS
iOS uses **File-Based Encryption (FBE)**. When a file is deleted, its unique per-file encryption key is **destroyed**. The raw data left on flash is permanently encrypted noise. Header/footer carving (JPEG FFD8→FFD9, PNG signatures, etc.) on unallocated disk blocks will yield **nothing usable**.

**Instead**: Focus on **Database Carving** — recovering deleted rows from SQLite free pages, WAL files, and journal files where data existed in plaintext within the database layer.

### 2. Physical Extraction is Pointless
A raw NAND bit-for-bit dump of iPhone 7 is **mathematically unreadable** off-device because every file is encrypted with keys entangled with the Secure Enclave's hardware UID. **Full File System (FFS) extraction** via checkm8 has entirely replaced physical extraction in modern iOS forensics.

### 3. BFU vs AFU State is Critical
- **BFU (Before First Unlock)**: Only ~5% of data accessible (system logs, network config). User content is heavily encrypted.
- **AFU (After First Unlock)**: ~95% of user data accessible (SMS, photos, keychain, location). Keys are loaded in RAM.
- **The prompt MUST detect device state before choosing extraction strategy.**

### 4. checkm8 + Blackbird SEP = Full Access on A10
- **checkm8**: Permanent bootrom exploit for A10. Cannot be patched by Apple.
- **Blackbird**: SEP ROM vulnerability allowing FFS extraction **without removing the passcode** on iOS 14+.
- Combined, they give complete file system + keychain access.

### 5. checkra1n/palera1n Do NOT Run on Windows
- checkra1n requires **macOS or Linux**
- palera1n requires **Linux**
- On Windows: Must use **Linux live USB** (checkn1x or palen1x) or **WSL2**

---

## Law Enforcement & Intelligence Tools

### Commercial / Government-Grade

| Tool | Capabilities for iPhone 7 | Notes |
|------|--------------------------|-------|
| **Cellebrite UFED Premium** | FFS + Keychain extraction, brute-force acceleration | Most widely used by FBI/law enforcement |
| **GrayKey (Magnet)** | Agent-based passcode brute-force, FFS extraction | Exploits A10 hardware permanently |
| **Elcomsoft EIFT** | checkm8-based FFS + Keychain without passcode removal | SEP exploit integrated |
| **Magnet AXIOM** | Ingests GrayKey/Cellebrite extractions, deep artifact parsing | Superior analysis engine |
| **Oxygen Forensic Detective** | FFS extraction, auto-decrypts Signal/WhatsApp | Best for third-party app parsing |
| **MSAB XRY** | Logical + advanced extractions, field triage | Chain of custody focused |
| **Belkasoft X** | checkm8 FFS, Keychain, unified logs | Cost-effective alternative |
| **MOBILedit** | Logical extractions, lockdown file bypass | Limited without FFS |

### Intelligence Agency Tools (Publicly Disclosed)
- **CIA Vault 7 (WikiLeaks 2017)**: Zero-day exploits and malware targeting iOS for audio/text/geolocation interception
- **FBI San Bernardino (2016)**: Paid ~$1M to Azimuth Security for chained zero-day exploits on iPhone 5C
- **FBI routinely uses Cellebrite + GrayKey** in court (acknowledged in warrants)
- FOIA requests heavily redacted under national security / vendor NDAs

---

## Forensic Standards & Legal Frameworks

### Methodology Standards

| Standard | Key Requirements |
|----------|-----------------|
| **NIST SP 800-101 Rev 1** | 4 phases: Preservation → Acquisition → Examination → Reporting. Tool validation required. |
| **NIST SP 800-86** | Collection → Examination → Analysis → Reporting (IT/IR focus) |
| **SWGDE** | Network isolation, independent tool validation against known datasets |
| **ACPO (UK)** | 4 principles: No data alteration, competency, audit trail, case officer responsibility |
| **ISO/IEC 27037** | International evidence handling: identification, collection, acquisition, preservation |
| **FBI RCFL** | FBI-certified examiners, mandatory peer review, ASCLD/LAB accreditation |
| **INTERPOL** | Global standardization framework for cross-border evidence admissibility |

### Legal Admissibility (Daubert Standard)
To survive a Daubert challenge:
- Strict hash verification at every stage
- Unbroken chain of custody documentation
- Detailed methodology documentation
- Reproducibility of all procedures
- Peer-reviewed, published methods preferred

---

## Open-Source Tool Matrix

### Device Communication & Acquisition

| Tool | Status | Windows | URL | Notes |
|------|--------|---------|-----|-------|
| **libimobiledevice** | ✅ Active | ⚠️ MSYS2/prebuilt | github.com/libimobiledevice | Core iOS USB communication |
| **checkra1n** | ✅ Stable | ❌ macOS/Linux only | checkra.in | iOS 12–14.8.1 jailbreak |
| **palera1n** | ✅ Active | ❌ Linux only | palera.in | iOS 15+ jailbreak |
| **checkn1x/palen1x** | ✅ Active | ✅ Live USB | — | Linux live USB for Windows users |
| **MVT** | ✅ Active | ⚠️ WSL/Docker | github.com/mvt-project/mvt | Spyware detection (Amnesty Intl) |

### Analysis & Parsing

| Tool | Status | Windows | URL | Notes |
|------|--------|---------|-----|-------|
| **iLEAPP** | ✅ Active | ✅ | github.com/abrignoni/iLEAPP | iOS artifact parser (HTML/TSV/KML) |
| **APOLLO** | ✅ Active | ✅ | github.com/mac4n6/APOLLO | KnowledgeC pattern-of-life analysis |
| **mac_apt / ios_apt** | ✅ Active | ✅ | github.com/ydkhatri/mac_apt | iOS/macOS artifact parsing to SQLite/Excel |
| **Autopsy + TSK** | ✅ Active | ✅ | sleuthkit.org | Limited APFS; good with iLEAPP module |
| **FQLite** | ✅ Active | ✅ | github.com/pawlaszczyk/fqlite | **Gold standard** SQLite deleted record recovery |
| **ExifTool** | ✅ Active | ✅ | exiftool.org | HEIC/MOV metadata, Apple MakerNotes |

### DEPRECATED / AVOID

| Tool | Reason |
|------|--------|
| **undark** | Obsolete, no WAL support, archived |
| **scalpel** | Unmaintained legacy |
| **foremost** | Unmaintained legacy |
| **iOS Backup Analyzer** | Abandoned, replaced by iLEAPP |

### Critical Python Libraries

| Library | Purpose |
|---------|---------|
| **pytsk3** | Sleuth Kit bindings for filesystem parsing |
| **libfsapfs-python** | APFS container/volume parsing |
| **ccl_bplist** | Binary plist parsing (CCL Solutions) |
| **nska_deserialize** | NSKeyedArchiver plist conversion |
| **biplist** | Binary plist read/write |
| **exifread** | EXIF metadata extraction |
| **pillow** | Image processing and thumbnail extraction |
| **pandas** | Data normalization and timeline construction |

---

## Academic Research — Key Papers

### APFS & Filesystem
- **Plum & Dewald (2018)** — *Forensic APFS File Recovery*: CoW makes traditional carving ineffective. Must parse APFS B-trees, object maps, and snapshots.

### SQLite Recovery
- **bring2lite (DFRWS)** — Structural recovery of deleted SQLite records from freelist pages
- **WALRUS (DFRWS APAC 2026)** — Reconstructing deleted/encrypted WAL pages from unallocated space using high-entropy cluster identification

### Acquisition
- **SoK: Cryptographic Confidentiality of Data on Mobile Devices** — Physical acquisition yields encrypted noise. FFS via exploits is the modern standard.

### Artifacts
- **DFRWS: Interpreting Apple Health location data** — HealthKit stores granular geolocation in `healthdb_secure.sqlite`, often overlooked.

### Anti-Forensics
- **D'Orazio et al. (2014, HICSS)** — iOS anti-forensics: data hiding/injection via backup mechanisms without jailbreak. Counter: residual evidence in SQLite freeblocks.

### Keychain
- **Katalov (DFIR Review)** — Logical extractions only get subset of keychain. FFS needed for full keychain including Signal/WhatsApp encryption keys.

### Timeline
- **SoK: Timeline based event reconstruction** — Standardized methodology using Plaso/log2timeline for automated timeline construction from heterogeneous mobile artifacts.

### Media Carving
- **AutoDFBench 1.0 (DFRWS)** — Benchmarking HEIC carving tools using perceptual hashing (pHash) for integrity validation.

---

## Community Knowledge & Practitioner Tips

### Key Blogs & Researchers
| Person | Resource | Specialty |
|--------|----------|-----------|
| **Sarah Edwards** | mac4n6.com | APOLLO, KnowledgeC, pattern-of-life |
| **Alexis Brignoni** | abrignoni.com | iLEAPP creator, artifact parsing |
| **Yogesh Khatri** | Swift Forensics | mac_apt, unified logging, custom parsers |
| **Heather Mahalik** | Smarter Forensics | SANS FOR585 lead, methodology |
| **Vladimir Katalov** | Elcomsoft Blog | iOS security internals, keychain |

### Critical Gotchas
1. **DFU mode timing is finicky** on iPhone 7 — requires precise button sequence
2. **WAL recovery is time-sensitive** — OS background processes (vacuum/checkpoint) overwrite deleted data
3. **Thumbnail caches survive photo deletion** — even after "Recently Deleted" purge
4. **interactionC.db** retains message metadata after sms.db deletion
5. **Signal requires SQLCipher key from Keychain** — impossible without FFS extraction
6. **WhatsApp** stores chats in `ChatStorage.sqlite` (unencrypted on-device, unlike Signal)

### Training & CTFs
- **SANS FOR585**: Gold standard, vendor-neutral methodology
- **CyberDefenders "Jailbroken"**: iOS artifact parsing with iLEAPP
- **TryHackMe "iOS Forensics"**: File system analysis practice
- **Digital Corpora**: Free iOS extraction dumps for practice

---

## Artifacts Often Missed (Must Add to Prompt)

| Artifact | Database/Location | What It Reveals |
|----------|-------------------|-----------------|
| **KnowledgeC** | CoreDuet/Knowledge/knowledgeC.db | App usage, screen time, device interactions |
| **HealthKit** | healthdb_secure.sqlite | GPS locations, timezone, step data |
| **interactionC** | interactionC.db | Contact interaction frequency/recency |
| **Biome** | (iOS 16+ replacement for KnowledgeC) | N/A for iPhone 7 max iOS 15 |
| **Powerlog** | CurrentPowerlog.PLSQL | Battery/charging/app power usage patterns |
| **Routine/Significant Locations** | Routine.sqlite | Frequently visited places |
| **sysdiagnose** | Triggered via Vol Up+Down+Power | Deep system logs without jailbreak |
| **Lockdown Certificates** | /var/db/lockdown/ | Previously trusted computers |
| **Apple Maps Cache** | GeoHistory.mapsdata | Map searches and navigation history |
