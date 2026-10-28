package mcp

import (
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/pinchtab/pinchtab/internal/handlers"
)

// normalizeSnapshotFormat used to be the only place a bad format was caught, so the
// guarantee reached MCP callers and nobody else. The HTTP handler enforces it now, which
// makes this layer an early, friendlier rejection rather than the enforcement — and that
// only holds while the two agree on what is valid. A format MCP accepts and the handler
// rejects would turn a clear tool error into a 400 from underneath.
func TestMCPAcceptsOnlyFormatsTheHandlerAlsoAccepts(t *testing.T) {
	for _, candidate := range []string{"compact", "text", "json", "yaml", "  TEXT  ", "xml", "compct", ""} {
		normalized, mcpErr := normalizeSnapshotFormat(candidate)
		if mcpErr != nil {
			continue
		}
		if _, err := handlers.ParseSnapshotCostControls(url.Values{"format": {normalized}}); err != nil {
			t.Errorf("MCP accepts format %q (as %q) but the handler rejects it: %v", candidate, normalized, err)
		}
	}
}

// The inverse is deliberately NOT required: the handler serves json and yaml, which the MCP
// tools do not offer. This pins that the narrowing is the only difference, so a future
// format added to the handler does not quietly become unreachable from MCP by accident.
func TestMCPNarrowsTheHandlerRatherThanDivergingFromIt(t *testing.T) {
	for _, format := range []string{"compact", "text"} {
		if _, err := normalizeSnapshotFormat(format); err != nil {
			t.Errorf("MCP rejects %q, which its own tools document: %v", format, err)
		}
	}
	for _, handlerOnly := range []string{"json", "yaml"} {
		if _, err := normalizeSnapshotFormat(handlerOnly); err == nil {
			t.Errorf("MCP now accepts %q; if that is intended, the tool schema and this test both need updating", handlerOnly)
		}
	}
}

func snapshotQueryFor(t *testing.T, args map[string]any) (url.Values, *mcp.CallToolResult) {
	t.Helper()
	var captured url.Values
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		captured = r.URL.Query()
		_, _ = w.Write([]byte("# snapshot\n"))
	}))
	t.Cleanup(srv.Close)
	result := callTool(t, "pinchtab_snapshot", args, srv)
	return captured, result
}

func TestTheSnapshotToolAsksForCompactUnlessToldOtherwise(t *testing.T) {
	for _, tc := range []struct {
		name string
		args map[string]any
		want string
	}{
		{name: "no format argument at all", args: map[string]any{}, want: "compact"},
		{name: "interactive only", args: map[string]any{"interactive": true}, want: "compact"},
		{name: "compact asked for explicitly", args: map[string]any{"compact": true}, want: "compact"},
		{name: "compact declined", args: map[string]any{"compact": false}, want: "json"},
		{name: "format wins over the default", args: map[string]any{"format": "text"}, want: "text"},
		{name: "format wins over compact", args: map[string]any{"format": "text", "compact": true}, want: "text"},
		{name: "format normalised", args: map[string]any{"format": "  COMPACT "}, want: "compact"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			query, result := snapshotQueryFor(t, tc.args)
			if result.IsError {
				t.Fatalf("the tool refused %v: %s", tc.args, resultText(t, result))
			}
			if got := query.Get("format"); got != tc.want {
				t.Errorf("the tool asked /snapshot for format=%q, want %q; the agent pays for the answer the server actually sends, not for the one the source reads like",
					got, tc.want)
			}
			if _, err := handlers.ParseSnapshotCostControls(query); err != nil {
				t.Errorf("the server rejects the query this tool sends: %v (query=%v)", err, query)
			}
		})
	}
}

func TestTheSnapshotToolRefusesAFormatBeforeSendingIt(t *testing.T) {
	query, result := snapshotQueryFor(t, map[string]any{"format": "xml"})
	if !result.IsError {
		t.Fatalf("format=xml was accepted; the caller gets an answer to a question it did not ask")
	}
	if query != nil {
		t.Errorf("the tool reached the server anyway with %v", query)
	}
}
