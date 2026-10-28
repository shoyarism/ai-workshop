# iOS Live Device Extraction — Windows-Specific Lessons (iseeyou Session)

**Session:** Project iseeyou — iPhone 7 "Gitartnaa" forensic acquisition (2026-09-23/24)

## New Lessons from Session

### 1. Sequential Extraction Only on Windows
When multiple `backup2 extract` commands fail with "Connection was terminated abruptly," the issue is likely device connection dropping under load. Solution:
- Run ONLY ONE extraction command at a time
- Wait for completion/failure before starting next
- Do NOT parallelize extraction commands on Windows

### 2. Partial Unback Is Resumable
If `backup2 unback` is interrupted (killed, timeout, crash):
- Existing extracted files in `<udid>.unback/` are preserved
- Running unback again resumes from where it left off
- No data loss — only newly extracted domains are processed
- Check progress via: `python -c "import os; count=sum([len(f) for r,d,f in os.walk(unback_dir)]); print(count)"`

### 3. Hash Computation Timing Expectations
For a ~20GB encrypted backup:
- SHA-256 + MD5 on 21,084 files: ~1 hour (background process required)
- Never run hash computation in foreground terminal — it will timeout
- Use `terminal(background=true)` and monitor via `process(action='poll')`

### 4. Device Connection Reliability
- pymobiledevice3 extraction commands may fail with "Connection was terminated abruptly"
- This is a Windows USB stack issue, not a device problem
- Retry the same command — it may succeed on second attempt
- If multiple retries fail, the device may have gone into low-power USB mode
- Solution: Disconnect and reconnect USB cable, then retry

### 5. Manifest.plist Parsing on Windows
- The Manifest.db is encrypted (not standard SQLite)
- Use Manifest.plist instead — parse with Python's plistlib
- Key info is in `ManifestKey` field (may be bytes, check type first)
- The `Applications` field contains full app inventory with metadata

### 6. Evidence Verification Workflow
After hash computation completes:
1. Verify hash files exist: `ls 00_Evidence/hashes.*`
2. Check line counts match: `wc -l hashes.sha256 hashes.md5` (should be equal)
3. Spot-check a known file: compute its hash manually and compare
4. Set READ-ONLY on evidence: `attrib +R "evidence\*.*" /S /D` (may timeout on large dirs)

### 7. Background Process Management
When running long forensic operations:
- Always use `terminal(background=true)` for processes >60 seconds
- Track session_id from background output
- Poll with `process(action='poll', timeout=300)` every 5 minutes
- Check disk space periodically: `python -c "import os; print(f'{os.path.getsize(path)/(1024**3):.2f} GB')"`
- Kill stuck processes after 2+ hours with no progress

### 8. App-Level vs System-Level Extraction
The partial unback (757 files, 24 domains) successfully extracted:
- WhatsApp (ChatStorage.sqlite, CallHistory.sqlite, ContactsV2.sqlite)
- TikTok (AwemeIM.db with contacts)
- Instagram (draft database)
- Telegram, Line, Facebook apps

Missing system databases (not extracted in partial unback):
- SMS (Library/SMS/sms.db) — requires full unback
- Keychain (keychain-backup.plist) — encrypted, requires full unback
- Safari (History.db, Bookmarks.db) — requires full unback
- HealthKit — requires full unback
- CoreDuet — requires full unback

**Recommendation:** Document which databases are in the partial extraction vs. missing. Future sessions should attempt full unback immediately after backup completes.

### 9. Windows Path Restrictions — Workaround
The `::` character in iOS filenames causes Windows NTFS errors. Workarounds:
1. **Use Linux environment** (WSL, virtual machine, or remote server) where `::` is valid
2. **Extract specific databases** using `backup2 extract` one at a time (bypasses full unback)
3. **Wait for device reconnection** and retry extract commands individually
4. **Document the limitation** in the report — partial extraction is still forensically valid

### 10. Final Report Generation
When acquisition is partial:
- Clearly document what WAS extracted vs. what COULDN'T be extracted
- Include root cause analysis (Windows NTFS limitation)
- Provide actionable next steps for complete extraction
- Generate professional report regardless of partial status
- Use `Mission Completed` or `Mission Completed (Partial)` as final status

## Tools Used in This Session
- pymobiledevice3 v11.17.2 — primary acquisition tool
- Python hashlib — dual hash computation
- Python plistlib — Manifest.plist parsing
- Python sqlite3 — database analysis
- Windows attrib — READ-ONLY setting (timeout on large dirs)

## Success Metrics
| Metric | Result |
|--------|--------|
| Backup completed | ✓ 19.84 GB encrypted backup |
| Hash computation | ✓ 21,084 files (SHA-256 + MD5) |
| Partial unback | ✓ 757 files, 24 app domains |
| Database analysis | ✓ 35 databases parsed |
| Critical system DBs | ✗ SMS, Keychain, Safari, HealthKit, CoreDuet missing |
| Final report | ✓ Daubert-compliant report generated |

**Overall Status:** PARTIAL EXTRACTION COMPLETE — sufficient for app-level forensic analysis, missing system-level databases due to Windows NTFS limitation.
