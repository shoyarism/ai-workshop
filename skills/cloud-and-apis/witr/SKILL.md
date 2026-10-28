---
name: witr
description: >
  "Why is this running?" Trace any process, port, container, or file back to what started it.
  CLI + TUI. Use for debugging, incident response, system investigation.
  Reference: https://github.com/pranshuparmar/witr
---

# witr — Why Is This Running?

Trace any process, port, container, or file back to the exact chain that started it.

## Installation

```bash
# Unix (Linux, macOS)
curl -fsSL https://raw.githubusercontent.com/pranshuparmar/witr/main/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/pranshuparmar/witr/main/install.ps1 | iex

# Package managers
brew install witr
npm install -g @pranshuparmar/witr
winget install PranshuParmar.witr
```

## Quick Commands

```bash
# Interactive TUI
witr

# Query by process name
witr node
witr nginx

# Query by port
witr --port 5000

# Query by PID
witr --pid 1234

# Query by file
witr --file /var/lib/dpkg/lock

# Query by container
witr --container redis

# JSON output for automation
witr node --json

# Tree view of ancestry
witr --pid 14233 --tree

# Short output
witr --port 5000 --short
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean: process found, no warnings |
| 1 | Warnings: process found but has issues |
| 2 | Not found: no matching process |
| 3 | Permission denied |
| 4 | Invalid input |
| 5 | Internal error |

## Platform Support

- **Linux**: Full support via /proc
- **macOS**: ps, lsof, sysctl
- **Windows**: Win32 APIs (ToolHelp32, PSAPI)
- **FreeBSD**: procstat, ps, lsof

## TUI Features

- Processes tab: live sortable list with ancestry
- Ports tab: listening ports with owning processes
- Containers tab: Docker, Podman, K8s, LXC
- Locks tab: file locks (Linux/macOS)
- Process actions: kill, terminate, pause, resume
