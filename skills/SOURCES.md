# Skill Library — Sources & Provenance

This library was originally assembled on 2026-08-06 and has since been systematically expanded into the 7 Sovereign Houses. Every skill folder contains a `SKILL.md` and follows the standard Agent Skills format. Current library size: **2,150+ skills** across 7 Sovereign Houses (2,146 verified in `skills/manifest.sha256`; 2,600+ discovered across companion roots).

## Original set (95 skills + 1 stub)

Downloaded from the [skills.sh](https://skills.sh) registry (Agent Skills Directory). Archive of the original download manifest is kept in `_archive/` (`download_log.txt`, `download_summary.json`, `all_slugs.json`).

> Note: the original download only produced 16-byte placeholder files for 126 slug entries; the real content (95 skills) lived in an `uncategorized/` folder. This library flattened and repaired that structure. The `code-quality` slug was unrecoverable and was rewritten as a fresh skill.

## Merged open-source repositories (2026-08-06, `--depth 1` clones)

| Repository | Skills contributed (examples) |
|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | algorithmic-art, brand-guidelines, canvas-design, doc-coauthoring, docx, frontend-design, mcp-builder, pdf, pptx, skill-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx, ... |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | find-skills |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | deploy-to-vercel, react-best-practices, react-native-skills, react-view-transitions, web-design-guidelines, ... |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | agent-browser |
| [microsoft/azure-skills](https://github.com/microsoft/azure-skills) | azure-ai, azure-deploy, azure-diagnostics, azure-observability, azure-prepare, azure-validate, azure-storage, azure-kusto, appinsights-instrumentation, entra-agent-id, ... (37 skills) |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | dev |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | supabase-postgres-best-practices |
| [prisma/skills](https://github.com/prisma/skills) | prisma-cli, prisma-database-setup, prisma-postgres, prisma-upgrade-v7, ... |
| [firebase/agent-skills](https://github.com/firebase/agent-skills) | firebase-security-rules-auditor |
| [get-convex/agent-skills](https://github.com/get-convex/agent-skills) | convex-* (30+ skills) |
| [shadcn/ui](https://github.com/shadcn/ui) | shadcn |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | ui-ux-pro-max, banner-design, brand, design, design-system, slides, ui-styling |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | design-taste-frontend, gpt-taste, minimalist-ui, industrial-brutalist-ui, stitch-design-taste, ... |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | impeccable |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | remotion-best-practices, remotion-create, remotion-multimedia, remotion-render, remotion-studio, remotion-upgrade, ... (12 skills) |
| [skills-collective/skills](https://github.com/skills-collective/skills) | ai-video-generation, ai-image-generation, ai-music, flux-2-klein, kling-3-0, seedance-v2, ... |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | marketing-* suite (60+ skills) |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | emil-design-eng |
| [arvindrk/extract-design-system](https://github.com/arvindrk/extract-design-system) | extract-design-system |
| [browser-act/skills](https://github.com/browser-act/skills) | browser-act, browser-act-skill-forge + e-commerce scraping solutions (100+ amazon/ebay/etsy/1688/airbnb/facebook/douyin skills) |
| [scrapegraphai/just-scrape](https://github.com/scrapegraphai/just-scrape) | just-scrape |
| [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | higgsfield-generate, higgsfield-game-generation, higgsfield-video-explainer, ... |
| [lllllllama/rigorpilot-skills](https://github.com/lllllllama/rigorpilot-skills) | rigorpilot-* |
| [lllllllama/ai-paper-reproduction-skill](https://github.com/lllllllama/ai-paper-reproduction-skill) | ai-research-reproduction |
| [magentosh/skills](https://github.com/magentosh/skills) | ads, emails, sms, video, social, image, ai-podcast, ai-content-pipeline, ... |
| [mattpocock/skills](https://github.com/mattpocock/skills) | brainstorming, tdd, handoff, grill-me, to-spec, to-tickets, code-review, diagnosing-bugs, ... |
| [obra/superpowers](https://github.com/obra/superpowers) | superpowers skill suite (writing-plans, writing-skills, brainstorming, systematic-debugging, test-driven-development, ...) |
| [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) | caveman, caveman-commit, caveman-compress, caveman-review, cavecrew, ... |
| [larksuite/cli](https://github.com/larksuite/cli) | lark-approval, lark-base, lark-doc, lark-im, lark-sheets, lark-wiki, lark-vc, ... (28 skills) |

## Agent packs (2026-08-06, second merge — persona/config packs)

Skills extracted from ready-to-drop agent configuration packs (full packs kept in `ai-agents-handbook/packs/`):

| Pack | Skills added |
|---|---|
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 39 (api-design, backend-patterns, coding-standards, deep-research, e2e-testing, eval-harness, mcp-server-patterns, security-review, tdd-workflow, ...) |
| [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) | 6 (ponytail, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help, ponytail-review) |
| [bitjaru/styleseed](https://github.com/bitjaru/styleseed) | 23 (ss-a11y … ss-verify, styleseed-design-review) |
| [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) | 4 (web-design-engineer, beautiful-article, kb-retriever, web-video-presentation; `gpt-image-2` already present) |
| [JimLiu/baoyu-design](https://github.com/JimLiu/baoyu-design) | 2 (baoyu-design, release-skills) |
| [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design) | 1 (huashu-design) |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 1 (karpathy-guidelines) |

## Agent Reach (2026-10-01)

Skills extracted from Agent Reach — Internet capability router for AI agents:

| Source | Skills added |
|---|---|
| [Panniantong/Agent-Reach](https://github.com/Panniantong/agent-reach) | `agent-reach` (Internet search/read for 16 platforms: Twitter, Reddit, YouTube, B站, 小红书, GitHub, RSS, etc.) |


## Albo Imports (2026-08-07)

Skills created from Albo imports:

| Source URL | Skills added |
|---|---|
| [UI Libraries Instead of AI Generation](https://albo.inc/imports/a9e5a0b4-b81e-50fb-ba9e-1364de86b775) | `driver-js`, `react-bits`, `tailark`, `assistant-ui` |
| [Automate Motion Design](https://albo.inc/imports/bd314169-7480-5635-93e9-e20f6e86dab7) | `motion-ai` |

## Web sweep additions (2026-08-11)

Skills found during a thorough audit of the `ai-agents-handbook/references/` awesome-lists, installed via sparse `git clone --depth 1`.

| Repository | Skills contributed |
|---|---|
| [google/skills](https://github.com/google/skills) | 103 skills across `cloud/`, `ads/`, `analytics/` — GKE (30+), Cloud SQL/AlloyDB/BigQuery basics, Gemini API, Google Agent Platform, Well-Architected Framework, Google Ads/Mobile Ads, Google Analytics. |
| [resend/resend-skills](https://github.com/resend/resend-skills) | 5 (resend, resend-cli, react-email, email-best-practices, agent-email-inbox) |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 25 (hyperframes, hyperframes-core, general-video, product-launch-video, faceless-explainer, talking-head-recut, motion-graphics, music-to-video, slideshow, embedded-captions, figma, captions-overlay, changelog-video, cut-the-curve, media-use, motion-doctrine, oversized-cursor, pr-to-video, remotion-to-hyperframes, seam-craft, hyperframes-cli, hyperframes-creative, hyperframes-keyframes, hyperframes-registry, hyperframes-animation) |

## Not merged

- `sentry/dev` — repository returned 404 (private or renamed); skills can be added when access is available.
- `lllllllama/rigorpilot-skills` — uses `.claude/commands/*.md` (slash-command format) rather than `SKILL.md`; its intent is covered by the merged `ai-research-explore` / `ai-research-reproduction` / `analyze-project` skills from the ai-paper-reproduction repo.
