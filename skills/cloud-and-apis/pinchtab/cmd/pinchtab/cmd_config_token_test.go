package main

import (
	"context"
	"os"
	"os/exec"
	"strings"
	"testing"
)

// stubClipboard makes copyToClipboard succeed or fail on demand, so the two
// halves of `config token` can be exercised without a real clipboard tool.
func stubClipboard(t *testing.T, available bool) {
	t.Helper()
	originalLookPath, originalExecCommand := clipboardLookPath, clipboardExecCommand
	if available {
		clipboardLookPath = func(name string) (string, error) { return name, nil }
		clipboardExecCommand = func(ctx context.Context, _ string, _ ...string) *exec.Cmd {
			return exec.CommandContext(ctx, os.Args[0], "-test.run=^$")
		}
	} else {
		clipboardLookPath = func(name string) (string, error) { return "", exec.ErrNotFound }
	}
	t.Cleanup(func() {
		clipboardLookPath, clipboardExecCommand = originalLookPath, originalExecCommand
	})
}

// stdout is the machine channel: TOKEN=$(pinchtab config token) has to capture
// the token or nothing. Prose there is captured verbatim and then sent as a
// bearer credential, which the server rejects as bad_token with no hint that
// the value was an English sentence.
func TestConfigTokenKeepsStdoutFreeOfHumanText(t *testing.T) {
	const token = "tok-abcdef0123456789"

	for _, tc := range []struct {
		name              string
		clipboardWorks    bool
		toStdout          bool
		wantErr           bool
		wantStdout        string
		wantStderrHasText bool
	}{
		{
			name:              "clipboard success says so on stderr only",
			clipboardWorks:    true,
			wantStdout:        "",
			wantStderrHasText: true,
		},
		{
			name:              "clipboard unavailable says so on stderr only",
			clipboardWorks:    false,
			wantErr:           true,
			wantStdout:        "",
			wantStderrHasText: false,
		},
		{
			name:           "explicit --stdout emits the token and nothing else",
			clipboardWorks: false,
			toStdout:       true,
			wantStdout:     token + "\n",
		},
	} {
		t.Run(tc.name, func(t *testing.T) {
			stubClipboard(t, tc.clipboardWorks)

			var err error
			stdout, stderr := captureStdoutStderr(t, func() {
				err = emitConfigToken(token, tc.toStdout)
			})

			if tc.wantErr != (err != nil) {
				t.Fatalf("error = %v, wantErr = %v", err, tc.wantErr)
			}
			if stdout != tc.wantStdout {
				t.Errorf("stdout = %q, want %q", stdout, tc.wantStdout)
			}
			if tc.wantStderrHasText && strings.TrimSpace(stderr) == "" {
				t.Errorf("stderr is empty; the human message has to go somewhere")
			}
			if !tc.toStdout && strings.Contains(stdout+stderr, token) {
				t.Errorf("the token leaked without --stdout:\n  stdout=%q\n  stderr=%q", stdout, stderr)
			}
		})
	}
}

// Whatever the clipboard does, a capture must never come back holding prose.
func TestCapturingConfigTokenNeverYieldsProse(t *testing.T) {
	const token = "tok-abcdef0123456789"

	for _, clipboardWorks := range []bool{true, false} {
		stubClipboard(t, clipboardWorks)
		stdout, _ := captureStdoutStderr(t, func() {
			_ = emitConfigToken(token, false)
		})
		captured := strings.TrimSpace(stdout)
		if captured != "" && captured != token {
			t.Errorf("clipboardWorks=%v: $(...) would capture %q — neither the token nor nothing", clipboardWorks, captured)
		}
	}
}

// AC-4: the advice the CLI gives on a protected listener has to work in the
// script the reader is standing in.
func TestProtectedListenerHintPointsAtACapturableCommand(t *testing.T) {
	hints, _ := nextStepsForState(healthSnapshotProtected)
	if len(hints) == 0 {
		t.Fatal("the protected-listener state offers no next steps")
	}

	var tokenHint string
	for _, hint := range hints {
		if strings.Contains(hint.Command, "config token") {
			tokenHint = hint.Command
		}
	}
	if tokenHint == "" {
		t.Fatal("the protected-listener hints no longer mention config token; a reader locked out by a token is not told how to get one")
	}
	if !strings.Contains(tokenHint, "--stdout") {
		t.Errorf("hint %q sends the reader to a command whose stdout is empty, so the $(...) they run captures nothing", tokenHint)
	}
}
