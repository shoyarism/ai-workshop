package activity

import internalurls "github.com/pinchtab/pinchtab/internal/urls"

const maxActivityURLBytes = 2048

// sanitizeActivityURL redacts raw for the activity feed. The feed keeps a
// larger cap than logs; every other rule is shared, so it is not restated here.
func sanitizeActivityURL(raw string) string {
	return internalurls.Redact(raw, maxActivityURLBytes)
}
