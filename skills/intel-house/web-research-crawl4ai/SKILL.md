---
name: web-research-crawl4ai
description: Web research and page extraction using crawl4ai + duckduckgo_search. Replaces Firecrawl with fully local, self-hosted scraping and LLM extraction.
version: 0.1.0
author: Workshop Collection, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web-research, crawl4ai, scraping, extraction, local]
    related_skills: [deep-research, browser-automation, grounded-citations]
---

# Web Research with crawl4ai

Self-hosted web research pipeline using `crawl4ai` for page extraction and `duckduckgo_search` for search. Replaces Firecrawl — no API key needed, fully local.

## When to Use

- Need web page content without an external API key.
- Research tasks requiring LLM-friendly markdown extraction.
- Scrape structured data from public websites.
- Multi-source synthesis with local processing.

Do NOT use for:
- Bypassing paywalls or access controls.
- High-volume scraping that violates site terms.

## Architecture

```
duckduckgo_search  →  Discover URLs
        ↓
crawl4ai          →  Extract clean markdown/HTML
        ↓
LLM synthesis     →  Structured report
```

## Dependencies

```bash
uv pip install crawl4ai duckduckgo_search beautifulsoup4 lxml
```

## Search → Extract Pipeline

```python
from ddgs import DDGS
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, ReadabilityExtractionStrategy

# Step 1: Search
with DDGS() as ddgs:
    results = list(ddgs.text("AI code assistant 2026", max_results=10))
urls = [r['href'] for r in results]

# Step 2: Crawl
async with AsyncWebCrawler() as crawler:
    tasks = [crawler.arun(url=url, config=CrawlerRunConfig(
        extraction_strategy=ReadabilityExtractionStrategy(),
        word_count_threshold=100
    )) for url in urls]
    results = await asyncio.gather(*tasks)

# Step 3: Process
for r in results:
    if r.success:
        print(f"URL: {r.url}")
        print(f"Markdown: {r.markdown[:2000]}")
```

## Extraction Strategies

| Strategy | Use Case |
|---|---|
| `ReadabilityScriptlet` | Article content (default) |
| `JsonCssExtractionStrategy` | Structured data via CSS selectors |
| `LlamaParseExtractionStrategy` | PDF/document parsing (if llama-index installed) |
| `RegexExtractionStrategy` | Pattern-based field extraction |

## Quality Rules

1. Always verify URL accessibility before crawling (timeout 30s).
2. Respect `robots.txt` — check before bulk crawling.
3. Rate-limit: max 1 request/second to same domain.
4. Cross-reference ≥3 sources for factual claims.
5. Flag unverified claims explicitly.

## Comparison: crawl4ai vs Firecrawl

| Feature | crawl4ai | Firecrawl |
|---|---|---|
| API key required | ❌ No | ✅ Yes |
| Local execution | ✅ Yes | ❌ Cloud only |
| Markdown extraction | ✅ Excellent | ✅ Excellent |
| PDF support | ✅ Yes | ✅ Yes |
| Batch crawling | ✅ Async | ✅ Batch API |
| Speed | Fast (local) | Medium (network) |
| Reliability | Depends on target | Managed infrastructure |

## Verification

```python
# Test crawl4ai on a known page
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")
    assert result.success, "Crawl failed"
    assert len(result.markdown) > 100, "Empty extraction"
    print("✅ crawl4ai operational")
```
