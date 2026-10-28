---
name: langgraph-agent-builder
description: Build stateful, cyclic multi-agent workflows with LangGraph — state graphs, nodes, edges, conditional routing, memory/checkpointers, human-in-the-loop, and persistence. Use when the user wants stateful agent systems rather than linear chains, with LangSmith tracing and LangGraph Studio support. Triggers on: langgraph, state graph, multi-agent workflow, agent orchestration, conditional edges, checkpointer, human-in-the-loop, langgraph studio, langsmith, cyclic agent, agent graph.
---

# LangGraph Agent Builder

Build stateful, cyclic multi-agent workflows with LangGraph. Unlike linear chains, LangGraph models agent systems as graphs with nodes (agents/tools) and edges (routing logic), supporting cycles, persistence, and human-in-the-loop interventions.

## When to trigger

- User wants multi-agent collaboration (researcher → writer → reviewer)
- User needs cycles (retry loops, self-correction, reflection)
- User requires persistent state across runs (checkpointers, threads)
- User wants human-in-the-loop approval gates before tool execution
- User is building with LangSmith tracing and LangGraph Studio visualization

## Core concepts

### State
The shared state object passed between nodes. Define it as a TypedDict or Pydantic model:

```python
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    research_notes: str
    draft: str
    approved: bool
    iteration: int
```

### Nodes
Functions that take state and return partial state updates:

```python
from langchain_core.messages import HumanMessage, AIMessage

def researcher_node(state: AgentState):
    return {
        "messages": [AIMessage(content="Research findings...")],
        "research_notes": "Key findings compiled",
        "iteration": state.get("iteration", 0) + 1
    }

def writer_node(state: AgentState):
    return {
        "messages": [AIMessage(content="Draft written based on research")],
        "draft": "Draft content here"
    }
```

### Edges
Define routing logic. Normal edges go node→node; conditional edges use a function to pick the next node:

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_edge("researcher", "writer")
workflow.add_conditional_edges("writer", should_continue)
workflow.set_entry_point("researcher")

def should_continue(state: AgentState):
    if state.get("approved"):
        return END
    return "writer"
```

### Memory / checkpointers
Persist state across runs using a checkpointer (e.g., MemorySaver, SqliteSaver, PostgresSaver):

```python
from langgraph.checkpoint.memory import MemorySaver

app = workflow.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "conversation-1"}}
app.invoke({"messages": [HumanMessage(content="Hello")]}, config=config)
```

### Human-in-the-loop
Interrupt before specific nodes to let a human review or modify state:

```python
app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["writer"]
)
```

## Example: Research → Write → Review loop

```python
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    topic: str
    research: str
    draft: str
    iteration: int

def research(state):
    return {"research": f"Research on {state['topic']}", "iteration": state["iteration"] + 1}

def write(state):
    return {"draft": f"Draft about {state['topic']} based on: {state['research']}"}

def review(state):
    return {}  # human reviews the draft

def route(state):
    if state["iteration"] > 3:
        return END
    return "write"

workflow = StateGraph(State)
workflow.add_node("research", research)
workflow.add_node("write", write)
workflow.add_node("review", review)
workflow.add_edge("research", "write")
workflow.add_edge("write", "review")
workflow.add_conditional_edges("review", route)
workflow.set_entry_point("research")

app = workflow.compile(checkpointer=MemorySaver(), interrupt_before=["review"])

# Run with human approval at the review step
result = app.invoke(
    {"messages": [HumanMessage(content="Research quantum computing")], "topic": "quantum computing", "iteration": 0},
    config={"configurable": {"thread_id": "1"}}
)
```

## Decision checklist

- [ ] State schema defined (TypedDict/Pydantic)
- [ ] Nodes implemented as state→state functions
- [ ] Entry point and edges defined (normal + conditional)
- [ ] Checkpointer chosen (MemorySaver for dev, SqliteSaver/PostgresSaver for prod)
- [ ] Human-in-the-loop interrupt points identified
- [ ] LangSmith tracing enabled (set `LANGCHAIN_TRACING_V2=true`)
- [ ] Thread IDs managed for conversation persistence

## Related Workshop skills

- `crewai-orchestrator` — alternative role-based multi-agent framework
- `mcp-builder` — expose LangGraph agents as MCP tools
- `rag-pipeline-builder` — combine LangGraph with RAG for agentic retrieval
- `ollama-local-ai` — run LangGraph with local LLMs via Ollama
