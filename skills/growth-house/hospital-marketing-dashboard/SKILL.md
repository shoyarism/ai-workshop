---
name: hospital-marketing-dashboard
description: >-
  Strategic and Operational Healthcare Digital Marketing, Humas, and Patient Flow Dashboard Framework.
  Full component specs, data flow, UI patterns, and cadence views.
---

# Hospital Marketing and Humas Dashboard Framework v2

Production blueprint for healthcare digital marketing dashboards.

## Architecture

Data Sources -> Connectors -> UnifiedMetrics Aggregator -> DashboardRenderer

Platforms: Meta Graph API v21.0, YouTube Data API v3, TikTok (browser-scraped), Threads (browser-scraped), Mekari Qontak

## Component Architecture

1. Top Navigation: Logo, date range selector, platform filter toggles, live indicator, settings
2. Executive Summary Row: 4 KPI cards (Total Followers, Total Reach, Total Engagements, Total Video Views) + MoM deltas
3. Platform Performance Grid: 6 cards (FB, IG, YT, TikTok, Threads, WhatsApp) with followers, reach, engagement rate, top post
4. Funnel Visualization: 3 horizontal bars (Awareness -> Engagement -> Conversion) with volumes
5. Time Series Chart: Multi-line daily/weekly trends (Chart.js)
6. Content Performance Table: Sortable by platform, date, engagement
7. Platform Deep-Dive Tabs: Per-platform detailed metrics

## Data Flow

1. Token Check -> configured? API call : simulated fallback
2. Parallel Fetch -> all platforms simultaneously
3. Normalize -> unified schema per platform
4. Aggregate -> roll up by selected period
5. KPI Calculation -> executive metrics with MoM/YoY
6. Render -> update dashboard DOM

## Cadence Views

Weekly: Content pacing, response SLA, post scheduling
Monthly: MoM growth, campaign ROI, platform comparison
Quarterly: Strategic trends, YoY comparison, budget allocation
Yearly: Annual trends, channel maturity, recommendations

## UI Patterns

Cards: White, shadow, 16px padding, icon + label + value + delta badge
Charts: Chart.js (time series, bars, doughnut), CSS ring charts
Grid: 4-col desktop, 2-col tablet, 1-col mobile

## Color Palette

Meta/Facebook: #1877F2, Instagram: #E4405F, YouTube: #FF0000, TikTok: #000000/#69C9D0
Threads: #000000, WhatsApp: #25D366, Primary: #1a56db, Success: #16a34a, Danger: #dc2626

## Typography

Headers: Inter 600, Body: Inter 400, Numbers: JetBrains Mono

## Settings (localStorage)

meta_page_id, meta_page_token, youtube_channel_id, youtube_api_key
tiktok_username, threads_username, qontak_token
polling_interval (default 300000ms), date_range (7d/30d/90d/1y)

## File Structure

dashboard/
  index.html, css/style.css
  js/connectors.js, metrics.js, charts.js, dashboard.js, settings.js
