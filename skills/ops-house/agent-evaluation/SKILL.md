---
name: agent-evaluation
description: Testing and benchmarking LLM agents including behavioral testing,
  capability assessment, reliability metrics, and production monitoring—where
  even top agents achieve less than 50% on real-world benchmarks
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Agent Evaluation

Testing and benchmarking LLM agents including behavioral testing, capability assessment, reliability metrics, and production monitoring—where even top agents achieve less than 50% on real-world benchmarks

## Capabilities

- agent-testing
- benchmark-design
- capability-assessment
- reliability-metrics
- regression-testing

## Prerequisites

- Knowledge: Testing methodologies, Statistical analysis basics, LLM behavior patterns
- Skills_recommended: autonomous-agents, multi-agent-orchestration
- Required skills: testing-fundamentals, llm-fundamentals

## Scope

- Does_not_cover: Model training evaluation (loss, perplexity), Fairness and bias testing, User experience testing
- Boundaries: Focus is agent capability and reliability, Covers functional and behavioral testing

## Ecosystem

### Primary_tools

- AgentBench - Multi-environment benchmark for LLM agents (ICLR 2024)
- τ-bench (Tau-bench) - Sierra's real-world agent benchmark
- ToolEmu - Risky behavior detection for agent tool use
- Langsmith - LLM tracing and evaluation platform

### Alternatives

- Braintrust - When: Need production monitoring integration LLM evaluation and monitoring
- PromptFoo - When: Focus on prompt-level evaluation Prompt testing framework

### Deprecated

- Manual testing only

## Patterns

### Statistical Test Evaluation

Run tests multiple times and analyze result distributions

**When to use**: Evaluating stochastic agent behavior

interface TestResult {
    testId: string;
    runId: string;
    passed: boolean;
    score: number;  // 0-1 for partial credit
    latencyMs: number;
    tokensUsed: number;
    output: string;