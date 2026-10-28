---
source: "https://github.com/larksuite/cli"
name: larksuite-cli
description: "Use when the user wants to interact with Lark/Feishu via CLI — Messenger, Docs, Base, Sheets, Slides, Calendar, Mail, Tasks, Meetings, and more. Official CLI with 200+ commands and 26 AI Agent Skills. Triggers: 'lark CLI', 'feishu CLI', 'larksuite', 'Lark automation', '飞书 CLI'."
risk: unknown
---

# Lark/Feishu CLI (lark-cli)

[GitHub](https://github.com/larksuite/cli) · ⭐ 16,905 · Go · MIT

The official Lark/飞书 CLI tool, maintained by the larksuite team — built for humans and AI Agents. Covers core business domains including Messenger, Docs, Base, Sheets, Slides, Calendar, Mail, Tasks, Meetings, and more, with 200+ commands and 26 AI Agent Skills.

## Install

```bash
# Via npm
npm install -g @larksuite/cli

# Or download pre-built binary
# https://github.com/larksuite/cli/releases

# Verify
lark --version
```

## When to Use

- User wants to **interact with Lark/Feishu** (飞书) workspace via CLI
- User wants to **manage Lark Docs, Sheets, Slides, Base** programmatically
- User needs to **send messages via Lark Messenger**
- User wants to **create/manage Lark Calendar events**
- User needs **Lark Mail or Tasks** automation
- Use when `lark-doc`, `lark-sheets`, `lark-slides` skills are too narrow
- Triggers: 'lark CLI', 'feishu CLI', 'larksuite', 'Lark automation', '飞书'

## Authentication

```bash
# Interactive login
lark auth login

# Check auth status
lark auth status

# Use app credentials
lark auth app --app-id <app_id> --app-secret <app_secret>
```

## Command Structure

```bash
lark <domain> <action> [options]

# Domains: messenger, docs, sheets, slides, calendar, mail, tasks, meetings, base, wiki
# Actions: list, get, create, update, delete, search
```

## Messenger

```bash
# Send message
lark messenger send --to <user_id> --text "Hello from CLI"

# List conversations
lark messenger conversations list

# Get message
lark messenger messages get --conversation-id <id> --message-id <id>
```

## Docs (云文档)

```bash
# Create document
lark docs create --title "Report" --folder-id <folder_id>

# Read document
lark docs get --doc-token <token>

# Update document
lark docs update --doc-token <token> --content '<h1>Title</h1><p>Content</p>'

# List documents in folder
lark docs list --folder-id <folder_id>
```

## Sheets (多维表格)

```bash
# Create spreadsheet
lark sheets create --title "Q3 Data" --folder-id <folder_id>

# Read sheet
lark sheets get --spreadsheet-id <id> --range "Sheet1!A1:D10"

# Write sheet
lark sheets update --spreadsheet-id <id> --range "Sheet1!A1" --values '[["Name","Score"]]'

# List spreadsheets
lark sheets list --folder-id <folder_id>
```

## Slides (幻灯片)

```bash
# Create presentation
lark slides create --title "Presentation" --folder-id <folder_id>

# Get slide
lark slides get --slide-token <token>

# Update slide
lark slides update --slide-token <token> --content '...'
```

## Calendar

```bash
# Create event
lark calendar events create \
  --summary "Team Meeting" \
  --start-time "2026-09-01T10:00:00" \
  --end-time "2026-09-01T11:00:00" \
  --description "Weekly sync"

# List events
lark calendar events list --start-time "2026-09-01T00:00:00" --end-time "2026-09-01T23:59:59"
```

## Base (多维表格)

```bash
# Create base
lark base create --title "Project Tracker" --folder-id <folder_id>

# List tables
lark base tables list --app-id <app_id>

# Query records
lark base records list --app-id <app_id> --table-id <table_id>
```

## Mail

```bash
# List messages
lark mail messages list --folder INBOX --limit 10

# Send message
lark mail send --to user@example.com --subject "Hello" --body "Body"
```

## Tasks

```bash
# Create task
lark tasks create --title "Complete report" --due "2026-09-15"

# List tasks
lark tasks list --status pending

# Update task
lark tasks update --task-id <id> --status completed
```

## Meetings

```bash
# Create meeting
lark meetings create --subject "Sync" --start-time "2026-09-01T14:00:00" --duration 60

# List meetings
lark meetings list --user-id <id>
```

## 26 AI Agent Skills

The CLI ships with 26 pre-built agent skills for common workflows:

| Category | Skills |
|----------|--------|
| Docs | create, read, update, search, comment |
| Sheets | create, read, update, export, chart |
| Slides | create, read, update, present |
| Messenger | send, receive, batch, schedule |
| Calendar | create, read, update, find-time |
| Mail | send, receive, search, filter |
| Tasks | create, update, batch, remind |
| Base | create, query, update, export |
| Wiki | create, read, update, search |
| Meetings | create, join, record |

## Three-Layer Command System

```
Shortcuts (human & AI friendly)
    ↓
API Commands (platform-synced)
    ↓
Raw API (full control)
```

## Security

- **OS-native keychain** for credential storage
- **Input injection protection** on all commands
- **Terminal output sanitization** for sensitive data
- **Scope-based access** per command

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Auth fails | Ensure Lark app has required scopes enabled |
| Rate limits | Use `--retry` flag for automatic retry |
| Token expires | Run `lark auth login` to re-authenticate |
| Chinese UI | Set `LC_ALL=zh_CN.UTF-8` for Chinese output |

## Resources

- **GitHub**: https://github.com/larksuite/cli
- **npm**: https://www.npmjs.com/package/@larksuite/cli
- **Releases**: https://github.com/larksuite/cli/releases
