/**
 * Hospital Live API Connector v2
 * Multi-platform connector: Meta Graph API, YouTube Data API, TikTok, Threads, Mekari Qontak
 * Includes simulated fallback for development without live credentials.
 */

const HospitalConnector = (() => {
  const TOKEN_KEY = 'hospital_connector_tokens';
  const POLL_KEY = 'hospital_connector_polling';

  function getTokens() {
    try { return JSON.parse(localStorage.getItem(TOKEN_KEY) || '{}'); }
    catch { return {}; }
  }

  function setToken(key, value) {
    const tokens = getTokens();
    tokens[key] = value;
    localStorage.setItem(TOKEN_KEY, JSON.stringify(tokens));
  }

  function getToken(key) {
    return getTokens()[key] || null;
  }

  function getConnectionStatus() {
    const t = getTokens();
    return {
      meta: !!(t.meta_page_token && t.meta_page_id),
      youtube: !!(t.youtube_api_key && t.youtube_channel_id),
      tiktok: t.tiktok_username ? 'browser' : false,
      threads: t.threads_username ? 'browser' : false,
      qontak: !!t.qontak_token,
    };
  }

  // --- SIMULATED DATA GENERATORS ---
  function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
  function randFloat(min, max) { return (Math.random() * (max - min) + min).toFixed(1); }

  function simulateFacebook(pageId) {
    const days = [];
    const baseFollowers = randInt(5000, 25000);
    for (let i = 30; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      days.push({
        date: d.toISOString().slice(0, 10),
        impressions: randInt(800, 5000),
        reach: randInt(500, 3000),
        engaged_users: randInt(50, 500),
        post_engagements: randInt(100, 800),
        video_views: randInt(200, 2000),
        fan_adds: randInt(5, 50),
        fan_removes: randInt(0, 15),
        reactions: { like: randInt(30, 300), love: randInt(5, 50), haha: randInt(2, 20), wow: randInt(1, 10), sad: randInt(0, 5), angry: randInt(0, 3) },
        link_clicks: randInt(10, 100)
      });
    }
    return {
      platform: 'facebook',
      page_id: pageId,
      name: 'Hospital Facebook Page',
      followers: baseFollowers + randInt(-50, 100),
      daily_data: days
    };
  }

  function simulateInstagram(igUserId) {
    const days = [];
    const baseFollowers = randInt(3000, 20000);
    for (let i = 30; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      days.push({
        date: d.toISOString().slice(0, 10),
        impressions: randInt(1000, 8000),
        reach: randInt(600, 4000),
        profile_views: randInt(50, 400),
        follower_count: baseFollowers + randInt(-10, 30),
        likes: randInt(40, 400),
        comments: randInt(5, 60),
        saves: randInt(3, 30),
        shares: randInt(2, 20),
        video_views: randInt(300, 3000)
      });
    }
    return {
      platform: 'instagram',
      user_id: igUserId,
      username: 'hospital_ig',
      followers: baseFollowers + randInt(-30, 80),
      media_count: randInt(100, 500),
      daily_data: days
    };
  }

  function simulateYouTube(channelId) {
    const days = [];
    const baseSubs = randInt(1000, 15000);
    for (let i = 30; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      days.push({
        date: d.toISOString().slice(0, 10),
        views: randInt(200, 3000),
        estimated_minutes_watched: randFloat(100, 2000),
        subscribers_gained: randInt(1, 20),
        subscribers_lost: randInt(0, 5),
        likes: randInt(10, 150),
        comments: randInt(2, 30)
      });
    }
    return {
      platform: 'youtube',
      channel_id: channelId,
      title: 'Hospital YouTube Channel',
      subscribers: baseSubs + randInt(-10, 20),
      total_views: randInt(100000, 2000000),
      video_count: randInt(50, 300),
      daily_data: days
    };
  }

  function simulateTikTok(username) {
    const days = [];
    const baseFollowers = randInt(2000, 30000);
    for (let i = 30; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      days.push({
        date: d.toISOString().slice(0, 10),
        video_views: randInt(500, 10000),
        likes: randInt(30, 500),
        comments: randInt(5, 80),
        shares: randInt(2, 50),
        saves: randInt(3, 40),
        profile_visits: randInt(20, 300),
        watch_time_seconds: randInt(200, 5000)
      });
    }
    return {
      platform: 'tiktok',
      username: username,
      followers: baseFollowers + randInt(-20, 60),
      following: randInt(50, 500),
      total_likes: randInt(50000, 500000),
      video_count: randInt(30, 200),
      daily_data: days
    };
  }

  function simulateThreads(username) {
    const days = [];
    const baseFollowers = randInt(500, 8000);
    for (let i = 30; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      days.push({
        date: d.toISOString().slice(0, 10),
        post_views: randInt(100, 2000),
        likes: randInt(10, 150),
        replies: randInt(2, 30),
        reposts: randInt(1, 20),
        quote_posts: randInt(0, 10)
      });
    }
    return {
      platform: 'threads',
      username: username,
      followers: baseFollowers + randInt(-5, 15),
      posts_count: randInt(50, 300),
      daily_data: days
    };
  }

  function simulateQontak() {
    const agents = ['Agent A', 'Agent B', 'Agent C', 'Agent D'];
    return {
      platform: 'whatsapp',
      total_contacts: randInt(1000, 10000),
      broadcast_sent: randInt(500, 3000),
      broadcast_opened: randInt(200, 1500),
      broadcast_clicked: randInt(50, 500),
      inbound_today: randInt(20, 200),
      avg_response_time_min: randFloat(2, 15),
      csat_score: randFloat(3.5, 5.0),
      agents: agents.map(name => ({
        name,
        tickets_handled: randInt(10, 80),
        avg_resolution_min: randFloat(5, 30),
        csat: randFloat(3.5, 5.0)
      }))
    };
  }


  }


  }

  // --- LIVE API FETCHERS ---

  async function fetchMeta(options = {}) {
    const token = getToken('meta_page_token');
    const pageId = options.pageId || getToken('meta_page_id');
    if (!token || !pageId) return simulateFacebook(pageId || '0');
    try {
      const base = 'https://graph.facebook.com/v21.0';
      const fields = 'id,name,fan_count,talking_about_count';
      const res = await fetch(base + '/' + pageId + '?fields=' + fields + '&access_token=' + token);
      if (!res.ok) throw new Error('Meta API error: ' + res.status);
      const pageData = await res.json();
      const since = options.since || Math.floor((Date.now() - 30*86400000)/1000);
      const until = options.until || Math.floor(Date.now()/1000);
      const insightsRes = await fetch(base + '/' + pageId + '/insights?metric=page_impressions,page_engaged_users,page_post_engagements,page_video_views,page_fan_adds,page_fan_removes&period=day&since=' + since + '&until=' + until + '&access_token=' + token);
      let insights = {};
      if (insightsRes.ok) {
        const idata = await insightsRes.json();
        (idata.data || []).forEach(m => { insights[m.name] = m.values; });
      }
      return { platform: 'facebook', ...pageData, insights, daily_data: [] };
    } catch(e) {
      console.warn('Meta fetch failed, using simulated:', e.message);
      return simulateFacebook(pageId);
    }
  }


  async function fetchInstagram(options = {}) {
    const token = getToken('meta_page_token');
    const igUserId = options.igUserId || getToken('meta_ig_user_id');
    if (!token || !igUserId) return simulateInstagram(igUserId || '0');
    try {
      const base = 'https://graph.facebook.com/v21.0';
      const res = await fetch(base + '/' + igUserId + '?fields=id,username,followers_count,media_count&access_token=' + token);
      if (!res.ok) throw new Error('Instagram API error: ' + res.status);
      const data = await res.json();
      return { platform: 'instagram', ...data, daily_data: [] };
    } catch(e) {
      console.warn('Instagram fetch failed, using simulated:', e.message);
      return simulateInstagram(igUserId);
    }
  }

  async function fetchYouTube(options = {}) {
    const key = getToken('youtube_api_key');
    const channelId = options.channelId || getToken('youtube_channel_id');
    if (!key || !channelId) return simulateYouTube(channelId || '0');
    try {
      const base = 'https://www.googleapis.com/youtube/v3';
      const res = await fetch(base + '/channels?part=snippet,statistics&id=' + channelId + '&key=' + key);
      if (!res.ok) throw new Error('YouTube API error: ' + res.status);
      const data = await res.json();
      const item = (data.items || [])[0];
      if (!item) return simulateYouTube(channelId);
      return {
        platform: 'youtube',
        channel_id: channelId,
        title: item.snippet.title,
        subscribers: parseInt(item.statistics.subscriberCount || '0'),
        total_views: parseInt(item.statistics.viewCount || '0'),
        video_count: parseInt(item.statistics.videoCount || '0'),
        daily_data: []
      };
    } catch(e) {
      console.warn('YouTube fetch failed, using simulated:', e.message);
      return simulateYouTube(channelId);
    }
  }

  async function fetchTikTok(options = {}) {
    const username = options.username || getToken('tiktok_username');
    if (!username) return simulateTikTok('hospital');
    return simulateTikTok(username);
  }

  async function fetchThreads(options = {}) {
    const username = options.username || getToken('threads_username');
    if (!username) return simulateThreads('hospital');
    return simulateThreads(username);
  }

  async function fetchQontak(options = {}) {
    const token = getToken('qontak_token');
    if (!token) return simulateQontak();
    try {
      const base = 'https://service-chat.qontak.com/api/open/v1';
      const headers = { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' };
      const statsRes = await fetch(base + '/broadcasts/statistics', { headers });
      if (!statsRes.ok) throw new Error('Qontak API error: ' + statsRes.status);
      const stats = await statsRes.json();
      return { platform: 'whatsapp', ...stats, daily_data: [] };
    } catch(e) {
      console.warn('Qontak fetch failed, using simulated:', e.message);
      return simulateQontak();
    }
  }


  // --- POLLING ---
  let pollingIntervals = {};

  function startPolling(intervals = {}) {
    stopPolling();
    const defaults = { meta: 300000, youtube: 300000, tiktok: 60000, threads: 60000, qontak: 15000 };
    const cfg = { ...defaults, ...intervals };
    const fetchers = { meta: fetchMeta, youtube: fetchYouTube, tiktok: fetchTikTok, threads: fetchThreads, qontak: fetchQontak };

    Object.keys(cfg).forEach(platform => {
      if (cfg[platform] > 0 && fetchers[platform]) {
        pollingIntervals[platform] = setInterval(() => {
          fetchers[platform]().then(data => {
            window.dispatchEvent(new CustomEvent('hospital-data-update', { detail: { platform, data } }));
          });
        }, cfg[platform]);
      }
    });
    localStorage.setItem(POLL_KEY, JSON.stringify(cfg));
  }

  function stopPolling() {
    Object.values(pollingIntervals).forEach(clearInterval);
    pollingIntervals = {};
  }

  // --- PUBLIC API ---
  return {
    setToken, getToken, getConnectionStatus,
    fetchMeta, fetchInstagram, fetchYouTube, fetchTikTok, fetchThreads, fetchQontak,
    startPolling, stopPolling,
    simulateFacebook, simulateInstagram, simulateYouTube, simulateTikTok, simulateThreads, simulateQontak
  };
})();
