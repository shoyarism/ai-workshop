/**
 * Boot `next start`, screenshot showcase pages, shut down. One-off
 * verification tool — not part of the deploy pipeline.
 */
import { spawn } from "node:child_process";
import { chromium } from "playwright";
import { writeFileSync, mkdirSync } from "node:fs";

const PORT = 3037;
const TARGETS = [
  { url: `http://localhost:${PORT}/showcase`, file: "showcase-index.png" },
  { url: `http://localhost:${PORT}/showcase/finance`, file: "showcase-finance-toss-spring.png" },
];

mkdirSync("scripts/captures", { recursive: true });

const server = spawn("npx", ["next", "start", "-p", String(PORT)], {
  stdio: ["ignore", "pipe", "pipe"],
});
let ready = false;
const readyP = new Promise((resolve) => {
  server.stdout.on("data", (chunk) => {
    const out = chunk.toString();
    if (!ready && /Ready in|started server on/i.test(out)) {
      ready = true;
      resolve();
    }
  });
});
server.stderr.on("data", (d) => process.stderr.write(d));

// safety timeout
const timeout = setTimeout(() => {
  console.error("next start timed out");
  server.kill("SIGTERM");
  process.exit(1);
}, 30_000);

await readyP;
clearTimeout(timeout);
// small grace period for routes to register
await new Promise((r) => setTimeout(r, 600));

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 2,
});
const page = await ctx.newPage();

for (const t of TARGETS) {
  await page.goto(t.url, { waitUntil: "networkidle" });
  // settle motion
  await page.waitForTimeout(900);
  const png = await page.screenshot({ type: "png", fullPage: false });
  writeFileSync(`scripts/captures/${t.file}`, png);
  console.log(`✓ ${t.file} (${(png.length / 1024).toFixed(1)}KB)`);
}

await browser.close();
server.kill("SIGTERM");
