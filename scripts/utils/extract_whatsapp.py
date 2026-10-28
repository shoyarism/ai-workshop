#!/usr/bin/env python3
"""Extract WhatsApp messages from backupInfo.db to CSV and JSON, generate summary."""

import sqlite3
import csv
import json
import os
from datetime import datetime, timezone

DB_PATH = r'D:/temp/Panfone WhatsApp Transfer/Gitartna ❤️/WhatsApp/backupInfo.db'
OUTPUT_DIR = r'./Backup'

# Connect to database
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ============================================================
# 1. Extract all messages
# ============================================================
print("Extracting messages...")
cursor.execute("""
    SELECT _id, uuid, datasource, chatid, opt,
           childmessagesdeliveredcount, childmessagesplayedcount, childmessagesreadcount,
           dataitemversion, filteredrecipientcount, flags, groupeventtype,
           isfromme, errorstatus, status, type, spotlightstatus, isstarred,
           groupmemberjid, lastchat, parentmessage, date, sentdate,
           fromjid, mediasectionid, phash, pushname, stanzaid, text,
           tojid, itemopt, filesize, mediaorigin, movieduration, aspectratio,
           haccuracy, latitude, longitude, mediaurldate, authorname,
           collectionname, medialocalpath, mediaurl, title, vcardname,
           vcardstring, xmppthumbpath, mediakey, metadata, dataitemopt,
           ownsthumbnail, dataitemtype, dataitemdate, content1, content2,
           matchedtext, sectionid, senderjid, summary, dataitemthumbailpath,
           dataitemtitle, infoopt, receiptinfo, localpath, thumbnaillocalpath,
           dataitemthumbnaillocalpath, rawdata, thumbimage, quoteuuid,
           isdeleted, isskipped
    FROM whatsappmessage
    ORDER BY _id
""")

columns = [desc[0] for desc in cursor.description]
rows = cursor.fetchall()
total_messages = len(rows)
print(f"Total messages extracted: {total_messages}")

# ============================================================
# 2. Export to CSV
# ============================================================
csv_path = os.path.join(OUTPUT_DIR, 'whatsapp_messages.csv')
print(f"Writing CSV: {csv_path}")
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for row in rows:
        writer.writerow(dict(row))
print(f"CSV written: {os.path.getsize(csv_path):,} bytes")

# ============================================================
# 3. Export to JSON
# ============================================================
json_path = os.path.join(OUTPUT_DIR, 'whatsapp_messages.json')
print(f"Writing JSON: {json_path}")
messages = [dict(row) for row in rows]
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(messages, f, ensure_ascii=False, indent=2, default=str)
print(f"JSON written: {os.path.getsize(json_path):,} bytes")

# ============================================================
# 4. Export lightweight summary JSON
# ============================================================
# Convert timestamps for readability
def ms_to_iso(ms_val):
    if ms_val is None or ms_val <= 0:
        return None
    try:
        return datetime.fromtimestamp(ms_val / 1000, tz=timezone.utc).isoformat()
    except:
        return None

# ============================================================
# 5. Analyze chats
# ============================================================
print("Analyzing chats...")
cursor.execute("""
    SELECT _id, contactjid, partnername, type, isarchived, unreadcount,
           lastmessagedate, isremoved, isdeleted
    FROM whatsappchat ORDER BY _id
""")
chats = [dict(r) for r in cursor.fetchall()]

# Message counts per chat
cursor.execute("SELECT chatid, COUNT(*) as cnt FROM whatsappmessage GROUP BY chatid ORDER BY cnt DESC")
chat_msg_counts = {row['chatid']: row['cnt'] for row in cursor.fetchall()}

# Message type breakdown
cursor.execute("SELECT type, COUNT(*) as cnt FROM whatsappmessage GROUP BY type ORDER BY cnt DESC")
type_counts = {row['type']: row['cnt'] for row in cursor.fetchall()}

# Status breakdown
cursor.execute("SELECT status, COUNT(*) as cnt FROM whatsappmessage GROUP BY status ORDER BY cnt DESC")
status_counts = {row['status']: row['cnt'] for row in cursor.fetchall()}

# isfromme breakdown
cursor.execute("SELECT isfromme, COUNT(*) as cnt FROM whatsappmessage GROUP BY isfromme ORDER BY cnt DESC")
direction_counts = {int(row['isfromme']): row['cnt'] for row in cursor.fetchall()}

# Date range
cursor.execute("SELECT MIN(date) as min_date, MAX(date) as max_date, MIN(sentdate) as min_sent, MAX(sentdate) as max_sent FROM whatsappmessage")
date_range = cursor.fetchone()

# Media messages
cursor.execute("SELECT COUNT(*) as cnt FROM whatsappmessage WHERE mediaorigin IS NOT NULL AND mediaorigin != 0 OR medialocalpath IS NOT NULL AND medialocalpath != '' OR mediaurl IS NOT NULL AND mediaurl != ''")
media_count = cursor.fetchone()['cnt']

# Deleted messages
cursor.execute("SELECT COUNT(*) as cnt FROM whatsappmessage WHERE isdeleted = 1")
deleted_count = cursor.fetchone()['cnt']

# Top senders (by fromjid for received messages)
cursor.execute("""
    SELECT fromjid, COUNT(*) as cnt FROM whatsappmessage
    WHERE isfromme = 0 AND fromjid IS NOT NULL AND fromjid != ''
    GROUP BY fromjid ORDER BY cnt DESC LIMIT 20
""")
top_senders = [dict(r) for r in cursor.fetchall()]

# Top chats by message count
cursor.execute("""
    SELECT chatid, COUNT(*) as cnt FROM whatsappmessage
    GROUP BY chatid ORDER BY cnt DESC LIMIT 20
""")
top_chats = [dict(r) for r in cursor.fetchall()]

# Group chats
cursor.execute("SELECT COUNT(*) as cnt FROM whatsappchat WHERE type = 'group'")
group_count = cursor.fetchone()['cnt']

# Personal chats
cursor.execute("SELECT COUNT(*) as cnt FROM whatsappchat WHERE type = 'session'")
personal_count = cursor.fetchone()['cnt']

# Status updates
cursor.execute("SELECT COUNT(*) as cnt FROM whatsappchat WHERE type = 'status'")
status_chat_count = cursor.fetchone()['cnt']

# Broadcast
cursor.execute("SELECT COUNT(*) as cnt FROM whatsappchat WHERE type = 'broadcast'")
broadcast_count = cursor.fetchone()['cnt']

# ============================================================
# 6. Build summary report
# ============================================================
min_date_ms = date_range['min_date']
max_date_ms = date_range['max_date']
min_date_iso = ms_to_iso(min_date_ms)
max_date_iso = ms_to_iso(max_date_ms)

summary = {
    "source": "Panfone WhatsApp Transfer - backupInfo.db",
    "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
    "database_path": DB_PATH,
    "output_files": {
        "csv": csv_path,
        "json": json_path,
    },
    "message_statistics": {
        "total_messages": total_messages,
        "total_chats": len(chats),
        "message_type_breakdown": type_counts,
        "status_breakdown": status_counts,
        "direction_breakdown": {
            "sent (isfromme=1)": direction_counts.get(1, 0),
            "received (isfromme=0)": direction_counts.get(0, 0),
        },
        "media_messages": media_count,
        "deleted_messages": deleted_count,
        "date_range": {
            "earliest_message": min_date_iso,
            "earliest_message_ms": min_date_ms,
            "latest_message": max_date_iso,
            "latest_message_ms": max_date_ms,
        },
    },
    "chat_statistics": {
        "total_chats": len(chats),
        "personal_chats": personal_count,
        "group_chats": group_count,
        "status_updates": status_chat_count,
        "broadcast_lists": broadcast_count,
        "archived_chats": sum(1 for c in chats if c.get('isarchived')),
        "unread_chats": sum(1 for c in chats if c.get('unreadcount', 0) > 0),
        "top_chats_by_messages": [
            {**tc, "chat_info": next((c for c in chats if c['_id'] == tc['chatid']), None)}
            for tc in top_chats[:10]
        ],
    },
    "top_senders_received": top_senders[:10],
    "verification": {
        "csv_rows": total_messages + 1,  # +header
        "json_records": len(messages),
        "csv_size_bytes": os.path.getsize(csv_path),
        "json_size_bytes": os.path.getsize(json_path),
    },
}

summary_path = os.path.join(OUTPUT_DIR, 'whatsapp_message_summary.json')
with open(summary_path, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"Summary written: {summary_path}")

# Print human-readable summary
print("\n" + "="*60)
print("WHATSAPP MESSAGE EXTRACTION SUMMARY")
print("="*60)
print(f"Source DB:    {DB_PATH}")
print(f"Total Messages: {total_messages:,}")
print(f"Date Range:   {min_date_iso} → {max_date_iso}")
print()
print("--- Message Types ---")
for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {t:30s}: {c:,} ({c*100/total_messages:.1f}%)")
print()
print("--- Message Direction ---")
for d, c in sorted(direction_counts.items(), key=lambda x: -x[1]):
    label = "SENT (me)" if d == 1 else "RECEIVED"
    print(f"  {label:30s}: {c:,} ({c*100/total_messages:.1f}%)")
print()
print("--- Chat Types ---")
print(f"  Personal chats : {personal_count}")
print(f"  Group chats    : {group_count}")
print(f"  Status updates : {status_chat_count}")
print(f"  Broadcast      : {broadcast_count}")
print()
print("--- Media & Deletions ---")
print(f"  Media messages: {media_count:,}")
print(f"  Deleted msgs  : {deleted_count:,}")
print()
print("--- Output Files ---")
print(f"  CSV  : {csv_path} ({os.path.getsize(csv_path):,} bytes)")
print(f"  JSON : {json_path} ({os.path.getsize(json_path):,} bytes)")
print(f"  Summary: {summary_path}")
print("="*60)

conn.close()
