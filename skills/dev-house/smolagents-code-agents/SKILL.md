---
name: smolagents-code-agents
description: Lightweight Python code-executing autonomous agents from Hugging Face smolagents.
---

# Smolagents Code-Executing Autonomous Agents

Smolagents is Hugging Face's minimalist library for building autonomous agents that write and execute Python code snippets directly to accomplish complex multi-step goals.

## Why Code Agents?
Instead of generating JSON tool calls, Code Agents write executable Python logic:
- Directly loop, condition, and manipulate variables.
- Pass intermediate outputs between tools without LLM token waste.
- Faster execution with local sandboxing.

## Example CodeAgent

```python
from smolagents import CodeAgent, HfApiModel, tool

@tool
def calculate_system_drift(local_rev: int, remote_rev: int) -> int:
    """Calculate the number of commits separating two revisions.
    
    Args:
        local_rev: Current commit count
        remote_rev: Remote upstream commit count
    """
    return remote_rev - local_rev

agent = CodeAgent(tools=[calculate_system_drift], model=HfApiModel())
agent.run("Calculate how many commits behind the workshop is if local is 100 and remote is 145.")
```
