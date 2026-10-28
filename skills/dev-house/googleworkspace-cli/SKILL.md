---
source: "https://github.com/googleworkspace/cli"
name: googleworkspace-cli
description: "Use when the user wants to interact with Google Workspace via CLI — Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more. One CLI tool built from Google's Discovery Service with 40+ AI agent skills. Triggers: 'Google Workspace CLI', 'gws', 'google drive CLI', 'google sheets CLI', 'google calendar CLI', 'gws CLI'."
risk: unknown
---

# Google Workspace CLI (gws)

[GitHub](https://github.com/googleworkspace/cli) · ⭐ 30,671 · Rust · Apache-2.0

One CLI for all of Google Workspace — built for humans and AI agents. Drive, Gmail, Calendar, and every Workspace API. Zero boilerplate. Structured JSON output. 40+ agent skills included.

## Install

```bash
# Download pre-built binary from releases
# https://github.com/googleworkspace/cli/releases

# Or via npm
npm install -g @googleworkspace/cli

# Verify installation
gws --version
```

## When to Use

- User wants to **manage Google Drive** files/folders via CLI
- User wants to **read/send Gmail** messages
- User wants to **create/manage Calendar events**
- User wants to **read/write Google Sheets**
- User wants to **create/edit Google Docs**
- User wants to **use Google Chat** for notifications
- User mentions `gws`, Google Workspace CLI, or needs to automate Google services
- Use instead of `google-docs` / `google-sheets` skills when CLI is preferred over API

## Authentication

```bash
# Interactive OAuth login
gws auth login

# Check current auth status
gws auth status

# List available scopes
gws auth scopes list
```

## Commands Overview

```bash
# Core commands
gws --help
gws auth --help
gws drive --help
gws gmail --help
gws calendar --help
gws sheets --help
gws docs --help
gws chat --help
gws admin --help
```

## Google Drive

```bash
# List files
gws drive files list --query "trashed=false" --format json

# Upload file
gws drive files upload --name "report.pdf" --path ./report.pdf

# Download file
gws drive files download --id <file-id> --output ./report.pdf

# Create folder
gws drive files create --name "My Folder" --mime-type application/vnd.google-apps.folder

# Search files
gws drive files list --query 'name contains "quarterly" and mimeType contains "document"'
```

## Gmail

```bash
# List emails
gws gmail messages list --labelId INBOX --max-results 10

# Read email
gws gmail messages get --id <message-id> --format full

# Send email
gws gmail messages send --to user@example.com --subject "Hello" --body "Message body"

# Search emails
gws gmail messages list --query "from:boss is:unread"
```

## Calendar

```bash
# List calendars
gws calendar calendars list

# Create event
gws calendar events create \
  --calendar-id primary \
  --summary "Team Meeting" \
  --start "2026-09-01T10:00:00" \
  --end "2026-09-01T11:00:00" \
  --description "Weekly sync"

# List events
gws calendar events list --calendar-id primary --time-min "2026-09-01T00:00:00" --time-max "2026-09-01T23:59:59"
```

## Google Sheets

```bash
# Create spreadsheet
gws sheets spreadsheets create --title "Q3 Report"

# Read data
gws sheets values get --spreadsheet-id <id> --range "Sheet1!A1:D10"

# Write data
gws sheets values update --spreadsheet-id <id> --range "Sheet1!A1" --values [["Name","Score"],["Alice",95]]

# Append rows
gws sheets values append --spreadsheet-id <id> --range "Sheet1" --values [["New Row","Data"]]
```

## Google Docs

```bash
# Create document
gws docs documents create --title "Report"

# Append content
gws docs documents batches update \
  --document-id <id> \
  --requests '[{"insertText":{"location":{"index":1},"text":"Hello World"}}]'

# Get content
gws docs documents get --document-id <id>
```

## AI Agent Skills

`gws` ships with **40+ pre-built AI agent skills** for common workflows:

| Skill Category | Skills |
|---------------|--------|
| Drive | file search, upload, download, folder management |
| Gmail | inbox triage, send, search, label management |
| Calendar | event creation, scheduling, availability check |
| Sheets | data export, dashboard creation, formula generation |
| Docs | report generation, template filling, content extraction |
| Chat | notifications, bot integration, message scheduling |
| Admin | user management, group operations, audit logs |

## Dynamic Command Generation

Unlike static CLIs, `gws` reads Google's [Discovery Service](https://developers.google.com/discovery) at runtime and builds commands dynamically. When Google adds new APIs, `gws` picks them up automatically.

```bash
# List all available services
gws services list

# Explore available methods for a service
gws drive files list --help
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Authentication error |
| 3 | Permission denied |
| 4 | Rate limit exceeded |
| 5 | Network error |

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Auth expires | Run `gws auth login` to refresh |
| Rate limits | Add `--retry` flag for automatic retry |
| Large exports | Use `--format json` and pipe to `jq` |
| Scoped access | Ensure OAuth scopes cover the API you need |

## Resources

- **GitHub**: https://github.com/googleworkspace/cli
- **npm**: https://www.npmjs.com/package/@googleworkspace/cli
- **Releases**: https://github.com/googleworkspace/cli/releases
