package external

import (
	"context"
	"fmt"

	"github.com/pinchtab/pinchtab/internal/autosolver"
)

// TwoCaptchaConfig holds 2Captcha API configuration.
type TwoCaptchaConfig struct {
	APIKey  string `json:"apiKey"`
	BaseURL string `json:"baseUrl,omitempty"` // Default: https://2captcha.com
}

// TwoCaptcha implements autosolver.Solver using the 2Captcha API.
// It supports reCAPTCHA v2/v3, hCaptcha, and Cloudflare Turnstile.
type TwoCaptcha struct {
	externalSolver
}

// NewTwoCaptcha creates a 2Captcha solver with the given configuration.
func NewTwoCaptcha(cfg TwoCaptchaConfig) *TwoCaptcha {
	if cfg.BaseURL == "" {
		cfg.BaseURL = "https://2captcha.com"
	}
	return &TwoCaptcha{externalSolver{
		name:     autosolver.TwoCaptchaSolverName,
		label:    "2captcha",
		apiKey:   cfg.APIKey,
		baseURL:  cfg.BaseURL,
		priority: 210,
	}}
}

// Solve submits the CAPTCHA to the 2Captcha API and injects the result.
//
// This is a skeleton implementation. The actual HTTP client logic
// (submit → poll → inject) must be filled in with the 2Captcha API protocol.
func (t *TwoCaptcha) Solve(ctx context.Context, page autosolver.Page, executor autosolver.ActionExecutor) (*autosolver.Result, error) {
	sitekey, result, err := t.prepare(page)
	if err != nil {
		return result, err
	}

	// TODO: Implement HTTP client for 2Captcha API.
	// POST in.php with method + sitekey + pageurl → get task ID
	// GET res.php with id → poll until ready → inject token
	_ = sitekey
	_ = page.URL()

	result.Error = "2captcha API client not yet implemented"
	return result, fmt.Errorf("2captcha: API client not yet implemented — skeleton only")
}
