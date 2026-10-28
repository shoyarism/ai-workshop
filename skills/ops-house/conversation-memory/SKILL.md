---
name: conversation-memory
description: Persistent memory systems for LLM conversations including
  short-term, long-term, and entity-based memory
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Conversation Memory

Persistent memory systems for LLM conversations including short-term, long-term, and entity-based memory

## Capabilities

- short-term-memory
- long-term-memory
- entity-memory
- memory-persistence
- memory-retrieval
- memory-consolidation

## Prerequisites

- Knowledge: LLM conversation patterns, Database basics, Key-value stores
- Skills_recommended: context-window-management, rag-implementation

## Scope

- Does_not_cover: Knowledge graph construction, Semantic search implementation, Database administration
- Boundaries: Focus is memory patterns for LLMs, Covers storage and retrieval strategies

## Ecosystem

### Primary_tools

- Mem0 - Memory layer for AI applications
- LangChain Memory - Memory utilities in LangChain
- Redis - In-memory data store for session memory

## Patterns

### Tiered Memory System

Different memory tiers for different purposes

**When to use**: Building any conversational AI

interface MemorySystem {
    // Buffer: Current conversation (in context)
    buffer: ConversationBuffer;

    // Short-term: Recent interactions (session)
    shortTerm: ShortTermMemory;

    // Long-term: Persistent across sessions
    longTerm: LongTermMemory;

    // Entity: Facts about people, places, things
    entity: EntityMemory;
}

class TieredMemory implements MemorySystem {
    async addMessage(message: Message): Promise<void> {
        // Always add to buffer
        this.buffer.add(message);

        // Extract entities
        const entities = await extractEntities(message);
        for (const entity of entities) {
            await this.entity.upsert(entity);
        }

        // Check for memorable content
        if (await isMemoryWorthy(message)) {
            await this.shortTerm.add({