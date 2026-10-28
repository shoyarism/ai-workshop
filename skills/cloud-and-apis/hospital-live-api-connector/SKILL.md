---
name: hospital-live-api-connector
description: >-
  Multi-platform live API connector engine for hospital marketing, patient flow, and customer care.
  Connects Meta Graph API v21.0 (Instagram Business, Facebook Pages, Meta Business Suite Insights),
  YouTube Data API v3, Threads (browser-scraped), TikTok (browser-scraped),
  Mekari Qontak WhatsApp Omnichannel, .
  Includes JavaScript connector library, token management, simulated fallback, and auto-polling.
---

# Hospital Live API Connector Engine v2

Production-grade real-time API connector for healthcare digital marketing and patient administration dashboards.

## Supported Platforms and Endpoints

### 1. Meta Graph API v21.0 (Instagram Business + Facebook Pages + Business Suite)

**Base URL**: `https://graph.facebook.com/v21.0/`

**Authentication**: Page Access Token or System User Token stored in localStorage.

**Facebook Page Endpoints**:
`
GET /{page-id}?fields=id,name,fan_count,talking_about_count,was_followed_read_count
GET /{page-id}/insights?metric=page_impressions,page_engaged_users,page_post_engagements,page_video_views,page_fan_adds,page_fan_removes&period=day&since={date}&until={date}
GET /{page-id}/posts?fields=id,message,created_time,shares,comments.summary(true),reactions.summary(true),insights.metric(post_reactions_by_type_total,post_impressions,post_video_complete_views_30_sec)&limit=25
`

**Instagram Business Endpoints**:
`
GET /{ig-user-id}?fields=id,username,followers_count,media_count
GET /{ig-user-id}/insights?metric=impressions,reach,profile_views,follower_count&period=day&since={date}&until={date}
GET /{ig-user-id}/media?fields=id,caption,media_type,media_url,timestamp,like_count,comments_count,insights.metric(impressions,reach,engagement,save,shares)&limit=25
`

**Meta Business Suite Insights** (via page token):
`
GET /{page-id}/insights?metric=page_impressions_organic,page_impressions_paid,page_engaged_users,page_post_engagements,page_video_views,page_fan_adds&period=day&since={date}&until={date}
GET /{page-id}/insights?metric=page_actions_post_reactions_total&period=day
`

**Rate Limits**: 200 calls/user/hour (User Tokens), 4800 calls/app/hour (App Tokens).

### 2. YouTube Data API v3

**Base URL**: `https://www.googleapis.com/youtube/v3/`

**Authentication**: API Key (read-only) or OAuth 2.0.

**Endpoints**:
`
GET /channels?part=snippet,statistics,contentDetails&id={channel-id}&key={api-key}
GET /search?part=snippet&channelId={channel-id}&order=date&maxResults=10&key={api-key}
GET /videos?part=snippet,statistics,contentDetails&id={video-ids}&key={api-key}
GET /channels?part=statistics&forHandle={handle}&key={api-key}
`

**Quota**: 10,000 units/day. channels.list = 1 unit, search.list = 100 units, videos.list = 1 unit.

### 3. Threads (Browser-Scraped)

No public API. Data extracted via browser automation from SSR-embedded JSON.

**Extractable Metrics**: Post count, follower count, following count, per-post likes/reposts/replies/views.

### 4. TikTok (Browser-Scraped)

Limited public API. Primary source is browser XHR interception.

**Endpoints Intercepted**: `/api/post/item_list/` (video list), `/api/user/detail/` (profile).

**Extractable Metrics**: Follower count, video count, per-video views/likes/comments/shares/watch time.

### 5. Mekari Qontak WhatsApp Omnichannel

**Base URL**: `https://service-chat.qontak.com/api/open/v1/`

**Authentication**: Bearer Token.

**Endpoints**: broadcasts/statistics, chats/inbox, chats/agents, csat.

## Architecture

`
Dashboard (Browser)
  -> Meta Connector (Graph API v21.0)
  -> YouTube Connector (Data API v3)
  -> TikTok Connector (browser-scraped)
  -> Threads Connector (browser-scraped)
  -> Qontak Connector (WhatsApp API)
    -> Unified Metrics Aggregator
  -> Simulated Fallback Generator (when tokens missing)
  -> localStorage Token Vault
`

## Token Management

`javascript
HospitalConnector.setToken('meta_page_token', 'EAA...')
HospitalConnector.getToken('meta_page_token')
HospitalConnector.getConnectionStatus()
// -> { meta: true, youtube: false, qontak: false, tiktok: 'browser', threads: 'browser' }
`

## Auto-Polling

`javascript
HospitalConnector.startPolling({ meta: 300000, youtube: 300000, tiktok: 60000, threads: 60000, qontak: 15000 })
`

## Simulated Fallback

When tokens are not populated or APIs return errors, generates realistic mock data matching each platform schema. Allows dashboard development without live credentials.
