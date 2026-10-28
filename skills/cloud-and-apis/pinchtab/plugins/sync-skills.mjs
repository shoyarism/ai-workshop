import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');

const mappings = {
  openclaw: [{ from: 'skills/pinchtab', to: 'plugins/openclaw/skills/pinchtab' }],
  grok: [
    { from: 'skills/pinchtab', to: 'plugins/grok/skills/pinchtab' },
    { from: 'skills/pinchtab-mcp', to: 'plugins/grok/skills/pinchtab-mcp' },
  ],
};

function listFiles(dir, prefix = '') {
  if (!existsSync(dir)) {
    return [];
  }
  const names = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.DS_Store') {
      continue;
    }
    const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      names.push(...listFiles(full, rel));
    } else {
      names.push(rel);
    }
  }
  return names.sort();
}

function sameTree(src, dest) {
  const left = listFiles(src);
  const right = listFiles(dest);
  if (left.join('\n') !== right.join('\n')) {
    return false;
  }
  return left.every((rel) =>
    readFileSync(join(src, rel)).equals(readFileSync(join(dest, rel))),
  );
}

function syncOne(fromRel, toRel, check) {
  const src = resolve(repoRoot, fromRel);
  const dest = resolve(repoRoot, toRel);
  if (!existsSync(src)) {
    console.error(`missing source skill directory: ${src}`);
    process.exit(1);
  }
  if (check) {
    if (!sameTree(src, dest)) {
      console.error(`out of date: ${toRel} (run: node plugins/sync-skills.mjs grok)`);
      process.exit(1);
    }
    console.log(`ok ${toRel}`);
    return;
  }
  mkdirSync(dirname(dest), { recursive: true });
  rmSync(dest, { recursive: true, force: true });
  cpSync(src, dest, { recursive: true });
  console.log(`synced ${src} -> ${dest}`);
}

const args = process.argv.slice(2);
const check = args.includes('--check');
const target = args.find((arg) => arg === 'openclaw' || arg === 'grok' || arg === 'all') ?? 'all';
const selected = target === 'all' ? ['openclaw', 'grok'] : [target];

for (const name of selected) {
  for (const mapping of mappings[name]) {
    syncOne(mapping.from, mapping.to, check);
  }
}
