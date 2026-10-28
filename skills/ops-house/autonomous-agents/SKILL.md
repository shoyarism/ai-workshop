---
name: autonomous-agents
description: Autonomous agents are AI systems that can independently decompose
  goals, plan actions, execute tools, and self-correct without constant human
  guidance. The challenge isn't making them capable - it's making them reliable.
  Every extra decision multiplies failure probability.
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Autonomous Agents

Autonomous agents are AI systems that can independently decompose goals,
plan actions, execute tools, and self-correct without constant human guidance.
The challenge isn't making them capable - it's making them reliable. Every
extra decision multiplies failure probability.

This skill covers agent loops (ReAct, Plan-Execute), goal decomposition,
reflection patterns, and production reliability. Key insight: compounding
error rates kill autonomous agents. A 95% success rate per step drops to
60% by step 10. Build for reliability first, autonomy second.

2025 lesson: The winners are constrained, domain-specific agents with clear
boundaries, not "autonomous everything." Treat AI outputs as proposals,
not truth.

## Principles

- Reliability over autonomy - every step compounds error probability
- Constrain scope - domain-specific beats general-purpose
- Treat outputs as proposals, not truth
- Build guardrails before expanding capabilities
- Human-in-the-loop for critical decisions is non-negotiable
- Log everything - every action must be auditable
- Fail safely with rollback, not silently with corruption

## Capabilities

- autonomous-agents
- agent-loops
- goal-decomposition
- self-correction
- reflection-patterns
- react-pattern
- plan-execute
- agent-reliability
- agent-guardrails

## Scope

- multi-agent-systems → multi-agent-orchestration
- tool-building → agent-tool-builder
- memory-systems → agent-memory-systems
- workflow-orchestration → workflow-automation

## Tooling

### Frameworks