---
name: go-playwright
description: "Expert capability for robust, stealthy, and efficient browser automation using Playwright Go."
risk: safe
source: "https://github.com/playwright-community/playwright-go"
date_added: "2026-02-27"
---

# Playwright Go Automation Expert

## Overview
This skill provides a comprehensive framework for writing high-performance, production-grade browser automation scripts using `github.com/playwright-community/playwright-go`. It enforces architectural best practices (contexts over instances), robust error handling, structured logging (Zap), and advanced human-emulation techniques to bypass anti-bot systems.

## When to Use This Skill
- Use when the user asks to "scrape," "automate," or "test" a website using Go.
- Use when the target site has complex dynamic content (SPA, React, Vue) requiring a real browser.
- Use when the user mentions "stealth," "avoiding detection," "cloudflare," or "human-like" behavior.
- Use when debugging existing Playwright scripts.

## Safety & Risk
**Risk Level: 🔵 Safe**

- **Sandboxed Execution:** Browser contexts are isolated; they do not persist data to the host machine unless explicitly saved.
- **Resource Management:** Designed to close browsers and contexts via `defer` to prevent memory leaks.
- **No External State-Change:** Default behavior is read-only (scraping/testing) unless the script is explicitly designed to submit forms or modify data.

## Limitations
- **Environment Dependencies:** Requires Playwright drivers and browsers to be installed (`go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps`).
- **Resource Intensity:** Launching full browser instances (even headless) consumes significant RAM/CPU. Use single-browser/multi-context architecture.
- **Bot Detection:** While this skill includes stealth techniques, extremely strict anti-bot systems (e.g., rigorous Cloudflare settings) may still detect automation.