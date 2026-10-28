/**
 * Submit the live sitemap URLs to IndexNow so Bing, Yandex, Seznam, and
 * other participating engines crawl new/changed pages near-instantly —
 * no waiting for an organic recrawl.
 *
 * The key is public by design: it is also hosted at
 *   https://styleseed-demo.vercel.app/<KEY>.txt
 * which proves we own the host. Run AFTER a production deploy:
 *   node scripts/indexnow.mjs
 */

const HOST = "styleseed-demo.vercel.app";
const KEY = "fd915a7d380a76cd7ba3fc3851eb40d4";
const SITEMAP = `https://${HOST}/sitemap.xml`;
const ENDPOINT = "https://api.indexnow.org/indexnow";

async function main() {
  const xml = await (await fetch(SITEMAP)).text();
  const urlList = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  if (urlList.length === 0) {
    console.error("No URLs found in sitemap — aborting.");
    process.exit(1);
  }
  console.log(`Submitting ${urlList.length} URLs to IndexNow…`);

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({
      host: HOST,
      key: KEY,
      keyLocation: `https://${HOST}/${KEY}.txt`,
      urlList,
    }),
  });

  // IndexNow returns 200 (accepted) or 202 (accepted, validation pending).
  console.log(`IndexNow responded: ${res.status} ${res.statusText}`);
  if (![200, 202].includes(res.status)) {
    console.error(await res.text());
    process.exit(1);
  }
  console.log("✓ Submitted. Bing/Yandex/Seznam will crawl these shortly.");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
