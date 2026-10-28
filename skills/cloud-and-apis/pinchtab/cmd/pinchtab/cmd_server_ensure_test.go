package main

import (
	"errors"
	"net/http"
	"strings"
	"testing"
	"time"

	"github.com/pinchtab/pinchtab/internal/server"
)

const unhealthyReason = "browser initialization failed: cloakbrowser binary not found: set browser.binary to the CloakBrowser binary path"

func unhealthyProbe(body string) server.HealthProbe {
	return server.HealthProbe{Reachable: true, StatusCode: http.StatusServiceUnavailable, Body: []byte(body)}
}

func TestEnsureServer_ReachableButUnhealthyReportsReasonAndSkipsAutoStart(t *testing.T) {
	started := false
	probes := 0

	err := ensureServerWith(
		"http://127.0.0.1:9877",
		"",
		"nav",
		func() error {
			started = true
			return nil
		},
		func(baseURL, token string) server.HealthProbe {
			probes++
			return unhealthyProbe(`{"reason":"` + unhealthyReason + `","status":"error"}`)
		},
		time.Second,
	)

	if err == nil {
		t.Fatal("expected an error for a reachable but unhealthy server")
	}
	if !strings.Contains(err.Error(), "is running but unhealthy") {
		t.Errorf("error = %q, want it to say the server is running but unhealthy", err)
	}
	if !strings.Contains(err.Error(), unhealthyReason) {
		t.Errorf("error = %q, want the server's own reason verbatim", err)
	}
	if strings.Contains(err.Error(), "is not running") {
		t.Errorf("error = %q, must not claim the server is not running", err)
	}
	if started {
		t.Error("auto-start ran against a server that is already up and answering")
	}
	if probes != 1 {
		t.Errorf("health probes = %d, want 1 — an unhealthy server must not be polled to the timeout", probes)
	}
}

func TestEnsureServer_UnhealthyWithUnparseableBodyReportsStatusOnly(t *testing.T) {
	for _, body := range []string{"", "not json at all", `{"status":"error"}`} {
		t.Run(body, func(t *testing.T) {
			started := false
			err := ensureServerWith(
				"http://127.0.0.1:9877",
				"",
				"nav",
				func() error {
					started = true
					return nil
				},
				func(baseURL, token string) server.HealthProbe { return unhealthyProbe(body) },
				time.Second,
			)

			if err == nil {
				t.Fatal("expected an error for a reachable but unhealthy server")
			}
			if !strings.Contains(err.Error(), "is running but unhealthy") {
				t.Errorf("error = %q, want the unhealthy message", err)
			}
			if !strings.Contains(err.Error(), "HTTP 503") {
				t.Errorf("error = %q, want the status code when no reason can be parsed", err)
			}
			if started {
				t.Error("auto-start ran against a reachable server")
			}
		})
	}
}

func TestEnsureServer_UnreachableStillAutoStarts(t *testing.T) {
	started := false
	probes := 0

	err := ensureServerWith(
		"http://127.0.0.1:9867",
		"",
		"nav",
		func() error {
			started = true
			return nil
		},
		func(baseURL, token string) server.HealthProbe {
			probes++
			if started {
				return server.HealthProbe{Reachable: true, StatusCode: http.StatusOK}
			}
			return server.HealthProbe{}
		},
		time.Second,
	)

	if err != nil {
		t.Fatalf("ensureServerWith() error = %v", err)
	}
	if !started {
		t.Fatal("expected an unreachable server to be auto-started")
	}
	if probes < 2 {
		t.Errorf("health probes = %d, want the post-start readiness poll too", probes)
	}
}

func TestEnsureServerWithDaemonRecoveryOwnsInstalledDaemonLifecycle(t *testing.T) {
	t.Run("installed healthy", func(t *testing.T) {
		ownershipCalled := false
		daemonStarted := false
		detachedStarted := false
		err := ensureServerWithDaemonRecovery(
			"http://127.0.0.1:9867", "", "nav", true,
			func() error { detachedStarted = true; return nil },
			func(string, string) server.HealthProbe {
				return server.HealthProbe{Reachable: true, StatusCode: http.StatusOK}
			},
			func() (bool, error) { ownershipCalled = true; return true, nil },
			func() (string, error) { daemonStarted = true; return "started", nil },
			time.Second,
		)
		if err != nil {
			t.Fatalf("ensureServerWithDaemonRecovery() error = %v", err)
		}
		if ownershipCalled || daemonStarted || detachedStarted {
			t.Fatalf("healthy installed daemon should be left alone: ownership=%t daemon=%t detached=%t", ownershipCalled, daemonStarted, detachedStarted)
		}
	})

	t.Run("installed unloaded starts through manager", func(t *testing.T) {
		daemonStarted := false
		detachedStarted := false
		probes := 0
		err := ensureServerWithDaemonRecovery(
			"http://127.0.0.1:9867", "", "nav", true,
			func() error { detachedStarted = true; return nil },
			func(string, string) server.HealthProbe {
				probes++
				if daemonStarted {
					return server.HealthProbe{Reachable: true, StatusCode: http.StatusOK}
				}
				return server.HealthProbe{}
			},
			func() (bool, error) { return true, nil },
			func() (string, error) { daemonStarted = true; return "Pinchtab daemon started.", nil },
			time.Second,
		)
		if err != nil {
			t.Fatalf("ensureServerWithDaemonRecovery() error = %v", err)
		}
		if !daemonStarted || detachedStarted || probes < 2 {
			t.Fatalf("expected bounded daemon recovery only: daemon=%t detached=%t probes=%d", daemonStarted, detachedStarted, probes)
		}
	})

	t.Run("installed wedged listener refuses detached fallback", func(t *testing.T) {
		daemonStarted := false
		detachedStarted := false
		err := ensureServerWithDaemonRecovery(
			"http://127.0.0.1:9867", "", "nav", true,
			func() error { detachedStarted = true; return nil },
			func(string, string) server.HealthProbe {
				return unhealthyProbe(`{"reason":"browser stuck","status":"error"}`)
			},
			func() (bool, error) { return true, nil },
			func() (string, error) { daemonStarted = true; return "started", nil },
			time.Second,
		)
		if err == nil || !strings.Contains(err.Error(), "installed PinchTab daemon owns lifecycle") || !strings.Contains(err.Error(), "port owner") {
			t.Fatalf("wedged installed daemon error = %v", err)
		}
		if daemonStarted || detachedStarted {
			t.Fatalf("wedged listener must not be restarted or replaced implicitly: daemon=%t detached=%t", daemonStarted, detachedStarted)
		}
	})

	t.Run("not installed auto-starts detached", func(t *testing.T) {
		daemonStarted := false
		detachedStarted := false
		err := ensureServerWithDaemonRecovery(
			"http://127.0.0.1:9867", "", "nav", true,
			func() error { detachedStarted = true; return nil },
			func(string, string) server.HealthProbe {
				if detachedStarted {
					return server.HealthProbe{Reachable: true, StatusCode: http.StatusOK}
				}
				return server.HealthProbe{}
			},
			func() (bool, error) { return false, nil },
			func() (string, error) { daemonStarted = true; return "started", nil },
			time.Second,
		)
		if err != nil {
			t.Fatalf("ensureServerWithDaemonRecovery() error = %v", err)
		}
		if !detachedStarted || daemonStarted {
			t.Fatalf("no installed daemon must cold-start a detached server: detached=%t daemon=%t", detachedStarted, daemonStarted)
		}
	})

	t.Run("unknown ownership refuses detached fallback", func(t *testing.T) {
		daemonStarted := false
		detachedStarted := false
		err := ensureServerWithDaemonRecovery(
			"http://127.0.0.1:9867", "", "nav", true,
			func() error { detachedStarted = true; return nil },
			func(string, string) server.HealthProbe { return server.HealthProbe{} },
			func() (bool, error) { return false, errors.New("service path unreadable") },
			func() (string, error) { daemonStarted = true; return "started", nil },
			time.Second,
		)
		if err == nil || !strings.Contains(err.Error(), "cannot determine background-service ownership") {
			t.Fatalf("unknown ownership error = %v", err)
		}
		if daemonStarted || detachedStarted {
			t.Fatalf("unknown ownership must not start anything: daemon=%t detached=%t", daemonStarted, detachedStarted)
		}
	})
}

func TestEnsureServer_ReadinessWaitTreatsUnhealthyAsNotReadyYet(t *testing.T) {
	started := false
	probes := 0

	err := ensureServerWith(
		"http://127.0.0.1:9867",
		"",
		"nav",
		func() error {
			started = true
			return nil
		},
		func(baseURL, token string) server.HealthProbe {
			probes++
			switch {
			case !started:
				return server.HealthProbe{}
			case probes < 4:
				return unhealthyProbe(`{"reason":"browser starting","status":"error"}`)
			default:
				return server.HealthProbe{Reachable: true, StatusCode: http.StatusOK}
			}
		},
		5*time.Second,
	)

	if err != nil {
		t.Fatalf("ensureServerWith() error = %v — a server answering 503 while it boots must be waited out", err)
	}
	if probes < 4 {
		t.Errorf("health probes = %d, want the wait to keep polling past the 503s", probes)
	}
}

func TestServerProbeHealthy_KeepsTheEnsurePathThreshold(t *testing.T) {
	cases := []struct {
		probe server.HealthProbe
		want  bool
	}{
		{server.HealthProbe{Reachable: true, StatusCode: http.StatusOK}, true},
		{server.HealthProbe{Reachable: true, StatusCode: http.StatusUnauthorized}, true},
		{server.HealthProbe{Reachable: true, StatusCode: http.StatusServiceUnavailable}, false},
		{server.HealthProbe{Reachable: true, StatusCode: http.StatusInternalServerError}, false},
		{server.HealthProbe{}, false},
	}
	for _, tc := range cases {
		if got := serverProbeHealthy(tc.probe); got != tc.want {
			t.Errorf("serverProbeHealthy(%+v) = %v, want %v", tc.probe, got, tc.want)
		}
	}
}
