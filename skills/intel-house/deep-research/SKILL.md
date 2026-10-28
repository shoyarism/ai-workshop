---
name: deep-research
description: Multi-source deep research using crawl4ai + duckduckgo_search (primary) or Firecrawl/Exa MCPs (fallback). Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when the user wants thorough research on any topic with evidence and citations.
version: 0.2.0
author: Workshop Collection, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, web-search, citations, reports, crawl4ai, duckduckgo]
    related_skills: [grounded-citations, web-research-crawl4ai]
---

# Deep Research

Produce thorough, cited research reports from multiple web sources. Primary: `crawl4ai` + `duckduckgo_search` (fully local, no API key). Fallback: Firecrawl/Exa MCPs if configured.

## When to Activate

- User asks to research any topic in depth
- Competitive analysis, technology evaluation, or market sizing
- Due diligence on companies, investors, or technologies
- Any question requiring synthesis from multiple sources
- User says "research", "deep dive", "investigate", or "what's the current state of"

## MCP / Library Requirements (priority order)

1. **crawl4ai + duckduckgo_search** (default, no API key needed)
2. **firecrawl** — `firecrawl_search`, `firecrawl_scrape`, `firecrawl_crawl`
3. **exa** — `web_search_exa`, `web_search_advanced_exa`, `crawling_exa`

Both crawl4ai + firecrawl together give the best coverage. Configure in `~/.claude.json` or `~/.codex/config.toml`.

## Workflow

### Step 1: Understand the Goal

Ask 1-2 quick clarifying questions:
- "What's your goal — learning, making a decision, or writing something?"
- "Any specific angle or depth you want?"

If the user says "just research it" — skip ahead with reasonable defaults.

### Step 2: Plan the Research

Break the topic into 3-5 research sub-questions. Example:
- Topic: "Impact of AI on healthcare"
  - What are the main AI applications in healthcare today?
  - What clinical outcomes have been measured?
  - What are the regulatory challenges?
  - What companies are leading this space?
  - What's the market size and growth trajectory?

### Step 3: Execute Multi-Source Search (crawl4ai + ddg primary)

For EACH sub-question, search then crawl:

**Primary: crawl4ai + ddgs**
```python
from ddgs import DDGS
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, ReadabilityExtractionStrategy
import asyncio

# Search
with DDGS() as ddgs:
    results = list(ddgs.text("<sub-question keywords>", max_results=10))
urls = [r['href'] for r in results]

# Crawl (async batch)
async def crawl_all(urls):
    async with AsyncWebCrawler() as crawler:
        tasks = [
            crawler.arun(url=url, config=CrawlerRunConfig(
                extraction_strategy="ReadabilityScriptlet",
                word_count_threshold=100
            )) for url in urls
        ]
        return await asyncio.gather(*tasks)

contents = await crawl_all(urls)
```

**Fallback: Firecrawl MCP**
```
firecrawl_search(query: "<sub-question keywords>", limit: 8)
firecrawl_scrape(url: "<url>")
```

**Fallback: Exa MCP**
```
web_search_exa(query: "<sub-question keywords>", numResults: 8)
web_search_advanced_exa(query: "<keywords>", numResults: 5, startPublishedDate: "2025-01-01")
crawling_exa(url: "<url>", tokensNum: 5000)
```

**Search strategy:**
- Use 2-3 different keyword variations per sub-question
- Mix general and news-focused queries (add date qualifiers like "2025" or "latest")
- Aim for 15-30 unique sources total
- Prioritize: academic, official, reputable news > blogs > forums

### Step 4: Deep-Read Key Sources

For the most promising URLs, fetch full content with crawl4ai (primary) or firecrawl/exa (fallback). Read 3-5 key sources in full for depth. Do not rely only on search snippets.

For large pages, crawl4ai's saved file path is in the result footer — follow it to read the omitted middle.

### Step 5: Synthesize and Write Report

Structure the report:

```markdown
# [Topic]: Research Report
*Generated: [date] | Sources: [N] | Confidence: [High/Medium/Low]*

## Executive Summary
[3-5 sentence overview of key findings]

## 1. [First Major Theme]
[Findings with inline citations]
- Key point ([Source Name](url))
- Supporting data ([Source Name](url))

## 2. [Second Major Theme]
...

## 3. [Third Major Theme]
...

## Key Takeaways
- [Actionable insight 1]
- [Actionable insight 2]
- [Actionable insight 3]

## Sources
1. [Title](url) — [one-line summary]
2. ...

## Methodology
Searched [N] queries across web and news. Analyzed [M] sources.
Sub-questions investigated: [list]
Primary tool: crawl4ai + duckduckgo_search (no API key)
```

### Step 6: Deliver

- **Short topics**: Post the full report in chat
- **Long reports**: Post the executive summary + key takeaways, save full report to a file with `write_file`

## Parallel Research

For broad topics, split research across parallel passes: run search batches per sub-question, collect results per theme, then synthesize everything into the final report in one pass. The main session always does the final synthesis — never delegate that.

## Quality Rules

1. **Every claim needs a source.** No unsourced assertions.
2. **Cross-reference.** If only one source says it, flag it as unverified.
3. **Recency matters.** Prefer sources from the last 12 months.
4. **Acknowledge gaps.** If you couldn't find good info on a sub-question, say so.
5. **No hallucination.** If you don't know, say "insufficient data found."
6. **Separate fact from inference.** Label estimates, projections, and opinions clearly.
7. **Respect robots.txt** — check before bulk crawling with crawl4ai.
8. **Rate-limit** — max 1 request/second to same domain.

## Examples

```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services in 2026"
"Research the best strategies for bootstrapping a SaaS business"
"What's happening with the US housing market right now?"
"Investigate the competitive landscape for AI code editors"
```