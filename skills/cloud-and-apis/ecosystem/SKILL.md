---
name: ecosystem
description: >
  Multi-agent orchestration framework for distributed research teams. Build autonomous
  research swarms, manage persistent agents, coordinate multi-agent workflows.
  Reference: https://github.com/abi-sabbir/ecosystem
---

# Ecosystem — Multi-Agent Orchestration

Build and run multi-agent research teams that collaborate autonomously on complex tasks.

## Installation

```bash
pip install ecosystem
```

## Core Concepts

### Agents
Persistent, stateful AI agents that can:
- Maintain conversation history
- Access tools and skills
- Collaborate with other agents

### Teams
Groups of agents coordinated for specific goals:
- Research teams
- Development sprints
- Multi-step workflows

### Tasks
Decomposable units of work assigned to agents:
- Parallel execution
- Dependency management
- Result aggregation

## Quick Start

```python
from ecosystem import Agent, Team, Task

# Create agents
researcher = Agent(
    name="researcher",
    role="research",
    model="gpt-4"
)

writer = Agent(
    name="writer",
    role="writing",
    model="gpt-4"
)

# Create team
team = Team(
    name="research-squad",
    members=[researcher, writer]
)

# Define task
task = Task(
    goal="Research and write about AI safety",
    steps=[
        {"agent": "researcher", "action": "research"},
        {"agent": "writer", "action": "write"}
    ]
)

# Execute
result = team.execute(task)
```

## Features

- **Autonomous operation** - Agents self-direct work
- **Persistent memory** - Context survives across sessions
- **Tool integration** - MCP, browser, code execution
- **Scalable** - Run hundreds of agents
- **Fault-tolerant** - Retry and recovery built-in

## Use Cases

- **Research teams** - Multi-agent literature review
- **Code sprints** - Parallel feature development
- **Content creation** - Research + write + edit pipeline
- **Data analysis** - Extract, analyze, visualize

## Advanced Patterns

```python
# Parallel agents
team.parallel(["research", "analysis", "summarize"])

# Agent handoffs
team.chain([agent1, agent2, agent3])

# Human-in-the-loop
team.with_reviewer(human_reviewer)
```
