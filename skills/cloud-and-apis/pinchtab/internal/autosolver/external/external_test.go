package external

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"testing"
	"time"

	"github.com/pinchtab/pinchtab/internal/autosolver"
)

// The reported solver identity has to be the registered one. Solve now builds it
// from Name(), which makes drift impossible rather than merely detectable; this
// test reds if either one goes back to spelling the name a second time.
func TestSolverUsedMatchesTheRegisteredName(t *testing.T) {
	for _, solver := range []autosolver.Solver{
		NewCapsolver(CapsolverConfig{}),
		NewTwoCaptcha(TwoCaptchaConfig{}),
	} {
		t.Run(solver.Name(), func(t *testing.T) {
			// An unset API key is the earliest return, and it is enough: the
			// Result is built before the check.
			result, err := solver.Solve(context.Background(), nil, nil)
			if err == nil {
				t.Fatal("expected the unset-API-key error, so this test exercises the real Solve path")
			}
			if result == nil {
				t.Fatal("Solve returned no Result to check")
			}
			if result.SolverUsed != solver.Name() {
				t.Errorf("Result.SolverUsed = %q but Name() = %q — the reported solver identity has drifted from the registered one", result.SolverUsed, solver.Name())
			}
		})
	}
}

// stubPage is the smallest Page the external solvers touch: they read HTML and
// URL and nothing else.
type stubPage struct {
	html    string
	htmlErr error
}

func (p stubPage) URL() string   { return "https://example.test/challenge" }
func (p stubPage) Title() string { return "" }
func (p stubPage) HTML() (string, error) {
	return p.html, p.htmlErr
}
func (p stubPage) HTMLWithin(time.Duration) (string, error) { return p.HTML() }
func (p stubPage) Screenshot() ([]byte, error)              { return nil, nil }

const recaptchaHTML = `<div class="g-recaptcha" data-sitekey="6LtestKEY"></div>`

// Every branch of Solve is pinned by exact string, because folding the shared
// prologue into a base moved these messages across a file boundary and the
// providers spell their own label differently from their registered name.
func TestSolveMessagesAreUnchangedOnEveryPath(t *testing.T) {
	for _, provider := range []struct {
		label   string
		build   func(key string) autosolver.Solver
		wantPri int
	}{
		{"capsolver", func(key string) autosolver.Solver { return NewCapsolver(CapsolverConfig{APIKey: key}) }, 200},
		{"2captcha", func(key string) autosolver.Solver { return NewTwoCaptcha(TwoCaptchaConfig{APIKey: key}) }, 210},
	} {
		t.Run(provider.label, func(t *testing.T) {
			keyed := provider.build("key")

			for _, tc := range []struct {
				name       string
				solver     autosolver.Solver
				page       autosolver.Page
				wantResult string
				wantErr    string
			}{
				{
					name:       "no api key",
					solver:     provider.build(""),
					page:       stubPage{html: recaptchaHTML},
					wantResult: provider.label + " API key not configured",
					wantErr:    provider.label + " API key not configured",
				},
				{
					name:       "page read fails",
					solver:     keyed,
					page:       stubPage{htmlErr: errors.New("boom")},
					wantResult: "get HTML: boom",
					wantErr:    "boom",
				},
				{
					name:       "no captcha on page",
					solver:     keyed,
					page:       stubPage{html: "<html><body>nothing here</body></html>"},
					wantResult: "no supported CAPTCHA detected",
					wantErr:    "no supported CAPTCHA detected on page",
				},
				{
					name:       "captcha without a sitekey",
					solver:     keyed,
					page:       stubPage{html: `<div class="g-recaptcha"></div>`},
					wantResult: "sitekey not found",
					wantErr:    "could not extract sitekey from page",
				},
				{
					name:       "reaches the unimplemented api call",
					solver:     keyed,
					page:       stubPage{html: recaptchaHTML},
					wantResult: provider.label + " API client not yet implemented",
					wantErr:    provider.label + ": API client not yet implemented — skeleton only",
				},
			} {
				t.Run(tc.name, func(t *testing.T) {
					result, err := tc.solver.Solve(context.Background(), tc.page, nil)
					if err == nil {
						t.Fatal("Solve reported success; every path here is an error path")
					}
					if err.Error() != tc.wantErr {
						t.Errorf("error = %q, want %q", err, tc.wantErr)
					}
					if result == nil {
						t.Fatal("Solve returned no Result")
					}
					if result.Error != tc.wantResult {
						t.Errorf("Result.Error = %q, want %q", result.Error, tc.wantResult)
					}
					if result.SolverUsed != tc.solver.Name() {
						t.Errorf("Result.SolverUsed = %q, want %q", result.SolverUsed, tc.solver.Name())
					}
				})
			}

			if got := keyed.Priority(); got != provider.wantPri {
				t.Errorf("Priority() = %d, want %d; the external stubs must keep sorting behind the real solvers", got, provider.wantPri)
			}
		})
	}
}

func TestCanHandleIsSharedAndKeyGated(t *testing.T) {
	for _, tc := range []struct {
		name   string
		solver autosolver.Solver
		page   autosolver.Page
		want   bool
	}{
		{"no key never handles", NewCapsolver(CapsolverConfig{}), stubPage{html: recaptchaHTML}, false},
		{"keyed handles a captcha page", NewCapsolver(CapsolverConfig{APIKey: "k"}), stubPage{html: recaptchaHTML}, true},
		{"keyed declines a plain page", NewCapsolver(CapsolverConfig{APIKey: "k"}), stubPage{html: "<p>hi</p>"}, false},
		{"page read failure declines", NewCapsolver(CapsolverConfig{APIKey: "k"}), stubPage{htmlErr: errors.New("boom")}, false},
		{"twocaptcha agrees with capsolver", NewTwoCaptcha(TwoCaptchaConfig{APIKey: "k"}), stubPage{html: recaptchaHTML}, true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			got, err := tc.solver.CanHandle(context.Background(), tc.page)
			if err != nil {
				t.Fatalf("CanHandle() error = %v", err)
			}
			if got != tc.want {
				t.Errorf("CanHandle() = %v, want %v", got, tc.want)
			}
		})
	}
}

func TestExtractSitekeyReadsBothQuoteStyles(t *testing.T) {
	for _, tc := range []struct{ name, html, want string }{
		{"double quotes", `<div data-sitekey="abc"></div>`, "abc"},
		{"single quotes", `<div data-sitekey='abc'></div>`, "abc"},
		{"absent", `<div class="g-recaptcha"></div>`, ""},
		{"unterminated", `<div data-sitekey="abc`, ""},
	} {
		t.Run(tc.name, func(t *testing.T) {
			if got := extractSitekey(tc.html); got != tc.want {
				t.Errorf("extractSitekey(%q) = %q, want %q", tc.html, got, tc.want)
			}
		})
	}
}

// captchaPatterns and detectCaptchaType encode the same domain rule twice:
// CanHandle scans the slice, prepare asks detectCaptchaType. They agree today,
// so a page one accepts the other must classify — otherwise CanHandle promises
// a solve that prepare immediately refuses with "no supported CAPTCHA detected".
func TestCanHandleAndDetectCaptchaTypeAgreeOnEveryPage(t *testing.T) {
	var corpus []string
	for _, marker := range []string{
		"recaptcha", "g-recaptcha", "hcaptcha", "h-captcha",
		"challenges.cloudflare.com/turnstile", "turnstile", "captcha", "funcaptcha",
		"arkoselabs", "geetest", "",
	} {
		for _, shape := range []string{
			`<div class="%s"></div>`,
			`<script src="https://%s/api.js"></script>`,
			`<p>%s</p>`,
			`<DIV CLASS="%s">`,
		} {
			corpus = append(corpus, fmt.Sprintf(shape, marker), strings.ToUpper(fmt.Sprintf(shape, marker)))
		}
	}
	corpus = append(corpus, "", "<html></html>", "<p>nothing here</p>")

	solver := NewCapsolver(CapsolverConfig{APIKey: "k"})
	var accepted, declined int
	for _, html := range corpus {
		canHandle, err := solver.CanHandle(context.Background(), stubPage{html: html})
		if err != nil {
			t.Fatalf("CanHandle(%q) error = %v", html, err)
		}
		detected := detectCaptchaType(html) != ""
		if canHandle != detected {
			t.Errorf("CanHandle = %v but detectCaptchaType(%q) != \"\" = %v; the two encodings of the supported-CAPTCHA rule have drifted, so CanHandle accepts a page prepare then refuses",
				canHandle, html, detected)
		}
		if canHandle {
			accepted++
		} else {
			declined++
		}
	}
	if accepted == 0 || declined == 0 {
		t.Fatalf("corpus exercised only one outcome (accepted=%d declined=%d); the agreement claim is vacuous unless both arms occur", accepted, declined)
	}
}
