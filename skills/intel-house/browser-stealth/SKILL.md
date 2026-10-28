---
name: browser-stealth
description: Stealth browser automation using Playwright + playwright-stealth. Anti-detect fingerprint masking, bot detection evasion, and undetected browser control.
version: 0.1.0
author: Workshop Collection, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [browser, stealth, anti-detect, playwright, fingerprint-masking]
    related_skills: [browser-automation, computer-use, dogfood]
---

# Browser Stealth

Undetected, anti-fingerprint browser automation using Playwright + `playwright-stealth`. Replaces camofox-browser for stealth web interaction without a separate stealth browser binary.

## When to Use

- Websites block headless browsers or detect automation fingerprints.
- Need to bypass Cloudflare, Datadome, PerimeterX, or similar bot detection.
- Scrape sites that serve different content to bots vs real browsers.
- Test anti-bot defenses on sites you own.

Do NOT use for:
- Credential stuffing, spam, or bypassing paid access controls.
- Activities violating a site's Terms of Service.

## Architecture

```
playwright-stealth patches Playwright's fingerprint signals:
  - webgl.vendor / renderer
  - navigator.plugins, languages, hardwareConcurrency
  - chrome.runtime (missed by stealth)
  - canvas noise, audio fingerprint
  - headless chrome detection flags
```

## Dependencies

```bash
uv pip install playwright playwright-stealth
playwright install chromium
```

## Quick Start

```python
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async

async with sync_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    await stealth_async(page)
    await page.goto("https://bot.sannysoft.com")
    # Fingerprint now appears as real Chrome
    await browser.close()
```

## Anti-Detection Checklist

| Signal | Status |
|---|---|
| WebGL vendor/renderer | ✅ Masked |
| Navigator plugins/languages | ✅ Spoofed |
| Canvas fingerprint noise | ✅ Added |
| AudioContext fingerprint | ✅ Noise |
| Headless chrome flags | ✅ Removed |
| chrome.runtime.messaging | ✅ Patched |
| Request interception | ✅ Hidden |

## Verification

Run fingerprint check after stealth:
```python
await page.goto("https://bot.sannysoft.com")
fingerprint = await page.evaluate("""() => ({
  webgl: document.getElementById('webgl').textContent,
  plugins: navigator.plugins.length,
  languages: navigator.languages
})""")
assert fingerprint['plugins'] > 0, "Still detected as headless"
```

## Notes

- Works with Chromium only (not Firefox/WebKit for stealth patches).
- `playwright-stealth` v2.x for Playwright v1.6x compatibility.
- Combine with `browser-automation` skill for full workflow control.
