# Plugins

Host-specific packs. Canonical skills live in [`skills/`](../skills/) and are synced into each plugin.

| Directory | Host | Install |
|---|---|---|
| [`openclaw/`](openclaw/) | OpenClaw | `openclaw plugins install @pinchtab/pinchtab` |
| [`grok/`](grok/) | Grok Build | `grok plugin install pinchtab/pinchtab#plugins/grok --trust` |

```bash
node plugins/sync-skills.mjs          # copy skills into both plugins
node plugins/sync-skills.mjs grok     # Grok only (committed)
node plugins/sync-skills.mjs grok --check
```

OpenClaw also syncs on `npm pack` / `npm test` via `plugins/openclaw/scripts/sync-skills.mjs`. Those copies are gitignored. Grok copies are committed so a git `#plugins/grok` install includes the skills.
