/**
 * Settings Panel Logic
 * Manages API key configuration via localStorage.
 */
const Settings = (() => {
  const STORAGE_KEY = 'hospital_connector_tokens';
  const FIELDS = [
    { id: 'meta_page_id', label: 'Meta Page ID', placeholder: '1234567890', group: 'Meta (Facebook + Instagram)' },
    { id: 'meta_page_token', label: 'Meta Page Access Token', placeholder: 'EAA...', group: 'Meta (Facebook + Instagram)', type: 'password' },
    { id: 'youtube_channel_id', label: 'YouTube Channel ID', placeholder: 'UC...', group: 'YouTube' },
    { id: 'youtube_api_key', label: 'YouTube API Key', placeholder: 'AIza...', group: 'YouTube', type: 'password' },
    { id: 'tiktok_username', label: 'TikTok Username', placeholder: '@hospital', group: 'TikTok (Browser Scraped)' },
    { id: 'threads_username', label: 'Threads Username', placeholder: '@hospital', group: 'Threads (Browser Scraped)' },
    { id: 'qontak_token', label: 'Mekari Qontak Token', placeholder: 'Bearer...', group: 'WhatsApp (Qontak)', type: 'password' }
  ];
  function getValues() { try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch { return {}; } }
  function save(key, value) { const t = getValues(); if (value) t[key] = value; else delete t[key]; localStorage.setItem(STORAGE_KEY, JSON.stringify(t)); }
  function getStatus() { const t = getValues(); return { meta: !!(t.meta_page_token && t.meta_page_id), youtube: !!(t.youtube_api_key && t.youtube_channel_id), tiktok: !!t.tiktok_username, threads: !!t.threads_username, qontak: !!t.qontak_token }; }
  function renderPanel(containerId) {
    const c = document.getElementById(containerId); if (!c) return;
    const v = getValues(), s = getStatus();
    let h = '<div class="settings-panel"><h3>API Configuration</h3>';
    let g = '';
    FIELDS.forEach(f => {
      if (f.group !== g) { g = f.group; h += '<div class="settings-group"><h4>' + f.group + '</h4>'; }
      const tp = f.type || 'text';
      h += '<div class="settings-field"><label>' + f.label + '</label><input type="' + tp + '" id="setting_' + f.id + '" value="' + (v[f.id]||'') + '" placeholder="' + f.placeholder + '" onchange="Settings.saveField(\'' + f.id + '\', this.value)" /></div>';
    });
    h += '</div><div class="settings-status"><h4>Connection Status</h4>';
    Object.entries(s).forEach(([k, v2]) => { h += '<span class="status-badge ' + (v2 ? 'connected' : 'disconnected') + '">' + k + ': ' + (v2 ? 'Connected' : 'Not Configured') + '</span> '; });
    h += '</div></div>';
    c.innerHTML = h;
  }
  function saveField(k, v) { save(k, v); }
  function exportConfig() { const b = new Blob([JSON.stringify(getValues(), null, 2)], { type: 'application/json' }); const u = URL.createObjectURL(b); const a = document.createElement('a'); a.href = u; a.download = 'hospital-dashboard-config.json'; a.click(); URL.revokeObjectURL(u); }
  function importConfig() { const i = document.createElement('input'); i.type = 'file'; i.accept = '.json'; i.onchange = e => { const r = new FileReader(); r.onload = ev => { try { const d = JSON.parse(ev.target.result); localStorage.setItem(STORAGE_KEY, JSON.stringify(d)); location.reload(); } catch(err) { alert('Invalid config file'); } }; r.readAsText(e.target.files[0]); }; i.click(); }
  return { getValues, save, getStatus, renderPanel, saveField, exportConfig, importConfig };
})();
