package activity

import (
	"strings"
	"testing"

	"github.com/pinchtab/pinchtab/internal/sanitize"
	internalurls "github.com/pinchtab/pinchtab/internal/urls"
)

// logCapBytes reads the log cap off the function instead of restating it: an
// input longer than any cap comes back exactly cap-length, so this cannot go
// stale if internal/urls changes its constant.
func logCapBytes() int {
	return len(internalurls.RedactForLog("https://example.com/" + strings.Repeat("a", 8192)))
}

// The two redactors are one control with two caps. This is the guard on that
// claim: for every input, the log form must be exactly the activity form put
// through the smaller cap — so a future edit to either caller that changes
// anything other than the cap reds here.
func TestBothRedactorsAgreeExceptWhereTheCapBites(t *testing.T) {
	inputs := []string{
		"/path://x",
		"https://u:p@Example.COM:8443/a?token=secret#frag",
		"javascript:alert(1)",
		"foo/bar",
		"://foo",
		"mailto://a@b?x=1",
		"./rel://x",
		"../up://x",
		"about:blank#frag",
		"pinchtab.com/reset?token=secret",
		"ftp://u:p@files.io:21/x?y#z",
		"",
		"   ",
		// Longer than the log cap, shorter than the activity cap, so the cap is
		// the only thing that can make the two disagree on it.
		"https://example.com/" + strings.Repeat("a", 700),
	}
	if len(inputs) == 0 {
		t.Fatal("the shared input set is empty, so this parity guard proves nothing")
	}

	logCap := logCapBytes()
	if logCap <= 0 {
		t.Fatal("could not determine the log cap; the parity comparison below would be meaningless")
	}

	capBit := 0
	for _, raw := range inputs {
		logged := internalurls.RedactForLog(raw)
		recorded := sanitizeActivityURL(raw)

		want := sanitize.TruncateUTF8BytesWithEllipsis(recorded, logCap)
		if logged != want {
			t.Errorf("the two redactors disagree on %q beyond the byte cap:\n  log      = %q\n  activity = %q\nOne security control implemented twice has drifted again.", raw, logged, recorded)
			continue
		}
		if logged != recorded {
			capBit++
		}
	}

	if capBit == 0 {
		t.Fatal("no input was long enough for the caps to differ, so this guard never proved the cap is the ONLY difference; add a case longer than the log cap")
	}
}

func TestActivityFeedDropsRelativePathsThatMerelyContainASchemeSeparator(t *testing.T) {
	for _, raw := range []string{"/path://x", "./rel://x", "../up://x", ".//x://y", "/a/b://c/d"} {
		if got := sanitizeActivityURL(raw); got != "" {
			t.Errorf("sanitizeActivityURL(%q) = %q, want %q; these used to be recorded verbatim because the validity guard was skipped on the Sanitize success path", raw, got, "")
		}
	}
}

func TestActivityFeedStillRecordsRealURLs(t *testing.T) {
	for _, tc := range []struct{ raw, want string }{
		{"https://u:p@Example.COM:8443/a?token=secret#frag", "https://example.com:8443/a"},
		{"pinchtab.com/reset?token=secret", "https://pinchtab.com/reset"},
		{"about:blank#frag", "about:blank"},
		{"path://x", "path://x"},
	} {
		if got := sanitizeActivityURL(tc.raw); got != tc.want {
			t.Errorf("sanitizeActivityURL(%q) = %q, want %q; the stricter guard must not drop real URLs", tc.raw, got, tc.want)
		}
	}
}

func TestActivityCapIsLargerThanTheLogCap(t *testing.T) {
	raw := "https://example.com/" + strings.Repeat("a", 700)
	logCap := logCapBytes()
	if got := len(sanitizeActivityURL(raw)); got <= logCap {
		t.Errorf("activity kept %d bytes, want more than the log cap of %d", got, logCap)
	}
}
