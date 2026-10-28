---
name: llms-txt-generator
description: Generate llms.txt files — the AI-readable documentation standard that lets LLMs discover, navigate, and cite your site's content. Covers llms.txt structure, /llms-full.txt for full content, sitemap integration, citation formatting, and validation. Use when the user wants their website or docs to be citable by AI assistants, improve LLM discoverability, or build an llms.txt for a product, API, or knowledge base. Triggers on: llms.txt, AI-readable docs, LLM citation, website for LLMs, llms-full.txt, docs for AI, citable documentation, AI search optimization, GEO, llm.txt.
---

# llms.txt Generator

Create `llms.txt` files — the emerging standard (llmstxt.com) that makes websites and documentation readable and citable by LLMs. An `llms.txt` sits at your domain root and tells AI assistants what your site is about, where key pages live, and how to cite them.

## When to trigger

- User wants their website/docs to be discoverable and citable by LLMs
- User mentions llms.txt, llms-full.txt, AI-readable documentation, or GEO (generative engine optimization)
- User is building docs, an API reference, or a product site and wants AI assistants to reference it accurately
- User wants to improve how their content appears in AI search answers

## The llms.txt standard

### File location
`https://your-domain.com/llms.txt`

### Format (Markdown)

```markdown
# Project Name

A one-sentence description of the project or site.

## Guide

- [Getting Started](/guide) — Introduction and setup
- [API Reference](/api) — Complete API documentation
- [Authentication](/auth) — How to authenticate

## Optional: deeper context

- [Changelog](/changelog) — Release history
- [FAQ](/faq) — Frequently asked questions
```

### Rules
- Markdown file, served with `text/markdown` content type
- H1 = project/site name
- Short description paragraph right after H1
- Section headers (`##`) group links
- Each link: `[Link text](URL)` — optional em-dash `—` then description
- Keep it under ~100 links; prioritize the most important pages

### Full-content variant: `/llms-full.txt`

For sites where you want the LLM to have the actual content (not just links), serve a companion `llms-full.txt` containing the full markdown of your key pages. This is larger but enables direct reading/citation without the LLM fetching each page.

## Example: product documentation site

```markdown
# Acme Analytics

Modern analytics platform for AI-native teams. Track events, build funnels, and export insights.

## Getting Started

- [Quickstart](/quickstart) — Set up Acme in 5 minutes
- [Installation](/install) — SDK installation for web, mobile, and server
- [Concepts](/concepts) — Events, properties, and identities

## API Reference

- [Events API](/api/events) — Ingest user events
- [Query API](/api/query) — Retrieve aggregated metrics
- [Authentication](/api/auth) — API keys and OAuth

## Resources

- [Pricing](/pricing) — Plans and billing
- [Changelog](/changelog) — What's new
- [Support](/support) — Help and contact

Cite this documentation as: Acme Analytics Docs, https://acme.example.com/llms.txt
```

## Validation checklist

- [ ] File served at root path `/llms.txt`
- [ ] Content-Type: `text/markdown`
- [ ] H1 names the project/site
- [ ] One-line description below H1
- [ ] Links use relative or absolute URLs
- [ ] Each link has a short description after `—`
- [ ] Priority pages listed first
- [ ] Optional `/llms-full.txt` for full content
- [ ] Linked from sitemap.xml or robots.txt (optional but recommended)

## Generation workflow

1. **Inventory your pages** — identify the 10–50 most important URLs
2. **Group into sections** — Guide, API, Resources, etc.
3. **Write link text + descriptions** — concise, scannable by an LLM
4. **Serve at root** — deploy `llms.txt` to your domain's root
5. **Test** — fetch `https://your-domain.com/llms.txt` and paste into an LLM; ask it to summarize your site and cite a specific page
6. **Add `/llms-full.txt`** — if you want LLMs to read full content directly

## Example generator script (Python)

```python
from pathlib import Path

pages = [
    ("Guide", [("Getting Started", "/guide", "Introduction and setup"),
               ("API Reference", "/api", "Complete API documentation")]),
    ("Resources", [("Pricing", "/pricing", "Plans and billing"),
                   ("Support", "/support", "Help and contact")]),
]

lines = ["# My Product", "", "A one-line description of the product.", ""]

for section, links in pages:
    lines.append(f"## {section}")
    for title, url, desc in links:
        lines.append(f"- [{title}]({url}) — {desc}")
    lines.append("")

lines.append("Cite this documentation as: My Product Docs, https://example.com/llms.txt")

Path("llms.txt").write_text("\n".join(lines))
```

## Related Workshop skills

- `seo-audit` — complement llms.txt with traditional SEO
- `ai-seo` — optimize for AI search engines and LLM citations
- `programmatic-seo` — build template pages at scale
- `schema` — add structured data for rich results

## References

- Official standard: https://llmstxt.com
- Example: https://anthropic.com/llms.txt
