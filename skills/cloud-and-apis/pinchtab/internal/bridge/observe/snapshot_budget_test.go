package observe

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/pinchtab/pinchtab/internal/srccensus"
	"gopkg.in/yaml.v3"
)

// minObserveSourceFiles is the vacuity floor: the package already has more non-test
// sources than this, so a scan that silently stops seeing most of it fails instead of
// passing for the wrong reason.
const minObserveSourceFiles = 8

// budgetProbeNodes is a page's worth of realistic interactive nodes: the mix of roles,
// names, values and states a real form or app shell produces, at varying depth. The budget
// is only meaningful against content like this — a fixture of empty nodes would let almost
// any estimator look correct.
func budgetProbeNodes(count int) []A11yNode {
	roles := []string{"button", "textbox", "link", "checkbox", "combobox", "heading", "listitem", "tab"}
	names := []string{
		"Submit order",
		"Email address",
		"Continue to payment",
		"Remember this device",
		"Country or region",
		"Shipping information",
		"Standard delivery, 3-5 business days",
		"Account",
	}
	values := []string{"", "user@example.com", "", "", "United Kingdom", "", "", ""}

	nodes := make([]A11yNode, 0, count)
	for i := 0; i < count; i++ {
		nodes = append(nodes, A11yNode{
			Ref:      fmt.Sprintf("e%d", i+1),
			Role:     roles[i%len(roles)],
			Name:     names[i%len(names)],
			Value:    values[i%len(values)],
			Depth:    i % 5,
			Focused:  i%9 == 0,
			Disabled: i%11 == 0,
			Checked:  []CheckedState{"", CheckedTrue, CheckedFalse, CheckedMixed}[i%4],
		})
	}
	return nodes
}

// renderedTokens is the ground truth the card measured against: the tokens the caller
// actually receives for the nodes the truncator kept, counted from the bytes the matching
// formatter emits.
func renderedTokens(t *testing.T, nodes []A11yNode, format string) int {
	t.Helper()
	switch format {
	case "compact":
		return estimateTokens(len(FormatSnapshotCompact(nodes)))
	case "text":
		return estimateTokens(len(FormatSnapshotText(nodes)))
	case "yaml":
		out, err := yaml.Marshal(nodes)
		if err != nil {
			t.Fatalf("marshal yaml: %v", err)
		}
		return estimateTokens(len(out))
	default:
		out, err := json.Marshal(nodes)
		if err != nil {
			t.Fatalf("marshal json: %v", err)
		}
		return estimateTokens(len(out))
	}
}

// The contract maxTokens now carries, stated as the two properties that make a budget a
// budget rather than a hint:
//
//  1. the output never exceeds it, and
//  2. nothing is left on the table — the first node that was dropped would not have fit.
//
// Property 2 is what a percentage floor cannot express. A shortfall is only legitimate
// when the next node was too big for the remainder, and that is checkable exactly, so
// there is no tolerance here to quietly widen until the current constants pass.
func TestTruncateToTokensDeliversTheBudgetItWasAsked(t *testing.T) {
	nodes := budgetProbeNodes(40)

	for _, format := range []string{"compact", "text", "json", "yaml"} {
		for _, budget := range []int{100, 300, 1000} {
			t.Run(fmt.Sprintf("%s/%d", format, budget), func(t *testing.T) {
				kept, truncated := TruncateToTokens(nodes, budget, format)
				actual := renderedTokens(t, kept, format)

				if actual > budget {
					t.Errorf("%s budget=%d kept %d/%d nodes but renders ~%d tokens (%+d%%): the budget is a ceiling and it was exceeded",
						format, budget, len(kept), len(nodes), actual, percentOff(actual, budget))
				}

				if truncated != (len(kept) < len(nodes)) {
					t.Errorf("%s budget=%d reported truncated=%v while keeping %d of %d nodes",
						format, budget, truncated, len(kept), len(nodes))
				}

				if truncated {
					withNext := renderedTokens(t, nodes[:len(kept)+1], format)
					if withNext <= budget {
						t.Errorf("%s budget=%d stopped at %d/%d nodes (~%d tokens) although the next node would have fit in ~%d: the caller was short-changed",
							format, budget, len(kept), len(nodes), actual, withNext)
					}
				}
			})
		}
	}
}

// The band the two properties above actually produce, recorded so the number in
// docs/reference/snapshot.md is measured rather than asserted. A format whose nodes are
// large relative to the budget lands lower in the band; that is the one-node gap, not
// slack in the estimator.
func TestBudgetDeliveryBandIsWorthDocumenting(t *testing.T) {
	nodes := budgetProbeNodes(40)
	worst := 100
	for _, format := range []string{"compact", "text", "json", "yaml"} {
		for _, budget := range []int{100, 300, 1000} {
			kept, truncated := TruncateToTokens(nodes, budget, format)
			got := renderedTokens(t, kept, format) * 100 / budget
			if !truncated {
				// Everything fit, so the budget was never the constraint and the
				// percentage says nothing about the allocator.
				t.Logf("%-8s budget=%4d -> kept all %d nodes (~%d%% of budget, not constrained)", format, budget, len(kept), got)
				continue
			}
			t.Logf("%-8s budget=%4d -> kept %2d/%d, ~%d%% of budget", format, budget, len(kept), len(nodes), got)
			if got < worst {
				worst = got
			}
		}
	}
	if worst < 80 {
		t.Errorf("worst delivery was %d%% of budget; docs claim at least 80%%", worst)
	}
}

func percentOff(actual, budget int) int {
	if budget == 0 {
		return 0
	}
	return (actual - budget) * 100 / budget
}

// The estimate cannot drift from the output because it IS the output: what the truncator
// charges for a node must be the bytes that node costs once rendered. Change a formatter
// without changing the charge and this reds — which is the link the old estimator did not
// have, and the reason maxTokens had already drifted from all four formats.
func TestWhatTheTruncatorChargesIsWhatTheFormatterEmits(t *testing.T) {
	nodes := budgetProbeNodes(40)

	for _, tc := range []struct {
		format string
		// slack is the array or document framing that belongs to the collection rather
		// than to any node: the bytes no per-node charge can be attributed.
		slack int
	}{
		{format: "compact", slack: 0},
		{format: "text", slack: 0},
		{format: "yaml", slack: 0},
		{format: "json", slack: 1},
	} {
		t.Run(tc.format, func(t *testing.T) {
			cost := nodeCost(tc.format)
			charged := 0
			for _, n := range nodes {
				charged += cost(n)
			}
			emitted := renderedBytes(t, nodes, tc.format)

			if diff := emitted - charged; diff != tc.slack {
				t.Errorf("%s: charged %d bytes for %d nodes but the formatter emits %d (off by %d, want %d): the cost model has drifted from the layout",
					tc.format, charged, len(nodes), emitted, diff, tc.slack)
			}
		})
	}
}

// A node's charge must also track its own shape, not just aggregate correctly: an empty
// name, a value, a focus marker and a checked state each change the bytes emitted, and a
// charge that ignores any of them under-bills that node shape specifically.
func TestEveryRenderedFieldIsChargedForCompactAndText(t *testing.T) {
	base := A11yNode{Ref: "e1", Role: "button"}
	for _, tc := range []struct {
		name string
		node A11yNode
	}{
		{name: "bare", node: base},
		{name: "named", node: A11yNode{Ref: "e1", Role: "button", Name: "Submit order"}},
		{name: "valued", node: A11yNode{Ref: "e1", Role: "textbox", Value: "user@example.com"}},
		{name: "focused", node: A11yNode{Ref: "e1", Role: "button", Focused: true}},
		{name: "disabled", node: A11yNode{Ref: "e1", Role: "button", Disabled: true}},
		{name: "hidden", node: A11yNode{Ref: "e1", Role: "button", Hidden: true}},
		{name: "checked", node: A11yNode{Ref: "e1", Role: "checkbox", Checked: CheckedTrue}},
		{name: "unchecked", node: A11yNode{Ref: "e1", Role: "checkbox", Checked: CheckedFalse}},
		{name: "mixed", node: A11yNode{Ref: "e1", Role: "checkbox", Checked: CheckedMixed}},
		{name: "deep", node: A11yNode{Ref: "e1", Role: "listitem", Depth: 4}},
		{name: "everything", node: A11yNode{Ref: "e12", Role: "checkbox", Name: "Remember me", Value: "on", Depth: 3, Focused: true, Disabled: true, Hidden: true, Checked: CheckedMixed}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			one := []A11yNode{tc.node}
			if got, want := nodeCost("compact")(tc.node), len(FormatSnapshotCompact(one)); got != want {
				t.Errorf("compact charged %d bytes, formatter emits %d", got, want)
			}
			if got, want := nodeCost("text")(tc.node), len(FormatSnapshotText(one)); got != want {
				t.Errorf("text charged %d bytes, formatter emits %d", got, want)
			}
		})
	}
}

func renderedBytes(t *testing.T, nodes []A11yNode, format string) int {
	t.Helper()
	switch format {
	case "compact":
		return len(FormatSnapshotCompact(nodes))
	case "text":
		return len(FormatSnapshotText(nodes))
	case "yaml":
		out, err := yaml.Marshal(nodes)
		if err != nil {
			t.Fatalf("marshal yaml: %v", err)
		}
		return len(out)
	default:
		out, err := json.Marshal(nodes)
		if err != nil {
			t.Fatalf("marshal json: %v", err)
		}
		return len(out)
	}
}

// The behavioural guards above compare a charge to an output, which cannot catch a FIFTH
// renderer that emits the layout inline and is never costed at all. This one can: the
// distinctive layout literals belong to appendNode and nowhere else.
func TestNodeLayoutIsWrittenDownExactlyOnce(t *testing.T) {
	pkg := srccensus.Load(t, ".", minObserveSourceFiles)

	for _, literal := range []string{` val="`, ` [focused]`, ` [disabled]`} {
		t.Run(strings.TrimSpace(literal), func(t *testing.T) {
			var sites []string
			for _, name := range pkg.Files() {
				body, err := os.ReadFile(filepath.Join(pkg.Dir(), name))
				if err != nil {
					t.Fatal(err)
				}
				for i, line := range strings.Split(string(body), "\n") {
					if strings.Contains(line, literal) {
						sites = append(sites, fmt.Sprintf("%s:%d: %s", name, i+1, strings.TrimSpace(line)))
					}
				}
			}
			if len(sites) != 1 {
				t.Errorf("%q appears %d times, want exactly 1 — a node's layout written down twice is what let maxTokens drift from every format; emit it through appendNode, or if the layout genuinely moved, re-point this guard at its new single home rather than deleting it:\n%s",
					literal, len(sites), strings.Join(sites, "\n"))
			}
		})
	}
}
