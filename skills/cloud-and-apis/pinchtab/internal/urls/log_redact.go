package urls

import (
	"net"
	"net/url"
	"strings"

	"github.com/pinchtab/pinchtab/internal/sanitize"
)

const maxLogURLBytes = 512

// Redact is the single implementation of the URL redaction control: it strips
// the components that must never reach a persisted record — userinfo, query and
// fragment — lowercases the host, and caps the result at maxBytes. Inputs that
// are not URLs return an empty string rather than echoing possibly-sensitive
// text through. Callers differ only in the cap they pass.
func Redact(raw string, maxBytes int) string {
	raw = strings.TrimSpace(raw)
	if raw == "" {
		return ""
	}

	normalized, err := Sanitize(raw)
	if err != nil {
		normalized = raw
	}

	parsed, err := url.Parse(normalized)
	if err != nil {
		return ""
	}
	// Sanitize returns any string containing "://" verbatim, so this guard has
	// to run on its success path too: a relative path such as "/path://x"
	// arrives here parsed as neither scheme, host nor opaque.
	if parsed.Scheme == "" && parsed.Host == "" && parsed.Opaque == "" {
		return ""
	}

	parsed.User = nil
	parsed.RawQuery = ""
	parsed.Fragment = ""
	parsed.ForceQuery = false

	if parsed.Host != "" {
		host := strings.ToLower(parsed.Hostname())
		if port := parsed.Port(); port != "" {
			parsed.Host = net.JoinHostPort(host, port)
		} else {
			parsed.Host = host
		}
	}

	return sanitize.TruncateUTF8BytesWithEllipsis(parsed.String(), maxBytes)
}

// RedactForLog redacts raw for log output.
func RedactForLog(raw string) string {
	return Redact(raw, maxLogURLBytes)
}
