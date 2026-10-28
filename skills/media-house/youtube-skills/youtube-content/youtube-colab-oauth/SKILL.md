---
name: youtube-colab-oauth
description: "YouTube OAuth from Google Colab (Full Scope Access)"
version: 1.0.0
author: Alpesh Makwana
license: MIT
platforms: [linux]
---

name: youtube-colab-oauth
description: Use when setting up YouTube full-scope OAuth via Colab.
version: 1.0.0
author: Alpesh Makwana
license: MIT
platforms: [linux, macos]
---

# YouTube OAuth from Google Colab (Full Scope Access)

Get `youtube_token.json` with all four scopes (youtube, youtube.upload, youtube.force-ssl, youtube.readonly) from Google Colab. This is the only flow that works because Colab has no browser and `run_local_server()` can't reach an external browser callback.

## When to Use

- User wants to upload/delete YouTube videos programmatically from Termux
- User has OAuth Client ID + Secret in a Desktop-type OAuth client
- User is on Colab and standard auth methods fail
- User asks about `run_local_server`, `get_user_credentials`, or `authenticate_user(scopes=)`

## Prerequisites

- OAuth Client ID (Desktop type) + Client Secret from Google Cloud Console
- Consent screen set to **External** (Internal gives `403 org_internal`)
- User added to **Test users** in the Consent screen Testing section
- Scopes registered in the client (add all 4)
- Google Cloud project's YouTube API v3 enabled

**Verify these exist before starting** — most failures come from missing setup, not code.

## The Working Flow (Manual Localhost URL Paste-Back)

### Why other approaches fail

| Approach | Why It Fails |
|---|---|
| `flow.run_local_server(port=0)` | Colab has no browser to open the auth URL |
| `colab_auth.get_user_credentials(scopes=)` | Removed in current `google.colab.auth` |
| `colab_auth.user_credentials(scopes=)` | Doesn't exist |
| `colab_auth.authenticate_user(scopes=SCOPES)` | Only accepts `scopes` as positional; errors out |
| `flow.run_console(message=)` | Not a real attribute |
| Device Authorization Flow | Only allows `youtube` + `youtube.readonly` — missing `youtube.force-ssl` needed for comments insert |

The manual flow below sidesteps all of these. It uses the installed-app `http://localhost` redirect URI, but does NOT need a callback listener — after Google approves, the browser may show a localhost connection error, but the authorization code is in the address bar. Copy and paste it back into Colab.

### Full script (paste into one Colab cell)

```python
import json, os, subprocess, sys
from urllib.parse import urlparse, parse_qs

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q',
    'google-auth-httplib2', 'google-auth-oauthlib', 'google-api-python-client'])

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.colab import files

CLIENT_ID = '<YOUR_CLIENT_ID>'
CLIENT_SECRET = '<YOUR_CLIENT_SECRET>'

REDIRECT_URI = 'http://localhost'
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.readonly',
]

client_config = {
    'web': {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'redirect_uris': [REDIRECT_URI],
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
flow.redirect_uri = REDIRECT_URI
auth_url, state = flow.authorization_url(
    access_type='offline', prompt='consent', include_granted_scopes='false')

print('1) Open this URL and approve all YouTube scopes:')
print(auth_url)
print('\n2) After approval, browser may show localhost connection error.')
print('   Copy the COMPLETE URL from the browser address bar.')
callback = input('\n3) Paste the complete localhost URL here: ').strip()

if callback.startswith('http://') or callback.startswith('https://'):
    query = parse_qs(urlparse(callback).query)
    returned_state = query.get('state', [''])[0]
    if returned_state and returned_state != state:
        raise RuntimeError('OAuth state mismatch; restart and don\'t reuse URL.')
    if 'error' in query:
        raise RuntimeError(f"Google auth failed: {query['error'][0]}")
    flow.fetch_token(authorization_response=callback)
else:
    if not callback:
        raise ValueError('No callback URL provided.')
    flow.fetch_token(code=callback)

creds = flow.credentials
if not creds.refresh_token:
    raise RuntimeError('No refresh token. Re-run with prompt=consent and approve.')

token_path = '/content/youtube_token.json'
with open(token_path, 'w') as f:
    f.write(creds.to_json())

print('\nAUTH SUCCESS')
for scope in (creds.scopes or []):
    print(' -', scope)
files.download(token_path)

youtube = build('youtube', 'v3', credentials=creds)
response = youtube.channels().list(part='snippet', mine=True).execute()
print(f'\nYouTube API test: {len(response.get("items", []))} channel(s) found.')
```

## Steps to Execute

1. Open Colab notebook, paste script into single cell
2. Run cell — an auth URL will print
3. Copy URL → open in browser → sign in with target account → approve all scopes
4. Browser will show a localhost connection error — that is expected and correct
5. Copy the **full URL from the browser address bar** (including `?code=...&state=...`)
6. Paste into Colab input prompt → cell continues
7. Output: `AUTH SUCCESS` + scopes list + `youtube_token.json` auto-downloads + channel list

## Pitfalls

- **`redirect_uri_mismatch` error**: your registered client redirect URIs must include the exact string `http://localhost` (with the trailing slash matching what you set in `redirect_uris`). Desktop-type clients usually come with this preset; if you added a different one, remove extras and keep just `http://localhost`.
- **`access_denied` from Google**: consent screen is in Testing mode and your email is not in Test users. Add yourself, then Publish App Version.
- **`org_internal` error**: consent screen is set to Internal. Switch to External.
- **`invalid_request` with device auth**: device code flow limits YouTube scopes to `youtube` and `youtube.readonly` — you'll never get `youtube.force-ssl` via device flow. Use this manual localhost flow instead.
- **Refresh token missing**: Google won't issue refresh tokens unless you pass `access_type='offline'` AND `prompt='consent'` on the auth URL. The script above does both — don't remove them.
- **State mismatch on reuse**: the auth URL contains a fresh state token each run. Do not reuse a callback URL from a previous run.
- **Token download missing**: `files.download(token_path)` requires Colab runtime; if running on a different runtime, copy the JSON content manually.

## After Download — Save to Termux

```bash
# Once you have youtube_token.json on your phone, save it and verify
mv ~/Downloads/youtube_token.json ~/.youtube_token.json

# Verify
python3 -c "
from google.auth.credentials import Credentials
import json
d = json.load(open('/root/.youtube_token.json'))
c = Credentials(d['token'], refresh_token=d['refresh_token'], token_uri=d['token_uri'], client_id=d['client_id'], client_secret=d['client_secret'], scopes=d['scopes'])
from googleapiclient.discovery import build
yt = build('youtube', 'v3', credentials=c)
ch = yt.channels().list(part='snippet', mine=True).execute()
print(f'Verified: {len(ch.get(\"items\", []))} channel(s)')
for x in ch.get('items', []): print(' -', x['snippet']['title'])
"
```

## Reference

- Installed-app OAuth: https://developers.google.com/youtube/v3/guides/auth/installed-apps
- Device flow limits: https://developers.google.com/youtube/v3/guides/auth/devices
- Comments.insert requires force-ssl: https://developers.google.com/youtube/v3/docs/comments/insert
