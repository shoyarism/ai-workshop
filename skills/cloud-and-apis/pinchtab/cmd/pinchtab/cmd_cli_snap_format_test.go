package main

import (
	"io"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strconv"
	"testing"

	"github.com/pinchtab/pinchtab/internal/handlers"
)

func snapWireFormat(t *testing.T, flags map[string]string) url.Values {
	t.Helper()
	var query url.Values
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/snapshot" {
			http.NotFound(w, r)
			return
		}
		query = r.URL.Query()
		_, _ = io.WriteString(w, "# snapshot\n")
	}))
	t.Cleanup(ts.Close)

	oldServerURL := serverURL
	serverURL = ts.URL
	t.Cleanup(func() { serverURL = oldServerURL })

	snapFlags := snapCmd.Flags()
	for flag, value := range flags {
		old, err := snapFlags.GetBool(flag)
		if err != nil {
			t.Fatalf("snap has no --%s flag: %v", flag, err)
		}
		t.Cleanup(func() { _ = snapFlags.Set(flag, strconv.FormatBool(old)) })
		if err := snapFlags.Set(flag, value); err != nil {
			t.Fatalf("cannot set --%s: %v", flag, err)
		}
	}

	_ = captureStdout(t, func() {
		snapCmd.Run(snapCmd, nil)
	})
	if query == nil {
		t.Fatal("snap never reached /snapshot, so this proves nothing about what it asks for")
	}
	return query
}

func TestSnapAsksForCompactWithNoFormatFlag(t *testing.T) {
	for _, tc := range []struct {
		name  string
		flags map[string]string
		want  string
	}{
		{name: "no flags", flags: nil, want: "compact"},
		{name: "json", flags: map[string]string{"json": "true"}, want: "json"},
		{name: "compact declined", flags: map[string]string{"compact": "false"}, want: "json"},
		{name: "full", flags: map[string]string{"full": "true"}, want: "json"},
		{name: "text", flags: map[string]string{"text": "true"}, want: "text"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			query := snapWireFormat(t, tc.flags)
			if got := query.Get("format"); got != tc.want {
				t.Errorf("snap asked for format=%q, want %q — read from the real command's own flags, so a default that drifts in registration shows up here", got, tc.want)
			}
			if _, err := handlers.ParseSnapshotCostControls(query); err != nil {
				t.Errorf("the server rejects the query snap sends: %v (query=%v)", err, query)
			}
		})
	}
}
