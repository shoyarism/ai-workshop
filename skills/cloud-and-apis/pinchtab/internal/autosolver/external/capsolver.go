package external

import (
	"context"
	"fmt"

	"github.com/pinchtab/pinchtab/internal/autosolver"
)

// CapsolverConfig holds Capsolver API configuration.
type CapsolverConfig struct {
	APIKey  string `json:"apiKey"`
	BaseURL string `json:"baseUrl,omitempty"` // Default: https://api.capsolver.com
}

// Capsolver implements autosolver.Solver using the Capsolver API.
// It supports reCAPTCHA v2/v3, hCaptcha, and Cloudflare Turnstile.
type Capsolver struct {
	externalSolver
}

// NewCapsolver creates a Capsolver solver with the given configuration.
func NewCapsolver(cfg CapsolverConfig) *Capsolver {
	if cfg.BaseURL == "" {
		cfg.BaseURL = "https://api.capsolver.com"
	}
	return &Capsolver{externalSolver{
		name:     autosolver.CapsolverSolverName,
		label:    "capsolver",
		apiKey:   cfg.APIKey,
		baseURL:  cfg.BaseURL,
		priority: 200,
	}}
}

// Solve submits the CAPTCHA to the Capsolver API and injects the result.
//
// This is a skeleton implementation. The actual HTTP client logic
// (create task → poll result → inject token) must be filled in
// with the Capsolver API v1 protocol.
func (c *Capsolver) Solve(ctx context.Context, page autosolver.Page, executor autosolver.ActionExecutor) (*autosolver.Result, error) {
	sitekey, result, err := c.prepare(page)
	if err != nil {
		return result, err
	}

	// TODO: Implement HTTP client for Capsolver API v1.
	// POST /createTask with task type + sitekey + page URL.
	_ = sitekey
	_ = page.URL()

	result.Error = "capsolver API client not yet implemented"
	return result, fmt.Errorf("capsolver: API client not yet implemented — skeleton only")
}
