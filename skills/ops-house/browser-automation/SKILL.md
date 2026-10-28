---
name: browser-automation
description: Browser automation powers web testing, scraping, and AI agent
  interactions. The difference between a flaky script and a reliable system
  comes down to understanding selectors, waiting strategies, and anti-detection
  patterns.
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Browser Automation

Browser automation powers web testing, scraping, and AI agent interactions.
The difference between a flaky script and a reliable system comes down to
understanding selectors, waiting strategies, and anti-detection patterns.

This skill covers Playwright (recommended) and Puppeteer, with patterns for
testing, scraping, and agentic browser control. Key insight: Playwright won
the framework war. Unless you need Puppeteer's stealth ecosystem or are
Chrome-only, Playwright is the better choice in 2025.

Critical distinction: Testing automation (predictable apps you control) vs
scraping/agent automation (unpredictable sites that fight back). Different
problems, different solutions.

## Principles

- Use user-facing locators (getByRole, getByText) over CSS/XPath
- Never add manual waits - Playwright's auto-wait handles it
- Each test/task should be fully isolated with fresh context
- Screenshots and traces are your debugging lifeline
- Headless for CI, headed for debugging
- Anti-detection is cat-and-mouse - stay current or get blocked

## Capabilities

- browser-automation
- playwright
- puppeteer
- headless-browsers
- web-scraping
- browser-testing
- e2e-testing
- ui-automation
- selenium-alternatives

## Scope

- api-testing → backend
- load-testing → performance-thinker
- accessibility-testing → accessibility-specialist
- visual-regression-testing → ui-design

## Tooling

### Frameworks

- Playwright - When: Default choice - cross-browser, auto-waiting, best DX Note: 96% success rate, 4.5s avg execution, Microsoft-backed