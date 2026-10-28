#!/usr/bin/env python3
"""
FreeLLMAPI Credential Migration Script
---------------------------------------
Migrates API keys from OmniRoute encrypted storage to FreeLLMAPI.

Usage:
    python migrate_keys_to_freellm.py

Prerequisites:
    - Python 3.11+ with `cryptography` package
    - OmniRoute export: ./Backup/omniroute/exports/providers_and_accounts.json
    - OmniRoute .env with STORAGE_ENCRYPTION_KEY
    - FreeLLMAPI running or stopped (both work)
"""

import os
import binascii
import json
import hashlib
import sqlite3
import datetime
import shutil
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_omni_key(secret_hex: str) -> bytes:
    """Derive OmniRoute AES key using scrypt with static salt."""
    static_salt = b"omniroute-field-encryption-v1"
    return hashlib.scrypt(
        secret_hex.encode("utf-8"),
        salt=static_salt,
        n=16384,
        r=8,
        p=1,
        dklen=32
    )


def decrypt_omni(ciphertext_str: str, omni_key: bytes) -> str | None:
    """Decrypt an OmniRoute encrypted API key."""
    parts = ciphertext_str.split(":")
    if len(parts) != 5 or parts[0] != "enc" or parts[1] != "v1":
        return ciphertext_str  # not encrypted

    iv = binascii.unhexlify(parts[2])
    ct = binascii.unhexlify(parts[3])
    tag = binascii.unhexlify(parts[4])

    aesgcm = AESGCM(omni_key)
    try:
        return aesgcm.decrypt(iv, ct + tag, None).decode("utf-8")
    except Exception as e:
        print(f"[!] Decryption error: {e}")
        return None


def encrypt_freellm(plaintext_str: str, freellm_key: bytes) -> dict:
    """Encrypt a plaintext API key using FreeLLMAPI's AES-256-GCM."""
    iv = os.urandom(16)
    aesgcm = AESGCM(freellm_key)
    ct_tag = aesgcm.encrypt(iv, plaintext_str.encode("utf-8"), None)
    ciphertext = ct_tag[:-16]
    tag = ct_tag[-16:]

    return {
        "encrypted": binascii.hexlify(ciphertext).decode("ascii"),
        "iv": binascii.hexlify(iv).decode("ascii"),
        "auth_tag": binascii.hexlify(tag).decode("ascii")
    }


def main():
    print("=" * 60)
    print("  FreeLLMAPI Credential Migration Script")
    print("=" * 60)

    # Paths
    backup_root = Path(r".\Backup")
    omni_env_path = backup_root / "omniroute" / ".env"
    omni_exports_path = backup_root / "omniroute" / "exports" / "providers_and_accounts.json"
    freellm_key_path = Path.home() / "AppData" / "Roaming" / "FreeLLMAPI" / ".encryption-key"
    freellm_db_path = Path.home() / "AppData" / "Roaming" / "FreeLLMAPI" / "freeapi.db"

    # 1. Read OmniRoute STORAGE_ENCRYPTION_KEY
    print("\n[1] Reading OmniRoute encryption key...")
    omni_secret = None
    with open(omni_env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("STORAGE_ENCRYPTION_KEY="):
                omni_secret = line.split("=", 1)[1].strip()
                break

    if not omni_secret:
        print("[!] Error: OmniRoute STORAGE_ENCRYPTION_KEY not found in .env")
        return

    omni_key = derive_omni_key(omni_secret)
    print("[OK] Derived OmniRoute encryption key")

    # 2. Read FreeLLMAPI encryption key
    print("\n[2] Reading FreeLLMAPI encryption key...")
    if not freellm_key_path.exists():
        print("[!] Error: FreeLLMAPI .encryption-key not found")
        return

    with open(freellm_key_path, "r", encoding="utf-8") as f:
        freellm_key_hex = f.read().strip()
    freellm_key = binascii.unhexlify(freellm_key_hex)
    print("[OK] Read FreeLLMAPI encryption key")

    # 3. Load OmniRoute exports
    print("\n[3] Loading OmniRoute provider connections...")
    if not omni_exports_path.exists():
        print("[!] Error: OmniRoute exports not found")
        return

    with open(omni_exports_path, "r", encoding="utf-8") as f:
        conns = json.load(f)
    print(f"[OK] Loaded {len(conns)} provider connections")

    # 4. Platform mapping (OmniRoute -> FreeLLMAPI)
    PLATFORM_MAP = {
        "agnes": "agnes",
        "aion": "aion",
        "bazaarlink": "bazaarlink",
        "cloudflare-ai": "cloudflare",
        "cohere": "cohere",
        "gemini": "google",
        "groq": "groq",
        "kilo-gateway": "kilo",
        "llm7": "llm7",
        "mistral": "mistral",
        "nvidia": "nvidia",
        "ollama": "ollama",
        "openai": "google",  # OpenAI models available via Google AI Studio
        "opencode-go": "opencode",
        "openrouter": "openrouter",
        "vertex-partner": "google",
    }

    # 5. Safety backup
    print("\n[4] Creating safety backup...")
    if freellm_db_path.exists():
        backup_db = freellm_db_path.parent / "freeapi.db.bak"
        shutil.copy2(freellm_db_path, backup_db)
        print(f"[OK] Backup created: {backup_db.name}")
    else:
        print("[!] Warning: FreeLLMAPI database not found")
        return

    # 6. Connect and migrate
    print("\n[5] Migrating keys...")
    conn = sqlite3.connect(str(freellm_db_path))
    cur = conn.cursor()

    imported = []
    skipped = []

    for c in conns:
        provider = c.get("provider")
        mapped_platform = PLATFORM_MAP.get(provider)

        if not mapped_platform:
            skipped.append({"provider": provider, "reason": "no_mapping"})
            continue

        if c.get("auth_type") != "apikey" or c.get("is_active") != 1:
            skipped.append({"provider": provider, "reason": "not_apikey_or_inactive"})
            continue

        api_key_enc = c.get("api_key")
        if not api_key_enc:
            skipped.append({"provider": provider, "reason": "no_api_key"})
            continue

        try:
            plaintext = decrypt_omni(api_key_enc, omni_key)
            if not plaintext:
                skipped.append({"provider": provider, "reason": "decrypt_failed"})
                continue

            enc_info = encrypt_freellm(plaintext, freellm_key)
            label = c.get("name") or "main"

            # Check if exists
            cur.execute(
                "SELECT id FROM api_keys WHERE platform = ? AND label = ?",
                (mapped_platform, label)
            )
            existing = cur.fetchone()

            if existing:
                cur.execute(
                    """
                    UPDATE api_keys
                    SET encrypted_key = ?, iv = ?, auth_tag = ?, status = 'healthy', enabled = 1
                    WHERE id = ?
                    """,
                    (enc_info["encrypted"], enc_info["iv"], enc_info["auth_tag"], existing[0])
                )
                action = "Updated"
            else:
                cur.execute(
                    """
                    INSERT INTO api_keys (platform, label, encrypted_key, iv, auth_tag, status, enabled, created_at)
                    VALUES (?, ?, ?, ?, ?, 'healthy', 1, datetime('now'))
                    """,
                    (mapped_platform, label, enc_info["encrypted"], enc_info["iv"], enc_info["auth_tag"])
                )
                action = "Inserted"

            imported.append({
                "provider": provider,
                "platform": mapped_platform,
                "label": label,
                "action": action
            })

        except Exception as e:
            skipped.append({"provider": provider, "reason": f"error: {e}"})

    conn.commit()
    conn.close()

    # 7. Summary
    print("\n" + "=" * 60)
    print(f"  Migration Complete!")
    print(f"  Imported: {len(imported)} keys")
    print(f"  Skipped:  {len(skipped)} connections")
    print("=" * 60)

    if imported:
        print("\nImported platforms:")
        platforms = sorted(set(i["platform"] for i in imported))
        for p in platforms:
            count = sum(1 for i in imported if i["platform"] == p)
            print(f"  - {p} ({count} key{'s' if count > 1 else ''})")

    if skipped:
        print("\nSkipped connections:")
        for s in skipped:
            print(f"  - {s['provider']}: {s['reason']}")

    print(f"\n[OK] FreeLLMAPI is now configured with {len(imported)} provider keys.")
    print("[OK] Restart FreeLLMAPI to activate keys.")


if __name__ == "__main__":
    main()
