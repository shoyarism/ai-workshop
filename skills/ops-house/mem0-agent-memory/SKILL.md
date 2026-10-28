---
name: mem0-agent-memory
description: Self-improving personalized memory and knowledge graph layer for AI agents using Mem0.
---

# Mem0 Personalized Agent Memory

Mem0 provides an intelligent memory layer for AI agents, continually learning user preferences, personalizing responses, and maintaining context across sessions.

## Architecture
- Extracts facts, preferences, and entity relationships automatically.
- Stores memories with vector search and graph-based retrieval.
- Supplements static vault Markdown with dynamic episodic memory.

## Usage Pattern

```python
from mem0 import Memory

# Initialize Mem0 client
m = Memory()

# Store user interaction or preference
m.add("Prefers high-density engineering responses with zero sycophancy and strict KaTeX formatting.", user_id="workshop_user")

# Query memory for relevant context
relevant_memories = m.search("What is the preferred communication style?", user_id="workshop_user")
for mem in relevant_memories:
    print(mem["memory"])
```
