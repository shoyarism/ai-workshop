---
name: pydantic-ai-workflows
description: Building production-grade, type-safe, and deterministic AI agents using PydanticAI.
---

# PydanticAI Type-Safe Agent Workflows

PydanticAI is the official Python agent framework developed by Pydantic to bring type validation, structured outputs, and dependency injection to LLM agents.

## Features
- **100% Type-Safe**: Native Pydantic models for inputs, outputs, and tool arguments.
- **Model Agnostic**: Works with Gemini, OpenAI, Anthropic, Ollama, and LiteLLM.
- **Dependency Injection**: Clean runtime dependency management.

## Example Agent

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class DiagnosticReport(BaseModel):
    subsystem: str
    healthy: bool
    issues: list[str] = Field(default_factory=list)

agent = Agent(
    "gemini-2.5-flash",
    result_type=DiagnosticReport,
    system_prompt="You are a strict Workshop diagnostic agent."
)

result = agent.run_sync("Analyze git status on subsystem 'browser-use'")
print(result.data)
```
