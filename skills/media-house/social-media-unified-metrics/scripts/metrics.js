/**
 * Unified Metrics Engine v2
 * Normalizes, aggregates, and computes KPIs across all platforms.
 */

const UnifiedMetrics = (() => {

  // --- NORMALIZATION ---
  function normalizeFacebook(raw) {
    if (!raw || !raw.daily_data) return [];
    return raw.daily_data.map(d => ({
      platform: 'facebook', date: d.date, period: 'daily',
      audience: { followers: raw.followers || 0, followers_delta: d.fan_adds - d.fan_removes, followers_delta_pct: 0 },
      reach: { impressions: d.impressions || 0, reach: d.reach || 0, profile_visits: 0 },
      engagement: {
        total_engagements: (d.reactions ? Object.values(d.reactions).reduce((a,b)=>a+b,0) : 0) + (d.link_clicks||0),
        likes: d.reactions ? (d.reactions.like||0) : 0,
        comments: 0, shares: 0, saves: 0, reposts: 0
      },
      content: { posts_count: 1, video_views: d.video_views || 0, watch_time_seconds: 0, avg_view_duration_seconds: 0 },
      conversion: { link_clicks: d.link_clicks || 0, profile_clicks: 0, website_clicks: 0 }
    }));
  }

  function normalizeInstagram(raw) {
    if (!raw || !raw.daily_data) return [];
    return raw.daily_data.map(d => ({
      platform: 'instagram', date: d.date, period: 'daily',
      audience: { followers: d.follower_count || raw.followers || 0, followers_delta: 0, followers_delta_pct: 0 },
      reach: { impressions: d.impressions || 0, reach: d.reach || 0, profile_visits: d.profile_views || 0 },
      engagement: {
        total_engagements: (d.likes||0) + (d.comments||0) + (d.saves||0) + (d.shares||0),
        likes: d.likes || 0, comments: d.comments || 0, shares: d.shares || 0, saves: d.saves || 0, reposts: 0
      },
      content: { posts_count: 1, video_views: d.video_views || 0, watch_time_seconds: 0, avg_view_duration_seconds: 0 },
      conversion: { link_clicks: 0, profile_clicks: 0, website_clicks: 0 }
    }));
  }

  function normalizeYouTube(raw) {
    if (!raw || !raw.daily_data) return [];
    return raw.daily_data.map(d => ({
      platform: 'youtube', date: d.date, period: 'daily',
      audience: { followers: raw.subscribers || 0, followers_delta: d.subscribers_gained - d.subscribers_lost, followers_delta_pct: 0 },
      reach: { impressions: d.views || 0, reach: d.views || 0, profile_visits: 0 },
      engagement: {
        total_engagements: (d.likes||0) + (d.comments||0),
        likes: d.likes || 0, comments: d.comments || 0, shares: 0, saves: 0, reposts: 0
      },
      content: { posts_count: 1, video_views: d.views || 0, watch_time_seconds: (d.estimated_minutes_watched||0)*60, avg_view_duration_seconds: 0 },
      conversion: { link_clicks: 0, profile_clicks: 0, website_clicks: 0 }
    }));
  }

  function normalizeTikTok(raw) {
    if (!raw || !raw.daily_data) return [];
    return raw.daily_data.map(d => ({
      platform: 'tiktok', date: d.date, period: 'daily',
      audience: { followers: raw.followers || 0, followers_delta: 0, followers_delta_pct: 0 },
      reach: { impressions: d.video_views || 0, reach: d.video_views || 0, profile_visits: d.profile_visits || 0 },
      engagement: {
        total_engagements: (d.likes||0) + (d.comments||0) + (d.shares||0) + (d.saves||0),
        likes: d.likes || 0, comments: d.comments || 0, shares: d.shares || 0, saves: d.saves || 0, reposts: 0
      },
      content: { posts_count: 1, video_views: d.video_views || 0, watch_time_seconds: d.watch_time_seconds || 0, avg_view_duration_seconds: 0 },
      conversion: { link_clicks: 0, profile_clicks: 0, website_clicks: 0 }
    }));
  }

  function normalizeThreads(raw) {
    if (!raw || !raw.daily_data) return [];
    return raw.daily_data.map(d => ({
      platform: 'threads', date: d.date, period: 'daily',
      audience: { followers: raw.followers || 0, followers_delta: 0, followers_delta_pct: 0 },
      reach: { impressions: d.post_views || 0, reach: d.post_views || 0, profile_visits: 0 },
      engagement: {
        total_engagements: (d.likes||0) + (d.replies||0) + (d.reposts||0) + (d.quote_posts||0),
        likes: d.likes || 0, comments: d.replies || 0, shares: d.reposts || 0, saves: 0, reposts: d.reposts || 0
      },
      content: { posts_count: 1, video_views: 0, watch_time_seconds: 0, avg_view_duration_seconds: 0 },
      conversion: { link_clicks: 0, profile_clicks: 0, website_clicks: 0 }
    }));
  }

  function normalize(platform, raw) {
    const normalizers = {
      facebook: normalizeFacebook, instagram: normalizeInstagram,
      youtube: normalizeYouTube, tiktok: normalizeTikTok, threads: normalizeThreads
    };
    return (normalizers[platform] || (() => []))(raw);
  }

  // --- AGGREGATION ---
  function aggregateByPeriod(dailyData, period) {
    if (!dailyData || dailyData.length === 0) return [];
    const groups = {};
    dailyData.forEach(d => {
      let key;
      if (period === 'daily') key = d.date;
      else if (period === 'weekly') {
        const dt = new Date(d.date);
        const weekStart = new Date(dt); weekStart.setDate(dt.getDate() - dt.getDay());
        key = weekStart.toISOString().slice(0, 10);
      }
      else if (period === 'monthly') key = d.date.slice(0, 7);
      else key = d.date.slice(0, 4);
      if (!groups[key]) groups[key] = [];
      groups[key].push(d);
    });
    return Object.entries(groups).map(([key, items]) => {
      const last = items[items.length - 1];
      return {
        period, date: key, platform: items[0].platform,
        audience: {
          followers: last.audience.followers,
          followers_delta: items.reduce((s, i) => s + i.audience.followers_delta, 0),
          followers_delta_pct: 0
        },
        reach: {
          impressions: items.reduce((s, i) => s + i.reach.impressions, 0),
          reach: items.reduce((s, i) => s + i.reach.reach, 0),
          profile_visits: items.reduce((s, i) => s + i.reach.profile_visits, 0)
        },
        engagement: {
          total_engagements: items.reduce((s, i) => s + i.engagement.total_engagements, 0),
          likes: items.reduce((s, i) => s + i.engagement.likes, 0),
          comments: items.reduce((s, i) => s + i.engagement.comments, 0),
          shares: items.reduce((s, i) => s + i.engagement.shares, 0),
          saves: items.reduce((s, i) => s + i.engagement.saves, 0),
          reposts: items.reduce((s, i) => s + i.engagement.reposts, 0)
        },
        content: {
          posts_count: items.reduce((s, i) => s + i.content.posts_count, 0),
          video_views: items.reduce((s, i) => s + i.content.video_views, 0),
          watch_time_seconds: items.reduce((s, i) => s + i.content.watch_time_seconds, 0),
          avg_view_duration_seconds: 0
        },
        conversion: {
          link_clicks: items.reduce((s, i) => s + i.conversion.link_clicks, 0),
          profile_clicks: items.reduce((s, i) => s + i.conversion.profile_clicks, 0),
          website_clicks: items.reduce((s, i) => s + i.conversion.website_clicks, 0)
        }
      };
    });
  }

  // --- KPI CALCULATION ---
  function engagementRate(data) {
    if (!data || data.reach.impressions === 0) return 0;
    return ((data.engagement.total_engagements / data.reach.impressions) * 100).toFixed(1);
  }

  function calculateKPIs(current, previous) {
    const platforms = ['facebook', 'instagram', 'youtube', 'tiktok', 'threads'];
    const allCurrent = platforms.map(p => (current[p] || []).reduce((acc, d) => {
      acc.reach.impressions += d.reach.impressions;
      acc.engagement.total_engagements += d.engagement.total_engagements;
      acc.engagement.likes += d.engagement.likes;
      acc.engagement.comments += d.engagement.comments;
      acc.engagement.shares += d.engagement.shares;
      acc.content.video_views += d.content.video_views;
      acc.conversion.link_clicks += d.conversion.link_clicks;
      return acc;
    }, { reach: { impressions: 0 }, engagement: { total_engagements: 0, likes: 0, comments: 0, shares: 0 }, content: { video_views: 0 }, conversion: { link_clicks: 0 } }));

    const totals = allCurrent.reduce((a, b) => ({
      reach: { impressions: a.reach.impressions + b.reach.impressions },
      engagement: { total_engagements: a.engagement.total_engagements + b.engagement.total_engagements, likes: a.engagement.likes + b.engagement.likes, comments: a.engagement.comments + b.engagement.comments, shares: a.engagement.shares + b.engagement.shares },
      content: { video_views: a.content.video_views + b.content.video_views },
      conversion: { link_clicks: a.conversion.link_clicks + b.conversion.link_clicks }
    }), { reach: { impressions: 0 }, engagement: { total_engagements: 0, likes: 0, comments: 0, shares: 0 }, content: { video_views: 0 }, conversion: { link_clicks: 0 } });

    return totals;
  }

  function formatNumber(n) {
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
    return n.toString();
  }

  return { normalize, aggregateByPeriod, engagementRate, calculateKPIs, formatNumber };
})();
