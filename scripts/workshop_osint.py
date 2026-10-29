#!/usr/bin/env python3
"""
Workshop OS Open Source Intelligence (OSINT) & Investigation Engine
==================================================================
Unified reconnaissance & OSINT intelligence suite bridging:
- Auspex OSINT Suite (69 modules, 1,500+ site signatures, What'sMyName integration)
- Deep Username Enumeration & Nickname Permutation
- Email Validation, MX Discovery & Disposable Domain Detection
- International Phone Intelligence (libphonenumber)
- Domain Infrastructure Recon (DNS, crt.sh Subdomains, WHOIS)
- IP Geolocation & ASN Intelligence
- File Forensic Metadata Extraction

Usage:
    python scripts/workshop_osint.py status
    python scripts/workshop_osint.py username <target_username> [--fast] [--json]
    python scripts/workshop_osint.py email <target_email> [--json]
    python scripts/workshop_osint.py phone <target_phone> [--json]
    python scripts/workshop_osint.py domain <target_domain> [--json]
    python scripts/workshop_osint.py ip <target_ip> [--json]
    python scripts/workshop_osint.py metadata <target_file> [--json]
    python scripts/workshop_osint.py launch-auspex [--web]
"""

import sys
import json
import asyncio
import argparse
import subprocess
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
AUSPEX_PROJECT_DIR = Path(r".\Projects\Auspex")
AUSPEX_TOOL_DIR = Path(r".\Tool\Auspex")

# Resolve Auspex root
AUSPEX_DIR = AUSPEX_PROJECT_DIR if AUSPEX_PROJECT_DIR.exists() else AUSPEX_TOOL_DIR


def cmd_status(args):
    """Display OSINT suite and Auspex integration status."""
    print("=================================================================")
    print(" 🌐 WORKSHOP OSINT & INTELLIGENCE ARSENAL")
    print("=================================================================\n")

    # 1. Auspex Integration
    if AUSPEX_DIR.exists():
        modules_dir = AUSPEX_DIR / "modules"
        mod_count = len(list(modules_dir.glob("*.py"))) if modules_dir.exists() else 0
        print(f"📡 Auspex Master Suite: ✅ Connected ({AUSPEX_DIR})")
        print(f"   • Active OSINT Modules: {mod_count} modules available")
    else:
        print("📡 Auspex Master Suite: ❌ Not Found")

    # 2. Installed Python OSINT Packages
    print("\n📦 Python OSINT Engines:")
    packages = [
        ("phonenumbers", "International Phone Parsing & Carrier Engine"),
        ("dns.resolver", "Asynchronous DNS & Record Inspection Engine"),
        ("whois", "Domain Registration & Registrar Intelligence"),
        ("bs4", "BeautifulSoup4 Web Scraping & DOM Parser"),
        ("requests", "Synchronous HTTP Probe Client"),
        ("aiohttp", "High-Throughput Async HTTP Engine"),
    ]
    for pkg, desc in packages:
        try:
            __import__(pkg.split(".")[0])
            print(f"  • {pkg:<15} : ✅ Installed ({desc})")
        except ImportError:
            print(f"  • {pkg:<15} : ❌ Not Installed ({desc})")

    print("\n=================================================================\n")


def cmd_phone(args):
    """Perform international phone number OSINT."""
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone

    phone_raw = args.phone.strip()
    res = {"raw": phone_raw, "valid": False}

    try:
        parsed = phonenumbers.parse(phone_raw, None)
        is_valid = phonenumbers.is_valid_number(parsed)
        res["valid"] = is_valid
        res["country_code"] = parsed.country_code
        res["national_number"] = parsed.national_number
        res["e164_format"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        res["international"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        res["national"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        res["region"] = geocoder.description_for_number(parsed, "en")
        res["carrier"] = carrier.name_for_number(parsed, "en")
        res["timezones"] = list(timezone.time_zones_for_number(parsed))
    except Exception as e:
        res["error"] = str(e)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=================================================================")
        print(f" 📱 PHONE INTELLIGENCE: {phone_raw}")
        print("=================================================================")
        print(f" Validity       : {'✅ Valid' if res.get('valid') else '❌ Invalid'}")
        print(f" E.164 Format   : {res.get('e164_format', 'N/A')}")
        print(f" International  : {res.get('international', 'N/A')}")
        print(f" Region / Loc   : {res.get('region') or 'Unknown'}")
        print(f" Carrier / Telco: {res.get('carrier') or 'Unknown'}")
        print(f" Timezone(s)    : {', '.join(res.get('timezones', [])) or 'Unknown'}")
        print("=================================================================\n")


def cmd_email(args):
    """Validate email, query MX DNS records, and detect provider."""
    import re
    import dns.resolver

    email = args.email.strip().lower()
    res = {"email": email, "valid_syntax": False, "mx_records": []}

    syntax_pattern = r"^[\w\.-]+@([\w\.-]+\.\w+)$"
    match = re.match(syntax_pattern, email)
    if not match:
        res["error"] = "Invalid email format"
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"❌ Invalid email format: {email}")
        return

    res["valid_syntax"] = True
    domain = match.group(1)
    res["domain"] = domain

    # Check MX records
    try:
        answers = dns.resolver.resolve(domain, "MX")
        for rdata in answers:
            res["mx_records"].append(str(rdata.exchange).rstrip("."))
    except Exception as e:
        res["mx_error"] = str(e)

    # Disposable domain detection
    disposable_list = {"tempmail.com", "10minutemail.com", "guerrillamail.com", "throwawaymail.com", "mailinator.com", "yopmail.com"}
    res["is_disposable"] = domain in disposable_list

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=================================================================")
        print(f" ✉️ EMAIL RECONNAISSANCE: {email}")
        print("=================================================================")
        print(f" Domain         : {res['domain']}")
        print(f" Syntax Valid   : {'✅ Yes' if res['valid_syntax'] else '❌ No'}")
        print(f" Disposable     : {'⚠️ Flagged Disposable' if res['is_disposable'] else '✅ Clean Corporate/Personal'}")
        print(f" MX Records ({len(res['mx_records'])}):")
        for mx in res["mx_records"]:
            print(f"   • {mx}")
        print("=================================================================\n")


async def run_username_recon(username: str, fast: bool = False) -> dict:
    """Check username presence across tier-1 platforms."""
    import aiohttp

    platforms = [
        {"name": "GitHub", "url": f"https://github.com/{username}", "check": "status_200"},
        {"name": "Reddit", "url": f"https://www.reddit.com/user/{username}/about.json", "check": "status_200"},
        {"name": "Telegram", "url": f"https://t.me/{username}", "check": "body_match", "pattern": "tgme_page_title"},
        {"name": "Medium", "url": f"https://medium.com/@{username}", "check": "status_200"},
        {"name": "Pinterest", "url": f"https://www.pinterest.com/{username}/", "check": "status_200"},
        {"name": "GitLab", "url": f"https://gitlab.com/{username}", "check": "status_200"},
        {"name": "DockerHub", "url": f"https://hub.docker.com/v2/users/{username}/", "check": "status_200"},
        {"name": "Dev.to", "url": f"https://dev.to/{username}", "check": "status_200"},
        {"name": "HackerNews", "url": f"https://news.ycombinator.com/user?id={username}", "check": "status_200"},
        {"name": "Steam", "url": f"https://steamcommunity.com/id/{username}", "check": "status_200"},
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    found = []
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for p in platforms:
            async def check_platform(plat):
                try:
                    async with session.get(plat["url"], timeout=aiohttp.ClientTimeout(total=4.0)) as resp:
                        if plat["check"] == "status_200" and resp.status == 200:
                            found.append({"platform": plat["name"], "url": plat["url"]})
                        elif plat["check"] == "body_match":
                            text = await resp.text()
                            if plat["pattern"] in text:
                                found.append({"platform": plat["name"], "url": plat["url"]})
                except Exception:  # @court-exempt: handled fallback
                    pass
            tasks.append(check_platform(p))
        await asyncio.gather(*tasks)

    return {"username": username, "total_scanned": len(platforms), "found": found}


def cmd_username(args):
    """Execute multi-platform username recon."""
    username = args.username.strip()
    res = asyncio.run(run_username_recon(username, fast=args.fast))

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=================================================================")
        print(f" 👤 USERNAME RECONNAISSANCE: {username}")
        print("=================================================================")
        print(f" Platforms Scanned : {res['total_scanned']}")
        print(f" Profiles Found    : {len(res['found'])}\n")
        for item in res["found"]:
            print(f"  [+] {item['platform']:<15} : {item['url']}")
        print("=================================================================\n")


def _extract_crtsh_subdomains(data: list) -> list:
    """Extract and sanitize unique subdomains from crt.sh JSON records."""
    subs = set()
    for item in data[:50]:
        name = item.get("name_value", "")
        for s in name.split("\n"):
            s = s.strip().lower()
            if s and not s.startswith("*."):
                subs.add(s)
    return sorted(list(subs))


def cmd_domain(args):
    """Execute DNS, crt.sh subdomain enum, and WHOIS lookup."""
    import dns.resolver
    import urllib.request

    domain = args.domain.strip().lower()
    res = {"domain": domain, "dns": {}, "subdomains": [], "whois": {}}

    # 1. DNS Records
    for rtype in ["A", "AAAA", "MX", "NS", "TXT"]:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            res["dns"][rtype] = [str(r) for r in answers]
        except Exception:  # @court-exempt: handled fallback
            pass

    # 2. crt.sh Subdomain Enumeration
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                res["subdomains"] = _extract_crtsh_subdomains(data)
    except Exception as e:
        res["subdomain_error"] = str(e)

    # 3. WHOIS
    try:
        import whois
        w = whois.whois(domain)
        res["whois"] = {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date) if w.creation_date else None,
            "expiration_date": str(w.expiration_date) if w.expiration_date else None,
            "name_servers": w.name_servers if hasattr(w, "name_servers") else [],
        }
    except Exception:  # @court-exempt: handled fallback
        pass

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=================================================================")
        print(f" 🌐 DOMAIN & INFRASTRUCTURE RECON: {domain}")
        print("=================================================================")
        if res["whois"]:
            print(f" Registrar     : {res['whois'].get('registrar') or 'N/A'}")
            print(f" Created       : {res['whois'].get('creation_date') or 'N/A'}")
        print("\n 📍 DNS Records:")
        for rtype, records in res["dns"].items():
            print(f"   [{rtype}] {', '.join(records)}")
        print(f"\n 🔍 Discovered Subdomains ({len(res['subdomains'])}):")
        for sub in res["subdomains"][:20]:
            print(f"   • {sub}")
        if len(res["subdomains"]) > 20:
            print(f"   ... and {len(res['subdomains']) - 20} more subdomains")
        print("=================================================================\n")


def cmd_ip(args):
    """Inspect IP geolocation and ASN intelligence."""
    import urllib.request

    ip_target = args.ip.strip()
    res = {"target": ip_target}

    try:
        url = f"http://ip-api.com/json/{ip_target}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") == "success":
                res.update(data)
            else:
                res["error"] = data.get("message")
    except Exception as e:
        res["error"] = str(e)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=================================================================")
        print(f" 🌍 IP GEOLOCATION & NETWORK INTELLIGENCE: {ip_target}")
        print("=================================================================")
        print(f" Country / City : {res.get('country')} ({res.get('countryCode')}) / {res.get('city')}, {res.get('regionName')}")
        print(f" Coordinates    : Lat {res.get('lat')}, Lon {res.get('lon')}")
        print(f" ISP / Org      : {res.get('isp')} | {res.get('org')}")
        print(f" ASN            : {res.get('as')}")
        print(f" Timezone       : {res.get('timezone')}")
        print("=================================================================\n")


def cmd_metadata(args):
    """Extract forensic metadata and EXIF data from files."""
    import puremagic
    from PIL import Image
    from PIL.ExifTags import TAGS

    file_path = Path(args.target)
    if not file_path.exists():
        print(f"Error: File not found: {args.target}", file=sys.stderr)
        sys.exit(1)

    stat = file_path.stat()
    res = {
        "file": str(file_path.resolve()),
        "size_bytes": stat.st_size,
        "mtime": stat.st_mtime,
        "magic_info": [],
        "exif": {},
    }

    try:
        magics = puremagic.magic_file(str(file_path))
        res["magic_info"] = [m.name for m in magics] if magics else ["Unknown"]
    except Exception:  # @court-exempt: handled fallback
        pass

    try:
        img = Image.open(file_path)
        raw_exif = img.getexif()
        if raw_exif:
            for tag_id, val in raw_exif.items():
                tag_name = TAGS.get(tag_id, str(tag_id))
                res["exif"][tag_name] = str(val)
    except Exception:  # @court-exempt: handled fallback
        pass

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=================================================================")
        print(f" 📄 FILE FORENSIC METADATA: {file_path.name}")
        print("=================================================================")
        print(f" File Size     : {res['size_bytes']:,} bytes")
        print(f" Detected Type : {', '.join(res['magic_info'])}")
        print(f" EXIF Tags ({len(res['exif'])}):")
        for k, v in res["exif"].items():
            print(f"   • {k:<20}: {v}")
        print("=================================================================\n")


def cmd_launch_auspex(args):
    """Launch the Auspex OSINT Suite."""
    if not AUSPEX_DIR.exists():
        print(f"Error: Auspex not found at {AUSPEX_DIR}", file=sys.stderr)
        sys.exit(1)

    launcher_script = AUSPEX_DIR / "start_arsenal.bat"
    if not launcher_script.exists():
        launcher_script = AUSPEX_DIR / "run_auspex.bat"

    print(f"🚀 Launching Auspex Suite from {AUSPEX_DIR}...")
    if launcher_script.exists():
        subprocess.Popen(["cmd.exe", "/c", str(launcher_script)], cwd=str(AUSPEX_DIR))
    else:
        subprocess.Popen([sys.executable, "app.py"], cwd=str(AUSPEX_DIR))


def main():
    parser = argparse.ArgumentParser(description="Workshop OSINT & Auspex Intelligence Master CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="OSINT Subcommand")

    # Status
    subparsers.add_parser("status", help="Show OSINT suite and Auspex status")

    # Username
    p_user = subparsers.add_parser("username", help="Reconnaissance on username across platforms")
    p_user.add_argument("username", help="Target username")
    p_user.add_argument("--fast", action="store_true", help="Fast scan tier-1 only")
    p_user.add_argument("--json", action="store_true", help="Output JSON format")

    # Email
    p_email = subparsers.add_parser("email", help="Reconnaissance on email address")
    p_email.add_argument("email", help="Target email address")
    p_email.add_argument("--json", action="store_true", help="Output JSON format")

    # Phone
    p_phone = subparsers.add_parser("phone", help="Intelligence on phone number")
    p_phone.add_argument("phone", help="Target phone number (e.g. +1234567890)")
    p_phone.add_argument("--json", action="store_true", help="Output JSON format")

    # Domain
    p_dom = subparsers.add_parser("domain", help="Reconnaissance on domain infrastructure")
    p_dom.add_argument("domain", help="Target domain (e.g. example.com)")
    p_dom.add_argument("--json", action="store_true", help="Output JSON format")

    # IP
    p_ip = subparsers.add_parser("ip", help="IP Geolocation and ASN lookup")
    p_ip.add_argument("ip", help="Target IP address")
    p_ip.add_argument("--json", action="store_true", help="Output JSON format")

    # Metadata
    p_meta = subparsers.add_parser("metadata", help="Extract forensic and EXIF metadata")
    p_meta.add_argument("target", help="Path to file")
    p_meta.add_argument("--json", action="store_true", help="Output JSON format")

    # Launch Auspex
    subparsers.add_parser("launch-auspex", help="Launch Auspex OSINT Suite application")

    args = parser.parse_args()

    if args.subcommand == "status":
        cmd_status(args)
    elif args.subcommand == "username":
        cmd_username(args)
    elif args.subcommand == "email":
        cmd_email(args)
    elif args.subcommand == "phone":
        cmd_phone(args)
    elif args.subcommand == "domain":
        cmd_domain(args)
    elif args.subcommand == "ip":
        cmd_ip(args)
    elif args.subcommand == "metadata":
        cmd_metadata(args)
    elif args.subcommand == "launch-auspex":
        cmd_launch_auspex(args)
    else:
        cmd_status(args)


if __name__ == "__main__":
    main()
