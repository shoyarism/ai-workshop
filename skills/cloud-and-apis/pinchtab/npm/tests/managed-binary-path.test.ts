/**
 * Managed binary path resolution (issue #628)
 *
 * The bug: the managed binary directory was derived from $HOME, so a global
 * install whose postinstall ran under one HOME (e.g. root, via `sudo npm i -g`)
 * placed the binary somewhere the CLI wrapper — running under the invoking
 * user's HOME — never looked. Install-time and run-time locations diverged.
 *
 * These tests pin the fix: the managed binary location is package-relative and
 * therefore independent of $HOME, while binaries left by older versions under
 * ~/.pinchtab/bin are still honored for backwards compatibility.
 */

import { test, describe, afterEach } from 'node:test';
import * as assert from 'node:assert';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import {
  detectPlatform,
  getBinaryName,
  getManagedBinaryPath,
  resolveManagedBinaryPath,
} from '../src/platform';

const BINARY_NAME = getBinaryName(detectPlatform());
const VERSION = '1.2.3';

describe('managed binary path (issue #628)', () => {
  const originalHome = process.env.HOME;
  const originalUserProfile = process.env.USERPROFILE;
  const tmpDirs: string[] = [];

  function restoreEnv(name: 'HOME' | 'USERPROFILE', value: string | undefined): void {
    if (value === undefined) {
      delete process.env[name];
    } else {
      process.env[name] = value;
    }
  }

  afterEach(() => {
    restoreEnv('HOME', originalHome);
    restoreEnv('USERPROFILE', originalUserProfile);
    for (const dir of tmpDirs.splice(0)) {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  // Build a throwaway installed-package layout: <root>/node_modules/pinchtab
  // with a package.json, and return the compiled-code dir the runtime resolves
  // from (dist/src, mirroring where platform.js lives when published).
  function makeInstalledPackage(version: string): { pkgDir: string; fromDir: string } {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pinchtab-pkg-'));
    tmpDirs.push(dir);
    const pkgDir = path.join(dir, 'node_modules', 'pinchtab');
    const fromDir = path.join(pkgDir, 'dist', 'src');
    fs.mkdirSync(fromDir, { recursive: true });
    fs.writeFileSync(
      path.join(pkgDir, 'package.json'),
      JSON.stringify({ name: 'pinchtab', version })
    );
    return { pkgDir, fromDir };
  }

  test('install target does not change with $HOME', () => {
    const { pkgDir, fromDir } = makeInstalledPackage(VERSION);

    process.env.HOME = '/root'; // postinstall as root under sudo
    const installPath = getManagedBinaryPath(fromDir, BINARY_NAME, VERSION);

    process.env.HOME = '/home/user1'; // CLI as the invoking user
    const runPath = getManagedBinaryPath(fromDir, BINARY_NAME, VERSION);

    assert.strictEqual(installPath, runPath, 'binary path must be independent of $HOME');
    assert.ok(
      installPath.startsWith(pkgDir + path.sep),
      `binary must live under the package root, got ${installPath}`
    );
    assert.ok(
      !installPath.includes(`${path.sep}.pinchtab${path.sep}`),
      `binary must not resolve under a $HOME-based ~/.pinchtab dir, got ${installPath}`
    );
  });

  test('resolve finds the package-relative binary under a different $HOME', () => {
    const { fromDir } = makeInstalledPackage(VERSION);

    // Simulate postinstall (root HOME) writing the downloaded binary.
    process.env.HOME = '/root';
    const installPath = getManagedBinaryPath(fromDir, BINARY_NAME, VERSION);
    fs.mkdirSync(path.dirname(installPath), { recursive: true });
    fs.writeFileSync(installPath, 'binary');

    // Resolve as a different user — must still find it.
    process.env.HOME = '/home/user1';
    assert.strictEqual(resolveManagedBinaryPath(fromDir), installPath);
  });

  test('falls back to a legacy ~/.pinchtab binary for already-installed users', () => {
    const { fromDir } = makeInstalledPackage(VERSION);

    const fakeHome = fs.mkdtempSync(path.join(os.tmpdir(), 'pinchtab-home-'));
    tmpDirs.push(fakeHome);
    process.env.HOME = fakeHome;
    delete process.env.USERPROFILE;

    // A binary only in the legacy versioned location under $HOME.
    const legacy = path.join(fakeHome, '.pinchtab', 'bin', VERSION, BINARY_NAME);
    fs.mkdirSync(path.dirname(legacy), { recursive: true });
    fs.writeFileSync(legacy, 'binary');

    // Package-relative path does not exist → resolver must fall back to legacy.
    assert.strictEqual(resolveManagedBinaryPath(fromDir), legacy);
  });

  test('reports the package-relative path when nothing is installed yet', () => {
    const { fromDir } = makeInstalledPackage(VERSION);
    process.env.HOME = '/home/user1';

    const resolved = resolveManagedBinaryPath(fromDir);
    assert.strictEqual(resolved, getManagedBinaryPath(fromDir, BINARY_NAME, VERSION));
    assert.ok(!resolved.includes(`${path.sep}.pinchtab${path.sep}`));
  });
});
