# Agent Skills Library — Master Index

Total skills: **2,150+ skills** organized across 7 Sovereign Houses (see [HOUSES.md](./HOUSES.md) for the master domain architecture; see [SOURCES.md](./SOURCES.md) for provenance).

Each entry is a folder containing `SKILL.md` (plus optional `references/`, `scripts/`). Load a skill by matching its folder name to the task. Sources and provenance: see [SOURCES.md](./SOURCES.md).

---

## Browser Automation, Scraping & E-commerce (61)

| Skill | Description |
|---|---|
| `1688-product-detail` | "Extracts comprehensive wholesale product data from 1688.com product detail pages: title, tiered pricing, SKU variants with dimensions/weight, product images... |
| `agent-browser` | Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking ... |
| `airbnb-listing-detail` | "Fetches complete Airbnb listing details for a given numeric listing ID via the internal GraphQL API, returning title, room type, description, amenities, pho... |
| `airbnb-search-listing` | "Extracts Airbnb accommodation search results from a destination query via SSR-embedded data, returning listing ID, URL, name, coordinates, rating, price, ph... |
| `amazon-alexa-qa` | "Amazon Alexa for Shopping Q&A automation: submits questions to Amazon's Alexa/Rufus AI shopping assistant and collects response text; supports optional keyw... |
| `amazon-asin-lookup-api-skill` | "This skill helps users extract structured product details from Amazon using a specific ASIN (Amazon Standard Identification Number). Use this skill when the... |
| `amazon-best-selling-products-finder-api-skill` | "This skill helps users extract structured best-selling product data from Amazon via the BrowserAct API. Agent should proactively apply this skill when users... |
| `amazon-bestseller-listing` | "Amazon Best Sellers listing scraper: extract product cards from any Amazon Best Sellers (zgbs) or /gp/bestsellers/ category page — returns rank (position on... |
| `amazon-buy-box-monitor-api-skill` | "This skill helps users extract basic product details other sellers prices and seller ratings from Amazon via ASIN automatically using the BrowserAct API. Ag... |
| `amazon-competitor-analyzer` | Scrapes Amazon product data from ASINs using browseract.com automation API and performs surgical competitive analysis. Compares specifications, pricing, revi... |
| `amazon-listing-competitor-analysis-skill` | "This skill helps users analyze Amazon competitor listings by ASIN and produce structured competitive intelligence plus strategic opportunity points for thei... |
| `amazon-product-api-skill` | "This skill helps users extract structured product listings from Amazon, including titles, ASINs, prices, ratings, and specifications. Use this skill when us... |
| `amazon-product-detail` | "Amazon product detail page scraper: extract full product data from any open Amazon product detail URL (any /dp/{asin} or /gp/product/{asin} page across all ... |
| `amazon-product-search-api-skill` | "This skill is designed to help users automatically extract product data from Amazon search results. The Agent should proactively apply this skill when users... |
| `amazon-reviews-api-skill` | "This skill helps users automatically extract Amazon product reviews via the Amazon Reviews API. Agent should proactively apply this skill when users express... |
| `amazon-search-listing` | "Amazon search and category listing scraper: extract product listings from any Amazon search results page, keyword search URL, or category browse page and re... |
| `browser-act` | "Browser automation CLI for AI agents. NEVER run browser-act commands directly via Bash — always invoke this skill first. Use browser-act when a user mention... |
| `browser-act-skill-forge` | "Forges reusable Skill packages (SKILL.md + scripts) from website exploration via browser-act — no re-exploration later. Use when: user wants a reusable Skil... |
| `browser-automation` | Browser automation powers web testing, scraping, and AI agent |
| `douyin-video-search` | "Searches Douyin (douyin.com) for videos by keyword and returns structured video data including author info, stats, cover, description, hashtags, and downloa... |
| `ebay-item-detail` | "Extracts full item detail from any open eBay item URL, returning JSON with url, itemNumber, title, subTitle, categories, price, priceWithCurrency, currency,... |
| `ebay-search-listing` | "Extracts product listings from any eBay search or category page URL, returning per-item cards (itemNumber, url, title, subtitle, caption, price, priceWithCu... |
| `ebay-sold-listings-search` | "eBay sold-listings scraper across 8 marketplaces (ebay.com/.co.uk/.de/.fr/.it/.es/.ca/.com.au). Takes keyword plus filters (category, price range, item cond... |
| `ecommerce-listing` | "Extract product list from any e-commerce category page, search results page, or keyword search with filters. Returns paginated product arrays with URL, name... |
| `ecommerce-product-detail` | "Extract complete product information from any e-commerce product page. Returns name, price, currency, brand, images, description, SKU/ASIN/EAN/UPC/GTIN/MPN ... |
| `ecommerce-reviews` | "Extract customer reviews from any e-commerce product page or reviews page. Returns reviewer name, star rating, date, review title, review body, verified pur... |
| `ecommerce-seller-info` | "Extract seller or merchant profile data from marketplace platform seller pages. Returns seller name, rating, review count, positive feedback percentage, joi... |
| `etsy-category-listing` | "Etsy category page scraper: given an Etsy category URL (e.g. https://www.etsy.com/c/jewelry) and optional page number, returns paginated product listings wi... |
| `etsy-keyword-search` | "Etsy keyword search scraper: given a search keyword and optional page number, returns paginated product listings with listingId, shopId, title, url, image, ... |
| `etsy-product-detail` | "Etsy product detail scraper: given an Etsy listing URL, returns full product detail including listingId, title, priceCurrent, priceOriginal, currency, image... |
| `etsy-shop-catalog` | "Etsy shop catalog scraper: given an Etsy shop URL (e.g. https://www.etsy.com/shop/{shop-name}) and optional page number, returns paginated product listings ... |
| `facebook-ads-library-search` | "Searches Meta Ad Library (Facebook/Instagram/WhatsApp ads) by keyword or Facebook page ID and extracts ad details including creatives, copy, CTA, publisher ... |
| `facebook-groups-scrape-posts` | "Scrapes posts from a Facebook group given a group URL, sort order, and desired count — returns structured post metadata including post_id, permalink, author... |
| `facebook-page-posts` | "Scrapes posts from any public Facebook Page timeline, returning structured data including post text, author info, engagement metrics (likes/comments/shares)... |
| `facebook-page-profile-posts` | "Scrapes posts from any public Facebook Page or personal Profile timeline, returning structured data including post text, author info with profile picture, e... |
| `go-playwright` | "Expert capability for robust, stealthy, and efficient browser automation using Playwright Go." |
| `goofish-item-detail` | "Extracts full detail data from a single Goofish (闲鱼/xianyu, goofish.com) second-hand item page. Input: item URL or item ID. Output: title, price, seller inf... |
| `goofish-search-list` | "Scrapes second-hand item search results from Goofish (闲鱼/xianyu, goofish.com) — China's largest second-hand marketplace. Input: keyword, optional sort/filte... |
| `indeed-job-search` | "Scrape job listings from Indeed.com by keyword, location, and country. Returns job title, company, salary, rating, description, benefits, and apply links. U... |
| `just-scrape` | Search, scrape, crawl, extract structured data, and monitor web pages via the ScrapeGraph AI CLI. Use when the user asks to search the web, scrape a webpage,... |
| `playwright-cli` | Automate browser interactions, test web pages and work with Playwright tests. |
| `taobao-keyword-search` | "Search Taobao and Tmall product listings by keyword, returning paginated product cards with title, price, shop, image, sales, and tags. Use when user asks t... |
| `taobao-product-detail` | "Fetch full product detail from a Taobao or Tmall product page by itemId, returning title, price, shop info, images, SKU variants, and product attributes. Us... |
| `taobao-shop-catalog` | "Browse a Taobao or Tmall shop's product catalog by shopId, returning paginated product listings with itemId and title. Use when user asks to scrape a Taobao... |
| `tiktok-hashtag-videos` | "TikTok hashtag video scraper: input a hashtag name → output paginated video list with full metadata (author profile, engagement stats, music, video meta, ha... |
| `tiktok-profile-videos` | "TikTok user profile video scraper: input a TikTok username → output the user's profile info plus paginated video list with full metadata (engagement stats, ... |
| `tiktok-search-videos` | "TikTok keyword search video scraper: input search keyword → output paginated video list with full metadata (author, engagement stats, music, video meta). Us... |
| `walmart-category-listing` | "Walmart category page scraper: input a walmart.com browse or category URL with optional page number, extract paginated product listings with itemId, url, ti... |
| `walmart-keyword-search` | "Walmart keyword search scraper: input a search keyword and page number, navigate to walmart.com search results, extract paginated product listings with item... |
| `walmart-product-detail` | "Walmart product detail page extractor: given a walmart.com product URL (walmart.com/ip/...), extract full product data including itemId, title, brand, model... |
| `web-search-scraper-api-skill` | "This skill helps users automatically extract complete Markdown content from any website via the BrowserAct Web Search Scraper API. The Agent should proactiv... |
| `webcrawler-deep-crawl` | "Deep-crawl any website from start URLs, return per-page LLM-ready text/markdown/HTML plus metadata (title, description, author, language, canonical URL, OG)... |
| `x-tweet-by-conversation` | "Collects every tweet in an X (Twitter) conversation thread given a conversation id (root tweet id) — the focal tweet plus all replies, sub-replies, and quot... |
| `x-tweet-by-handle` | "Scrapes tweets from an X (Twitter) user profile timeline given a handle, with selectable mode: tweets, tweets+replies, or media-only. Returns normalized per... |
| `x-tweet-by-url` | "Scrapes tweets from any X (Twitter) URL — search results, user profile, single tweet detail, or list timeline — and returns normalized per-tweet data with t... |
| `x-tweet-search` | "Scrapes tweets from X (Twitter) by search query, user handle, or direct URL — returns full tweet data including text, author info, engagement metrics, media... |
| `x-tweet-search-by-query` | "Searches X (Twitter) for tweets by free-form advanced query and returns a normalized tweet list with text, author profile, engagement counts, media, hashtag... |
| `xiaohongshu-note-detail` | "Fetch Xiaohongshu (RedNote / xhs) note detail and comments by note ID, returning title, description, author info, engagement stats, tags, and paginated comm... |
| `xiaohongshu-search` | "Search Xiaohongshu (RedNote / xhs) notes by keyword and return a paginated list with title, author, engagement stats (likes, collects, comments), cover imag... |
| `xiaohongshu-search-full` | "Search Xiaohongshu (XHS / RedNote) notes by keyword with full field extraction including body text, topics/tags, image list URLs, video stream URL, publish ... |
| `xiaohongshu-user-profile` | "Fetch Xiaohongshu (RedNote / xhs) user profile information and their published notes list by user ID, returning nickname, bio, follower/following counts, en... |

## Security & Intelligence (9)

| Skill | Description |
|---|---|
| `007` | Security audit, hardening, threat modeling (STRIDE/PASTA), Red/Blue Team, OWASP checks, code review, incident response, and infrastructure security for any p... |
| `accessibility-compliance-accessibility-audit` | "You are an accessibility expert specializing in WCAG compliance, inclusive design, and assistive technology compatibility. Conduct audits, identify barriers... |
| `active-directory-attacks` | "Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, late... |
| `adhx` | "Fetch any X/Twitter post as clean LLM-friendly JSON. Converts x.com, twitter.com, or adhx.com links into structured data with full article content, author i... |
| `aegisops-ai` | "Autonomous DevSecOps & FinOps Guardrails. Orchestrates Gemini 3 Flash to audit Linux Kernel patches, Terraform cost drifts, and K8s compliance." |
| `azure-compliance` | "Run Azure compliance and security audits with azqr plus Key Vault expiration checks. Covers best-practice assessment, resource review, policy/compliance val... |
| `extension-to-functions-codebase` | Skill for converting an installed Firebase Extension (or extension source) into a standalone Cloud Functions for Firebase codebase or publishable npm package... |
| `firebase-security-rules-auditor` | >- |
| `security-review` | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Pro... |

## Video, Audio & Image Generation (107)

| Skill | Description |
|---|---|
| `ace-step` | > |
| `affirmations` | "Reset your own trajectory when you're stuck, looping, or demoralized — read these affirmations, then re-ground and take one clean step. Use when: you've tri... |
| `ai-avatar-video` | > |
| `ai-image-generation` | > |
| `ai-marketing-videos` | "Create AI marketing videos for ads, promos, product launches, and brand content. Models: Veo, Seedance, Wan, FLUX for visuals, Kokoro for voiceover. Types: ... |
| `ai-music` | > |
| `ai-product-photography` | "Generate professional AI product photography and commercial images. Models: FLUX, Imagen 3, Grok, Seedream for product shots, lifestyle images, mockups. Cap... |
| `ai-social-media-content` | "Create AI-powered social media content for TikTok, Instagram, YouTube, Twitter/X. Generate: images, videos, reels, shorts, thumbnails, captions, hashtags. T... |
| `ai-video-generation` | > |
| `algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, gener... |
| `animate` | Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at all, what purpose, which too... |
| `animation-vocabulary` | Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a popover opens" → Pop... |
| `book-cover-design` | "Book cover design with genre-specific conventions, typography rules, and AI image generation. Covers fiction and non-fiction genres, sizing, thumbnail testi... |
| `character-design-sheet` | "Character consistency across AI-generated images with reference sheets and LoRA techniques. Covers turnaround views, expression sheets, color palettes, and ... |
| `codex-pet` | > |
| `controlnet-pose` | > |
| `elevenlabs-music-generation` | > |
| `explainer-video-guide` | "Explainer video production guide: scripting, voiceover, visuals, and assembly. Covers script formulas, pacing rules, scene planning, and multi-tool pipeline... |
| `face-swap` | > |
| `fal-ai-media` | Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance, Kling, Veo 3), text-to-... |
| `fal-audio` | "Text-to-speech and speech-to-text using fal.ai audio models" |
| `fal-generate` | "Generate images and videos using fal.ai AI models" |
| `fal-image-edit` | "AI-powered image editing with style transfer and object removal" |
| `fal-platform` | "Platform APIs for model management, pricing, and usage tracking" |
| `fal-upscale` | "Upscale and enhance image and video resolution using AI" |
| `fal-workflow` | "Generate workflow JSON files for chaining AI models" |
| `find-animation-opportunities` | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes motion with exact values, it d... |
| `flux-2-klein` | > |
| `flux-kontext` | > |
| `gpt-image-2` | > |
| `gpt-image-edit` | > |
| `happyhorse-1-0` | > |
| `higgsfield-brandkit` | \| |
| `higgsfield-game-generation` | \| |
| `higgsfield-generate` | \| |
| `higgsfield-marketplace-cards` | \| |
| `higgsfield-product-photoshoot` | \| |
| `higgsfield-soul-id` | \| |
| `higgsfield-video-explainer` | \| |
| `higgsfield-websites` | \| |
| `higgsfield-youtube-thumbnail` | \| |
| `image-edit` | > |
| `image-inpainting` | > |
| `image-outpainting` | > |
| `image-to-video` | > |
| `impeccable` | Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize, extract, or otherw... |
| `kling-3-0` | > |
| `lipsync` | > |
| `motion-ai` | Motion AI is an automated motion design framework and MCP tool for generating video assets, promotional clips, and animations directly within AI agents like Claude. |
| `nano-banana-2` | > |
| `nano-banana-edit` | > |
| `product-photography` | "AI product photography with studio lighting, lifestyle shots, and packshot conventions. Covers angles, backgrounds, shadow types, hero shots, and e-commerce... |
| `relight` | > |
| `remotion-best-practices` | Router for all Remotion skills |
| `remotion-captions` | Transcribing, displaying and animating captions |
| `remotion-create` | Create a new Remotion video |
| `remotion-docs` | Search Remotion documentation |
| `remotion-interactivity` | Structure Remotion markup for interactivity |
| `remotion-maps` | Remotion Map animation knowledge |
| `remotion-markup` | Content, animation and effects best practices |
| `remotion-multimedia` | Interacting with Mediabunny |
| `remotion-render` | Export a Remotion video |
| `remotion-saas` | Build an app with Remotion |
| `remotion-studio` | Preview a Remotion video |
| `remotion-upgrade` | Upgrade Remotion, and related packages |
| `run-train` | Rigor Train skill for deep learning research repositories. Use when a documented or selected training command should be run conservatively for startup verifi... |
| `runcomfy-cli` | > |
| `seedance-v2` | > |
| `ss-motion` | Apply a named StyleSeed motion to a component — either one of the 5 personality seeds (Spring/Silk/Snap/Float/Pulse × entrance/exit/hover/press/layout) or a ... |
| `tiktok-video-detail` | "TikTok single video detail scraper: input a TikTok video URL → output full video metadata (author profile, engagement stats, music, video meta, hashtags, me... |
| `video` | "When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use when the user mentions 'video producti... |
| `video-ad-specs` | "Video ad creation with exact platform-specific specs for TikTok, Instagram, YouTube, Facebook, LinkedIn. Covers dimensions, duration limits, AIDA framework,... |
| `video-edit` | > |
| `video-editing` | AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpeg, Remotion... |
| `video-extend` | > |
| `video-inpainting` | > |
| `video-outpainting` | > |
| `video-prompting-guide` | "Best practices and techniques for writing effective AI video generation prompts. Covers: Veo, Seedance, Wan, Grok, Kling, Runway, Pika, Sora prompting strat... |
| `wan-2-7` | > |
| `web-video-presentation` | 把一篇文章或口播稿，做成"看起来像视频"的点击驱动 16:9 网页演示，可选合成口播音频。流程：原始文章 → **一次产出**口播稿 + outline 开发计划 → 用户**一次对齐** 5 件事（稿子 / outline / 主题 / 素材 / 开发模式）→ 网页开发（逐章 / 顺序 / 并行）→ 可选音频合... |
| `youtube-thumbnail-design` | "YouTube thumbnail design with specific dimensions, contrast rules, and mobile preview optimization. Covers safe zones, text placement, face expression psych... |
| `
| `captions-overlay` | Overlay doctrine for the embedded-captions workflow — the caption MODEL (drop / rail / embed) and the rule that captions are an OVERLAY composited on ... |
| `changelog-video` | Turn a weekly changelog .md into a finished branded changelog video (square 1080, ~45-60s, Annie VO, animated brand background, mock-UI visualizations... |
| `cut-the-curve` | The technique catalog: five velocity-matched SEAMS (zoom-through, INVERSE zoom-through, cut-the-curve, waterfall cut, rack-focus blur-cut) plus the tw... |
| `embedded-captions` | Agent skill from official repository |
| `faceless-explainer` | Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video: there is no site or footage to capture, so the visuals ar... |
| `figma` | Import Figma content into a HyperFrames composition — rendered assets, brand tokens, components, storyboard sections → reconstructed motion (frames re... |
| `general-video` | Agent skill from official repository |
| `hyperframes` | Agent skill from official repository |
| `hyperframes-animation` | All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND ... |
| `hyperframes-cli` | Agent skill from official repository |
| `hyperframes-core` | The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`, tr... |
| `hyperframes-creative` | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat pl... |
| `hyperframes-keyframes` | Agent skill from official repository |
| `hyperframes-registry` | Install, discover, and wire registry blocks and components into HyperFrames compositions. Use when running hyperframes add or hyperframes catalog, ins... |
| `media-use` | Agent Media OS, the single skill for every media need in a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color grade, or LUT ... |
| `motion-doctrine` | GATEWAY — load FIRST before composing any HyperFrames animation or video. The high-level motion law that makes a multi-scene video feel like ONE conti... |
| `motion-graphics` | Agent skill from official repository |
| `music-to-video` | Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into a beat-synced video — lyric video, slidesh... |
| `oversized-cursor` | House-style oversized macOS cursor technique for HyperFrames launch videos. Load whenever a scene involves cursors or a pointer-led action, when kicki... |
| `pr-to-video` | Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change explainer video — changelog, feature reveal... |
| `product-launch-video` | Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos, feature reveals, product demos, app and co... |
| `remotion-to-hyperframes` | Port an existing Remotion (React) composition''s source to HyperFrames HTML. Use ONLY on an explicit ask to port/convert/migrate/translate a Remotion ... |
| `seam-craft` | Render-correctness doctrine for scene-to-scene seams in HyperFrames launch videos — the prerequisites that make transitions composite correctly on the... |
| `slideshow` | Agent skill from official repository |
| `talking-head-recut` | Package an existing talking-head / interview / podcast video with timed, designed GRAPHIC OVERLAY cards — kinetic titles, lower-thirds, data callouts,... |youtube-video-api-skill` | This skill helps users automatically extract channel-level and video detail data from a specific YouTube channel via BrowserAct API. Agent should proactively... |

## Marketing, Sales & Growth (102)

| Skill | Description |
|---|---|
| `activecampaign-automation` | "Automate ActiveCampaign tasks via Rube MCP (Composio): manage contacts, tags, list subscriptions, automation enrollment, and tasks. Always search tools firs... |
| `ad-creative` | "Create, iterate, and scale paid ad creative for Google Ads, Meta, LinkedIn, TikTok, and similar platforms. Use when generating headlines, descriptions, prim... |
| `ads` | "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad platforms. Also use when... |
| `ai-content-pipeline` | "Build multi-step AI content creation pipelines combining image, video, audio, and text. Workflow examples: generate image -> animate -> add voiceover -> mer... |
| `ai-podcast` | "Generate multi-person talking head podcast videos from scratch using AI — character creation, TTS, avatar animation, and video stitching. Use when the user ... |
| `ai-podcast-creation` | "Create AI-powered podcasts with text-to-speech, music, and audio editing. Tools: Kokoro TTS, DIA TTS, Chatterbox, AI music generation, media merger. Capabil... |
| `ai-seo` | "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the user mentions 'AI SEO... |
| `analytics` | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "GA4," "Google Analyt... |
| `aso` | "When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentions 'ASO audit,' 'app store optimization,' 'optimi... |
| `attribution` | When the user wants to figure out which marketing actually drives conversions and revenue, choose or interpret an attribution model, or reconcile conflicting... |
| `brandkit` | Premium brand-kit image generation skill for creating high-end brand-guidelines boards, logo systems, identity decks, and visual-world presentations. Trained... |
| `business-contact-social-links-skill` | "This skill helps users automatically extract official website and social media profiles. Agent should proactively apply this skill when users express needs ... |
| `capacity` | "Discovers available Azure OpenAI model capacity across regions and projects. Analyzes quota limits, compares availability, and recommends optimal deployment... |
| `churn-prevention` | "When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement retention strategies. Also use when... |
| `co-marketing` | "When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities. Use when the user says 'co-marketing,' 'pa... |
| `cold-email` | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails, prospecting emails, cold email campaig... |
| `community-marketing` | "Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to create a community strategy, grow a Discord or S... |
| `competitive-platform-analysis` | >- |
| `competitive-report-structure` | >- |
| `competitor-profiling` | "When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user mentions 'competitor profile,' 'competitor research... |
| `competitor-teardown` | "Structured competitive analysis with feature matrices, SWOT, positioning maps, and UX review. Covers research frameworks, pricing comparison, review mining,... |
| `competitors` | "When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when the user mentions 'alternative page,' '... |
| `content-engine` | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social... |
| `content-repurposing` | "Content atomization — turn one piece of content into many formats. Covers blog-to-thread, blog-to-carousel, podcast-to-blog, video-to-quotes, and more. Use ... |
| `content-strategy` | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content s... |
| `convex-crons` | "Add recurring scheduled jobs (crons) to the Convex app." |
| `convex-launch-readiness` | "Run every Convex audit (authz, reviewer, advisor, insights) into one scored, deduped readiness report with an ordered fix plan — Lighthouse for your backend." |
| `copywriting` | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about pages,... |
| `cro` | "When the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage, landing pages, pricing pages, feature ... |
| `crosspost` | Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never posts identica... |
| `customer-persona` | "Research-backed customer persona creation with market data and avatar generation. Covers demographics, psychographics, jobs-to-be-done, journey mapping, and... |
| `customer-research` | When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "customer research," "ICP research," "talk to customers,... |
| `design` | "Comprehensive design skill: brand identity, design tokens, UI styling, logo generation (55 styles, Gemini AI), corporate identity program (50 deliverables, ... |
| `directory-submissions` | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directories for backlinks, domain rating, and discovery. Als... |
| `email-systems` | Email has the highest ROI of any marketing channel. $36 for every |
| `emails` | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions... |
| `free-tools` | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or brand awareness. Also use when the user m... |
| `google-social-media-finder` | "Searches Google to discover social media profiles associated with a person, brand, or username; returns platform name, profile URL, username, bio snippet, a... |
| `image` | "When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product mockups, profile banners, listing vi... |
| `influencer-marketing` | "When the user wants to run influencer, creator, or ambassador partnerships to promote their product — finding and vetting partners, structuring deals, brief... |
| `investor-materials` | Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models, and fundraising materials. Use when the user needs inv... |
| `investor-outreach` | Draft cold emails, warm intro blurbs, follow-ups, update emails, and investor communications for fundraising. Use when the user wants outreach to angels, VCs... |
| `launch` | "When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,' 'Product Hunt,' 'feature ... |
| `lead-magnets` | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the user mentions "lead magnet," "gated co... |
| `market-research` | Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use... |
| `marketing-council` | "When the user wants multiple expert perspectives on a marketing question — a simulated board of advisors staffed by legendary marketers (Seth Godin, David O... |
| `marketing-ideas` | "When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks for 'marketing ideas,' 'grow... |
| `marketing-loops` | "When the user wants to set up a recurring, self-running marketing workflow — a repeatable loop an AI agent runs on a cadence (weekly, daily, on a trigger) r... |
| `marketing-plan` | When the user needs a comprehensive marketing plan for a client, a company they advise, or their own product. Also use when the user mentions "marketing plan... |
| `marketing-psychology` | "When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when the user mentions 'psychology,' 'men... |
| `microsoft-foundry` | "Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous ev... |
| `newsletter-curation` | "Newsletter curation with content sourcing, editorial structure, and subscriber growth strategies. Covers issue formatting, link roundups, commentary style, ... |
| `offers` | "When the user wants to design, construct, or improve an offer — the thing they actually sell — including value framing, bonus stacking, guarantee design, sc... |
| `onboarding` | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the user mentions "onboarding ... |
| `paywalls` | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the user mentions "paywall," "upgr... |
| `pitch-deck-visuals` | "Investor pitch deck structure with slide-by-slide framework, visual design rules, and data presentation. Covers the 12-slide framework, chart types, team sl... |
| `popups` | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when the user mentions "exit inte... |
| `preset` | "Intelligently deploys Azure OpenAI models to optimal regions by analyzing capacity across all available regions. Automatically checks current region first a... |
| `pricing` | "When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'pricing,' 'pricing tiers,' 'freemium,... |
| `product-capability` | Translate PRD intent, roadmap asks, or product discussions into an implementation-ready capability plan that exposes constraints, invariants, interfaces, and... |
| `product-hunt-launch` | "Product Hunt launch optimization with specific specs, timing, and gallery strategy. Covers taglines, gallery images, maker comments, and launch day tactics.... |
| `product-marketing` | "When the user wants to create or update their product marketing context document. Also use when the user mentions 'product context,' 'marketing context,' 's... |
| `producthunt-launches` | "Scrape Product Hunt daily/weekly/monthly/yearly leaderboard launches with full product details, maker profiles, and website contact info. Use when user ment... |
| `programmatic-seo` | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "template pages," "page... |
| `prospecting` | When the user wants to find, qualify, and build a list of prospects to reach out to — across B2B SaaS, general B2B, or local small businesses. Also use when ... |
| `public-relations` | "When the user wants help with public relations, earned media, press coverage, journalist outreach, or media strategy (not pull requests). Also use when the ... |
| `reddit-competitor-analysis-api-skill` | "This skill helps users extract structured data from Reddit posts and comments via BrowserAct API. Agent should proactively apply this skill when users expre... |
| `reddit-warmup` |  |
| `referrals` | "When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the user mentions 'refer... |
| `revops` | "When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Also use when the user mentions 'RevOp... |
| `sales-enablement` | "When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also use when the user mentions 'sales de... |
| `schema` | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "schema markup," "structured da... |
| `seo-audit` | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranki... |
| `seo-content-brief` | "SEO content brief creation with keyword research, search intent analysis, and content structure. Covers SERP analysis, heading hierarchy, word count targets... |
| `signup` | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions "signup conversions," "reg... |
| `site-architecture` | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. Also use when the user menti... |
| `sms` | When the user wants to plan, build, or optimize SMS or MMS marketing — including welcome flows, abandoned cart texts, post-purchase, win-back, promotional se... |
| `social` | "When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, or other platforms, ... |
| `social-media-carousel` | "Multi-slide carousel design for Instagram, LinkedIn, and Twitter/X with layout rules and hooks. Covers slide structure, text hierarchy, swipe psychology, an... |
| `social-media-finder-skill` | "This skill helps users automatically find social media profiles across platforms like Facebook, Twitter, Instagram, LinkedIn, etc. using the BrowserAct API.... |
| `talking-head-production` | "Talking head video production with AI avatars, lipsync, and voiceover. Recommended: P-Video-Avatar (fastest, cheapest, built-in TTS). Also covers OmniHuman,... |
| `threads-keyword-search` | "Searches Threads posts by keyword or hashtag and returns matching posts with engagement metrics, extracted from SSR-embedded JSON. Use when user asks to sea... |
| `threads-profile-search` | "Discovers Threads user accounts by keyword, extracting profile data including username, display name, verification status, biography, and follower count. Us... |
| `threads-user-posts` | "Fetches public posts from a Threads user's profile page, extracting post text, engagement metrics, and media info from SSR-embedded JSON. Use when user asks... |
| `twitter-thread-creation` | "Twitter/X thread writing with hook tweets, thread structure, and engagement optimization. Covers tweet formatting, character limits, media attachments, and ... |
| `x-dm-auto-chat` | "X (Twitter) DM automated chat end-to-end Skill: scan DM inbox to identify pending-reply conversations, read message history, generate persona-based replies ... |
| `x-keyword-comment` | "X (Twitter) keyword-based reply posting: search tweets by keyword, read each tweet's content, generate contextual replies from a configured brand persona, a... |
| `xiaohongshu-auto-posting` | "Automates the complete Xiaohongshu (XHS / Little Red Book) content operation workflow: pain-point topic collection → style case collection → topic selection... |
| `
| `data-manager-api-audience-ingestion` | Agent skill from official repository |
| `data-manager-api-event-ingestion` | Agent skill from official repository |
| `data-manager-api-setup` | Agent skill from official repository |
| `google-ads-api-account-diagnostics` | Agent skill from official repository |
| `google-ads-api-mcp-setup` | Guides developers through downloading, configuring, and installing the official open-source Google Ads MCP Server. Use this skill when a user wants to... |
| `google-ads-api-quickstart` | Agent skill from official repository |
| `google-analytics-admin-api-basics` | Agent skill from official repository |
| `google-analytics-data-api-basics` | Agent skill from official repository |
| `google-mobile-ads-android-migrate-to-next-gen` | Migrates Android applications from the old, legacy Google Mobile |
| `google-mobile-ads-banner` | Agent skill from official repository |
| `google-mobile-ads-get-started` | Provides instructions for integrating the Google Mobile Ads (GMA) |
| `google-mobile-ads-interstitial` | Provides instructions for implementing, integrating, or configuring |
| `google-mobile-ads-rewarded` | Provides instructions for implementing, integrating, or configuring |youtube-influencer-finder-api-skill` | This skill helps users extract YouTube influencer profiles including social links, subscriber counts, and channel stats via the BrowserAct API. Agent should ... |

## Agent Engineering & Orchestration (97)

| Skill | Description |
|---|---|
| `00-andruia-consultant` | "Arquitecto de Soluciones Principal y Consultor Tecnológico de Andru.ia. Diagnostica y traza la hoja de ruta óptima para proyectos de IA en español." |
| `10-andruia-skill-smith` | "Ingeniero de Sistemas de Andru.ia. Diseña, redacta y despliega nuevas habilidades (skills) dentro del repositorio siguiendo el Estándar de Diamante." |
| `20-andruia-niche-intelligence` | "Estratega de Inteligencia de Dominio de Andru.ia. Analiza el nicho específico de un proyecto para inyectar conocimientos, regulaciones y estándares únicos d... |
| `acceptance-orchestrator` | Use when a coding task should be driven end-to-end from issue intake through implementation, review, deployment, and acceptance verification with minimal hum... |
| `advanced-evaluation` | This skill should be used when the user asks to "implement LLM-as-judge", "compare model outputs", "create evaluation rubrics", "mitigate evaluation bias", o... |
| `agent-evaluation` | Testing and benchmarking LLM agents including behavioral testing, |
| `agent-framework-azure-ai-py` | "Build persistent agents on Azure AI Foundry using the Microsoft Agent Framework Python SDK." |
| `agent-introspection-debugging` | Structured self-debugging workflow for AI agent failures using capture, diagnosis, contained recovery, and introspection reports. |
| `agent-manager-skill` | "Manage multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling." |
| `agent-memory-mcp` | "A hybrid memory system that provides persistent, searchable knowledge management for AI agents (Architecture, Patterns, Decisions)." |
| `agent-memory-systems` | "Memory is the cornerstone of intelligent agents. Without it, every |
| `agent-orchestration-improve-agent` | "Systematic improvement of existing agents through performance analysis, prompt engineering, and continuous iteration." |
| `agent-orchestration-multi-agent-optimize` | "Optimize multi-agent systems with coordinated profiling, workload distribution, and cost-aware orchestration. Use when improving agent performance, throughp... |
| `agent-orchestrator` | Meta-skill que orquestra todos os agentes do ecossistema. Scan automatico de skills, match por capacidades, coordenacao de workflows multi-skill e registry m... |
| `agent-sort` | Build an evidence-backed ECC install plan for a specific repo by sorting skills, commands, rules, hooks, and extras into DAILY vs LIBRARY buckets using paral... |
| `agent-tool-builder` | Tools are how AI agents interact with the world. A well-designed |
| `agentflow` | "Orchestrate autonomous AI development pipelines through your Kanban board (Asana, GitHub Projects, Linear). Manages multi-worker Claude Code dispatch, deter... |
| `agentfolio` | "Skill for discovering and researching autonomous AI agents, tools, and ecosystems using the AgentFolio directory." |
| `agentic-actions-auditor` | > |
| `agentmail` | Email infrastructure for AI agents. Create accounts, send/receive emails, manage webhooks, and check karma balance via the AgentMail API. |
| `agentphone` | Build AI phone agents with AgentPhone API. Use when the user wants to make phone calls, send/receive SMS, manage phone numbers, create voice agents, set up w... |
| `agents-md` | This skill should be used when the user asks to "create AGENTS.md", "update AGENTS.md", "maintain agent docs", "set up CLAUDE.md", or needs to keep agent ins... |
| `agents-v2-py` | "Build container-based Foundry Agents with Azure AI Projects SDK (ImageBasedHostedAgentDefinition). Use when creating hosted agents with custom container ima... |
| `ai-agent-development` | "AI agent development workflow for building autonomous agents, multi-agent systems, and agent orchestration with CrewAI, LangGraph, and custom agents." |
| `ai-agents-architect` | Expert in designing and building autonomous AI agents. Masters tool |
| `ai-automation-workflows` | "Build automated AI workflows combining multiple models and services. Patterns: batch processing, scheduled tasks, event-driven pipelines, agent loops. Tools... |
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `autonomous-agents` | Autonomous agents are AI systems that can independently decompose |
| `benchmark-methodology` | >- |
| `brainstorming` | "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requ... |
| `cavecrew` | > |
| `caveman` | > |
| `caveman-commit` | > |
| `caveman-compress` | > |
| `caveman-help` | > |
| `caveman-review` | > |
| `caveman-stats` | > |
| `claude-handoff` | Hand the current conversation off to a fresh background agent that picks up the work immediately. |
| `coding-standards` | Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backend skills for framewo... |
| `computer-use-agents` | Build AI agents that interact with computers like humans do - |
| `context-window-management` | Strategies for managing LLM context windows including |
| `conversation-memory` | Persistent memory systems for LLM conversations including |
| `convex-optimize` | "Audit and optimize an existing Convex app: security, scale, upgrades, observability." |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `dmux-workflows` | Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows across Claude Code, Codex, OpenCode, and other ... |
| `e2e-testing` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. |
| `entra-agent-id` | "Provision Microsoft Entra Agent Identity Blueprints, BlueprintPrincipals, and per-instance Agent Identities via Microsoft Graph, and configure OAuth 2.0 tok... |
| `eval-harness` | Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles |
| `everything-claude-code` | Development conventions and patterns for everything-claude-code. JavaScript project with conventional commits. |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express ... |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| `full-output-enforcement` | Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any... |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent des... |
| `grill-me` | A relentless interview to sharpen a plan or design. |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `implement` | "Implement a piece of work based on a spec or set of tickets." |
| `karpathy-guidelines` | Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes... |
| `loop-me` | Grill me about specs for the workflows I want to build, within this workspace. |
| `mcp-server-patterns` | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for lates... |
| `plan-canvas` | Open plans and HTML artifacts in a local browser canvas where the human annotates elements, chats, and approves or requests changes without leaving the page.... |
| `ponytail` | > |
| `ponytail-audit` | > |
| `ponytail-debt` | > |
| `ponytail-gain` | > |
| `ponytail-help` | > |
| `ponytail-review` | > |
| `prisma-driver-adapter-implementation` | Required reference for Prisma ORM 7 SQL driver adapter work. Use when implementing or modifying adapters, adding database drivers, or touching SqlDriverAdapt... |
| `prompt-engineering` | "Master prompt engineering for AI models: LLMs, image generators, video models. Techniques: chain-of-thought, few-shot, system prompts, negative prompts. Mod... |
| `prototype` | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live and promote the one... |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technic... |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `resolving-merge-conflicts` | "Use when you need to resolve an in-progress git merge/rebase conflict." |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the o... |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up ... |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize a... |
| `strategic-compact` | Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction. |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `teach` | Teach the user a new skill or concept, within this workspace. |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| `to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed. |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker —... |
| `triage` | Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs. |
| `unified-memory` | Share durable, inspectable context and handoffs between Claude, Codex, Hermes, Cursor, OpenCode, and other agents through the local ECC Memory Vault. Use whe... |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists vi... |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| `vercel-optimize` | "Use for Vercel cost and performance optimization on deployed projects, especially Next.js, SvelteKit, Nuxt, and limited Astro apps. Collect Vercel metrics, ... |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output... |
| `verification-loop` | "A comprehensive verification system for Claude Code sessions." |
| `wait-what` | Stop. That last message did not land — re-pitch it. |
| `wayfinder` | Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets on your issue tracker, and resolve them one at a time ... |
| `wizard` | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or C... |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

## Frontend, UI & Design (89)

| Skill | Description |
|---|---|
| `3d-web-experience` | Expert in building 3D experiences for the web - Three.js, React |
| `address-github-comments` | "Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI." |
| `api-design` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. |
| `app-store-screenshots` | "App Store and Google Play screenshot creation with exact platform specs. Covers iOS/Android dimensions, gallery ordering, device mockups, and preview videos... |
| `apple-design` | Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI, spring animations,... |
| `assistant-ui` | assistant-ui is an open-source React component library for building ChatGPT-style AI conversational interfaces, copilots, sidebars, and chat widgets. |
| `banner-design` | "Design banners for social media, ads, website heroes, creative assets, and print. Multiple art direction options with AI-generated visuals. Actions: design,... |
| `baoyu-design` | >- |
| `beautiful-article` | "把用户提供的素材（网页 URL / PDF / DOCX / Markdown / 纯文本 / 截图 / 粘贴材料）编辑、设计成一篇美丽的、可离线打开和分享的**单文件 HTML 网页文章**。基于 reacticle 组件协议：不手写裸 HTML/CSS，而用语义组件 + 受主题约束的 Raw 自由层；按 s... |
| `brand` | Brand voice, visual identity, messaging frameworks, asset management, brand consistency. Activate for branded content, tone of voice, marketing assets, brand... |
| `brand-discovery` | >- |
| `brand-guidelines` | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand co... |
| `brand-voice` | Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across content, outreach, and... |
| `browser-extension-builder` | Expert in building browser extensions that solve real problems - |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art... |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a... |
| `convex-create-component` | Builds reusable Convex components with isolated tables and app-facing APIs. |
| `convex-design` | "Design and build reactive, type-safe, production-grade backends on Convex. Covers schema, queries/mutations/actions, indexes, auth, file storage, scheduling... |
| `design-md` | "Analyze Stitch projects and synthesize a semantic design system into DESIGN.md files" |
| `design-system` | Token architecture, component specifications, and slide generation. Three-layer tokens (primitive→semantic→component), CSS variables, spacing/typography scal... |
| `design-taste-frontend` | Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces tha... |
| `design-taste-frontend-v1` | The original v1 taste-skill, preserved for projects depending on its exact behavior. The current default is `design-taste-frontend` (v2 experimental), which ... |
| `driver-js` | Driver.js is a lightweight (~5kb), no-dependency vanilla JavaScript library for creating product tours, feature highlights, popovers, and contextual onboarding guides. |
| `email-design` | "Email marketing design with layout patterns, subject line formulas, and deliverability rules. Covers welcome sequences, promotional emails, transactional te... |
| `emil-design-eng` | This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great. |
| `extract-design-system` | Extract design primitives from a public website and generate starter token files for your project. |
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making... |
| `frontend-expert` | Use when creating React/TypeScript components, pages, or features. For modern patterns including Suspense, useSuspenseQuery, lazy loading, MUI v7 styling, Ta... |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. |
| `frontend-slides` | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a... |
| `gpt-taste` | Elite UX/UI & Advanced GSAP Motion Engineer. Enforces Python-driven true randomization for layout variance, strict AIDA page structure, wide editorial typogr... |
| `high-end-visual-design` | Teaches the AI to design like a high-end agency. Defines the exact fonts, spacing, shadows, card structures, and animations that make a website feel expensiv... |
| `huashu-design` | 花叔Design——用HTML做高保真原型、幻灯片、动画、可视化与专家评审。任何新设计100%先出三个方向初稿给用户选（指定风格/品牌也不豁免），选定后才执行。触发词：做原型、PPT、幻灯片、动画、设计风格、评审、做个HTML页面、UI mockup、导出MP4/GIF、做个好看的。生产级Web App/需后端的... |
| `image-to-code` | Elite website image-to-code skill for Codex. For visually important web tasks, it must first generate the design image(s) itself, deeply analyze them, then i... |
| `imagegen-frontend-mobile` | Elite mobile app image-generation skill for creating premium, app-native screen concepts and flows. Designed for iOS, Android, and cross-platform mobile prod... |
| `imagegen-frontend-web` | Elite frontend image-direction skill for generating premium, conversion-aware website design references. CRITICAL OUTPUT RULE — generate ONE separate horizon... |
| `improve-animations` | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other ... |
| `industrial-brutalist-ui` | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, anal... |
| `landing-page-design` | "Landing page conversion optimization with layout rules, hero section design, and CTA psychology. Covers above-the-fold formula, social proof placement, mobi... |
| `lark-slides` | "飞书幻灯片：创建和编辑幻灯片。创建演示文稿、读取幻灯片内容、管理幻灯片页面（创建、删除、读取、局部替换）。当用户需要创建或编辑幻灯片、读取或修改单个页面时使用。当用户给出 doubao.com 的 /slides/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetc... |
| `logo-design-guide` | "Logo design principles and AI image generation best practices for creating logos. Covers logo types, prompting techniques, scalability rules, and iteration ... |
| `minimalist-ui` | Clean editorial-style interfaces. Warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows. |
| `nextjs-turbopack` | Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use Turbopack vs webpack. |
| `og-image-design` | "Open Graph and social sharing image design with platform specs, text placement, and branding. Covers OG meta tags, Twitter cards, LinkedIn previews, and dyn... |
| `pick-ui-library` | Pick the right library for a given frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, virtualization, drag and drop... |
| `press-release-writing` | "Press release writing in AP style with inverted pyramid structure. Covers formatting, datelines, quotes, boilerplates, and fact-checking. Use for: product l... |
| `redesign-existing-projects` | Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without ... |
| `react-bits` | React Bits is an open-source library of animated, interactive, and fully customizable React UI components built with Framer Motion and Tailwind CSS. |
| `review-animations` | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned. |
| `shadcn` | Manages shadcn/ui components and projects, providing context, documentation, and usage patterns for building modern design systems. |
| `slides` | Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies. |
| `ss-a11y` | Audit a component or page for accessibility issues and fix them |
| `ss-audit` | Audit screens for UX issues using Nielsen's heuristics and modern mobile UX best practices |
| `ss-build` | Build a screen with StyleSeed's composed design method — choose or compile an output grammar, apply a brand recipe plus domain/page/profile/lock constraints,... |
| `ss-component` | Generate a new UI component following the StyleSeed design conventions |
| `ss-copy` | Generate UX microcopy (button labels, error messages, empty states, toasts) following a casual-but-polite voice and tone |
| `ss-dial` | Turn ONE design axis up or down as a coordinated, deterministic transform — "denser", "sharper corners", "more muted", "bolder", "flatter", "livelier". Not a... |
| `ss-feedback` | Add appropriate user feedback states (loading, success, error, empty) to a component or page |
| `ss-flow` | Design user flows and navigation structure following proven UX patterns |
| `ss-lint` | Quick automated lint — detects common design system violations in seconds |
| `ss-page` | Scaffold a new product page or screen from the compiled StyleSeed output grammar, surface adapter, brand recipe, and project lock. |
| `ss-pattern` | Generate a composed UI pattern from the active StyleSeed grammar and brand recipe using existing primitives. |
| `ss-reference` | Compile screenshots, URLs, Figma exports, or an existing UI into a project-local StyleSeed output grammar with evidence, tokens, confidence, anti-patterns, a... |
| `ss-resolve` | Compile a small, deterministic StyleSeed rule bundle for one agent, output grammar, surface adapter, domain, page type, brand recipe, palette recipe, and opt... |
| `ss-restyle` | Apply one optional StyleSeed aesthetic profile without changing the selected output grammar, product job, or core design judgment. |
| `ss-review` | Review UI code for design system compliance, accessibility, and best practices |
| `ss-score` | Score a visual artifact's implementation quality 0-100 against its composed StyleSeed rule set — category breakdown, evidence, and prioritized fixes. |
| `ss-setup` | Configure StyleSeed by selecting the output grammar, domain, page type, brand recipe, semantic palette recipe, optional aesthetic profile, and bounded brand ... |
| `ss-studio` | Turn a product brief and optional references into three distinct creative directions, a human-selected StyleSeed interaction plan, generated image/video asse... |
| `ss-tokens` | View, add, or modify design tokens in the StyleSeed design system |
| `ss-update` | Update StyleSeed engine in your project — analyzes what's outdated and updates safely |
| `ss-verify` | The VISUAL gate — render a UI or visual artifact through its surface adapter, inspect the actual pixels, then fix and re-render until it passes the composed ... |
| `stitch-design-taste` | Semantic Design System Skill for Google Stitch. Generates agent-friendly DESIGN.md files that enforce premium, anti-generic UI standards — strict typography,... |
| `storyboard-creation` | "Film and video storyboarding with shot vocabulary, continuity rules, and panel layout. Covers shot types, camera angles, movement, 180-degree rule, and anno... |
| `tailark` | Tailark is a Shadcn UI component registry providing marketing website blocks, hero sections, pricing tables, feature grids, and illustrations. |
| `styleseed-design-review` | Reviews UI/frontend code and tells you exactly why it "looks AI-generated" — then how to fix it. Use it when a React/Tailwind/HTML interface looks off, gener... |
| `theme-factory` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors... |
| `ui-styling` | Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first styling, and canvas-based v... |
| `ui-ux-pro-max` | "UI/UX design intelligence for web and mobile. Searchable local database with 84 styles, 192 color palettes, 74 font pairings, 192 product types, 98 UX guide... |
| `uiux-designer` | "Use this skill when designing UI components, choosing color palettes, implementing responsive layouts, or reviewing code for UX issues. For landing pages, d... |
| `vercel-react-best-practices` | React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.j... |
| `vercel-react-native-skills` | React Native and Expo best practices for building performant mobile apps. Use |
| `vercel-react-view-transitions` | Guide for implementing smooth, native-feeling animations using React's View Transition API (`<ViewTransition>` component, `addTransitionType`, and CSS view t... |
| `web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use ... |
| `web-design-engineer` | "Build or redesign polished browser-rendered visual artifacts with HTML/CSS/JavaScript/React: pages, dashboards, prototypes, slide decks, animations, UI mock... |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my si... |
| `web-research-assistant` | AI-powered web research assistant that leverages BrowserAct API to supplement restricted web access by searching the internet for additional information. Des... |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing... |
| `youtube-channel-business-email` | "YouTube channel business email and contact extractor: accepts a channel id (UCxxx), handle (@name), or URL; navigates the channel About view; extracts the b... |

## AI, ML & Data Science (33)

| Skill | Description |
|---|---|
| `ai-dev-jobs-mcp` | "Search 8,400+ AI and ML jobs across 489 companies, inspect listings and employers, match roles, and view salary and market stats via AI Dev Jobs MCP" |
| `ai-engineer` | Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Implements vector search, multimodal AI, agent orchestration, and ente... |
| `ai-ml-developer` | Use when building LLM applications, RAG systems, or AI agents with production requirements. For implementing vector search, prompt engineering, model evaluat... |
| `ai-product` | Every product will be AI-powered. The question is whether you'll |
| `ai-research-explore` | Rigor Explore compatible skill slug for meaningful and potentially novel deep learning research candidates. Use when the researcher has chosen the task famil... |
| `ai-research-reproduction` | Rigor Reproduce compatible skill slug for README-first deep learning repository reproduction. Use when the user wants an end-to-end, minimal-trustworthy flow... |
| `ai-wrapper-product` | Expert in building products that wrap AI APIs (OpenAI, Anthropic, |
| `biopython` | "Biopython is a comprehensive set of freely available Python tools for biological computation. It provides functionality for sequence manipulation, file I/O,... |
| `data-analyst` | Use when analyzing data for business decisions, designing statistical or ML algorithms, creating data visualizations, or presenting insights to stakeholders.... |
| `data-visualization` | "Data visualization with chart selection, color theory, and annotation best practices. Covers chart types (bar, line, scatter, heatmap), axes rules, and stor... |
| `deep-research` | Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when... |
| `finetuning` | "Fine-tune models on Azure AI Foundry using SFT (supervised), DPO (preference), or RFT (reinforcement with graders). Covers dataset preparation, training job... |
| `hugging-face-cli` | "Use the Hugging Face Hub CLI (`hf`) to download, upload, and manage models, datasets, and Spaces." |
| `hugging-face-community-evals` | Run local evaluations for Hugging Face Hub models with inspect-ai or lighteval. |
| `hugging-face-dataset-viewer` | Query Hugging Face datasets through the Dataset Viewer API for splits, rows, search, filters, and parquet links. |
| `hugging-face-gradio` | Build or edit Gradio apps, layouts, components, and chat interfaces in Python. |
| `hugging-face-jobs` | Run workloads on Hugging Face Jobs with managed CPUs, GPUs, TPUs, secrets, and Hub persistence. |
| `hugging-face-model-trainer` | Train or fine-tune TRL language models on Hugging Face Jobs, including SFT, DPO, GRPO, and GGUF export. |
| `hugging-face-paper-publisher` | Publish and manage research papers on Hugging Face Hub. Supports creating paper pages, linking papers to models/datasets, claiming authorship, and generating... |
| `hugging-face-papers` | Read and analyze Hugging Face paper pages or arXiv papers with markdown and papers API metadata. |
| `hugging-face-trackio` | Track ML experiments with Trackio using Python logging, alerts, and CLI metric retrieval. |
| `hugging-face-vision-trainer` | Train or fine-tune vision models on Hugging Face Jobs for detection, classification, and SAM or SAM2 segmentation. |
| `mle-workflow` | Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment, monitoring, and rollback. Use when ... |
| `networkx` | "NetworkX is a Python package for creating, manipulating, and analyzing complex networks and graphs." |
| `paper-context-resolver` | Rigor Paper Context helper for README-first deep learning repo reproduction. Use only when the README and repository files leave a narrow reproduction-critic... |
| `sympy` | "SymPy is a Python library for symbolic mathematics that enables exact computation using mathematical symbols rather than numerical approximations." |
| `
| `bigquery-ai-ml` | Agent skill from official repository |
| `gemini-agents-api` | Manages custom Agent resources on Gemini Enterprise Agent Platform. Use when the user wants to programmatically create, configure, list, update, or de... |
| `gemini-api` | Use when the user asks about using Gemini in an enterprise environment or explicitly mentions Vertex AI, Google Cloud, or Agent Platform. Guides the u... |
| `gemini-interactions-api` | Guides the usage of Gemini Interactions API on Gemini Enterprise Agent Platform. Use when the user wants to use the stateful, server-managed Interacti... |
| `gemini-live-api` | Agent skill from official repository |
| `google-agents-cli-onboarding` | Agent skill from official repository |transformers-js` | Run Hugging Face models in JavaScript or TypeScript with Transformers.js in Node.js or the browser. |

## Cloud, DevOps & Infrastructure (131)

| Skill | Description |
|---|---|
| `airunway-aks-setup` | "Set up AI Runway on AKS — from bare cluster to running model. Covers cluster verification, controller install, GPU assessment, provider setup, and first dep... |
| `appdeploy` | "Deploy web apps with backend APIs, database, and file storage. Use when the user asks to deploy or publish a website or web app and wants a public URL. Uses... |
| `appinsights-instrumentation` | "Guidance for instrumenting webapps with Azure Application Insights. Provides telemetry patterns, SDK setup, and configuration references. WHEN: how to instr... |
| `aws-serverless` | Specialized skill for building production-ready serverless |
| `azure-ai` | "Use for Azure AI: Search, Speech, OpenAI, Document Intelligence. Helps with search, vector/hybrid search, speech-to-text, text-to-speech, transcription, OCR... |
| `azure-aigateway` | "Configure Azure API Management as an AI Gateway for AI models, MCP tools, and agents. WHEN: semantic caching, token limit, content safety, load balancing, A... |
| `azure-app-onboard` | "End-to-end orchestrator: from a business idea, app idea, or existing app to running Azure deployment with cost estimates and pre-deploy approval. Analyzes y... |
| `azure-app-onboard-prereq` | "Assess whether source code is ready to deploy to Azure — the check BEFORE infrastructure work. Evaluates build health, app completeness, dependencies and lo... |
| `azure-cloud-migrate` | "Assess and migrate cross-cloud workloads to Azure with reports and code conversion. Supports Lambda→Functions, Beanstalk/Heroku/App Engine→App Service, Farg... |
| `azure-compute` | "Azure VM/VMSS router. WHEN: create / provision / deploy / spin-up VM, recommend VM size, compare VM pricing, VMSS, scale set, autoscale, burstable, lightwei... |
| `azure-cost` | "Azure cost management: query costs, forecast spending, optimize to reduce waste. WHEN: \"Azure costs\", \"Azure bill\", \"cost breakdown\", \"how much am I ... |
| `azure-deploy` | "Execute Azure deployments for ALREADY-PREPARED applications that have existing .azure/deployment-plan.md and infrastructure files. DO NOT use this skill whe... |
| `azure-diagnostics` | "Debug Azure production issues on Azure using AppLens, Azure Monitor, resource health, and safe triage. WHEN: debug production issues, troubleshoot app servi... |
| `azure-enterprise-infra-planner` | "Architect and provision enterprise Azure infrastructure from workload descriptions. For cloud architects and platform engineers planning networking, identit... |
| `azure-functions` | Expert patterns for Azure Functions development including isolated |
| `azure-kubernetes` | "Plan, create, and configure production-ready Azure Kubernetes Service (AKS) clusters. Covers Day-0 checklist, SKU selection (Automatic vs Standard), network... |
| `azure-kubernetes-automatic-readiness` | "Assess Kubernetes workloads and cluster configuration for AKS Automatic compatibility. Identifies incompatibilities, generates fixes, and guides migration f... |
| `azure-kusto` | "Query and analyze data in Azure Data Explorer (Kusto/ADX) using KQL for log analytics, telemetry, and time series analysis. WHEN: KQL queries, Kusto databas... |
| `azure-messaging` | "Troubleshoot and resolve issues with Azure Messaging SDKs for Event Hubs and Service Bus. Covers connection failures, authentication errors, message process... |
| `azure-prepare` | "Prepare azd-based Azure projects for deployment: generates azure.yaml, infrastructure (Bicep/Terraform), and Dockerfiles for the Azure Developer CLI (azd) w... |
| `azure-quotas` | "Check/manage Azure quotas and usage across providers. For deployment planning, capacity validation, region selection. WHEN: \"check quotas\", \"service limi... |
| `azure-reliability` | "Assess and improve the reliability posture of PaaS Applications (Azure Functions and Azure App Service). Scans deployed resources for zone redundancy, ZRS s... |
| `azure-resource-lookup` | "List, find, and show Azure resources across subscriptions or resource groups. Handles prompts like \"list the websites in my subscription\", \"list my web a... |
| `azure-resource-visualizer` | "Analyze Azure resource groups and generate detailed Mermaid architecture diagrams showing the relationships between individual resources. WHEN: create archi... |
| `azure-storage` | "Azure Storage Services including Blob Storage, File Shares, Queue Storage, Table Storage, and Data Lake. Answers questions about storage access tiers (hot, ... |
| `azure-upgrade` | "Assess and upgrade Azure workloads between plans, tiers, or SKUs, or modernize Azure SDK dependencies in source code. WHEN: upgrade Consumption to Flex Cons... |
| `azure-validate` | "Pre-deployment validation for Azure readiness. Run deep checks on configuration, infrastructure (Bicep or Terraform), RBAC role assignments, managed identit... |
| `bun-runtime` | Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support. |
| `convex-deploy-guard` | "Classify + announce the target Convex deployment before any deployment-affecting command; fresh explicit consent for prod actions; session read-only mode." |
| `convex-migrate` | "Migrate schema + backfill data on a deployed Convex app using @convex-dev/migrations." |
| `convex-migrate-rehearse` | "Rehearse a live-app schema change + backfill on a snapshot-seeded preview deployment, verify, then promote the proven change to prod with the snapshot as ro... |
| `customize` | "Interactive guided deployment flow for Azure OpenAI models with full customization control. Step-by-step selection of model version, SKU (GlobalStandard/Sta... |
| `deploy` |  |
| `deploy-model` | "Unified Azure OpenAI model deployment skill with intelligent intent-based routing. Handles quick preset deployments, fully customized deployments (version/S... |
| `deploy-to-vercel` | Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this liv... |
| `devcontainer-setup` | Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes. Use when adding devcontainer support to a pr... |
| `entra-app-registration` | "Guides Microsoft Entra ID app registration, OAuth 2.0 authentication, and MSAL integration. USE FOR: create app registration, register Azure AD app, configu... |
| `env-and-assets-bootstrap` | Rigor Setup skill for README-first deep learning repo reproduction. Use when the task is specifically to prepare a conservative conda-first environment, chec... |
| `expo-deployment` | "Deploy Expo apps to production" |
| `migrate-radix-to-base` | Migrates React projects and components from Radix UI to Base UI. Use when asked to migrate from radix, move to base-ui, convert radix primitives, or switch a... |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial... |
| `prepare` |  |
| `prisma-mongodb-upgrade` | Decision and migration guide for Prisma ORM MongoDB projects on v6, which have no upgrade path to v7. Use when a MongoDB project asks about upgrading Prisma,... |
| `prisma-upgrade-v7` | Complete migration guide from Prisma ORM v6 to v7 covering all breaking changes. Use when upgrading Prisma versions, encountering v7 errors, or migrating exi... |
| `python-appservice-deploy` | "Deploy Python (Flask/Django/FastAPI) code to Azure App Service Linux. WHEN: \"Flask App Service\", \"Django App Service\", \"FastAPI App Service\", \"deploy... |
| `scaffold` |  |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create ... |
| `vercel-cli-with-tokens` | Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than interactive login — e... |
| `
| `agent-platform-alert-configuration` | Agent skill from official repository |
| `agent-platform-deploy` | Agent skill from official repository |
| `agent-platform-endpoint-management` | Agent skill from official repository |
| `agent-platform-eval-flywheel` | Agent skill from official repository |
| `agent-platform-inference` | Agent skill from official repository |
| `agent-platform-migrate-from-ai-studio` | Agent skill from official repository |
| `agent-platform-model-registry` | Agent skill from official repository |
| `agent-platform-prompt-management` | Agent skill from official repository |
| `agent-platform-rag-engine-management` | Agent skill from official repository |
| `agent-platform-skill-registry` | Agent skill from official repository |
| `agent-platform-troubleshooting` | Agent skill from official repository |
| `agent-platform-tuning` | Agent skill from official repository |
| `agent-platform-tuning-management` | Agent skill from official repository |
| `alloydb-basics` | Agent skill from official repository |
| `bigquery-basics` | Agent skill from official repository |
| `bigquery-bigframes` | Agent skill from official repository |
| `bigtable-basics` | Agent skill from official repository |
| `cloud-logging-configuration-basics` | Agent skill from official repository |
| `cloud-logging-cross-project-configuration` | Agent skill from official repository |
| `cloud-logging-query-generation` | Agent skill from official repository |
| `cloud-monitoring-chart-generation` | Agent skill from official repository |
| `cloud-monitoring-metric-selection` | Agent skill from official repository |
| `cloud-run-basics` | Agent skill from official repository |
| `cloud-sql-basics` | Agent skill from official repository |
| `datalineage-bigquery-asset-impact-analysis` | Agent skill from official repository |
| `datalineage-summary` | Agent skill from official repository |
| `detection-engineering-coverage-evaluation` | Agent skill from official repository |
| `developer-device-platform-basics` | Agent skill from official repository |
| `gcloud` | Agent skill from official repository |
| `gke-ai-troubleshooting-handle-disruption-gpu-tpu` | Agent skill from official repository |
| `gke-ai-troubleshooting-jobset-interruption` | Agent skill from official repository |
| `gke-ai-troubleshooting-tpu-vbar-oom` | Agent skill from official repository |
| `gke-app-onboarding` | Agent skill from official repository |
| `gke-backup-dr` | Agent skill from official repository |
| `gke-basics` | Agent skill from official repository |
| `gke-batch-hpc` | Agent skill from official repository |
| `gke-cluster-autoscaler` | Agent skill from official repository |
| `gke-cluster-creation` | Agent skill from official repository |
| `gke-compute-classes` | Agent skill from official repository |
| `gke-cost-analysis` | Agent skill from official repository |
| `gke-cost-optimization` | Agent skill from official repository |
| `gke-golden-path` | Agent skill from official repository |
| `gke-inference` | Agent skill from official repository |
| `gke-manifest-generation` | Agent skill from official repository |
| `gke-multitenancy` | Agent skill from official repository |
| `gke-networking` | Agent skill from official repository |
| `gke-observability` | Agent skill from official repository |
| `gke-platform-security` | Agent skill from official repository |
| `gke-productionize` | Orchestrates comprehensive production readiness reviews and assessments for GKE clusters and workloads across scalability, security, reliability, obse... |
| `gke-reliability` | Agent skill from official repository |
| `gke-service-networking` | Agent skill from official repository |
| `gke-storage` | Agent skill from official repository |
| `gke-tpu-dynamic-slices-monitoring` | Agent skill from official repository |
| `gke-tpu-metrics-monitoring` | Agent skill from official repository |
| `gke-upgrades` | Agent skill from official repository |
| `gke-workload-scaling` | Agent skill from official repository |
| `gke-workload-security` | Agent skill from official repository |
| `gke-workload-troubleshooting` | Agent skill from official repository |
| `google-cloud-global-frontend-configuration` | Agent skill from official repository |
| `google-cloud-networking-observability` | Agent skill from official repository |
| `google-cloud-recipe-auth` | Provides expert guidance on authenticating and authorizing to Google Cloud services and APIs, covering human users, service identities, Application De... |
| `google-cloud-recipe-foundation-builder` | Agent skill from official repository |
| `google-cloud-recipe-onboarding` | Agent skill from official repository |
| `google-cloud-slo-alert-configuration` | Agent skill from official repository |
| `google-cloud-solution-agentic-ai-bidirectional-streaming` | Agent skill from official repository |
| `google-cloud-solution-agentic-ai-borderless-data-lakehouse` | Agent skill from official repository |
| `google-cloud-solution-agentic-ai-data-science-workflow` | Agent skill from official repository |
| `google-cloud-solution-agentic-analytics-spark-knowledge-catalog` | Agent skill from official repository |
| `google-cloud-solution-architecture` | Agent skill from official repository |
| `google-cloud-solution-build-deploy-agents` | Agent skill from official repository |
| `google-cloud-solution-guided-gke-ai-migration` | Agent skill from official repository |
| `google-cloud-solution-n-tier-serverless-web-app` | Agent skill from official repository |
| `google-cloud-solution-rag-enterprise-search-gke-sqldb` | Agent skill from official repository |
| `google-cloud-storage-basics` | Agent skill from official repository |
| `google-cloud-waf-cost-optimization` | Generates cost optimization guidance for Google Cloud workloads based on the Google Cloud Well-Architected Framework (WAF). Use this skill to evaluate... |
| `google-cloud-waf-operational-excellence` | Agent skill from official repository |
| `google-cloud-waf-performance-optimization` | Agent skill from official repository |
| `google-cloud-waf-reliability` | Agent skill from official repository |
| `google-cloud-waf-security` | Agent skill from official repository |
| `google-cloud-waf-sustainability` | Agent skill from official repository |
| `spanner-basics` | Agent skill from official repository |
| `workload-manager-basics` | Agent skill from official repository |vercel-composition-patterns` | React composition patterns that scale. Use when refactoring components with |

## Databases & Data Stores (47)

| Skill | Description |
|---|---|
| `algolia-search` | Expert patterns for Algolia search implementation, indexing |
| `bullmq-specialist` | BullMQ expert for Redis-backed job queues, background processing, |
| `convex` | "Convex is the backend agents get right on the first try: an all-TypeScript reactive platform where the database, server functions, scheduling, file storage,... |
| `convex-add` | "Add a capability to the CURRENT Convex app — consults the served Convex capability catalog for always-current procedures (billing, crons, auth, agent, searc... |
| `convex-advisor` | "Read the Convex deployment's 72h insights (read limits, OCC contention), root-cause each event in code, report evidence-backed perf/cost findings with fixes." |
| `convex-agent` | "Add an AI agent / RAG backend (@convex-dev/agent) to the Convex app." |
| `convex-auth` | "Add authentication (passkeys/OAuth) to the current Convex app, including the auth.config.ts wiring." |
| `convex-authz` | "Audit and harden Convex authorization: identity-from-arg impersonation, missing per-document ownership checks, PII-leaking public queries, and writes into c... |
| `convex-backup` | "Set up Convex backups and run a restore DRILL that proves recovery — snapshot, restore into a throwaway preview, assert the data came back — plus a schedule... |
| `convex-billing` | "Add Stripe billing/payments to the Convex app via @convex-dev/stripe (checkout + webhook + gating)." |
| `convex-cost` | "Preview Convex spend — rank functions by bytes/documents-read × call-volume from insights, project each cost driver's growth curve, name the cheapest fix; c... |
| `convex-docs` | "Pull version-current Convex docs for the version this project uses — pin the installed version, fetch page-as-markdown or check node_modules types, freshnes... |
| `convex-domains` | "Point a domain you already own at your Convex app (DNS records, custom-domain attach, auth-origin rebind)." |
| `convex-env` | "Set and wire Convex deployment env vars / secrets for the app." |
| `convex-expert` | "Convex backend specialist. Use this agent for any code inside a `convex/` directory — function definitions, schemas, indexes, queries, mutations, actions, H... |
| `convex-explain-app` | "Explain an existing Convex app — data model + relationships, public vs internal functions, auth/ownership model, components, a request→data flow — read from... |
| `convex-improve-convex-plugin` | "Send this coding session's transcript to the Convex team for an AI post-mortem that improves the quickstart system." |
| `convex-insights` | "Query a running Convex app's logs + health in natural language (official MCP): failures, slow/expensive functions, deploy causality — scoped, evidence-backe... |
| `convex-monitor` | "Watch for the next dev/prod error or request in a Convex app and react to it." |
| `convex-quickstart` | "Get a barebones Convex + web template running from a one-sentence idea." |
| `convex-reviewer` | "Convex code reviewer — security, auth, validators, performance, and pattern checks for code in a convex/ directory. Use to review or audit Convex functions ... |
| `convex-seed` | "Seed or import data into the Convex database." |
| `convex-self-heal` | "Production error → triaged, root-caused, repaired, and certified (tsc + rehearsal + reproduce-then-gone) fix PR for a human to merge — then confirm the erro... |
| `convex-sentinel` | "Set up Sentinel production error capture in your own Convex deployment." |
| `convex-suggest` | "Suggest the matching Convex component when the user hand-rolls a pattern it already solves (crons, sharded-counter, rate-limiter, storage, search, presence,... |
| `convex-test` | "Generate convex-test tests for the app's Convex functions." |
| `convex-verify` | "Prove a Convex feature works — seed, drive as multiple mocked users via convex-test, assert behavior including the negative authz cases (wrong user refused,... |
| `firebase-ai-logic-basics` | Official skill for integrating Firebase AI Logic (Gemini API) into web applications. Covers setup, multimodal inference, structured output, and security. |
| `firebase-app-hosting-basics` | >- |
| `firebase-auth-basics` | Guide for setting up and using Firebase Authentication. Use this skill when the user's app requires user sign-in, user management, or secure data access usin... |
| `firebase-basics` | >- |
| `firebase-crashlytics` | Comprehensive guide for Firebase Crashlytics, including provisioning and SDK usage. Use this skill when the user needs help setting up Crashlytics, adding cr... |
| `firebase-data-connect` | Builds and deploys Firebase SQL Connect (aka Firebase Data Connect) backends with PostgreSQL securely. Use when designing schemas with tables and relations, ... |
| `firebase-firestore` | >- |
| `firebase-hosting-basics` | >- |
| `firebase-remote-config-basics` | >- |
| `kb-retriever` | 面向本地知识库目录的检索和问答助手。核心流程：(1)分层索引导航 (2)遇到PDF/Excel时必须先读取references学习处理方法 (3)处理文件后再检索。按文件类型组合使用 grep、Read、pdfplumber、pandas 进行渐进式检索，避免整文件加载。用户问题涉及"从知识库目录回答问题/检索信... |
| `prisma-cli` | Prisma ORM CLI commands reference covering init, generate, migrate, db, dev, complete, studio, validate, format, debug, and mcp. Use for ORM/database CLI wor... |
| `prisma-client-api` | Prisma Client API reference covering model queries, filters, operators, and client methods. Use when writing database queries, using CRUD operations, filteri... |
| `prisma-compute` | Prisma Compute deployment and hosting guide. Use whenever the user mentions Prisma Compute, `prisma.compute.ts`, `defineComputeConfig`, deploying or hosting ... |
| `prisma-database-setup` | Guides for configuring Prisma with different database providers (PostgreSQL, MySQL, SQLite, MongoDB, etc.). Use when setting up a new project, changing datab... |
| `prisma-postgres` | Prisma Postgres setup and operations guidance across Console, create-db CLI, Management API, and Management API SDK. Use when creating Prisma Postgres databa... |
| `prisma-postgres-setup` | Set up a new Prisma Postgres database and connect it to a local project using the Management API. Use when asked to "set up a database", "create a Prisma Pos... |
| `sql-optimization` | Use when debugging slow SQL queries, designing database indexes, or rewriting queries for better performance. For EXPLAIN analysis, index strategy, N+1 probl... |
| `supabase` | "Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client l... |
| `supabase-postgres-best-practices` | "Postgres best practices maintained by Supabase, for Postgres running anywhere. Load this skill BEFORE writing or changing anything that lives in a Postgres ... |
| `using-neon` | "Neon is a serverless Postgres platform that separates compute and storage to offer autoscaling, branching, instant restore, and scale-to-zero. It's fully co... |

## Backend & API Development (31)

| Skill | Description |
|---|---|
| `analyze-project` | Rigor Analyze / Rigor Audit read-only skill for deep learning research repositories. Use when the user wants to read and understand a repository, inspect mod... |
| `api-builder` | Use when building REST/GraphQL APIs with Python (FastAPI or Django). For API design, authentication, documentation, testing, mock services, observability, an... |
| `backend-patterns` | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| `claude-api` | "Build apps with the Claude API or Anthropic SDK. TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`, or user asks to use Claude A... |
| `doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision do... |
| `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision... |
| `explore-code` | Rigor Improve implementation leaf skill for auditable candidate implementation in deep learning research repositories. Use when the researcher explicitly aut... |
| `explore-run` | Rigor Improve / Rigor Explore run leaf skill for bounded exploratory evidence in deep learning research repositories. Use when the researcher explicitly auth... |
| `github-project-contributor-finder-api-skill` | "This skill helps users extract GitHub repository project details and contributor contact information using keywords, stars, and update dates. Agent should p... |
| `google-image-api-skill` | This skill helps users automatically extract structured image data from Google Images via BrowserAct API. Agent should proactively apply this skill when user... |
| `google-maps-api-skill` | "This skill helps users automatically scrape business data from Google Maps using the BrowserAct Google Maps API. Agent should proactively trigger this skill... |
| `google-maps-reviews-api-skill` | "This skill is designed to help users automatically extract reviews from Google Maps via the Google Maps Reviews API. Agent should proactively apply this ski... |
| `google-maps-search-api-skill` | "This skill is designed to help users automatically extract business data from Google Maps search results. The Agent should proactively apply this skill when... |
| `google-news-api-skill` | "This skill helps users automatically extract structured news data from Google News via BrowserAct API. Agent should proactively apply this skill when users ... |
| `industry-key-contact-radar-api-skill` | "This skill helps users discover key contacts across industries, roles, and social platforms via the BrowserAct API. Agent should proactively apply this skil... |
| `lark-openapi-explorer` | "飞书/Lark 原生 OpenAPI 探索：从官方文档库中挖掘未经 CLI 封装的原生 OpenAPI 接口。当用户的需求无法被现有 lark-* skill 或 lark-cli 已注册命令满足，需要查找并调用原生飞书 OpenAPI 时使用。" |
| `repo-intake-and-plan` | Rigor Intake helper for README-first deep learning repo reproduction. Use when the task is specifically to scan a repository, read the README and common proj... |
| `wechat-article-search-api-skill` | "This skill helps users extract full article contents from WeChat using the BrowserAct API. The Agent should proactively apply this skill when users express ... |
| `youtube-api-skill` | "This skill helps users automatically extract detailed video metrics and channel information from YouTube based on keyword searches using the BrowserAct API.... |
| `youtube-batch-transcript-extractor-api-skill` | "This skill helps users automatically extract YouTube video transcripts and metadata in batch via the BrowserAct API. The Agent should proactively apply this... |
| `youtube-channel-api-skill` | "This skill helps users automatically extract structured channel data from YouTube search results via BrowserAct API. Agent should proactively apply this ski... |
| `youtube-comments-api-skill` | "This skill helps users extract structured video list data and comment data from YouTube using the BrowserAct API. The Agent should proactively apply this sk... |
| `youtube-search-api-skill` | This skill helps users automatically extract structured data from YouTube search results using the BrowserAct API. The Agent should proactively apply this sk... |
| `youtube-transcript-analysis-api-skill` | "This skill helps users extract YouTube video transcripts and perform deep competitive analysis on the content. Agent should proactively apply this skill whe... |
| `youtube-transcript-extractor-api-skill` | "This skill helps users automatically extract YouTube video transcripts and metadata via the BrowserAct API. The Agent should proactively apply this skill wh... |
| `
| `agent-email-inbox` | Use when building any system where email content triggers actions — AI agent inboxes, automated support handlers, email-to-task pipelines, or any work... |
| `email-best-practices` | Use when building email features, emails going to spam, high bounce rates, setting up SPF/DKIM/DMARC authentication, implementing email capture, ensur... |
| `react-email` | Use when building HTML email templates with React components, adding a visual email editor to an application using the React Email visual editor, rend... |
| `resend` | Use when working with the Resend email API — sending transactional emails (single or batch), receiving inbound emails via webhooks, managing email tem... |
| `resend-cli` | Agent skill from official repository |zhihu-search-api-skill` | "This skill helps users automatically extract structured article details and full content from Zhihu via the BrowserAct API. Agent should proactively apply t... |

## Testing, QA & Code Quality (18)

| Skill | Description |
|---|---|
| `ab-test-setup` | "Structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness." |
| `ab-testing` | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. Also use when the user mentions "A/B ... |
| `app-store-changelog` | Generate user-facing App Store release notes from git history since the last tag. |
| `code-quality` | Enforce code quality standards across a codebase. Use when asked to audit code quality, review for maintainability, find anti-patterns, enforce coding standa... |
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding st... |
| `code-reviewer` | Automated code review assistant for analyzing Pull Requests and enforcing coding standards. Use when you need to review complex PRs, check for anti-patterns,... |
| `dev` | Development workflows for the playwright-cli repository. Use when the user asks about rolling dependencies, releasing, or other repo maintenance tasks. |
| `fix-review` | "Verify fix commits address audit findings without new bugs" |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use whe... |
| `minimal-run-and-audit` | Rigor Run skill for README-first deep learning repo reproduction. Use when the task is specifically to capture or normalize evidence from the selected smoke ... |
| `mobile-developer` | Use this skill when building React Native or Flutter apps with native integrations. For cross-platform UI, offline-first sync, push notifications, and App St... |
| `safe-debug` | Rigor Debug / Rigor Audit skill for deep learning research work. Use when the user pastes a traceback, terminal error, CUDA OOM, checkpoint load failure, sha... |
| `taobao-product-reviews` | "Fetch customer reviews for a Taobao or Tmall product by itemId, returning reviewer name, date, purchased variant, review text, and photo URLs. Use when user... |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. |
| `tdd-workflow` | Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, ... |
| `trustpilot-reviews` | "Trustpilot customer reviews scraper for any company listed on trustpilot.com — given a company domain (e.g. shopify.com, apple.com, shopwagandtail.com) plus... |
| `walmart-product-reviews` | "Walmart product reviews scraper: given a walmart.com product item ID, navigate to the reviews page and extract paginated customer reviews including reviewId... |

## Integrations & Platforms (43)

| Skill | Description |
|---|---|
| `discord-bot-architect` | Specialized skill for building production-ready Discord bots. |
| `emblemai-crypto-wallet` | "Crypto wallet management across 7 blockchains via EmblemAI Agent Hustle API. Balance checks, token swaps, portfolio analysis, and transaction execution for ... |
| `exa-search` | Neural search via Exa MCP for web, code, and company research. Use when the user needs web search, code examples, company intel, people lookup, or AI-powered... |
| `google-maps-contact-extract` | "Extracts business contact details from Google Maps search results and place detail pages, then visits each business website to collect emails, phone numbers... |
| `google-search-serp` | "Extracts Google Search results page (SERP) data including organic results, paid ads, related searches, People Also Ask questions, AI Overview text, and tota... |
| `instagram-hashtag-posts` | "Scrapes Instagram posts by hashtag, returning media items with captions, like/comment counts, media URLs and user info from the hashtag explore feed. Use wh... |
| `instagram-place-posts` | "Scrapes Instagram posts tagged at a specific location or place, returning media items with captions, like/comment counts, media URLs and user info. Use when... |
| `instagram-post-comments` | "Fetches comments from an Instagram post including comment text, username, timestamp, like count and reply count. Use when user mentions Instagram comments s... |
| `instagram-profile-meta` | "Fetches Instagram user profile metadata including bio, follower count, following count, post count, verification status and other profile details. Use when ... |
| `instagram-profile-posts` | "Scrapes posts from an Instagram user's profile feed including captions, media URLs, like/comment counts, timestamps and location tags. Use when user mention... |
| `lark-approval` | "飞书审批：查询和处理审批待办/已办/实例，搜索可发起审批定义、查看定义详情并发起原生审批实例。当用户要处理审批任务、查看审批实例、搜索或发起审批时使用。审批待办不是飞书任务；非审批类待办走 lark-task。不负责创建审批定义；三方审批定义不走原生提单。" |
| `lark-apps` | "妙搭（Spark/Miaoda）应用开发与托管：应用创建、本地全栈开发、云端生成迭代、创意设计（UI mockup / 可交互原型 / 线框图 / 落地页 / 仪表盘 / 幻灯片 deck / 视觉探索）、AI相关能力和飞书平台能力或者其他外部能力集成、日志/Trace/监控指标/PV/UV 查询、环境变量管理... |
| `lark-attendance` | "飞书考勤打卡：查询自己的考勤打卡记录" |
| `lark-base` | "飞书多维表格（Base）操作：建表、字段、记录、视图、统计、公式/lookup、表单、仪表盘、workflow、角色权限；遇到 Base/多维表格/bitable 或 /base/ 链接时使用。文件导入/导出转 lark-drive，认证/授权转 lark-shared。" |
| `lark-calendar` | "飞书日历：管理日历日程和会议室。查看/搜索日程、创建/更新日程、管理参会人、查询忙闲和推荐时段、预定会议室。当用户需要查看日程安排、创建/修改会议、查询/预定会议室时使用。不负责：查询过去的视频会议记录（走 lark-vc）、待办任务（走 lark-task）。" |
| `lark-contact` | "飞书 / Lark 通讯录:按姓名 / 邮箱解析成 open_id,或按 open_id 反查姓名 / 部门 / 邮箱 / 联系方式 / 个人状态 / 签名,以及按关键词搜索当前用户可见的机器人 / 智能体(agent)。当用户提到一个名字要下一步发消息 / 排日程,或拿到 open_id 想查具体信息时使用。... |
| `lark-demo` | Demo skill |
| `lark-doc` | "飞书云文档（Docx / Wiki 文档）：读取和编辑飞书文档内容。当用户给出文档 URL 或 token，或需要查看、创建、编辑文档、插入或下载文档图片附件时使用。文档中嵌入的电子表格、多维表格、画板，先用本 skill 提取 token 再切到对应 skill。当用户给出 doubao.com 的 /doc... |
| `lark-drive` | "飞书云空间（云盘/云存储）：管理 Drive 文件和文件夹，包含上传/下载、创建文件夹、复制/移动/删除、查看元数据、查询权限设置、评论/权限/订阅、标题、版本、飞书文档密级标签（secure labels）和本地文件导入。用户需要整理云盘目录、处理云空间资源 URL/token、判断链接类型/真实 token... |
| `lark-event` | "Lark/Feishu real-time event listening / subscribing / consuming: stream events as NDJSON via `lark-cli event consume <EventKey>` (covers IM messages/reactio... |
| `lark-im` | "飞书即时通讯：收发消息和管理群聊。发送和回复消息、搜索聊天记录、管理群聊成员、上传下载图片和文件（支持大文件分片下载）、管理表情回复、发送应用内/短信/电话加急、发送和处理交互卡片（Interactive Card）、监听卡片按钮回调（card.action.trigger）。当用户需要发消息、查看或搜索聊天记... |
| `lark-mail` | "飞书邮箱：Use when user mentions 起草邮件、写邮件、草稿、发送/回复/转发邮件、查阅邮件、看邮件、搜索邮件、邮件文件夹、邮件标签、邮件联系人、监听新邮件、邮件收信规则等；use for mail/email intent only. Do not use for docs/sheets/c... |
| `lark-markdown` | "飞书 Markdown：查看、创建、上传、编辑和比较 Markdown 文件。当用户需要创建或编辑 Markdown 文件、读取、修改、局部 patch 或比较差异时使用。不负责将 Markdown 导入为飞书在线文档，也不负责文件搜索、权限、评论、移动、删除等云空间管理操作。" |
| `lark-minutes` | "飞书妙记：搜索妙记、查看妙记基础信息、下载/上传音视频、读取或编辑妙记的产物内容、改标题、替换说话人/关键词、申请妙记查看/编辑权限。当给出minute_token、本地音视频文件，要查/改/转妙记产物，或用户明确要主动申请妙记权限时使用；本地音视频转纪要/逐字稿优先走本 skill，不要用 ffmpeg/wh... |
| `lark-note` | "飞书会议纪要（Note）直查：已知 note_id 时查询纪要详情、展示类型、关联文档 token，并读取 unified 原始逐字记录。当用户已持有 note_id，或从文档显式 vc-node-id 获得 note_id 时使用。不负责会议/日程/妙记定位、文档标题搜索或 Docx 正文读取。" |
| `lark-okr` | "飞书 OKR：管理目标与关键结果。查看和编辑 OKR 周期、目标、关键结果、对齐关系、量化指标和进展记录。当用户需要查看或创建 OKR、管理目标和关键结果、查看对齐关系时使用。不负责：待办任务管理（lark-task）、日程/会议安排（lark-calendar）、绩效评估" |
| `lark-shared` | "Use for lark-cli setup/auth tasks: auth login/status/logout, user vs bot identity, business-domain permissions (--domain, including all/docs/drive), missing... |
| `lark-sheets` | "飞书电子表格：创建和操作电子表格。支持创建表格、管理工作表与行列结构（增删/合并/调整尺寸/隐藏/冻结）、读写单元格（值/公式/样式/批注/单元格图片）、查找替换、多操作原子批量更新，以及图表、透视表、条件格式、筛选器、迷你图、浮动图片等对象的创建与维护。当用户需要创建电子表格、管理工作表、批量读写或编辑数据、... |
| `lark-skill-maker` | "创建 lark-cli 的自定义 Skill。当用户需要把飞书 API 操作封装成可复用的 Skill（包装原子 API 或编排多步流程）时使用。" |
| `lark-task` | "飞书任务：管理任务、清单和任务智能体。创建待办任务、查看和更新任务状态、拆分子任务、组织任务清单、分配协作成员、上传任务附件、注册或注销任务智能体、更新任务智能体的主页数据、写入智能体任务记录。当用户需要创建待办事项、查看任务列表、跟踪任务进度、管理项目清单或给他人分配任务、为任务上传附件文件、注册注销任务智能... |
| `lark-vc` | "飞书视频会议：搜索历史会议记录、查询会议纪要（总结/待办/章节/逐字稿）、查询参会人快照。当用户查询已结束的会议、获取会议产物（纪要/妙记）、查看参会人时使用；查询未来日程走 lark-calendar。不负责：Agent 真实入会/离会、会中实时事件（走 lark-vc-agent）。" |
| `lark-vc-agent` | "飞书视频会议会中能力：用于让应用机器人真实加入或离开正在进行的会议，并读取当前身份可见的会中事件、发送会中文本消息或会中表情。适用于用户询问正在开的会议发生了什么、谁在发言、是否共享内容，或需要发现当前可读的进行中会议 ID。不负责已结束会议搜索、参会人快照、纪要、逐字稿或录制查询，这些使用 lark-vc 技能。" |
| `lark-whiteboard` | > |
| `lark-wiki` | "飞书知识库：管理知识空间、空间成员和文档节点。创建和查询知识空间、查看和管理空间成员、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、查看或管理空间成员、移动或复制节点时使用。当用户给出 doubao.com 的 /wiki/ URL/token 时，也应直... |
| `lark-workflow-meeting-summary` | "会议纪要整理工作流：汇总指定时间范围内的会议纪要并生成结构化报告。当用户需要整理会议纪要、生成会议周报、回顾一段时间内的会议内容时使用。" |
| `lark-workflow-standup-report` | "日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要。适用于了解今天/明天/本周的安排。" |
| `linkedin-content` | "LinkedIn post writing with hook formulas, formatting rules, and engagement patterns. Covers post types, algorithm signals, character limits, and content pil... |
| `linkedin-jobs-search` | "Search LinkedIn job listings and extract full job details. Supports filtering by work type (remote/on-site/hybrid), contract type (full-time/part-time/contr... |
| `release-skills` | Universal release workflow. Auto-detects version files and changelogs. Supports Node.js, Python, Rust, Claude Plugin, GitHub Releases, annotated tags, histor... |
| `slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users reques... |
| `upgrading-expo` | "Upgrade Expo SDK versions" |
| `x-api` | X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native... |
| `youtube-transcript` | "YouTube transcript extraction and content reformatting: given a YouTube video URL, opens the video's transcript panel, extracts all timestamped segments, an... |

## Mobile & Desktop (1)

| Skill | Description |
|---|---|
| `xcode-project-setup` | Safely modifies Xcode projects (.pbxproj) to add Swift Packages and link files. Use this skill whenever an iOS project needs dependencies installed (e.g. Fir... |

## Document & Office (20)

| Skill | Description |
|---|---|
| `article-writing` | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand ... |
| `case-study-writing` | "B2B case study writing with STAR framework, data visualization, and research. Covers structure, customer quotes, metrics presentation, and distribution form... |
| `copy-editing` | "When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the user mentions 'edit this copy,' 'rev... |
| `docs-generator` | Use when user wants to write documentation, proposals, technical specs, or decision docs. Guide users through a structured 3-stage workflow for co-authoring ... |
| `documentation-lookup` | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when th... |
| `docx` | "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: ... |
| `excel-master` | "Use when creating, editing, or analyzing Excel spreadsheets (.xlsx, .xlsm, .csv, .tsv). For building financial models with formulas, reading data for analys... |
| `humanizer` | \| |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `internal-comms` | "Write internal communications such as status reports, leadership updates, 3P updates, newsletters, FAQs, incident reports, and project updates using repeata... |
| `pdf` | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multipl... |
| `pptx` | "Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or prese... |
| `product-changelog` | "Product changelog and release notes that users actually read. Covers categorization, user-facing language, visuals, and distribution. Use for: release notes... |
| `technical-blog-writing` | "Technical blog post writing with structure, code examples, and developer audience conventions. Covers post types, code formatting, explanation depth, and de... |
| `writing-beats` | Writing, exploit — assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |
| `writing-fragments` | Writing, explore — mine raw fragments, no structure yet. |
| `writing-guidelines` | Review docs/prose for Writing Guidelines compliance. Use when asked to "review my docs", "check writing style", "audit prose", "review docs voice and tone", ... |
| `writing-shape` | Writing, exploit — shape raw material into an article, paragraph by paragraph. |
| `xlsx` | "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing... |

## Languages & Tooling (2)

| Skill | Description |
|---|---|
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep module — implementation hidden in subfolders, reachable only through its entry-point... |
| `trustpilot-company-info` | "Trustpilot company profile lookup on trustpilot.com — input a company domain (e.g. apple.com, shopify.com, shopwagandtail.com) and extract company metadata:... |

## General Purpose & Uncategorized (5)

| Skill | Description |
|---|---|
| `advogado-criminal` | Advogado criminalista especializado em Maria da Penha, violencia domestica, feminicidio, direito penal brasileiro, medidas protetivas, inquerito policial e a... |
| `advogado-especialista` | 'Advogado especialista em todas as areas do Direito brasileiro: familia, criminal, trabalhista, tributario, consumidor, imobiliario, empresarial, civil e con... |
| `
| `ima-sdk-basics` | Agent skill from official repository |
| `managed-airflow-migrations` | Provides guidance for migrating Apache Airflow DAGs in Managed Service for Apache Airflow (MSAA; formerly Cloud Composer). Covers migration to Airflow... |research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched... |

---

_Generated by Workshop management tooling._
