package main

import (
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestFetchHealthSnapshotClassifiesOnlyValidDashboardHealthAsRunning(t *testing.T) {
	tests := []struct {
		name   string
		status int
		body   string
		want   healthSnapshotState
	}{
		{
			name:   "valid dashboard health",
			status: http.StatusOK,
			body:   `{"status":"ok","mode":"dashboard","version":"dev","security":{"allowedDomains":["localhost"],"idpiEnabled":true}}`,
			want:   healthSnapshotRunning,
		},
		{
			name:   "valid dashboard health without security block",
			status: http.StatusOK,
			body:   `{"status":"ok","mode":"dashboard","version":"dev"}`,
			want:   healthSnapshotRunning,
		},
		{
			name:   "protected listener",
			status: http.StatusUnauthorized,
			body:   `{"code":"missing_token","message":"unauthorized"}`,
			want:   healthSnapshotProtected,
		},
		{
			name:   "foreign json",
			status: http.StatusOK,
			body:   `{"status":"ok"}`,
			want:   healthSnapshotInvalid,
		},
		{
			name:   "foreign text",
			status: http.StatusOK,
			body:   `ok`,
			want:   healthSnapshotInvalid,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			srv := newLocalhostHealthServer(t, tt.status, tt.body)
			defer srv.Close()

			_, port, err := net.SplitHostPort(srv.Listener.Addr().String())
			if err != nil {
				t.Fatalf("SplitHostPort() error = %v", err)
			}
			_, got := fetchHealthSnapshot(port)
			if got != tt.want {
				t.Fatalf("fetchHealthSnapshot() state = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestPrintAgentHintsDoesNotTreatAuthFailureAsRunning(t *testing.T) {
	srv := newLocalhostHealthServer(t, http.StatusUnauthorized, `{"code":"missing_token","message":"unauthorized"}`)
	defer srv.Close()

	_, port, err := net.SplitHostPort(srv.Listener.Addr().String())
	if err != nil {
		t.Fatalf("SplitHostPort() error = %v", err)
	}
	cfg := testRuntimeConfig()
	cfg.Port = port
	cfg.Token = "wrong-token"

	output := captureStdout(t, func() {
		printAgentHints(cfg)
	})
	if !strings.Contains(output, "protected listener") {
		t.Fatalf("expected protected listener status, got\n%s", output)
	}
	if strings.Contains(output, "pinchtab nav <url>") {
		t.Fatalf("protected listener should not show running-server next steps\n%s", output)
	}
}

func TestPrintAgentHintsReportsALiveListenerAsRunning(t *testing.T) {
	var probed bool
	srv := newLocalhostHealthServerWithHandler(t, func(w http.ResponseWriter, r *http.Request) {
		probed = true
		w.WriteHeader(http.StatusOK)
		_, _ = io.WriteString(w, `{"status":"ok","mode":"dashboard","version":"dev"}`)
	})
	defer srv.Close()

	_, port, err := net.SplitHostPort(srv.Listener.Addr().String())
	if err != nil {
		t.Fatalf("SplitHostPort() error = %v", err)
	}
	cfg := testRuntimeConfig()
	cfg.Port = port

	output := captureStdout(t, func() {
		printAgentHints(cfg)
	})
	if !probed {
		t.Fatal("bare banner did not probe localhost, so it can only be guessing the server state")
	}
	if strings.Contains(output, string(healthSnapshotStopped)) {
		t.Fatalf("bare banner reported %q while a listener was answering on the configured port\n%s", healthSnapshotStopped, output)
	}
	if !strings.Contains(output, string(healthSnapshotRunning)) {
		t.Fatalf("expected %q status, got\n%s", healthSnapshotRunning, output)
	}
}

func TestPrintAgentHintsNeverOffersToStartAListeningServer(t *testing.T) {
	for _, tc := range []struct {
		name   string
		status int
		body   string
	}{
		{"running", http.StatusOK, `{"status":"ok","mode":"dashboard","version":"dev"}`},
		{"protected listener", http.StatusUnauthorized, `{"code":"missing_token","message":"unauthorized"}`},
		{"unhealthy", http.StatusInternalServerError, `{"status":"error"}`},
		{"foreign listener", http.StatusOK, `not json`},
	} {
		t.Run(tc.name, func(t *testing.T) {
			srv := newLocalhostHealthServer(t, tc.status, tc.body)
			defer srv.Close()

			_, port, err := net.SplitHostPort(srv.Listener.Addr().String())
			if err != nil {
				t.Fatalf("SplitHostPort() error = %v", err)
			}
			cfg := testRuntimeConfig()
			cfg.Port = port

			output := captureStdout(t, func() {
				printAgentHints(cfg)
			})
			if strings.Contains(output, "# start the server") {
				t.Fatalf("banner told the user to start a server that is already listening\n%s", output)
			}
		})
	}
}

func TestPrintAgentHintsReportsAStoppedServerWhenNothingListens(t *testing.T) {
	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("Listen() error = %v", err)
	}
	_, port, err := net.SplitHostPort(listener.Addr().String())
	if err != nil {
		t.Fatalf("SplitHostPort() error = %v", err)
	}
	if err := listener.Close(); err != nil {
		t.Fatalf("Close() error = %v", err)
	}

	cfg := testRuntimeConfig()
	cfg.Port = port

	output := captureStdout(t, func() {
		printAgentHints(cfg)
	})
	if !strings.Contains(output, string(healthSnapshotStopped)) {
		t.Fatalf("expected %q status with nothing listening, got\n%s", healthSnapshotStopped, output)
	}
	if !strings.Contains(output, "# start the server") {
		t.Fatalf("a stopped server should still be offered a start hint\n%s", output)
	}
}

func TestFetchHealthSnapshotDoesNotSendBearerToken(t *testing.T) {
	var gotAuth string
	srv := newLocalhostHealthServerWithHandler(t, func(w http.ResponseWriter, r *http.Request) {
		gotAuth = r.Header.Get("Authorization")
		w.WriteHeader(http.StatusUnauthorized)
		_, _ = io.WriteString(w, `{"code":"missing_token","message":"unauthorized"}`)
	})
	defer srv.Close()

	_, port, err := net.SplitHostPort(srv.Listener.Addr().String())
	if err != nil {
		t.Fatalf("SplitHostPort() error = %v", err)
	}
	_, got := fetchHealthSnapshot(port)
	if got != healthSnapshotProtected {
		t.Fatalf("fetchHealthSnapshot() state = %q, want %q", got, healthSnapshotProtected)
	}
	if gotAuth != "" {
		t.Fatalf("Authorization = %q, want empty", gotAuth)
	}
}

func TestPrintAgentHintsStaysBoundedAgainstASilentListener(t *testing.T) {
	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("Listen() error = %v", err)
	}
	defer func() { _ = listener.Close() }()

	held := make(chan struct{})
	defer close(held)
	go func() {
		for {
			conn, acceptErr := listener.Accept()
			if acceptErr != nil {
				return
			}
			go func() {
				<-held
				_ = conn.Close()
			}()
		}
	}()

	_, port, err := net.SplitHostPort(listener.Addr().String())
	if err != nil {
		t.Fatalf("SplitHostPort() error = %v", err)
	}
	cfg := testRuntimeConfig()
	cfg.Port = port

	const ceiling = 10 * time.Second
	start := time.Now()
	output := captureStdout(t, func() {
		printAgentHints(cfg)
	})
	elapsed := time.Since(start)

	if elapsed >= ceiling {
		t.Fatalf("bare banner spent %v on a port that accepts the connection and never answers; the probe must stay bounded or `pinchtab` hangs on a firewalled port, which is the whole reason the banner used to refuse to probe", elapsed)
	}
	if !strings.Contains(output, string(healthSnapshotStopped)) {
		t.Fatalf("expected %q after the probe gave up, got\n%s", healthSnapshotStopped, output)
	}
}

func newLocalhostHealthServer(t *testing.T, status int, body string) *httptest.Server {
	t.Helper()

	return newLocalhostHealthServerWithHandler(t, func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(status)
		_, _ = io.WriteString(w, body)
	})
}

func newLocalhostHealthServerWithHandler(t *testing.T, handler http.HandlerFunc) *httptest.Server {
	t.Helper()

	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("Listen() error = %v", err)
	}
	srv := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/health" {
			t.Fatalf("path = %q, want /health", r.URL.Path)
		}
		handler(w, r)
	}))
	srv.Listener = listener
	srv.Start()
	return srv
}
