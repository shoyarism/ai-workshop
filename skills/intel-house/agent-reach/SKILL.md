---
name: agent-reach
description: "Universal zero-API-cost intelligence engine. Scrapes, searches, and extracts live data across Twitter/X, Reddit, YouTube transcripts, GitHub, and web articles without paid API keys."
userFacing: true
---

# 🌐 Agent Reach: Zero-Cost Multi-Platform Intelligence

> **Purpose:** Connects AI agents to the live internet across walled gardens and modern social platforms without recurring subscription fees or API rate-limit walls.

---

## 1. Supported Platform Adapters

| Platform | Extraction Mechanism | Capability |
|---|---|---|
| **Twitter / X** | Direct scraping via headless browser & public mirrors | Post extraction, user threads, search queries, reply trees |
| **Reddit** | Clean `.json` endpoints & DOM extraction | Subreddit scans, comment hierarchy, top/rising sentiment |
| **YouTube** | `yt-dlp` & transcript parsers | Video metadata, timed captions, full transcript assembly |
| **GitHub** | Public Git APIs & raw content scrapers | Commits, releases, READMEs, issue discussions, trending repos |
| **Web / Articles** | Readability DOM extraction & Markdown converters | Ad-free, boilerplate-free article prose and technical docs |

---

## 2. Operating Discipline

- **Scrape Surgical Targets:** Extract only the relevant content blocks rather than dumping megabytes of raw HTML.
- **Engagement Grounding:** Report platform metrics alongside extracted content (e.g., upvotes, view count, retweet counts, dates) to ground findings in real-world reception.
- **Synthesized Briefing:** Compile findings into an executive intelligence brief:
  - Key Consensus Points
  - Divergent Opinions / Counter-Arguments
  - Code Snippets / Repository Links
  - Timestamps & Verification Sources
