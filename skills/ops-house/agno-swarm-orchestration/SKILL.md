---
name: agno-swarm-orchestration
description: High-performance, lightweight multimodal agent orchestration and multi-agent teams with Agno.
---

# Agno Multimodal & Multi-Agent Swarms

Agno (formerly Phidata) is a lightweight Python agent framework designed for high-performance memory, knowledge, and multi-agent coordination.

## Features
- First-class multi-modal support (text, audio, image, video).
- Team and swarm coordination out-of-the-box.
- Native integration with MCP and SQLite/PostgreSQL storage.

## Example Agent Team

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

researcher = Agent(
    name="Researcher",
    role="Research engineering trends and literature",
    tools=[],
    show_tool_calls=True
)

agent_team = Agent(
    team=[researcher],
    instructions=["Delegate deep research questions to the Researcher agent."],
    show_tool_calls=True
)

agent_team.print_response("What are the best practices for agent memory in 2026?")
```
