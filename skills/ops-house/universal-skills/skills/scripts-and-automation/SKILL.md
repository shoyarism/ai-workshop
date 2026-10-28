---
name: scripts-and-automation
description: Use for scripts, batch files, launchers and repeatable tasks.
---

# Scripts And Automation

- Prefer one-click launchers: a .bat (Windows) or .sh that does everything, with clear messages and a pause at the end on error.
- Check prerequisites first (is the tool installed, is the folder there). Fail with a useful message.
- Use relative or clearly configurable paths. Quote paths with spaces.
- Make it safe to run twice (idempotent). Never delete without confirmation.
- Log what it does. Keep a dry-run option for anything destructive.
- Test on a copy before the real data. Document how to run it in two lines.
