---
pmid: PM-002
title: Silent Exception Blackhole Production Outage
date: 2026-09-22
severity: P1
impact: 2h service degradation, 15k failed requests
root_cause: AI-generated code with empty exception handlers
fix_verified: 2026-09-22
---

# PM-002: Silent Exception Blackhole Production Outage

## Incident Summary

On 2026-09-22, a database connection pool exhaustion silently failed in production due to AI-generated code with `except Exception: pass` handlers.

## Timeline

| Time | Event |
|------|-------|
| 14:08 | Database connection pool at 95% capacity |
| 14:15 | Requests start timing out (but not failing fast) |
| 14:22 | Internal monitoring alerts fire |
| 14:25 | Engineers investigate logs (no errors found!) |
| 14:35 | Code inspection reveals `except: pass` pattern |
| 14:40 | Hotfix deployed with proper logging |
| 16:15 | Full service restored |

## Root Cause Analysis

### The Problematic Code

```python
def fetch_user_data(user_id: str):
    try:
        conn = get_db_connection()
        result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return result.fetchall()
    except Exception:
        pass  # "Error handling" - this is the bug!

def retry_fetch():
    users = []
    for uid in user_ids:
        users.append(fetch_user_data(uid))
    return users
```

### Why It Happened

1. **AI pattern mimicry**: Model copied "robust error handling" pattern without understanding
2. **Silent failure**: Errors swallowed, no logs, connection leak
3. **No observability**: Circuit breaker pattern missing
4. **Test coverage gap**: Unit tests didn't simulate connection failures

## Impact Assessment

- **User Experience**: 2-hour degraded performance
- **Request Volume**: 15,000 failed requests
- **Error Visibility**: 100% of errors went unlogged
- **Debugging Time**: 17 minutes wasted (no error traces)

## Fix Implementation

### Immediate

1. Replaced empty handlers with structured logging
2. Added connection pool monitoring alerts
3. Implemented circuit breaker pattern

### Corrected Code

```python
import logging
from circuitbreaker import circuit

logger = logging.getLogger(__name__)

@circuit(failure_threshold=5, expected_exception=ConnectionError)
def fetch_user_data(user_id: str) -> list:
    try:
        conn = get_db_connection()
        result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return result.fetchall()
    except Exception as e:
        logger.exception(f"Database fetch failed for user {user_id}")
        raise ConnectionError(f"Failed to fetch user {user_id}") from e
    finally:
        if 'conn' in locals():
            conn.close()
```

### Prevention System

#### Detection Patterns

```regex
except\s*:\s*pass
except\s+Exception\s*:\s*pass
catch\s*\([^)]*\)\s*\{\s*\}
```

#### AST Verification

```python
def check_exception_handlers(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                return True  # Naked exception detected
    return False
```

## Lessons Learned

1. **Empty exception handlers are catastrophic**: Must always log and re-raise
2. **Observability is non-negotiable**: Silent failures hide critical bugs
3. **Circuit breakers are essential**: Prevent cascade failures
4. **AI agents must learn "fail fast"**: Never swallow errors silently

## Metrics Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Mean time to detect silent failures | ∞ | < 30s | ∞ |
| Error log volume | 0 | +2500/day | +∞ |
| Circuit breaker opens | 0 | 12/day | +100% |

## Follow-up Actions

- [x] Block `except: pass` via Slop Court FEL-03 statute
- [x] Add circuit breaker to all DB operations
- [ ] Audit all existing exception handlers (Q4 2026)
- [ ] Add "Never swallow exceptions" to agent training (Q4 2026)

## Related Artifacts

- [[ADR-001-slop-court-implementation#FEL-03]]
- [[ADR-005-git-bailiff-enforcement-system]]
- [[ADR-007-zero-clone-cloud-streaming]]