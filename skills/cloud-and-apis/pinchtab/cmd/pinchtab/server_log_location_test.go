package main

import (
	"bytes"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
	"time"

	"github.com/pinchtab/pinchtab/internal/config"
	"github.com/pinchtab/pinchtab/internal/srccensus"
)

func renderAgentHintsString(t *testing.T, st agentStatus) string {
	t.Helper()
	var buf bytes.Buffer
	renderAgentHints(&buf, st)
	return buf.String()
}

// The card's dead end: a server.log last written weeks ago, sitting beside a server
// that has never touched it. Whichever way the server was started, the banner has to
// name the sink that is live and disown the one that is not.
func TestServerLogWhereNamesTheLiveSinkAndDisownsTheStaleFile(t *testing.T) {
	stateDir := "/home/op/.pinchtab"
	backgroundLog := filepath.Join(stateDir, "server.log")
	daemonLog := "/home/op/.pinchtab/logs/daemon.err.log"

	for _, tc := range []struct {
		name            string
		daemonInstalled bool
		backgroundChild bool
		running         bool
		serverLogExists bool
		wantDestination string
		wantStale       string
	}{
		{
			name:            "daemon owns the server, so its log is the live one and server.log is not",
			daemonInstalled: true, running: true, serverLogExists: true,
			wantDestination: daemonLog,
			wantStale:       backgroundLog,
		},
		{
			name:            "background child writes server.log, which is therefore not stale",
			backgroundChild: true, running: true, serverLogExists: true,
			wantDestination: backgroundLog,
			wantStale:       "",
		},
		{
			name:    "foreground server logs to its terminal, so a server.log on disk is a leftover",
			running: true, serverLogExists: true,
			wantDestination: "stdout/stderr of the terminal running `pinchtab server`",
			wantStale:       backgroundLog,
		},
		{
			name:            "nothing running: say so rather than point at a file",
			serverLogExists: true,
			wantDestination: "no server running",
			wantStale:       backgroundLog,
		},
		{
			name:            "no leftover file, nothing to disown",
			running:         true,
			wantDestination: "stdout/stderr of the terminal running `pinchtab server`",
			wantStale:       "",
		},
	} {
		t.Run(tc.name, func(t *testing.T) {
			got := resolveServerLogWhere(stateDir, daemonLog, tc.daemonInstalled, tc.backgroundChild, tc.running, tc.serverLogExists)
			if got.Destination != tc.wantDestination {
				t.Errorf("destination = %q, want %q", got.Destination, tc.wantDestination)
			}
			if got.StalePath != tc.wantStale {
				t.Errorf("stale path = %q, want %q", got.StalePath, tc.wantStale)
			}
		})
	}
}

// A listener that refuses the token is still a running server. Keying the lookup on
// the strictest state reported "no server running" beside a server that was serving,
// and flagged its live log as stale.
func TestProtectedListenerCountsAsRunningForTheLogLookup(t *testing.T) {
	for _, state := range []healthSnapshotState{
		healthSnapshotRunning,
		healthSnapshotProtected,
		healthSnapshotUnhealthy,
		healthSnapshotInvalid,
	} {
		t.Run(string(state), func(t *testing.T) {
			if state == healthSnapshotStopped {
				t.Fatal("stopped must not be in this list")
			}
			got := resolveServerLogWhere("/home/op/.pinchtab", "", false, true, state != healthSnapshotStopped, true)
			if got.Destination != filepath.Join("/home/op/.pinchtab", "server.log") {
				t.Errorf("state %q resolved to %q, want the background log it is actually writing", state, got.Destination)
			}
			if got.StalePath != "" {
				t.Errorf("state %q flagged its own live log as stale", state)
			}
		})
	}
}

// A banner that resolves the log location and then does not print it leaves the
// operator exactly where the card found them.
func TestBannerPrintsTheLogDestinationAndFlagsAStaleServerLog(t *testing.T) {
	out := renderAgentHintsString(t, agentStatus{
		state:          healthSnapshotRunning,
		running:        true,
		listenAddr:     "127.0.0.1:9867",
		logDestination: "/home/op/.pinchtab/logs/daemon.err.log",
		staleLogPath:   "/home/op/.pinchtab/server.log",
	})

	if !strings.Contains(out, "/home/op/.pinchtab/logs/daemon.err.log") {
		t.Errorf("the banner does not name the live log:\n%s", out)
	}
	if !strings.Contains(out, "logs") {
		t.Errorf("the banner has no logs row:\n%s", out)
	}
	if !strings.Contains(out, "/home/op/.pinchtab/server.log is not being written by this server") {
		t.Errorf("the banner does not disown the stale server.log:\n%s", out)
	}
}

const minCmdPinchtabSourceFiles = 40

// The banner decides "this server writes server.log" from the --background-child flag in
// the recorded argv alone. Both detached spawn paths set that flag, so both have to
// actually write the file. The auto-start path — the one every browser CLI command and
// `pinchtab mcp` take — passed no writer, Go connected the child to /dev/null, and the
// banner vouched for a file frozen at whatever a long-dead server left behind.
func TestDetachedServerSpawnWritesTheLogFileTheBannerNames(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("the probe spawns /bin/sh")
	}
	stateDir := filepath.Join(t.TempDir(), "state")
	const marker = "detached-child-wrote-here"

	if _, err := spawnDetachedServer(stateDir, "/bin/sh", []string{"-c", "echo " + marker}); err != nil {
		t.Fatalf("spawnDetachedServer: %v", err)
	}

	logPath := serverLogFilePath(stateDir)
	deadline := time.Now().Add(10 * time.Second)
	for {
		data, err := os.ReadFile(logPath)
		if err == nil && strings.Contains(string(data), marker) {
			return
		}
		if time.Now().After(deadline) {
			t.Fatalf("%s never received the child's output (read %q, err %v); the spawn discarded it, so the log the banner names holds nothing this server wrote", logPath, data, err)
		}
		time.Sleep(20 * time.Millisecond)
	}
}

// A unit test on the logging spawn helper stays green while a second spawn site bypasses
// it — which is exactly how the auto-start path came to write nowhere. Only the census
// sees a new caller.
func TestEveryDetachedSpawnGoesThroughTheLoggingHelper(t *testing.T) {
	pkg := srccensus.Load(t, ".", minCmdPinchtabSourceFiles)

	owner, ok := pkg.Func("spawnDetachedServer")
	if !ok {
		t.Fatal("spawnDetachedServer is gone; do not delete this guard — re-point it at whatever now owns wiring a detached server to its log file")
	}

	var offenders []string
	for _, site := range pkg.Calls(t, "spawnDetachedChild") {
		if !pkg.Contains(owner, site) {
			offenders = append(offenders, site.String())
		}
	}
	if len(offenders) > 0 {
		t.Errorf("these sites spawn a detached server without routing its output to server.log, so the banner names a log this server never writes and the unredacted failure cause is recoverable from nowhere; call spawnDetachedServer instead:\n%s",
			strings.Join(offenders, "\n"))
	}
}

// serverLogWhereForConfig is where the resolver's premises are gathered, and it had no
// test: every case above hand-feeds backgroundChild. Drive it from the argv the auto-start
// path really produces, so a change to autoStartServerArgs that drops the flag is caught
// where the booleans are derived rather than where they are assumed.
func TestAutoStartedServerIsRecognisedAsWritingServerLog(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	stateDir := filepath.Join(home, "state")

	args := autoStartServerArgs("marker-abc")
	if err := writeServerPID(stateDir, serverPIDInfo{
		PID:        os.Getpid(),
		Executable: "/usr/local/bin/pinchtab",
		Args:       args,
		Marker:     "marker-abc",
	}); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(serverLogFilePath(stateDir), []byte("old\n"), 0o600); err != nil {
		t.Fatal(err)
	}

	where := serverLogWhereForConfig(&config.RuntimeConfig{StateDir: stateDir}, true)
	if where.Destination != serverLogFilePath(stateDir) {
		t.Errorf("destination = %q, want the server.log the auto-started child writes", where.Destination)
	}
	if where.StalePath != "" {
		t.Errorf("the live log was disowned as stale: %q", where.StalePath)
	}
}
