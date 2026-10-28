---
name: agent-memory-systems
description: "Memory is the cornerstone of intelligent agents. Without it, every
  interaction starts from zero. This skill covers the architecture of agent
  memory: short-term (context window), long-term (vector stores), and the
  cognitive architectures that organize them."
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Agent Memory Systems

Memory is the cornerstone of intelligent agents. Without it, every interaction
starts from zero. This skill covers the architecture of agent memory: short-term
(context window), long-term (vector stores), and the cognitive architectures
that organize them.

Key insight: Memory isn't just storage - it's retrieval. A million stored facts
mean nothing if you can't find the right one. Chunking, embedding, and retrieval
strategies determine whether your agent remembers or forgets.

The field is fragmented with inconsistent terminology. We use the CoALA cognitive
architecture framework: semantic memory (facts), episodic memory (experiences),
and procedural memory (how-to knowledge).

## Principles

- Memory quality = retrieval quality, not storage quantity
- Chunk for retrieval, not for storage
- Context isolation is the enemy of memory
- Right memory type for right information
- Decay old memories - not everything should be forever
- Test retrieval accuracy before production
- Background memory formation beats real-time

## Capabilities

- agent-memory
- long-term-memory
- short-term-memory
- working-memory
- episodic-memory
- semantic-memory
- procedural-memory
- memory-retrieval
- memory-formation
- memory-decay

## Scope

- vector-database-operations → data-engineer
- rag-pipeline-architecture → llm-architect
- embedding-model-selection → ml-engineer
- knowledge-graph-design → knowledge-engineer

## Tooling

### Memory_frameworks

- LangMem (LangChain) - When: LangGraph agents with persistent memory Note: Semantic, episodic, procedural memory types