---
name: notion-second-brain
description: >
  Connect Workshop to Notion as a second brain. Search, create, update Notion pages and databases.
  Use when user mentions "Notion", "second brain", "knowledge base", "sync to Notion".
  Reference: https://developers.notion.com/docs
---

# Notion — Second Brain Integration

Connect the Workshop to Notion for persistent knowledge management, cross-session memory, and team collaboration.

## Connected Master Notion Hubs
- **AI AGENT SECOND BRAIN**: [`https://app.notion.com/p/AI-AGENT-SECOND-BRAIN-3cc6d0c8ba0c80c1980bcd0a2b601008?source=copy_link`](https://app.notion.com/p/AI-AGENT-SECOND-BRAIN-3cc6d0c8ba0c80c1980bcd0a2b601008?source=copy_link)
  - `🛠️ Error Post-Mortem & Fixes Database` (`3cf6d0c8-ba0c-8174-89f2-cedf8b5906d0`)
  - `👤 User DNA & Environment Profile` (`3cf6d0c8-ba0c-8108-be11-f0d9c20f79df`)
  - `📐 Architecture Decision Records (ADRs)` (`3cf6d0c8-ba0c-816e-95b2-f35cc4211ab8`)
  - `⚡ Autonomous Task Queue & Session Handoffs` (`3cf6d0c8-ba0c-8105-a7e1-fd587c8a45c9`)
  - `🌐 Local Service & Gateway Registry` (`3cf6d0c8-ba0c-81d2-9bcb-effcd5c7f8d3`)
  - `📖 Meta-Prompts & SOP Playbooks` (`3cf6d0c8-ba0c-817f-9ea1-c22e4394204a`)
- **AI AGENT WORKSHOP**: [`https://app.notion.com/p/AI-AGENT-WORKSHOP-3cc6d0c8ba0c8097a87bc9dd87c4f922?source=copy_link`](https://app.notion.com/p/AI-AGENT-WORKSHOP-3cc6d0c8ba0c8097a87bc9dd87c4f922?source=copy_link)

## CLI Synchronization
To sync all workshop architecture, skills, and cognitive hierarchies to Notion:
```bash
python scripts/notion_sync.py
python scripts/deploy_second_brain_hierarchy.py
```

## Setup

1. **Create Notion Integration**:
   - Go to https://www.notion.so/my-integrations
   - Create new internal integration
   - Copy integration token

2. **Configure Environment**:
   ```bash
   export NOTION_API_KEY="secret_your_integration_key_here"
   ```

3. **Install Python SDK**:
   ```bash
   pip install notion-client
   ```

## Core Operations

### Search Pages
```python
from notion_client import Client

notion = Client(auth="YOUR_NOTION_API_KEY")

# Search by query
results = notion.search(query="project", filter={"property": "object", "value": "page"})

# Search databases
results = notion.search(filter={"property": "object", "value": "database"})
```

### Read Page
```python
# Get full page content
page = notion.pages.retrieve(page_id="YOUR_PAGE_ID")

# Query page content (blocks)
blocks = notion.blocks.children.list(block_id="YOUR_PAGE_ID")
```

### Create Page
```python
notion.pages.create(
    parent={"database_id": "YOUR_DB_ID"},
    properties={
        "Name": {"title": [{"text": {"content": "New Task"}}]},
        "Status": {"status": {"name": "Not Started"}}
    },
    children=[
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Details"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Task description..."}}]
            }
        }
    ]
)
```

### Update Page
```python
notion.pages.update(
    page_id="YOUR_PAGE_ID",
    properties={
        "Status": {"status": {"name": "In Progress"}}
    }
)
```

### Query Database
```python
# Filter by property
results = notion.databases.query(
    database_id="YOUR_DB_ID",
    filter={
        "property": "Status",
        "status": {"equals": "Done"}
    },
    sorts=[{"property": "Due Date", "direction": "ascending"}]
)
```

## Workshop Integration

### Export Findings to Notion
```bash
# Export session notes
python scripts/export_to_notion.py --source workshop --target notion --page "Session Notes"
```

### Sync Knowledge Base
```bash
# Sync workshop skills index to Notion
python scripts/sync_skills_to_notion.py
```

## Common Use Cases

| Use Case | Notion Feature | Workflow |
|----------|---------------|----------|
| Project tracking | Databases | Create from task list |
| Meeting notes | Pages | Export from session |
| Research archive | Database | Index by tags |
| Knowledge graph | Linked databases | Connect related notes |
| Second brain | All of above | Daily sync |

## MCP Alternative

Consider using the built-in `memory` MCP server for graph-based knowledge:
```bash
npx -y @modelcontextprotocol/server-memory
```

Use Notion for human-readable documentation, memory MCP for agent-to-agent knowledge transfer.
