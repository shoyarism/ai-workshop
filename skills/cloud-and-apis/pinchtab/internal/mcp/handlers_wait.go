package mcp

import (
	"context"
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
)

var waitModes = map[string]string{
	"ms":       "ms",
	"selector": "selector",
	"text":     "text",
	"url":      "url",
	"load":     "load",
	"function": "fn",
}

func handleWait(c *Client) func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	return func(ctx context.Context, r mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		mode, field, refusal := pickMode(r, "for", waitModes)
		if refusal != nil {
			return refusal, nil
		}
		value, refusal := suppliedStringArg(r, "wait", "value", "", "value")
		if refusal != nil {
			return refusal, nil
		}
		if strings.TrimSpace(value) == "" {
			return mcp.NewToolResultError(fmt.Sprintf("wait for=%q needs a non-empty 'value'", mode)), nil
		}
		if mode == "ms" {
			return sleepFor(ctx, strings.TrimSpace(value))
		}
		return callWaitEndpoint(ctx, c, r, map[string]any{field: value})
	}
}

func sleepFor(ctx context.Context, value string) (*mcp.CallToolResult, error) {
	ms, err := strconv.ParseFloat(value, 64)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("wait for=\"ms\" needs a numeric 'value' in milliseconds, got %q", value)), nil
	}
	if ms < 0 {
		ms = 0
	}
	if ms > maxWaitMS {
		ms = maxWaitMS
	}
	select {
	case <-time.After(time.Duration(ms) * time.Millisecond):
		return mcp.NewToolResultText(fmt.Sprintf(`{"waited_ms":%d}`, int(ms))), nil
	case <-ctx.Done():
		return mcp.NewToolResultError("wait cancelled"), nil
	}
}

func callWaitEndpoint(ctx context.Context, c *Client, r mcp.CallToolRequest, payload map[string]any) (*mcp.CallToolResult, error) {
	if timeout, ok := optFloat(r, "timeout"); ok {
		payload["timeout"] = int(timeout)
	}
	if state := optString(r, "state"); state != "" {
		payload["state"] = state
	}
	if tabID := optString(r, "tabId"); tabID != "" {
		payload["tabId"] = tabID
	}
	body, code, err := c.Post(ctx, routedPath(r, "/wait"), payload)
	if err != nil {
		return mcp.NewToolResultError(err.Error()), nil
	}
	return resultFromBytes(body, code)
}
