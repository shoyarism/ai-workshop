# 🔍 Error Post-Mortems & Incident Forensics

Episodic memory of verified engineering fixes and root-cause analyses.

All post-mortems follow the format: `PM-XXX-summary-title.md`

## Post-Mortem Log

| PM ID | Title | Severity | Date |
|-------|-------|----------|------|
| [[PM-001-truncated-code-fraud\|PM-001]] | Truncated Code Fraud Incident | P0 | 2026-09-15 |
| [[PM-002-naked-exception-blackhole\|PM-002]] | Silent Exception Blackhole Outage | P1 | 2026-09-22 |

## Post-Mortem Template

```markdown
---
pmid: PM-XXX
title: <Title>
date: YYYY-MM-DD
severity: P0 | P1 | P2
impact: <brief description>
root_cause: <brief description>
fix_verified: YYYY-MM-DD
---

# PM-XXX: <Title>

## Incident Summary

## Timeline

| Time | Event |
|------|-------|

## Root Cause Analysis

## Impact Assessment

## Fix Implementation

### Immediate

### Long-term

## Prevention System

## Lessons Learned

## Metrics Impact

## Follow-up Actions

- [ ] Action item 1
- [ ] Action item 2

## Related Artifacts

- [[ADR-XXX-related-decision]]
- [[PM-XXX-previous-incident]]
```

## Post-Mortem Creation Protocol

1. **Log the Incident**: Record when discovered
2. **Timeline Reconstruction**: Exact sequence of events
3. **Root Cause**: Deep dive into why (5 Whys)
4. **Impact Quantification**: Users, revenue, trust
5. **Fix Verification**: Confirm fix in staging
6. **Prevention System**: Automated detection/prevention
7. **Lessons Learned**: Share with team
8. **Follow-up Tracking**: Monitor action items

## Severity Levels

| Level | Definition | Response Time |
|-------|------------|---------------|
| **P0** | Catastrophic/outage | < 30 min |
| **P1** | Major degradation | < 4 hours |
| **P2** | Minor issues | Next sprint |

## CLI Operations

```bash
# Create new post-mortem
python scripts/workshop.py vault postmortem new "<title>"

# Search post-mortems
python scripts/workshop.py vault search "authentication"
```