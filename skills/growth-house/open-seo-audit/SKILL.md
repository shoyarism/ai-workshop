---
name: open-seo-audit
description: Automated technical SEO auditing, sitemap crawling, Core Web Vitals inspection, and search indexing analysis with OpenSEO.
---

# OpenSEO Automated Audit Engine

OpenSEO is an open-source technical SEO audit suite providing automated page crawling, meta tag validation, canonical checks, structured data (JSON-LD) verification, and Core Web Vitals profiling.

## Core Capabilities
- **Sitemap & Deep Crawl**: Extract internal links, orphan pages, redirect chains, and broken anchors.
- **Technical SEO Audit**: Analyze title tags, meta descriptions, Open Graph, Twitter Cards, H1-H6 hierarchy.
- **Search Performance Scorecards**: Compute actionable audit scores and JSON recommendations.

## CLI Usage
`ash
# Crawl site and run full technical SEO audit
python open-seo/cli.py audit --url https://example.com --max-pages 100 --output seo_audit.json
`
