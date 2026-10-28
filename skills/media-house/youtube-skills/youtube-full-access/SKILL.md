---
name: youtube-full-access
description: "YouTube Full Access — Alpesh's Channel"
version: 1.0.0
author: Alpesh Makwana
license: MIT
platforms: [linux]
---

name: youtube-full-access
description: Use for YouTube video upload, delete, and channel work.
version: 1.0.0
author: Alpesh Makwana
license: MIT
platforms: [linux, macos]
---

# YouTube Full Access — Alpesh's Channel

## Setup

Token file: `~/.youtube_token.json` (chmod 600)
CLI: `~/yt.py` (chmod +x)
Channel: Alpesh Makwana (`UCsfMATdjAtTdeVH0J4KdlnA`)
OAuth client: `917626090327-2stg62jak40p3lh0p9mo63fb737dfh17`

## Quick Commands

```bash
~/yt.py info              # channel stats
~/yt.py list [N]          # last N uploads
~/yt.py upload FILE TITLE [DESC]  # upload (PUBLIC by default)
~/yt.py setpublic VID_ID  # make public
~/yt.py delete VID_ID     # delete (safety prompt)
~/yt.py comment VID_ID TEXT   # comment
~/yt.py refresh           # force token refresh
```

## Image → Video Workflow

YouTube only accepts video. Convert images with ffmpeg:

```bash
ffmpeg -loop 1 -i IMAGE.jpg -vf "scale=720:-2,format=yuv420p" \
  -t 30 -r 30 -c:v libx264 -preset veryfast -crf 28 -pix_fmt yuv420p \
  OUTPUT.mp4
```

## Thumbnail Extraction

For auto-thumbnail from video frame:
```bash
ffmpeg -ss 5 -i VIDEO.mp4 -frames:v 1 THUMB.png -y
```

## Custom Thumbnails Limitation

YouTube blocks custom thumbnails via API for channels with <50 subs:
```
HTTP 403: doesn't have permissions to upload custom thumbnails
```

**Workaround:** Upload via YouTube Studio UI, OR wait for 50 subs, OR channel verify.

## Token Refresh (auto, every 60 min)

Token expires every 3599 sec. Refresh with client_id + client_secret + refresh_token.
Refresh_token is permanent — never expires unless revoked.

## Upload Format (multipart)

YouTube requires 2 parts: JSON metadata + binary video.
```python
{
  'snippet': {'title': T, 'description': D, 'tags': [...], 'categoryId': '26', 'defaultLanguage': 'hi'},
  'status': {'privacyStatus': 'public', 'embeddable': True, 'license': 'youtube'}
}
```

Endpoint: `POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status`
Headers: `Authorization: Bearer <token>`, `Content-Type: multipart/related; boundary=X`

## Categories (Top Used)

- 26: People & Blogs
- 10: Music
- 24: Entertainment
- 22: People & Blogs
- 28: Science & Technology
- 25: News & Politics
- 17: Sports

## Delete Safety

DELETE is IRRECOVERABLE. `yt.py delete` requires typing `DELETE` to confirm.
Fetches title first, prints warning, then deletes.

## Reference Files (Almari)

- `~/Hermes_Almari/99_COLLABORATION/hermes_output/` — upload records
- `~/.youtube_env` — credential reference
- `~/Hermes_Almari/02_DATA/youtube/` — video metadata cache

## Pitfalls

- **`snippet` in URL params = unexpectedPart error** → use `part=snippet,status` in URL
- **3-part multipart with thumbnail = error** → upload video first, then thumbnail separately
- **Custom thumbnails blocked** for <50 subs — YouTube auto-generates default
- **Duration: None** after upload = still processing (5-10 min)
- **Privacy default in yt.py = PUBLIC** (per user preference)
- **Rate limit**: YouTube allows 1600 units/day per user (~50 uploads/day)

## Full API Reference

See `~/Hermes_Almari/02_DATA/youtube/YT_API_REFERENCE.md` for full endpoints.
