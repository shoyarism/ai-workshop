import * as path from 'path';
import * as fs from 'fs';

export interface Platform {
  os: 'darwin' | 'linux' | 'windows';
  arch: 'amd64' | 'arm64';
}

// detectPlatform maps Node's process.platform/process.arch to the goreleaser
// binary triple. The values are injectable so tests can drive the full matrix
// without re-declaring the mapping.
export function detectPlatform(
  platform: string = process.platform,
  nodeArch: string = process.arch
): Platform {
  // Only support x64 (amd64) and arm64
  let arch: 'amd64' | 'arm64';
  if (nodeArch === 'x64') {
    arch = 'amd64';
  } else if (nodeArch === 'arm64') {
    arch = 'arm64';
  } else {
    throw new Error(
      `Unsupported architecture: ${nodeArch}. ` + `Only x64 (amd64) and arm64 are supported.`
    );
  }

  const osMap: Record<string, 'darwin' | 'linux' | 'windows'> = {
    darwin: 'darwin',
    linux: 'linux',
    win32: 'windows',
  };

  const os_name = osMap[platform];
  if (!os_name) {
    throw new Error(`Unsupported platform: ${platform}`);
  }

  return { os: os_name, arch };
}

export function getBinaryName(platform: Platform): string {
  const { os, arch } = platform;
  const archName = arch === 'arm64' ? 'arm64' : 'amd64';

  if (os === 'windows') {
    return `pinchtab-${os}-${archName}.exe`;
  }
  return `pinchtab-${os}-${archName}`;
}

// getBinDir returns the LEGACY $HOME-based managed binary directory
// (~/.pinchtab/bin). New installs use the package-relative getManagedBinDir;
// this remains only so resolveManagedBinaryPath can still find binaries placed
// by older versions. Deriving the location from $HOME is exactly what caused
// issue #628 (install as root under sudo, run as the user → different $HOME).
export function getBinDir(): string {
  return path.join(process.env.HOME || process.env.USERPROFILE || '', '.pinchtab', 'bin');
}

export function findRepoRoot(fromDir: string): string | null {
  let dir = path.resolve(fromDir);

  while (dir) {
    if (
      fs.existsSync(path.join(dir, 'go.mod')) &&
      fs.existsSync(path.join(dir, 'cmd', 'pinchtab'))
    ) {
      return dir;
    }

    const parent = path.dirname(dir);
    if (parent === dir) {
      break;
    }
    dir = parent;
  }

  return null;
}

export function getCheckoutBinaryPath(fromDir: string): string | null {
  const repoRoot = findRepoRoot(fromDir);
  if (!repoRoot) {
    return null;
  }
  return path.join(repoRoot, 'pinchtab-dev');
}

// getBinaryPath returns the LEGACY $HOME-based binary path. Retained for
// backwards-compatible lookups (see resolveManagedBinaryPath); new installs
// write to the package-relative getManagedBinaryPath instead.
export function getBinaryPath(binaryName: string, version?: string): string {
  // Version-specific path: ~/.pinchtab/bin/0.7.0/pinchtab-darwin-arm64
  // This allows multiple versions to coexist and prevents silent overwrites
  if (version) {
    return path.join(getBinDir(), version, binaryName);
  }

  // Fallback to version-less for backwards compat
  return path.join(getBinDir(), binaryName);
}

// findPackageRoot walks up from fromDir to the nearest directory containing a
// package.json and returns it (or null if none is found). This is the installed
// npm package's own directory, which — unlike $HOME — is identical whether
// postinstall runs as root/sudo or the CLI runs as the invoking user. It is the
// anchor for the managed binary location so the two can never diverge (#628).
export function findPackageRoot(fromDir: string): string | null {
  let dir = path.resolve(fromDir);

  while (dir) {
    if (fs.existsSync(path.join(dir, 'package.json'))) {
      return dir;
    }

    const parent = path.dirname(dir);
    if (parent === dir) {
      break;
    }
    dir = parent;
  }

  return null;
}

// MANAGED_BIN_DIRNAME is the directory, inside the installed package, that holds
// the downloaded Go binary. A dot-prefixed name keeps it out of the way; it is
// created at install time (not shipped in the package tarball).
const MANAGED_BIN_DIRNAME = '.managed-bin';

// getManagedBinDir returns the package-relative managed binary directory for the
// package containing fromDir. It falls back to the legacy $HOME location only
// when no package root can be found, which should not happen for an installed
// package but keeps resolution defined in odd layouts.
export function getManagedBinDir(fromDir: string): string {
  const root = findPackageRoot(fromDir);
  if (!root) {
    return getBinDir();
  }
  return path.join(root, MANAGED_BIN_DIRNAME);
}

// getManagedBinaryPath returns the versioned managed binary path (version-less
// when version is omitted). Both the installer (download.ts, write) and the
// resolver (resolveManagedBinaryPath, read) go through this single function so
// the install-time and run-time locations cannot drift apart.
export function getManagedBinaryPath(
  fromDir: string,
  binaryName: string,
  version?: string
): string {
  const dir = getManagedBinDir(fromDir);
  return version ? path.join(dir, version, binaryName) : path.join(dir, binaryName);
}

// readPackageVersion walks up from fromDir to the nearest package.json and
// returns its version. Shared so the wrapper, SDK, and installer agree on which
// versioned binary directory to look in.
export function readPackageVersion(fromDir: string): string {
  let dir = path.resolve(fromDir);

  while (dir) {
    const pkgPath = path.join(dir, 'package.json');
    if (fs.existsSync(pkgPath)) {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
      if (typeof pkg.version === 'string' && pkg.version.trim() !== '') {
        return pkg.version;
      }
    }

    const parent = path.dirname(dir);
    if (parent === dir) {
      break;
    }
    dir = parent;
  }

  throw new Error(`package.json with a version not found above ${fromDir}`);
}

// resolveManagedBinaryPath returns the path of the downloaded binary for the
// current platform. It prefers the package-relative managed location (stable
// across $HOME and user — issue #628), then falls back to binaries left by
// older versions under the legacy $HOME/.pinchtab/bin so existing installs keep
// working. It does NOT assert existence for the value it returns when nothing is
// found — callers decide how to report a missing binary; that value is the
// canonical (package-relative) path.
export function resolveManagedBinaryPath(fromDir: string): string {
  const binaryName = getBinaryName(detectPlatform());

  let version: string | undefined;
  try {
    version = readPackageVersion(fromDir);
  } catch {
    // Fall back to the version-less path when no package.json version is found.
  }

  // Preferred: package-relative, independent of $HOME.
  const preferred = getManagedBinaryPath(fromDir, binaryName, version);
  if (fs.existsSync(preferred)) {
    return preferred;
  }

  // Backwards compatibility: honor binaries installed by older versions under
  // the legacy $HOME/.pinchtab/bin location (versioned first, then version-less).
  const legacyCandidates = version
    ? [getBinaryPath(binaryName, version), getBinaryPath(binaryName)]
    : [getBinaryPath(binaryName)];
  for (const candidate of legacyCandidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return preferred;
}

// firstSubcommand returns the first non-flag argument, skipping the global
// `--server <url>` / `--server=<url>` option so callers can detect the
// subcommand (e.g. `mcp`) regardless of preceding flags.
export function firstSubcommand(argv: string[]): string | null {
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--server') {
      i += 1;
      continue;
    }
    if (arg.startsWith('--server=')) continue;
    if (!arg.startsWith('-')) return arg;
  }
  return null;
}
