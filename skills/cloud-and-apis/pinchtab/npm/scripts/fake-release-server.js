#!/usr/bin/env node
'use strict';

// fake-release-server serves a single release asset (the platform binary) and a
// matching checksums.txt over plain http, mirroring the GitHub release layout
// that download.ts expects: <base>/v<version>/<asset>. It exists so the install
// smoke test can drive the real postinstall download path — checksum verify,
// atomic rename, chmod, HOME-based install dir — without the network or a
// published release. The checksum it serves is computed from the served bytes,
// so the real verifySHA256 check passes.
//
// Driven entirely by env so the shell harness stays declarative:
//   FAKE_RELEASE_PORT          port to listen on (default 0 → OS-assigned)
//   FAKE_RELEASE_VERSION       version segment, e.g. 0.15.1
//   FAKE_RELEASE_BINARY_NAME   asset name, e.g. pinchtab-linux-amd64
//   FAKE_RELEASE_BINARY_PATH   path to the file served as that asset
// On listen it prints "listening <port>" so the caller can learn an OS-assigned
// port and wait for readiness.

const http = require('http');
const fs = require('fs');
const crypto = require('crypto');

const version = process.env.FAKE_RELEASE_VERSION;
const binaryName = process.env.FAKE_RELEASE_BINARY_NAME;
const binaryPath = process.env.FAKE_RELEASE_BINARY_PATH;
const port = Number(process.env.FAKE_RELEASE_PORT || 0);

for (const [name, value] of [
  ['FAKE_RELEASE_VERSION', version],
  ['FAKE_RELEASE_BINARY_NAME', binaryName],
  ['FAKE_RELEASE_BINARY_PATH', binaryPath],
]) {
  if (!value) {
    console.error(`fake-release-server: missing ${name}`);
    process.exit(1);
  }
}

const binaryBytes = fs.readFileSync(binaryPath);
const sha256 = crypto.createHash('sha256').update(binaryBytes).digest('hex');
const checksums = `${sha256}  ${binaryName}\n`;

const prefix = `/v${version}/`;

const server = http.createServer((req, res) => {
  if (!req.url || !req.url.startsWith(prefix)) {
    res.writeHead(404).end('not found');
    return;
  }
  const asset = req.url.slice(prefix.length);
  if (asset === 'checksums.txt') {
    res.writeHead(200, { 'content-type': 'text/plain' }).end(checksums);
    return;
  }
  if (asset === binaryName) {
    res.writeHead(200, { 'content-type': 'application/octet-stream' }).end(binaryBytes);
    return;
  }
  res.writeHead(404).end('not found');
});

server.listen(port, '127.0.0.1', () => {
  const actualPort = server.address().port;
  // Single stable line the harness greps for.
  console.log(`listening ${actualPort}`);
});

for (const sig of ['SIGINT', 'SIGTERM']) {
  process.on(sig, () => server.close(() => process.exit(0)));
}
