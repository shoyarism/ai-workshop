package urls

import (
	"strings"
	"testing"
)

func TestRedactStripsEveryCredentialBearingComponent(t *testing.T) {
	const raw = "https://u:p@Example.COM:8443/a?token=secret#frag"
	got := Redact(raw, maxLogURLBytes)

	if got != "https://example.com:8443/a" {
		t.Fatalf("Redact(%q) = %q, want %q", raw, got, "https://example.com:8443/a")
	}
	for _, leaked := range []string{"u:p@", "token", "secret", "frag", "?", "#", "Example.COM"} {
		if strings.Contains(got, leaked) {
			t.Errorf("redacted URL still carries %q: %q", leaked, got)
		}
	}
}

func TestRedactRejectsInputsThatAreNotURLs(t *testing.T) {
	// Sanitize passes anything containing "://" through untouched, so these
	// reach the parse step looking valid and are caught only by the guard.
	for _, raw := range []string{"/path://x", "./rel://x", "../up://x", "://foo", "", "   "} {
		if got := Redact(raw, maxLogURLBytes); got != "" {
			t.Errorf("Redact(%q) = %q, want %q; a non-URL must not be echoed into a persisted record", raw, got, "")
		}
	}
}

func TestRedactKeepsInputsThatAreURLs(t *testing.T) {
	for _, tc := range []struct{ raw, want string }{
		{"path://x", "path://x"},
		{"x://y", "x://y"},
		{"foo/bar", "https://foo/bar"},
		{"about:blank#frag", "about:blank"},
		{"mailto://a@b?x=1", "mailto://b"},
		{"javascript:alert(1)", "javascript:alert(1)"},
	} {
		if got := Redact(tc.raw, maxLogURLBytes); got != tc.want {
			t.Errorf("Redact(%q) = %q, want %q", tc.raw, got, tc.want)
		}
	}
}

func TestRedactAppliesTheCapItIsGiven(t *testing.T) {
	raw := "https://example.com/" + strings.Repeat("a", 700)

	short := Redact(raw, 512)
	long := Redact(raw, 2048)

	if len(short) != 512 {
		t.Errorf("len(Redact(raw, 512)) = %d, want 512", len(short))
	}
	if len(long) <= 512 {
		t.Errorf("len(Redact(raw, 2048)) = %d, want the larger cap to keep more of the URL", len(long))
	}
	if !strings.HasPrefix(long, "https://example.com/") {
		t.Errorf("the redacted URL lost its origin: %q", long[:40])
	}
}
