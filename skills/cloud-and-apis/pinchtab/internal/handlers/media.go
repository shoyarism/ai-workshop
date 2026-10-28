package handlers

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/pinchtab/pinchtab/internal/activity"
	"github.com/pinchtab/pinchtab/internal/httpx"
)

type mediaRequest struct {
	TabID   string `json:"tabId"`
	Feature string `json:"feature"`
	Value   string `json:"value"`
}

// HandleSetMedia emulates a CSS media feature via CDP.
// POST /emulation/media
func (h *Handlers) HandleSetMedia(w http.ResponseWriter, r *http.Request) {
	req, ok := decodeJSONBody[mediaRequest](w, r)
	if !ok {
		return
	}

	h.setMedia(w, r, req)
}

// HandleTabSetMedia emulates a CSS media feature for a specific tab.
// POST /tabs/{id}/emulation/media
func (h *Handlers) HandleTabSetMedia(w http.ResponseWriter, r *http.Request) {
	req, ok := decodeJSONBody[mediaRequest](w, r)
	if !ok {
		return
	}
	tabID, ok := h.requirePathTabIDMatch(w, r, req.TabID)
	if !ok {
		return
	}
	req.TabID = tabID

	h.setMedia(w, r, req)
}

func (h *Handlers) setMedia(w http.ResponseWriter, r *http.Request, req mediaRequest) {
	if req.Feature == "" {
		httpx.Error(w, 400, fmt.Errorf("missing required field: feature"))
		return
	}
	if req.Value == "" {
		httpx.Error(w, 400, fmt.Errorf("missing required field: value"))
		return
	}

	ctx, resolvedTabID, ok := h.guardedTabContext(w, r, req.TabID, guardDomainPolicy|guardHandoffPause)
	if !ok {
		return
	}

	tCtx, tCancel := context.WithTimeout(ctx, 5*time.Second)
	defer tCancel()

	if err := h.Bridge.SetEmulatedMedia(tCtx, req.Feature, req.Value); err != nil {
		httpx.Error(w, 500, fmt.Errorf("CDP set emulated media: %w", err))
		return
	}

	h.recordActivity(r, activity.Update{Action: "emulation.media", TabID: resolvedTabID})

	httpx.JSON(w, 200, map[string]any{
		"feature": req.Feature,
		"value":   req.Value,
		"status":  "applied",
	})
}
