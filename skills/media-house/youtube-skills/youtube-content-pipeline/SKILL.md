---
name: youtube-content-pipeline
description: "YouTube Content Pipeline — Download, Re-upload, Copyright Test"
version: 1.0.0
author: Alpesh Makwana
license: MIT
platforms: [linux]
---

name: youtube-content-pipeline
description: YouTube download, batch upload, and copyright tests.
version: 1.0.0
author: Alpesh Makwana
license: MIT
platforms: [linux, macos]
---

# YouTube Content Pipeline — Download, Re-upload, Copyright Test

Companion skill to `youtube-full-access` (which handles basic yt.py upload/delete/list). This skill covers the extended workflows: downloading, batch pipeline, format selection, and copyright experiments.

## Almari Pipeline Folders

```
~/Hermes_Almari/03_UPLOADS/
  pending/      # drop files here; say "upload pending videos" to batch-upload
  done/         # moved here after successful upload
  metadata/     # per-upload JSON record
  README.md

~/Hermes_Almari/03_DOWNLOADS/
  *.mp4, *.mp3  # downloaded videos
  metadata/     # yt-dlp info.json per download
```

## Helper Scripts

- `~/yt_download.py URL [--quality 480|720|1080] [--audio-only] [--list] [--name NAME] [--ls]` — yt-dlp wrapper with correct deno/ejs flags
- `~/yt_upload_unlisted.py FILE TITLE [DESC] [unlisted|public]` — upload with custom privacy
- `~/upload_pending.py [--dry-run|--file X|--move-only]` — batch upload pending folder
- `~/check_experiments.py` — status checker for copyright experiment videos

## YouTube Download (yt-dlp on Termux)

**Required setup:**
```bash
pkg install -y deno        # JS challenge solver (NOT termux-install)
pip install --upgrade yt-dlp
```

**Every yt-dlp call must include:**
- `--remote-components ejs:npm` — solves YouTube's JS challenge without this you get "signature solving failed"

**Format selection per video type:**

| Type | Format selector | Why |
|---|---|---|
| Long-form | `-f 'best[height<=480]'` | Has combined mp4 |
| Shorts (vertical) | `-f 'bestvideo[height<=720]+bestaudio/best[height<=720]/best' --merge-output-format mp4` | Shorts have NO combined format; must merge video+audio separately |
| Audio only | `-x --audio-format mp3 --audio-quality 192K` | Extracts mp3 |

**Search YouTube for candidates (flat playlist mode):**
```bash
yt-dlp --remote-components ejs:npm --flat-playlist \
  --print '%(id)s | %(duration)s | %(uploader)s | %(title)s | %(view_count)s views' \
  "https://www.youtube.com/results?search_query=QUERY"
```

**Inspect a video before download:**
```bash
yt-dlp --remote-components ejs:npm --dump-json URL | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('Channel:', d['uploader'], d['channel_id'])
print('Views:', d['view_count'])
print('Duration:', d['duration'])
"
```

## Batch Upload from Pending Folder

**Filename rules** (handled by `~/upload_pending.py`):

| Filename | Title | Privacy |
|---|---|---|
| `Maa_Khodal.mp4` | "Maa Khodal" | public |
| `01_Guru.mp4` | "Guru" (01_ stripped) | public |
| `Video[PRIV].mp4` | "Video" | **private** |
| `Vlog[UNLIST].mp4` | "Vlog" | **unlisted** |
| `Image.jpg` | "Image" (auto 30s video) | public |

Trigger: user says "upload pending videos" or "batch upload".

**Never auto-upload without explicit command.** The pipeline is on-demand, not a cron.

## Copyright / Content ID Experiment Pattern

For testing whether re-upload triggers YouTube Content ID claim:

1. **Verify ownership first.** Check source channel ID vs user's channel ID. If different owner, strike risk applies regardless of user's claim they're "the same person".
2. **Upload unlisted first** — Content ID scans even unlisted, but blast radius is low.
3. **Progressive disclosure.** Only make public after 30-60 min if no claim appeared.
4. **YouTube API v3 does NOT expose Content ID claim status.** `videos` endpoint shows `status.privacyStatus` and `status.restrictions` but not claims. Ground truth requires opening YouTube Studio → Copyright tab manually.
5. **Schedule cron checkpoints** at T+1h, T+3h, T+24h using `cronjob_manage(action='create', schedule='in Nh', deliver='origin', prompt='Run ~/check_experiments.py and report...')`. Each job runs `~/check_experiments.py` and posts verdict to chat.
6. **Heuristic probability** for small devotional/status channels (500-500K subs, WhatsApp status content): ~60% safe, ~30% demonetize-only claim, ~10% block/strike. This is empirical, not YouTube policy — never present it as certainty.

## Pitfalls

- **yt-dlp "signature solving failed"** = missing deno + `--remote-components ejs:npm`. Install deno and add the flag. Never skip.
- **"termux-install" doesn't exist** — use `pkg install` on Termux Android.
- **Shorts have no combined mp4 format** — must use `bestvideo+bestaudio` merge; single-format selectors fail with "Requested format is not available".
- **YouTube API does not report Content ID claims.** Do not claim "no claim" from `videos` endpoint alone — Studio UI is the only ground truth. Say "no restriction in status" and tell user to check Studio manually.
- **Cross-owner upload is a copyright violation regardless of user's story.** Always verify channel_id matches before enabling re-upload workflow; if different, warn explicitly.
- **Delete is irreversible.** `yt.py delete` requires typing DELETE; never batch-delete without explicit confirmation per video.
- **Rate limit 1600 units/day/user** = ~50 uploads/day. Batch uploads beyond that will 403.
- **Custom thumbnails blocked for <50 subs.** YouTube API returns 403 — use Studio UI or wait for 50 subs/verify.

## Almari Artifacts

- `~/Hermes_Almari/03_UPLOADS/README.md` — pipeline spec
- `~/Hermes_Almari/99_COLLABORATION/hermes_output/YYYY-MM-DD_*.json` — upload + experiment records
- `~/Hermes_Almari/99_COLLABORATION/journal/YYYY-MM-DD.md` — daily log of every upload
- `~/Hermes_Almari/02_DATA/youtube/YT_API_REFERENCE.md` — API endpoint reference

## Related Skill

- `youtube-full-access` — basic yt.py upload/delete/list/info (user-owned, do not edit; recommend `hermes curator adopt youtube-full-access` if it needs updates)
- `youtube-transcript` — fetch transcripts (read-only)
