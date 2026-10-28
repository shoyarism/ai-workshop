# Workshop Second Brain — Notion Integration

## Quick Start

```bash
# 1. Set your Notion API key
export NOTION_API_KEY="secret_your_key_here"

# 2. Search your workspace
python scripts/notion_sync.py --search "workshop"

# 3. Export session notes
python scripts/notion_sync.py --export session_notes.md

# 4. Sync skills index
python scripts/notion_sync.py --sync-skills
```

## Notion Workspace

**Primary URL**: https://app.notion.com/p/AI-AGENT-WORKSHOP-3cc6d0c8ba0c8097a87bc9dd87c4f922

This is the centralized knowledge base for:
- Session notes and decisions
- Skill inventory and updates
- Research findings
- Architecture documents

## Setup Steps

1. **Create Integration** at https://www.notion.so/my-integrations
2. **Share** your Notion pages with the integration
3. **Set API Key** in environment or `.env` file

## Integration Points

| Source | Target | Method |
|--------|--------|--------|
| Workshop sessions | Notion pages | Auto-export |
| Skills index | Notion database | Sync script |
| Research notes | Notion database | Manual or CLI |
| Decision logs | Notion database | CLI export |

## Using with Skills

The `notion-second-brain` skill provides instructions for:
- Searching Notion content
- Creating/updating pages
- Querying databases
- Exporting workshop data

## Alternative: MCP Memory

For agent-to-agent memory (machine-readable):
```bash
npx -y @modelcontextprotocol/server-memory
```
