package handlers

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/pinchtab/pinchtab/internal/activity"
	"github.com/pinchtab/pinchtab/internal/bridge"
	"github.com/pinchtab/pinchtab/internal/httpx"
)

type viewportRequest struct {
	TabID             string  `json:"tabId"`
	Width             int     `json:"width"`
	Height            int     `json:"height"`
	DeviceScaleFactor float64 `json:"deviceScaleFactor"`
	Mobile            bool    `json:"mobile"`
}

// HandleSetViewport sets the browser viewport dimensions via CDP emulation.
// POST /emulation/viewport
func (h *Handlers) HandleSetViewport(w http.ResponseWriter, r *http.Request) {
	req, ok := decodeJSONBody[viewportRequest](w, r)
	if !ok {
		return
	}

	h.setViewport(w, r, req)
}

// HandleTabSetViewport sets the browser viewport dimensions for a specific tab.
// POST /tabs/{id}/emulation/viewport
func (h *Handlers) HandleTabSetViewport(w http.ResponseWriter, r *http.Request) {
	req, ok := decodeJSONBody[viewportRequest](w, r)
	if !ok {
		return
	}
	tabID, ok := h.requirePathTabIDMatch(w, r, req.TabID)
	if !ok {
		return
	}
	req.TabID = tabID

	h.setViewport(w, r, req)
}

func (h *Handlers) setViewport(w http.ResponseWriter, r *http.Request, req viewportRequest) {
	if req.Width <= 0 || req.Height <= 0 {
		httpx.Error(w, 400, fmt.Errorf("width and height must be positive integers"))
		return
	}

	if req.DeviceScaleFactor <= 0 {
		req.DeviceScaleFactor = 1.0
	}

	ctx, resolvedTabID, ok := h.guardedTabContext(w, r, req.TabID, guardDomainPolicy|guardHandoffPause)
	if !ok {
		return
	}

	tCtx, tCancel := context.WithTimeout(ctx, 5*time.Second)
	defer tCancel()

	if err := h.Bridge.SetViewport(tCtx, bridge.ViewportParams{
		Width:             int64(req.Width),
		Height:            int64(req.Height),
		DeviceScaleFactor: req.DeviceScaleFactor,
		Mobile:            req.Mobile,
	}); err != nil {
		httpx.Error(w, 500, fmt.Errorf("CDP viewport override: %w", err))
		return
	}

	h.recordActivity(r, activity.Update{Action: "emulation.viewport", TabID: resolvedTabID})

	httpx.JSON(w, 200, map[string]any{
		"width":             req.Width,
		"height":            req.Height,
		"deviceScaleFactor": req.DeviceScaleFactor,
		"mobile":            req.Mobile,
		"status":            "applied",
	})
}
