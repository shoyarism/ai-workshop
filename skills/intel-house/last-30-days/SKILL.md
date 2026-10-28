---
name: last-30-days
description: "Real-time 30-day recency intelligence by Matt Van Horn. Scrapes discussions, trending tools, and sentiment from the last 30 days across Reddit, X, YouTube, and Hacker News, scoring insights by actual engagement."
userFacing: true
---

# ⏱️ Last 30 Days: Real-Time Recency Intelligence

> **Purpose:** Cuts through stale LLM training data by querying the open internet exclusively for events, releases, discussions, and consensus formed within the preceding 30 days.

---

## 1. Operating Rules & Time Windows

- **Strict Temporal Filter:** Enforce `date:>=now-30d` or explicit date parameters across all scrapers and search queries.
- **Cross-Platform Triangulation:**
  - **Hacker News:** Algolia HN API (`created_at_i>{timestamp}`) for developer consensus, postmortems, and technical critique.
  - **Reddit:** Top/relevant discussions across domain-specific subreddits (`r/programming`, `r/localllama`, `r/design`, `r/webdev`).
  - **X (Twitter):** Influential creator threads, release announcements, and breaking discussions.
  - **GitHub:** Trending repositories created or heavily starred in the last 30 days.

---

## 2. Engagement-Weighted Scoring

Raw search hits are weighted according to verified community signals:
$$\text{Score} = (\text{Upvotes} \times 1.0) + (\text{Comments} \times 1.5) + (\text{Stars/Retweets} \times 2.0)$$

Filters out low-effort bot noise, ensuring only battle-tested community insights enter the prompt context.

---

## 3. Output Format

```markdown
### ⏱️ LAST 30 DAYS INTELLIGENCE BRIEF: [Topic]
*Scan Window: [Date -30d] to [Today]*

1. **Major Releases & Breaking Changes:**
   - [Tool/Version]: Released [Date] — [Core change & impact]
2. **Community Consensus & Best Practices:**
   - What developers currently recommend vs what has fallen out of favor.
3. **Emerging Tools & Repositories:**
   - [Repo Name] ([Stars], [Date]): [Value Proposition]
4. **Key Warnings & Known Regressions:**
   - [Documented bugs or issues reported by users in the last 30 days]
```
