/**
 * Capture a hero screenshot for every showcase entry, using each
 * entry's default skin + seed. Saves to public/showcase-hero/{id}.png
 * so the index card grid can render them at deploy time.
 *
 * Each Playwright context gets a fresh localStorage so the default
 * skin/seed encoded in the entry metadata is what's rendered.
 */
import { spawn } from "node:child_process";
import { chromium } from "playwright";
import { writeFileSync, mkdirSync } from "node:fs";

const PORT = 3038;
const ENTRIES = [
  "finance",
  "chat",
  "pricing",
  "issues",
  "settings",
  "marketing",
  "notes",
  "wallet",
  "food",
  "fitness",
  "music",
];

mkdirSync("public/showcase-hero", { recursive: true });

const server = spawn("npx", ["next", "start", "-p", String(PORT)], {
  stdio: ["ignore", "pipe", "pipe"],
});

const readyP = new Promise((resolve, reject) => {
  const timer = setTimeout(() => reject(new Error("next start timed out")), 30_000);
  server.stdout.on("data", (chunk) => {
    if (/Ready in|started server on/i.test(chunk.toString())) {
      clearTimeout(timer);
      resolve();
    }
  });
  server.on("error", (err) => {
    clearTimeout(timer);
    reject(err);
  });
});
server.stderr.on("data", (d) => process.stderr.write(d));

try {
  await readyP;
  await new Promise((r) => setTimeout(r, 600));

  const browser = await chromium.launch({ headless: true });

  for (const id of ENTRIES) {
    // fresh context wipes localStorage so the entry's primarySkin/Seed take effect
    const ctx = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      deviceScaleFactor: 2,
    });
    const page = await ctx.newPage();
    await page.goto(`http://localhost:${PORT}/showcase/${id}`, {
      waitUntil: "networkidle",
    });
    // wait for the dual toggle bar + content to settle motion
    await page.waitForTimeout(1100);

    // capture just the rendered showcase frame, not the whole header
    const frame = await page.locator("div[data-skin]").first();
    const png = await frame.screenshot({ type: "png" });
    writeFileSync(`public/showcase-hero/${id}.png`, png);
    console.log(`✓ ${id}.png (${(png.length / 1024).toFixed(1)}KB)`);

    await ctx.close();
  }

  await browser.close();
} finally {
  server.kill("SIGTERM");
}
