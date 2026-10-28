---
name: live-browser-agent
description: Autonomous browser navigation and task execution with real-time live stream observation on localhost:7860. Supports Chromium, Firefox, WebKit, remote CDP attachment, and user profile mounting. Use when the user asks to browse websites, inspect web apps, or connect to their browser.
---

# Live Browser Agent Skill

This skill guides agents in running autonomous browser automation tasks while providing a real-time live visual feed for the user to watch on `http://localhost:7860`.

## 1. Quick Start / Running Browser Tasks

When the user asks to interact with a web page, perform web scraping, test a frontend app, or watch an agent browse:

```bash
# 1. Start the Live Browser Hub (if not already active)
python scripts/live_browser_hub.py --port 7860 &

# 2. Run the Autonomous Browser Agent with live streaming
python scripts/run_browser_agent.py --url "https://example.com" --task "Inspect pricing plans" --live

# Or via the Workshop master CLI:
python scripts/workshop.py browser --url "https://example.com" --task "Inspect pricing plans"
```

## 2. Multi-Engine & Existing Browser Integration

The agent runner supports connecting to running browsers and mounting existing user profiles:

### A. Targeting Specific Browser Engines (Firefox / WebKit)
```bash
# Target Firefox engine directly
python scripts/workshop.py browser --url "https://huggingface.co" --browser firefox

# Target Chromium engine (default)
python scripts/workshop.py browser --url "https://huggingface.co" --browser chromium
```

### B. Attaching to an Existing Running User Browser (CDP)
When the user wants the agent to inspect or interact with their running browser instance:
1. Start Chrome/Edge/Brave with remote debugging enabled:
   ```bash
   chrome.exe --remote-debugging-port=9222
   ```
2. Attach the agent directly:
   ```bash
   python scripts/workshop.py browser --cdp "http://localhost:9222" --task "Analyze active tab"
   ```

### C. Mounting Existing User Profiles (Persistent Context)
To inherit logged-in sessions, cookies, and extensions without credential prompts:
```bash
# Point to existing Firefox or Chrome user profile directory
python scripts/workshop.py browser --url "https://internal-app.com" --profile "C:/Users/<User>/AppData/Roaming/Mozilla/Firefox/Profiles/<profile-id>"
```

## 3. OS Architecture Invariant: Windows Display Surface Boundaries
- When AI agents execute in non-interactive background sessions (e.g. background tasks or service contexts), Windows GDI security restricts `BitBlt` and desktop screen grabbing of `WinSta0\Default` (interactive user display).
- **The Ground-Truth Solution**: Never rely on raw OS desktop window coordinate clicking for web apps. Always use Playwright protocol-level automation (`workshop.py browser`), CDP connection, or headless streaming to the Live Browser Hub (:7860).

## 4. Live Watching Dashboard
Always notify the user of the live dashboard:
- **Dashboard URL**: `http://localhost:7860`
- Provides real-time page snapshots, action logs, navigation history, and manual takeover controls.
