#!/usr/bin/env bash
#
# Hermetic install smoke test for the "global install downloads to the wrong
# HOME" bug (issue #628). It reproduces the mechanism WITHOUT Docker, sudo, or
# the network: the only thing that bug needs is postinstall running under a
# different HOME than the CLI wrapper.
#
#   1. Serve a fake release (real binary bytes + matching checksums.txt) from a
#      local http server, pointed at via PINCHTAB_DOWNLOAD_BASE_URL.
#   2. `npm install -g` with HOME=$INSTALL_HOME  -> postinstall downloads the
#      binary into $INSTALL_HOME/.pinchtab/bin/... (the "root" side of the bug).
#   3. Run the CLI with HOME=$RUN_HOME (a different HOME) -> the wrapper must
#      still find the binary and run.
#
# On unfixed code the CLI exits non-zero with "binary not found" -- this script
# fails and prints exactly where the binary landed vs. where the wrapper looked.
# After the package-relative fix, step 3 passes regardless of HOME.
#
# Usage: npm-install-home-divergence.sh [npm-install-target]
#   npm-install-target defaults to a freshly packed tarball of this package.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NPM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TMP_ROOT="$(mktemp -d)"
INSTALL_HOME="$TMP_ROOT/install-home"   # HOME during 'npm install' (~ root under sudo)
RUN_HOME="$TMP_ROOT/run-home"           # HOME when running the CLI (the real user)
PREFIX_DIR="$TMP_ROOT/prefix"           # global npm prefix, OUTSIDE the repo tree
SERVER_LOG="$TMP_ROOT/server.log"
SERVER_PID=""

cleanup() {
  if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
    wait "$SERVER_PID" >/dev/null 2>&1 || true
  fi
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

mkdir -p "$INSTALL_HOME" "$RUN_HOME" "$PREFIX_DIR"

# Ensure the package is built (we need dist/ for the platform helper and pack).
if [ ! -f "$NPM_DIR/dist/src/platform.js" ]; then
  echo "Building npm package (dist/ missing)..."
  (cd "$NPM_DIR" && npm run build >/dev/null)
fi

VERSION="$(node -p "require('$NPM_DIR/package.json').version")"
BINARY_NAME="$(node -e "const p=require('$NPM_DIR/dist/src/platform');process.stdout.write(p.getBinaryName(p.detectPlatform()))")"
echo "Platform binary: $BINARY_NAME   version: $VERSION"

# Resolve the install target (packed tarball by default -> hermetic, no registry).
if [ "$#" -ge 1 ]; then
  INSTALL_TARGET="$1"
else
  # Discard pack output entirely: prepack/prepare lifecycle scripts print to
  # stdout, so parsing the tarball name from it is unreliable. The name is
  # deterministic for this unscoped package: <name>-<version>.tgz.
  echo "Packing tarball from ${NPM_DIR} ..."
  (cd "$NPM_DIR" && npm pack --pack-destination "$TMP_ROOT" >/dev/null 2>&1)
  INSTALL_TARGET="$TMP_ROOT/pinchtab-$VERSION.tgz"
  if [ ! -f "$INSTALL_TARGET" ]; then
    echo "smoke failed: npm pack did not produce $INSTALL_TARGET" >&2
    exit 1
  fi
fi
echo "Install target: $INSTALL_TARGET"

# Fake release binary: a tiny executable stub that prints a recognizable marker.
MARKER="pinchtab-home-divergence-smoke $VERSION"
FAKE_BINARY="$TMP_ROOT/$BINARY_NAME"
printf '#!/bin/sh\necho "%s"\nexit 0\n' "$MARKER" >"$FAKE_BINARY"
chmod +x "$FAKE_BINARY"

# Start the local fake-release server on an OS-assigned port.
FAKE_RELEASE_VERSION="$VERSION" \
FAKE_RELEASE_BINARY_NAME="$BINARY_NAME" \
FAKE_RELEASE_BINARY_PATH="$FAKE_BINARY" \
FAKE_RELEASE_PORT=0 \
  node "$SCRIPT_DIR/fake-release-server.js" >"$SERVER_LOG" 2>&1 &
SERVER_PID="$!"

PORT=""
for _ in $(seq 1 50); do
  PORT="$(sed -n 's/^listening \([0-9]*\)$/\1/p' "$SERVER_LOG" 2>/dev/null | head -1)"
  [ -n "$PORT" ] && break
  sleep 0.1
done
if [ -z "$PORT" ]; then
  echo "smoke failed: fake release server never reported a port" >&2
  cat "$SERVER_LOG" >&2
  exit 1
fi
BASE_URL="http://127.0.0.1:$PORT"
echo "Fake release server: $BASE_URL"

# -- Install side: postinstall runs with HOME=$INSTALL_HOME -------------------
echo
echo "Installing (HOME=$INSTALL_HOME) ..."
HOME="$INSTALL_HOME" \
PINCHTAB_DOWNLOAD_BASE_URL="$BASE_URL" \
  npm install -g --prefix "$PREFIX_DIR" "$INSTALL_TARGET" >"$TMP_ROOT/install.log" 2>&1 || {
  echo "smoke failed: npm install errored" >&2
  cat "$TMP_ROOT/install.log" >&2
  exit 1
}

# postinstall must have downloaded the binary somewhere. After the fix it lands
# in the package-relative managed dir; before the fix it lands under
# $INSTALL_HOME/.pinchtab. Accept either here -- the run-side check below is what
# actually gates on the bug -- but fail clearly if NEITHER exists, which means
# postinstall never ran (a broken test env, not issue #628).
PKG_BINARY="$PREFIX_DIR/lib/node_modules/pinchtab/.managed-bin/$VERSION/$BINARY_NAME"
LEGACY_BINARY="$INSTALL_HOME/.pinchtab/bin/$VERSION/$BINARY_NAME"
if [ -f "$PKG_BINARY" ]; then
  DOWNLOADED_TO="$PKG_BINARY"
  echo "postinstall downloaded binary -> $DOWNLOADED_TO (package-relative)"
elif [ -f "$LEGACY_BINARY" ]; then
  DOWNLOADED_TO="$LEGACY_BINARY"
  echo "postinstall downloaded binary -> $DOWNLOADED_TO (legacy \$HOME location)"
else
  echo "smoke inconclusive: postinstall did not download a binary to either" >&2
  echo "  $PKG_BINARY" >&2
  echo "  $LEGACY_BINARY" >&2
  echo "install log:" >&2; cat "$TMP_ROOT/install.log" >&2
  exit 1
fi

# -- Run side: the CLI runs with a DIFFERENT HOME=$RUN_HOME -------------------
CLI="$PREFIX_DIR/bin/pinchtab"
echo
echo "Running CLI (HOME=$RUN_HOME) : $CLI --version"
set +e
CLI_OUT="$(HOME="$RUN_HOME" "$CLI" --version 2>&1)"
CLI_RC=$?
set -e

echo "-- CLI output --"
echo "$CLI_OUT"
echo "-- exit code: $CLI_RC --"

if [ "$CLI_RC" -eq 0 ] && printf '%s' "$CLI_OUT" | grep -qF "$MARKER"; then
  echo
  echo "[PASS] CLI resolved the binary across the install/run HOME boundary."
  exit 0
fi

echo
echo "[FAIL] CLI could not find the binary when run under a different HOME." >&2
echo "  installed at : $DOWNLOADED_TO" >&2
echo "  wrapper HOME : $RUN_HOME (looked under \$HOME/.pinchtab/bin/...)" >&2
echo "This is issue #628: the managed binary dir is derived from HOME, so an" >&2
echo "install as one user/HOME and a run as another can never agree." >&2
exit 1
