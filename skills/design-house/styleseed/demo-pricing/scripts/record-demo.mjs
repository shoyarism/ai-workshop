import { chromium } from "playwright";
import { mkdirSync, rmSync } from "node:fs";

const URL = "https://styleseed-demo.vercel.app/";
const OUT = "scripts/recordings";

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ channel: "chrome", headless: true });
const context = await browser.newContext({
  viewport: { width: 720, height: 980 },
  deviceScaleFactor: 2,
  recordVideo: { dir: OUT, size: { width: 720, height: 980 } },
});
const page = await context.newPage();

await page.goto(URL, { waitUntil: "networkidle" });

await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(1500);

const fontInfo = await page.evaluate(() => ({
  body: getComputedStyle(document.body).fontFamily,
  msgFont: getComputedStyle(document.querySelector("h1, .text-\\[15px\\], div") || document.body).fontFamily,
  fonts: Array.from(document.fonts).map((f) => ({ family: f.family, status: f.status })),
}));
console.log("FONT DIAGNOSTIC:", JSON.stringify(fontInfo, null, 2));

// Re-trigger streaming by re-clicking current skin so animation starts
// after fonts are ready (initial useEffect already ran during font load)
await page.getByRole("button", { name: "Raycast" }).click();
await page.waitForTimeout(200);
await page.getByRole("button", { name: "Toss" }).click();

// Initial Toss stream
await page.waitForTimeout(5500);

// Click Raycast
await page.getByRole("button", { name: "Raycast" }).click();
await page.waitForTimeout(5500);

// Click Arc
await page.getByRole("button", { name: "Arc" }).click();
await page.waitForTimeout(5500);

// Back to Toss
await page.getByRole("button", { name: "Toss" }).click();
await page.waitForTimeout(2200);

await context.close();
await browser.close();

console.log("done — check", OUT);
