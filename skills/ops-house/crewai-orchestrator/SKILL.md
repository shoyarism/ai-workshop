---
name: crewai-orchestrator
description: Build role-based agent crews with CrewAI — agents, tasks, tools, processes (sequential/hierarchical), memory, planning, and crew kickoff. Use when the user wants to orchestrate specialized agents with defined roles, backstories, and delegation. Triggers on: crewai, agent crew, role-based agents, task delegation, sequential process, hierarchical process, agent memory, crew kickoff, agent tools, multi-agent collaboration.
---

# CrewAI Orchestrator

Orchestrate role-based agent crews with CrewAI. Each agent has a role, goal, backstory, and tools; tasks define what needs doing; processes define how agents collaborate (sequential or hierarchical with a manager agent).

## When to trigger

- User wants specialized agents with distinct roles (researcher, writer, editor, coder)
- User needs task delegation between agents
- User wants sequential or hierarchical process flows
- User wants agent memory and planning capabilities
- User is building a crew-based multi-agent system

## Core concepts

### Agents
Agents have a role, goal, backstory, tools, and optional delegation:

```python
from crewai import Agent, LLM

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in {topic}",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends and synthesizing complex information.""",
    tools=[],
    llm=LLM(model="gpt-4o-mini"),
    verbose=True,
    allow_delegation=True,
    memory=True
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging, well-structured content based on research",
    backstory="""You are a skilled writer who turns research into compelling narratives.""",
    tools=[],
    llm=LLM(model="gpt-4o-mini"),
    verbose=True,
    allow_delegation=False
)
```

### Tasks
Tasks define description, expected output, and the responsible agent:

```python
from crewai import Task

research_task = Task(
    description="Research the latest trends in {topic} and summarize key findings.",
    expected_output="A bulleted list of top 5 trends with sources and dates.",
    agent=researcher
)

write_task = Task(
    description="Write a blog post based on the research findings.",
    expected_output="A complete blog post with introduction, body, and conclusion.",
    agent=writer,
    context=[research_task]
)
```

### Crews & processes

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # or Process.hierarchical
    manager_llm=LLM(model="gpt-4o"),  # required for hierarchical
    verbose=True,
    memory=True,
    planning=True
)

result = crew.kickoff(inputs={"topic": "quantum computing in 2026"})
```

### Process types

| Process | Description | Best for |
|---|---|---|
| Sequential | Tasks execute in order, output flows to next | Linear pipelines, simple workflows |
| Hierarchical | Manager agent coordinates, delegates tasks | Complex workflows needing oversight |

## Example: Content creation crew

```python
from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="gpt-4o-mini")

researcher = Agent(role="Researcher", goal="Find facts", backstory="Expert researcher", llm=llm)
writer = Agent(role="Writer", goal="Write articles", backstory="Professional writer", llm=llm)
editor = Agent(role="Editor", goal="Polish content", backstory="Senior editor", llm=llm)

t1 = Task(description="Research {topic}", agent=researcher, expected_output="Facts and sources")
t2 = Task(description="Write article from research", agent=writer, context=[t1], expected_output="Draft article")
t3 = Task(description="Edit and finalize", agent=editor, context=[t2], expected_output="Final polished article")

crew = Crew(agents=[researcher, writer, editor], tasks=[t1, t2, t3], process=Process.sequential)
result = crew.kickoff(inputs={"topic": "AI agent frameworks"})
print(result)
```

## Decision checklist

- [ ] Roles defined for each agent (role, goal, backstory)
- [ ] Tools assigned to agents that need them
- [ ] Tasks have clear expected outputs
- [ ] Task dependencies via `context` parameter where needed
- [ ] Process type chosen (sequential vs hierarchical)
- [ ] Memory enabled if agents need to retain context
- [ ] Planning enabled if the crew should strategize before executing

## Related Workshop skills

- `langgraph-agent-builder` — alternative state-graph multi-agent framework
- `mcp-builder` — expose CrewAI crews as MCP tools
- `ollama-local-ai` — run CrewAI with local LLMs
- `rag-pipeline-builder` — ground CrewAI agents in retrieved documents
