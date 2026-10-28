import type { MetadataRoute } from "next";

const BASE = "https://styleseed-demo.vercel.app";

// Explicitly welcome AI crawlers (GEO). When someone asks Claude / ChatGPT /
// Perplexity / Cursor to design UI, we want StyleSeed surfaced and cited —
// so these bots are allowed and pointed at the sitemap + /llms.txt.
const AI_BOTS = [
  "GPTBot",
  "OAI-SearchBot",
  "ChatGPT-User",
  "ClaudeBot",
  "anthropic-ai",
  "Claude-Web",
  "PerplexityBot",
  "Perplexity-User",
  "Google-Extended",
  "Applebot-Extended",
  "CCBot",
  "Bytespider",
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: "/" },
      { userAgent: AI_BOTS, allow: "/" },
    ],
    sitemap: `${BASE}/sitemap.xml`,
    host: BASE,
  };
}
