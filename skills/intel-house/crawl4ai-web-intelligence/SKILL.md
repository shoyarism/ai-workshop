---
name: crawl4ai-web-intelligence
description: High-speed, LLM-friendly asynchronous web crawling, heuristic markdown extraction, and structured scraping with Crawl4AI.
---

# Crawl4AI Web Intelligence & Extraction

Crawl4AI is an open-source, LLM-friendly asynchronous web crawler engineered specifically for generative AI pipelines and autonomous agents.

## Features
- Blazing-fast asynchronous crawling with Playwright/Patchright backend
- Automated heuristic extraction converting complex HTML to clean Markdown
- Media, link, and metadata extraction
- Support for dynamic JavaScript rendering, infinite scroll, and session persistence

## Usage Pattern

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def extract_markdown(url: str):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        print("Markdown Output:")
        print(result.markdown[:500])
        return result.markdown

if __name__ == "__main__":
    asyncio.run(extract_markdown("https://example.com"))
```

## CLI Execution
```powershell
uv run python -c "import asyncio; from crawl4ai import AsyncWebCrawler; asyncio.run(AsyncWebCrawler().arun('https://example.com'))"
```
