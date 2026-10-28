package mcp

import (
	"context"
	"strings"
	"testing"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
)

func TestHandleWait(t *testing.T) {
	srv := mockPinchTab()
	defer srv.Close()

	r := callTool(t, "pinchtab_wait", map[string]any{
		"for":   "ms",
		"value": "50",
	}, srv)

	text := resultText(t, r)
	if !strings.Contains(text, "waited_ms") {
		t.Errorf("expected waited_ms, got %s", text)
	}
}

func TestHandleWaitClampsMax(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	c := NewClient("http://localhost:1", "")
	handlers := handlerMap(c)
	h := handlers["pinchtab_wait"]
	req := mcp.CallToolRequest{}
	req.Params.Name = "pinchtab_wait"
	req.Params.Arguments = map[string]any{"for": "ms", "value": "999999"}
	r, err := h(ctx, req)
	if err != nil {
		t.Fatal(err)
	}

	text := resultText(t, r)
	if !strings.Contains(text, "cancelled") && !strings.Contains(text, "30000") {
		t.Errorf("expected 'cancelled' or '30000', got %s", text)
	}
}

func TestHandleWaitForSelector(t *testing.T) {
	srv := mockPinchTab()
	defer srv.Close()

	r := callTool(t, "pinchtab_wait", map[string]any{
		"for":     "selector",
		"value":   ".loaded",
		"timeout": float64(5000),
	}, srv)

	text := resultText(t, r)
	if !strings.Contains(text, "waited") {
		t.Errorf("expected waited, got %s", text)
	}
}

// browser must be forwarded as a query param (routing is query-based), not the
// body — otherwise browser=cloak is silently dropped by the router.
func TestHandleWaitForSelectorForwardsBrowser(t *testing.T) {
	srv := mockPinchTab()
	defer srv.Close()

	r := callTool(t, "pinchtab_wait", map[string]any{
		"for":     "selector",
		"value":   ".loaded",
		"browser": "cloak",
	}, srv)

	text := resultText(t, r)
	if !strings.Contains(text, "query") || !strings.Contains(text, "browser") || !strings.Contains(text, "cloak") {
		t.Errorf("expected forwarded browser=cloak in query, got %s", text)
	}
}

func TestHandleWaitForSelectorMissing(t *testing.T) {
	srv := mockPinchTab()
	defer srv.Close()

	r := callTool(t, "pinchtab_wait", map[string]any{"for": "selector"}, srv)
	if !r.IsError {
		t.Error("expected error for missing selector")
	}
}

func TestHandleWaitRefusesAnUnknownCondition(t *testing.T) {
	srv := mockPinchTab()
	defer srv.Close()

	r := callTool(t, "pinchtab_wait", map[string]any{"for": "element", "value": ".loaded"}, srv)
	if !r.IsError {
		t.Fatal("expected an error for an unknown 'for' value")
	}
	text := resultText(t, r)
	for _, want := range []string{"element", "selector", "function"} {
		if !strings.Contains(text, want) {
			t.Errorf("refusal %q does not name %q, so the caller cannot correct it", text, want)
		}
	}
}

// The five browser-backed conditions are one operation on the wire: each has to
// reach POST /wait under the field name that endpoint decodes, or the server
// answers "one of selector, text, url, load, fn, or ms is required".
func TestEveryWaitConditionReachesItsWireField(t *testing.T) {
	for _, tc := range []struct{ condition, value, field string }{
		{"selector", ".loaded", "selector"},
		{"text", "Success", "text"},
		{"url", "**/dashboard", "url"},
		{"load", "network-idle", "load"},
		{"function", "window.ready", "fn"},
	} {
		t.Run(tc.condition, func(t *testing.T) {
			srv := mockPinchTab()
			defer srv.Close()

			r := callTool(t, "pinchtab_wait", map[string]any{"for": tc.condition, "value": tc.value}, srv)
			if r.IsError {
				t.Fatalf("for=%q was rejected: %s", tc.condition, resultText(t, r))
			}
			body, _ := resultJSON(t, r)["body"].(map[string]any)
			if got, _ := body[tc.field].(string); got != tc.value {
				t.Errorf("for=%q sent %s=%q, want the value under %q — the endpoint reads that field only (body=%v)",
					tc.condition, tc.field, got, tc.field, body)
			}
		})
	}
}

func TestHandleWaitForSelectorForwardsState(t *testing.T) {
	srv := mockPinchTab()
	defer srv.Close()

	r := callTool(t, "pinchtab_wait", map[string]any{
		"for":   "selector",
		"value": ".gone",
		"state": "hidden",
	}, srv)

	body, _ := resultJSON(t, r)["body"].(map[string]any)
	if got, _ := body["state"].(string); got != "hidden" {
		t.Errorf("state reached the wait body as %q, want hidden (body=%v)", got, body)
	}
}

func TestHandleWaitNegativeMs(t *testing.T) {
	srv := mockPinchTab()
	defer srv.Close()

	r := callTool(t, "pinchtab_wait", map[string]any{"for": "ms", "value": "-100"}, srv)
	text := resultText(t, r)
	if !strings.Contains(text, "waited_ms") {
		t.Errorf("expected waited_ms, got %s", text)
	}
	if !strings.Contains(text, "0") {
		t.Errorf("expected 0ms for negative input, got %s", text)
	}
}
