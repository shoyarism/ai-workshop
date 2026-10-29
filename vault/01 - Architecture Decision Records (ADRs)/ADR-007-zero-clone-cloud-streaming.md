---
adrid: ADR-007
title: Zero-Clone Cloud Streaming Protocol
status: Accepted
date: 2026-09-22
authors: ["shoyarism", "Antigravity"]
---

# ADR-007: Zero-Clone Cloud Streaming Protocol

## Context

AI agent harnesses in ephemeral environments face challenges:

1. **Clone Overhead**: 5-15 minute `git clone` in CI/CD
2. **Large Repositories**: ai-workshop is 2.3GB with 2,150+ skills
3. **Token Limits**: Full repo context exceeds model capacity
4. **Network Constraints**: Some environments have no Git access

## Decision

Implement **streaming skill access** via GitHub Raw API:

### Protocol Flow

```
[ Agent in ephemeral container ]
            ↓
[ Request skill via curl ]
            ↓
[ GitHub raw content returned ]
            ↓
[ skill used in agent context ]
            ↓
[ No clone required ]
```

### Command Pattern

```bash
# Stream any skill directly into context
curl -fsSL https://raw.githubusercontent.com/shoyarism/ai-workshop/main/skills/dev-house/superpowers/SKILL.md

# With authentication for higher rate limits
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3.raw" \
     https://api.github.com/repos/shoyarism/ai-workshop/contents/skills/dev-house/superpowers/SKILL.md
```

### Workshop CLI Wrapper

```bash
# New CLI command
python scripts/workshop.py stream skills/dev-house/superpowers/SKILL.md

# Batch streaming
python scripts/workshop.py stream skills/dev-house/superpowers/ skills/security-house/slop-court/
```

### Implementation in workshop.py

```python
def cmd_stream(args):
    import urllib.request
    
    skill_path = getattr(args, "path", "")
    if not skill_path:
        print("[!] No skill path specified")
        return
    
    url = f"https://raw.githubusercontent.com/shoyarism/ai-workshop/main/{skill_path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Workshop-Agent"})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            print(content)
    except Exception as e:
        print(f"[!] Failed to stream: {e}")
```

## Rate Limit Management

### Public Access (No Auth)
- **60 requests/hour** per IP
- Sufficient for single skill fetches
- Use via `curl -fsSL`

### Authenticated Access
- **5000 requests/hour** with token
- Set via `GITHUB_TOKEN` environment variable
- Recommended for CI/CD pipelines

## Caching Strategy

```python
# Local cache in ephemeral environment
CACHE_DIR = Path("/tmp/workshop_cache")
CACHE_TTL = 3600  # 1 hour

def get_skill(path: str) -> str:
    cache_file = CACHE_DIR / path.replace("/", "_")
    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL:
        return cache_file.read_text()
    
    content = stream_skill(path)
    cache_file.write_text(content)
    return content
```

## Fallback Protocol

When GitHub API is unavailable:

1. **Local fallback**: Check existing `skills/` directory
2. **Offline mode**: `workshop.py doctor --offline` validates local state
3. **Vendor bundle**: Pre-download essentials with `workshop.py sync --bundle`

## Consequences

### Positive
- **Instant access** to 2,150+ skills without clone
- **Perfect for CI/CD** ephemeral containers
- **Reduced token usage** (only stream needed skills)
- **Fails gracefully** when GitHub unavailable

### Negative
- Requires GitHub availability
- Higher latency than local disk (but no clone wait)
- Rate limits can be hit in bulk operations

## Usage Examples

```bash
# Quick skill fetch
WORKSHOP_SKILL=$(curl -s https://raw.githubusercontent.com/shoyarism/ai-workshop/main/skills/dev-house/superpowers/SKILL.md)
cat >> agent_prompt.md << EOF
# Context: Superpowers Skill
$WORKSHOP_SKILL
EOF

# Zero-clone environment setup
pip install pydantic yaml requests
curl -s https://raw.githubusercontent.com/shoyarism/ai-workshop/main/skills/dev-house/tdd/SKILL.md > /tmp/tdd.md

# Bulk fetch for offline work
python scripts/workshop.py sync --bundle --output /tmp/offline_skills/
```

## Related

- ADR-003: Obsidian Second Brain
- ADR-006: Workshop CLI Architecture