---
name: api-scout
description: Fast discovery and querying of over 1,500+ curated public APIs, free developer tiers (free-for-dev), and self-hosted tools in Workshop.
---

# API Scout — Public APIs & Free Developer Tooling Discovery

Use this skill whenever the user or project needs:
- Free public APIs for data ingestion, mock data, or live feeds (crypto, weather, sports, finance, AI, books, geocoding, etc.).
- Free cloud infrastructure tiers (databases, auth, storage, hosting, serverless functions).
- Self-hostable open source solutions for microservices and backends.

---

## 1. Quick CLI Search Command

Agents can run the local `search_apis.py` script directly:

```bash
# Search by keyword
python "./skills/api-scout/search_apis.py" "weather"

# Search for completely free APIs with No Auth & CORS enabled (ready for frontend/fetch)
python "./skills/api-scout/search_apis.py" "finance" --no-auth --cors

# Search by category
python "./skills/api-scout/search_apis.py" --category "Machine Learning"

# Search free cloud developer tiers (free-for-dev)
python "./skills/api-scout/search_apis.py" "postgres" --free-dev

# Search self-hosted open source software
python "./skills/api-scout/search_apis.py" "analytics" --self-hosted
```

---

## 2. Supported Catalogs in Workshop

1. [`./public-apis`](file:///./public-apis): 1,500+ curated public APIs across 50+ categories.
2. [`./free-for-dev`](file:///./free-for-dev): Curated list of SaaS/PaaS/IaaS with free developer tiers.
3. [`./awesome-selfhosted`](file:///./awesome-selfhosted): Curated list of self-hostable open-source systems.
4. [`./awesome`](file:///./awesome): Master index of curated developer resources across all ecosystems.
