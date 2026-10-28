---
name: social-media-unified-metrics
description: >-
  Cross-platform analytics normalization and aggregation engine for hospital digital marketing.
  Supports Meta (Facebook + Instagram + Business Suite), YouTube, TikTok, Threads, and WhatsApp.
  Includes time-series aggregation, MoM/YoY comparisons, KPI templates, and funnel metrics.
---

# Social Media Unified Metrics Engine v2

Normalizes disparate platform metrics into a single, comparable schema for dashboards, reports, and executive summaries.

## Normalized Unified Schema

Every platform raw data maps to this canonical shape:

  platform: facebook|instagram|youtube|tiktok|threads|whatsapp
  period: daily|weekly|monthly|yearly
  date: 2026-08-31
  audience: { followers, followers_delta, followers_delta_pct }
  reach: { impressions, reach, profile_visits }
  engagement: { total_engagements, likes, comments, shares, saves, reposts }
  content: { posts_count, video_views, watch_time_seconds, avg_view_duration_seconds }
  conversion: { link_clicks, profile_clicks, website_clicks }

## Platform Field Mapping

Facebook:  fan_count -> audience.followers,  page_impressions -> reach.impressions,  reactions -> engagement.likes
Instagram: followers_count -> audience.followers,  insights.impressions -> reach.impressions,  like_count -> engagement.likes
YouTube:   subscriberCount -> audience.followers,  viewCount -> content.video_views,  videoCount -> content.posts_count
TikTok:    followerCount -> audience.followers,  diggCount -> engagement.likes,  commentCount -> engagement.comments
Threads:   follower_count -> audience.followers,  like_count -> engagement.likes,  reply_count -> engagement.replies
WhatsApp:  follower_count -> audience.followers,  reaction_count -> engagement.reactions

## Aggregation Rules

Rollup (daily -> weekly/monthly/yearly):
  SUM: impressions, reach, video_views, engagements, watch_time, profile_visits
  LAST: followers (point-in-time, not additive)
  WEIGHTED AVG: CTR, save_rate, avg_view_duration

Engagement Rate = (likes + comments + shares + saves) / impressions * 100
  YouTube variant: (likes + comments) / views * 100
  TikTok variant: (likes + comments + shares) / views * 100

## KPI Templates

Weekly: follower_growth, engagement_rate, post_volume, total_reach, video_views
Monthly: mom_follower_growth_pct, mom_reach_growth_pct, top_platform_by_engagement, content_velocity, platform_diversification
Yearly: yoy_follower_growth_pct, yoy_reach_growth_pct, annual_impressions, platform_cagr

## Funnel Metrics

Top (Awareness): total_impressions, total_reach, total_video_views, brand_mentions
Mid (Engagement): total_engagements, avg_engagement_rate, dm_inquiries, whatsapp_messages
Bottom (Conversion): website_clicks, profile_visits_to_website, whatsapp_to_appointment, poliklinik_bookings

## Refresh Strategy

  Meta: 5min (REST API),  YouTube: 5min (REST API),  TikTok: 1min (browser scrape)
  Threads: 1min (browser scrape),  WhatsApp: 15sec (REST API),  SIMRS: 10sec (local REST)