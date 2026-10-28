---
name: scrapling-fast-scraper
description: High-speed, undetectable web scraping in Python using Scrapling. Features intelligent DOM traversal, stealth browser fingerprinting, CSS/XPath querying, and markdown conversion.
---

# Scrapling Web Scraping Engine

Scrapling is an undetectable, ultra-fast Python web scraper and DOM crawler that operates up to 700x faster than traditional BeautifulSoup/Selenium setups. It features intelligent fingerprint masking, adaptive CSS/XPath selection, dynamic JavaScript rendering, and direct LLM-ready markdown extraction.

## Key Capabilities
1. **Undetectable Fetching**: Built-in HTTP and headless browser engines that bypass anti-bot challenges (Cloudflare, Akamai, Datadome).
2. **Lightning Fast DOM Parser**: Highly optimized C/Rust-backed HTML parser with fluid XPath and CSS query chains.
3. **Adaptive Auto-Selector**: Elements are tracked across layout changes and responsive design shifts.
4. **Structured Data Extraction**: Direct export to JSON, Pandas DataFrames, or LLM-clean Markdown.

## Python Usage Patterns
`python
from scrapling import Fetcher, StealthFetcher

# Fast static fetch
fetcher = Fetcher(headless=True)
page = fetcher.get('https://news.ycombinator.com')
titles = page.css('span.titleline > a::text').get_all()

# Stealth JavaScript fetch
with StealthFetcher() as session:
    page = session.get('https://example.com/spa')
    md = page.to_markdown()
`
