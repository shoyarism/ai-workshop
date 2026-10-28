---
name: desktop-automation
description: OS-level Windows desktop automation, mouse clicking, keyboard typing, hotkeys, window management, and application launching via Workshop desktop engine.
risk: low
source: workshop-arsenal
date_added: 2026-09-14
---

# Desktop Automation Engine

## Overview
The Desktop Automation Engine gives autonomous AI agents direct control over the local Windows operating system environment, including mouse positioning and clicking, text input, key combinations, window manipulation, and process launching.

---

## Capabilities & Commands

Execute from any directory using the Workshop CLI:

```bash
# 1. Screen Capture
python scripts/workshop.py desktop screenshot [output.png] [--monitor 1]

# 2. Mouse Operations
python scripts/workshop.py desktop click <x> <y> [--button left|right|middle] [--clicks 1|2]

# 3. Keyboard Input & Typing
python scripts/workshop.py desktop type "<text>" [--press enter]
python scripts/workshop.py desktop hotkey ctrl c
python scripts/workshop.py desktop hotkey alt tab
python scripts/workshop.py desktop hotkey win r

# 4. Window Management
python scripts/workshop.py desktop windows [--json]
python scripts/workshop.py desktop focus "<window_title>"

# 5. Application Launching (Detached)
python scripts/workshop.py desktop launch "notepad.exe"
python scripts/workshop.py desktop launch "code ."
```

---

## Operating Invariants & Grounding

1. **Session Awareness**:
   * Desktop operations require an interactive window station (`WinSta0\Default`).
   * When executed inside headless or non-interactive service runners, `workshop.py desktop screenshot` catches display context limits and reports them clearly without crashing.
2. **Text Input Safety**:
   * For blocks $>25$ characters or containing non-ASCII Unicode characters, input is safely piped via clipboard (`pyperclip`) to prevent dropped keystrokes.
3. **Visual Grounding**:
   * Combine `workshop.py desktop screenshot` with `workshop.py see` or OCR to visually locate UI elements and derive exact coordinate targets prior to invoking `click`.
