#!/usr/bin/env python3
"""
Workshop OS Digital Forensics & Data Recovery Engine
===================================================
Integrated professional forensic toolchain combining:
- The Sleuth Kit (TSK 4.15) for filesystem inspection & deleted file recovery
- CGSecurity TestDisk & PhotoRec 7.3 for partition repair & signature carving
- Fox-IT Dissect Framework for raw/E01/VMDK/VHD dissection & NTFS MFT parsing
- Volatility 3 for memory dump analysis
- Puremagic & Hash algorithms for cryptographic chain of custody

Usage:
    python scripts/workshop_forensics.py status
    python scripts/workshop_forensics.py hash <file_or_image>
    python scripts/workshop_forensics.py partitions <image_path>
    python scripts/workshop_forensics.py fsstat <image_path> [--offset <sector_offset>]
    python scripts/workshop_forensics.py list-deleted <image_path> [--offset <sector_offset>]
    python scripts/workshop_forensics.py recover <image_path> <inode> <output_file> [--offset <sector_offset>]
    python scripts/workshop_forensics.py carve <image_path> <output_dir>
    python scripts/workshop_forensics.py strings <file_path> [--min <length>] [--grep <pattern>]
    python scripts/workshop_forensics.py dissect <image_path> [--query <info|files|volumes>]
"""

import sys
import json
import hashlib
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
TOOLS_DIR = WORKSHOP_DIR / "tools" / "forensics"
TSK_BIN = TOOLS_DIR / "sleuthkit" / "sleuthkit-4.15.0-win32" / "bin"
TESTDISK_BIN = TOOLS_DIR / "testdisk"


def get_bin(tool_name: str) -> Path:
    """Find forensic executable in workshop tools or system PATH."""
    tsk_candidate = TSK_BIN / f"{tool_name}.exe"
    if tsk_candidate.exists():
        return tsk_candidate

    td_candidate = TESTDISK_BIN / f"{tool_name}.exe"
    if td_candidate.exists():
        return td_candidate

    # Try system PATH
    import shutil
    sys_path = shutil.which(tool_name) or shutil.which(f"{tool_name}.exe")
    if sys_path:
        return Path(sys_path)

    return tsk_candidate  # Fallback


def cmd_status(args):
    """Check forensic toolchains and environment status."""
    print("=================================================================")
    print(" 🛡️ WORKSHOP DIGITAL FORENSICS & DATA RECOVERY ARSENAL")
    print("=================================================================\n")

    # 1. TSK
    tsk_tools = ["mmls", "fsstat", "fls", "icat", "tsk_recover", "img_stat"]
    print("📦 The Sleuth Kit (TSK 4.15.0):")
    for t in tsk_tools:
        p = get_bin(t)
        status = "✅ Ready" if p.exists() else "❌ Missing"
        print(f"  • {t:<15} : {status} ({p})")

    # 2. TestDisk & PhotoRec
    td_tools = ["testdisk_win", "photorec_win", "fidentify_win"]
    print("\n📦 CGSecurity TestDisk & PhotoRec 7.3:")
    for t in td_tools:
        p = get_bin(t)
        status = "✅ Ready" if p.exists() else "❌ Missing"
        print(f"  • {t:<15} : {status} ({p})")

    # 3. Python Forensic Frameworks
    print("\n🐍 Python DFIR Suites:")
    for mod_name, desc in [
        ("dissect", "Fox-IT Dissect Incident Response Framework"),
        ("volatility3", "Volatility 3 Memory Forensics Engine"),
        ("pefile", "PE Executable Header & Section Parser"),
        ("puremagic", "MIME & Magic Byte Signature Analyzer"),
        ("construct", "Binary Data Structure Unpacker"),
    ]:
        try:
            __import__(mod_name)
            print(f"  • {mod_name:<15} : ✅ Installed ({desc})")
        except ImportError:
            print(f"  • {mod_name:<15} : ❌ Not Installed ({desc})")

    print("\n=================================================================\n")


def compute_hashes(file_path: str) -> dict:
    """Calculate cryptographic hashes of digital evidence (file or directory)."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Target path not found: {file_path}")

    if path.is_dir():
        file_manifests = []
        total_dir_bytes = 0
        for p in sorted(path.rglob("*")):
            if p.is_file():
                file_res = compute_hashes(str(p))
                file_manifests.append(file_res)
                total_dir_bytes += file_res["size_bytes"]
        return {
            "directory": str(path.resolve()),
            "name": path.name,
            "total_size_bytes": total_dir_bytes,
            "total_size_mb": round(total_dir_bytes / (1024 * 1024), 2),
            "files_count": len(file_manifests),
            "files": file_manifests,
            "verified_utc": datetime.now(timezone.utc).isoformat(),
        }

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    total_bytes = 0
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            total_bytes += len(chunk)
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    return {
        "file": str(path.resolve()),
        "name": path.name,
        "size_bytes": total_bytes,
        "size_mb": round(total_bytes / (1024 * 1024), 2),
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest(),
        "verified_utc": datetime.now(timezone.utc).isoformat(),
    }


def cmd_hash(args):
    """Execute cryptographic verification and output evidence manifest."""
    res = compute_hashes(args.target)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=================================================================")
        print(" 🔒 EVIDENCE INTEGRITY & CHAIN OF CUSTODY HASH MANIFEST")
        print("=================================================================")
        print(f" Evidence File : {res['file']}")
        print(f" File Size     : {res['size_bytes']:,} bytes ({res['size_mb']} MB)")
        print(f" Verified UTC  : {res['verified_utc']}")
        print("-----------------------------------------------------------------")
        print(f" MD5           : {res['md5']}")
        print(f" SHA-1         : {res['sha1']}")
        print(f" SHA-256       : {res['sha256']}")
        print("=================================================================\n")


def cmd_partitions(args):
    """Inspect partition layout using mmls."""
    mmls = get_bin("mmls")
    if not mmls.exists():
        print(f"Error: mmls binary not found at {mmls}", file=sys.stderr)
        sys.exit(1)

    cmd = [str(mmls), args.image]
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        print(f"Error inspecting partition table:\n{proc.stderr}", file=sys.stderr)
    else:
        print(proc.stdout)


def cmd_fsstat(args):
    """Inspect filesystem statistics using fsstat."""
    fsstat = get_bin("fsstat")
    if not fsstat.exists():
        print(f"Error: fsstat binary not found at {fsstat}", file=sys.stderr)
        sys.exit(1)

    cmd = [str(fsstat)]
    if args.offset is not None:
        cmd.extend(["-o", str(args.offset)])
    cmd.append(args.image)

    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        print(f"Error inspecting filesystem:\n{proc.stderr}", file=sys.stderr)
    else:
        print(proc.stdout)


def cmd_list_deleted(args):
    """List deleted files and inodes using fls."""
    fls = get_bin("fls")
    if not fls.exists():
        print(f"Error: fls binary not found at {fls}", file=sys.stderr)
        sys.exit(1)

    cmd = [str(fls), "-r", "-p", "-d"]
    if args.offset is not None:
        cmd.extend(["-o", str(args.offset)])
    cmd.append(args.image)

    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        print(f"Error listing deleted files:\n{proc.stderr}", file=sys.stderr)
    else:
        print(proc.stdout)


def cmd_recover(args):
    """Extract file by inode/MFT reference using icat."""
    icat = get_bin("icat")
    if not icat.exists():
        print(f"Error: icat binary not found at {icat}", file=sys.stderr)
        sys.exit(1)

    cmd = [str(icat)]
    if args.offset is not None:
        cmd.extend(["-o", str(args.offset)])
    cmd.extend([args.image, str(args.inode)])

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "wb") as f_out:
        proc = subprocess.run(cmd, stdout=f_out, stderr=subprocess.PIPE)

    if proc.returncode != 0:
        print(f"Error extracting inode {args.inode}:\n{proc.stderr.decode('utf-8', errors='replace')}", file=sys.stderr)
        if out_path.exists() and out_path.stat().st_size == 0:
            out_path.unlink()
    else:
        size = out_path.stat().st_size if out_path.exists() else 0
        print(f"✅ Successfully recovered inode {args.inode} to {out_path} ({size:,} bytes)")


def cmd_carve(args):
    """Carve files using PhotoRec non-destructively."""
    photorec = get_bin("photorec_win")
    if not photorec.exists():
        print(f"Error: photorec_win binary not found at {photorec}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Launch PhotoRec in batch carve mode (/cmd <image> search)
    cmd = [str(photorec), "/cmd", args.image, "search"]
    print(f"🚀 Launching PhotoRec Carving on {args.image} -> Output: {out_dir}")
    proc = subprocess.run(cmd, cwd=str(out_dir))
    print(f"Carving finished with return code {proc.returncode}")


def cmd_strings(args):
    """Extract printable strings from binary evidence."""
    path = Path(args.target)
    if not path.exists():
        print(f"Error: File not found: {args.target}", file=sys.stderr)
        sys.exit(1)

    min_len = args.min or 4
    grep_pattern = args.grep.lower() if args.grep else None

    import re
    ascii_re = re.compile(rf"[ -~]{{{min_len},}}".encode("ascii"))
    count = 0

    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            matches = ascii_re.findall(chunk)
            for m in matches:
                decoded = m.decode("ascii", errors="ignore")
                if grep_pattern and grep_pattern not in decoded.lower():
                    continue
                print(decoded)
                count += 1
                if args.limit and count >= args.limit:
                    return


def cmd_dissect(args):
    """Dissect disk image or evidence container using Fox-IT Dissect."""
    try:
        from dissect.target import Target
    except ImportError:
        print("Error: dissect library is not installed in the python environment.", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Dissecting target image: {args.image}")
    try:
        target = Target.open(args.image)
        query = args.query or "info"
        if query == "info":
            print(f" Target Hostname : {target.hostname}")
            print(f" OS Type         : {target.os}")
            print(f" Disks Found     : {len(target.disks)}")
            for idx, disk in enumerate(target.disks):
                print(f"   Disk #{idx}: size={disk.size:,} bytes")
            print(f" Volumes Found   : {len(target.volumes)}")
            for idx, vol in enumerate(target.volumes):
                print(f"   Volume #{idx}: fs={vol.fs_type} size={vol.size:,} bytes")
        elif query == "files":
            for entry in target.fs.walk("/"):
                print(entry.path)
    except Exception as e:
        print(f"Dissect inspection error: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Workshop OS Digital Forensics & Recovery Master CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Forensic Subcommand")

    # Status
    subparsers.add_parser("status", help="Inspect forensic arsenal and tools")

    # Hash
    p_hash = subparsers.add_parser("hash", help="Cryptographic hash verification (MD5, SHA1, SHA256)")
    p_hash.add_argument("target", help="Path to evidence file or image")
    p_hash.add_argument("--json", action="store_true", help="Output JSON manifest")

    # Partitions
    p_part = subparsers.add_parser("partitions", help="Inspect partition table layout (mmls)")
    p_part.add_argument("image", help="Path to raw/dd/e01 disk image")

    # Fsstat
    p_fs = subparsers.add_parser("fsstat", help="Inspect filesystem details (fsstat)")
    p_fs.add_argument("image", help="Path to disk image")
    p_fs.add_argument("--offset", "-o", type=int, default=None, help="Sector offset to partition")

    # List Deleted
    p_ld = subparsers.add_parser("list-deleted", help="List deleted files and inode references (fls)")
    p_ld.add_argument("image", help="Path to disk image")
    p_ld.add_argument("--offset", "-o", type=int, default=None, help="Sector offset to partition")

    # Recover
    p_rec = subparsers.add_parser("recover", help="Extract file by inode reference (icat)")
    p_rec.add_argument("image", help="Path to disk image")
    p_rec.add_argument("inode", help="Inode / MFT record number")
    p_rec.add_argument("output", help="Destination file path")
    p_rec.add_argument("--offset", "-o", type=int, default=None, help="Sector offset to partition")

    # Carve
    p_carve = subparsers.add_parser("carve", help="Carve files via PhotoRec")
    p_carve.add_argument("image", help="Path to image")
    p_carve.add_argument("output_dir", help="Output directory")

    # Strings
    p_str = subparsers.add_parser("strings", help="Extract printable strings from evidence")
    p_str.add_argument("target", help="Path to evidence file")
    p_str.add_argument("--min", "-m", type=int, default=4, help="Minimum string length")
    p_str.add_argument("--grep", "-g", default=None, help="Filter string pattern")
    p_str.add_argument("--limit", "-n", type=int, default=100, help="Max lines to output")

    # Dissect
    p_dis = subparsers.add_parser("dissect", help="Dissect target using Fox-IT framework")
    p_dis.add_argument("image", help="Path to image or VMDK/VHD")
    p_dis.add_argument("--query", choices=["info", "files", "volumes"], default="info")

    # iOS Mobile Extraction & Forensics Engine
    p_ios = subparsers.add_parser("ios", help="iOS Mobile Forensics & Acquisition Engine (pymobiledevice3)")
    p_ios.add_argument("ios_args", nargs=argparse.REMAINDER, help="Arguments passed to workshop_ios.py")

    args = parser.parse_args()

    if args.subcommand == "status":
        cmd_status(args)
    elif args.subcommand == "hash":
        cmd_hash(args)
    elif args.subcommand == "partitions":
        cmd_partitions(args)
    elif args.subcommand == "fsstat":
        cmd_fsstat(args)
    elif args.subcommand == "list-deleted":
        cmd_list_deleted(args)
    elif args.subcommand == "recover":
        cmd_recover(args)
    elif args.subcommand == "carve":
        cmd_carve(args)
    elif args.subcommand == "strings":
        cmd_strings(args)
    elif args.subcommand == "dissect":
        cmd_dissect(args)
    elif args.subcommand == "ios":
        sub_argv = args.ios_args
        subprocess.run([sys.executable, str(SCRIPTS_DIR / "workshop_ios.py")] + sub_argv)
    else:
        cmd_status(args)


if __name__ == "__main__":
    main()
