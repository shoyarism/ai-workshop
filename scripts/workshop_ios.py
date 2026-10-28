#!/usr/bin/env python3
"""
Workshop iOS Forensic & Media Recovery Engine
=============================================
Integrates pymobiledevice3 to perform:
- Device triage & lockdown inspection
- Direct AFC media extraction (DCIM, PhotoData, Thumbnails)
- Full logical backup & backup unpack
- In-depth Photos.sqlite forensic parsing (Active vs. Trashed/Deleted media)
"""

import sys
import argparse
import subprocess
import sqlite3
import csv
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
APPLE_EPOCH_OFFSET = 978307200  # Jan 1 2001 -> Unix Epoch offset


def apple_time_to_iso(ts):
    if ts is None or ts == 0:
        return "N/A"
    try:
        return datetime.fromtimestamp(ts + APPLE_EPOCH_OFFSET, timezone.utc).isoformat()
    except Exception:
        return str(ts)


def cmd_info(args):
    """Retrieve device lockdown info."""
    print("📱 Querying iOS Device Information...")
    cmd = [sys.executable, "-m", "pymobiledevice3", "lockdown", "info"]
    subprocess.run(cmd)


def cmd_pull_dcim(args):
    """Pull DCIM folder to local destination."""
    out_dir = Path(args.destination)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"📥 Pulling DCIM camera roll to: {out_dir}")
    cmd = [sys.executable, "-m", "pymobiledevice3", "afc", "pull", "DCIM", str(out_dir), "--ignore-errors"]
    subprocess.run(cmd)


def cmd_pull_photodata(args):
    """Pull PhotoData directory (Photos.sqlite, WAL, Thumbnails) to destination."""
    out_dir = Path(args.destination)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"📥 Pulling PhotoData to: {out_dir}")
    cmd = [sys.executable, "-m", "pymobiledevice3", "afc", "pull", "PhotoData", str(out_dir), "--ignore-errors"]
    subprocess.run(cmd)


def cmd_backup(args):
    """Perform full logical backup."""
    out_dir = Path(args.destination)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"📦 Initiating Full Logical Backup to: {out_dir}")
    cmd = [sys.executable, "-m", "pymobiledevice3", "backup2", "backup", str(out_dir)]
    subprocess.run(cmd)


def cmd_unback(args):
    """Unpack a backup into native folder tree."""
    src = Path(args.backup_dir)
    out_dir = Path(args.destination)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"📂 Unpacking Backup from {src} to: {out_dir}")
    cmd = [sys.executable, "-m", "pymobiledevice3", "backup2", "unback", str(src), str(out_dir)]
    subprocess.run(cmd)


def cmd_parse_photos(args):
    """Parse Photos.sqlite for active vs. deleted/trashed media."""
    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    recovered_dir = out_dir / "Recovered_Deleted_Media"
    recovered_dir.mkdir(parents=True, exist_ok=True)

    dcim_dir = Path(args.dcim_dir) if args.dcim_dir else None

    print(f"🔍 Analyzing Photos Database: {db_path}")
    conn = sqlite3.connect(f"file:{db_path.resolve()}?immutable=1", uri=True)
    c = conn.cursor()

    # Determine asset table name (ZASSET on iOS 14+, ZGENERICASSET on older)
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in c.fetchall()]
    table_name = "ZASSET" if "ZASSET" in tables else "ZGENERICASSET"

    print(f"📊 Using table: {table_name}")

    # Inspect columns
    c.execute(f"PRAGMA table_info({table_name})")  # @court-exempt: literal pragma table inspection
    cols = [r[1] for r in c.fetchall()]

    filename_col = "ZFILENAME" if "ZFILENAME" in cols else cols[1]
    dir_col = "ZDIRECTORY" if "ZDIRECTORY" in cols else "None"
    trashed_col = "ZTRASHEDSTATE" if "ZTRASHEDSTATE" in cols else "None"
    trashed_date_col = "ZTRASHEDDATE" if "ZTRASHEDDATE" in cols else "None"
    created_col = "ZDATECREATED" if "ZDATECREATED" in cols else "None"
    modified_col = "ZMODIFICATIONDATE" if "ZMODIFICATIONDATE" in cols else "None"
    lat_col = "ZLATITUDE" if "ZLATITUDE" in cols else "None"
    lon_col = "ZLONGITUDE" if "ZLONGITUDE" in cols else "None"
    width_col = "ZWIDTH" if "ZWIDTH" in cols else "None"
    height_col = "ZHEIGHT" if "ZHEIGHT" in cols else "None"
    duration_col = "ZDURATION" if "ZDURATION" in cols else "None"
    uti_col = "ZUNIFORMTYPEIDENTIFIER" if "ZUNIFORMTYPEIDENTIFIER" in cols else "None"

    query_cols = [
        ("Filename", filename_col),
        ("Directory", dir_col),
        ("TrashedState", trashed_col),
        ("TrashedDate", trashed_date_col),
        ("DateCreated", created_col),
        ("ModificationDate", modified_col),
        ("Latitude", lat_col),
        ("Longitude", lon_col),
        ("Width", width_col),
        ("Height", height_col),
        ("Duration", duration_col),
        ("UTI", uti_col),
    ]

    select_clause = ", ".join([col if col != "None" else "NULL" for _, col in query_cols])
    query = f"SELECT {select_clause} FROM {table_name}"
    c.execute(query)
    rows = c.fetchall()

    active_items = []
    trashed_items = []

    for r in rows:
        item = {
            "Filename": r[0] or "UNKNOWN",
            "Directory": r[1] or "",
            "TrashedState": r[2] or 0,
            "TrashedDate_ISO": apple_time_to_iso(r[3]),
            "DateCreated_ISO": apple_time_to_iso(r[4]),
            "ModificationDate_ISO": apple_time_to_iso(r[5]),
            "Latitude": r[6] if r[6] not in (None, -180.0) else "",
            "Longitude": r[7] if r[7] not in (None, -180.0) else "",
            "Width": r[8] or "",
            "Height": r[9] or "",
            "Duration_sec": round(r[10], 2) if r[10] else "",
            "UTI": r[11] or "",
        }

        if item["TrashedState"] != 0:
            trashed_items.append(item)
        else:
            active_items.append(item)

    print(f"✅ Total records found: {len(rows)}")
    print(f"   • Active Media: {len(active_items):,}")
    print(f"   • Trashed/Deleted Media: {len(trashed_items):,}")

    # Write CSV manifests
    active_csv = out_dir / "active_media_manifest.csv"
    trashed_csv = out_dir / "deleted_media_manifest.csv"

    fieldnames = list(active_items[0].keys()) if active_items else [name for name, _ in query_cols]

    with open(active_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(active_items)

    with open(trashed_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trashed_items)

    # Physical file recovery for trashed items if DCIM dir provided
    copied_count = 0
    if dcim_dir and dcim_dir.exists():
        print(f"\n📂 Scanning {dcim_dir} to extract physical files for {len(trashed_items)} deleted records...")
        for item in trashed_items:
            fname = item["Filename"]
            rel_dir = item["Directory"]
            # Look for file in rel_dir or recursively in dcim_dir
            candidate = dcim_dir / rel_dir / fname if rel_dir else dcim_dir / fname
            if not candidate.exists():
                # Search recursively in DCIM
                matches = list(dcim_dir.rglob(fname))
                if matches:
                    candidate = matches[0]

            if candidate.exists():
                dest_file = recovered_dir / f"DELETED_{fname}"
                try:
                    shutil.copy2(candidate, dest_file)
                    copied_count += 1
                except Exception as e:
                    print(f"Error copying {candidate}: {e}")

        print(f"🎯 Successfully extracted {copied_count} physical deleted media files to: {recovered_dir}")

    # Generate Markdown Forensic Summary Report
    report_file = out_dir / "ios_photos_forensic_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# iOS Photos Forensic & Recovery Examination Report\n\n")
        f.write(f"- **Analysis Date (UTC):** {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"- **Database Source:** `{db_path.name}`\n")
        f.write(f"- **Total Asset Records:** {len(rows):,}\n")
        f.write(f"- **Active Media Records:** {len(active_items):,}\n")
        f.write(f"- **Trashed / Deleted Media Records:** {len(trashed_items):,}\n")
        if dcim_dir:
            f.write(f"- **Physical Trashed Files Recovered:** {copied_count:,} files (saved to `Recovered_Deleted_Media/`)\n")
        f.write("\n---\n\n")
        f.write("## 1. Recently Deleted Media Breakdown\n\n")
        f.write("| Filename | Directory | Created Date (UTC) | Trashed Date (UTC) | GPS Coordinates |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for item in trashed_items[:50]:
            gps = f"{item['Latitude']}, {item['Longitude']}" if item['Latitude'] else "No GPS"
            f.write(f"| `{item['Filename']}` | `{item['Directory']}` | {item['DateCreated_ISO']} | {item['TrashedDate_ISO']} | {gps} |\n")
        if len(trashed_items) > 50:
            f.write(f"\n*(...and {len(trashed_items) - 50} more items recorded in `deleted_media_manifest.csv`)*\n")

    conn.close()
    print(f"📋 Forensic Report generated at: {report_file}")
    print(f"📊 Active Manifest: {active_csv}")
    print(f"📊 Trashed/Deleted Manifest: {trashed_csv}")


def main():
    parser = argparse.ArgumentParser(description="Workshop iOS Forensic & Media Recovery Engine")
    subparsers = parser.add_subparsers(dest="subcommand", help="iOS Subcommand")

    # Info
    subparsers.add_parser("info", help="Inspect connected iOS device lockdown info")

    # Pull DCIM
    p_dcim = subparsers.add_parser("pull-dcim", help="Pull DCIM camera roll via AFC")
    p_dcim.add_argument("destination", help="Target destination folder")

    # Pull PhotoData
    p_pd = subparsers.add_parser("pull-photodata", help="Pull PhotoData (Photos.sqlite, Thumbnails) via AFC")
    p_pd.add_argument("destination", help="Target destination folder")

    # Backup
    p_bak = subparsers.add_parser("backup", help="Perform full logical backup")
    p_bak.add_argument("destination", help="Target destination folder")

    # Unback
    p_unb = subparsers.add_parser("unback", help="Unpack backup directory")
    p_unb.add_argument("backup_dir", help="Path to raw backup folder")
    p_unb.add_argument("destination", help="Target destination folder")

    # Parse Photos
    p_parse = subparsers.add_parser("parse-photos", help="Parse Photos.sqlite for active vs. deleted media")
    p_parse.add_argument("db_path", help="Path to Photos.sqlite")
    p_parse.add_argument("output_dir", help="Output directory for manifests and reports")
    p_parse.add_argument("--dcim-dir", default=None, help="Path to extracted DCIM folder to physically isolate deleted files")

    args = parser.parse_args()

    if args.subcommand == "info":
        cmd_info(args)
    elif args.subcommand == "pull-dcim":
        cmd_pull_dcim(args)
    elif args.subcommand == "pull-photodata":
        cmd_pull_photodata(args)
    elif args.subcommand == "backup":
        cmd_backup(args)
    elif args.subcommand == "unback":
        cmd_unback(args)
    elif args.subcommand == "parse-photos":
        cmd_parse_photos(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
