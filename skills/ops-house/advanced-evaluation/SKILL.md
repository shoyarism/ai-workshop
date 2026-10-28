---
name: advanced-evaluation
description: This skill should be used when the user asks to "implement LLM-as-judge", "compare model outputs", "create evaluation rubrics", "mitigate evaluation bias", or mentions direct scoring, pairwise comparison, position bias, evaluation pipelines, or automated quality assessment.
risk: safe
source: community
date_added: 2026-03-18
---

# Advanced Evaluation

This skill covers production-grade techniques for evaluating LLM outputs using LLMs as judges. It synthesizes research from academic papers, industry practices, and practical implementation experience into actionable patterns for building reliable evaluation systems.

**Key insight**: LLM-as-a-Judge is not a single technique but a family of approaches, each suited to different evaluation contexts. Choosing the right approach and mitigating known biases is the core competency this skill develops.

## When to Use
Activate this skill when:

- Building automated evaluation pipelines for LLM outputs
- Comparing multiple model responses to select the best one
- Establishing consistent quality standards across evaluation teams
- Debugging evaluation systems that show inconsistent results
- Designing A/B tests for prompt or model changes
- Creating rubrics for human or automated evaluation
- Analyzing correlation between automated and human judgments

## Core Concepts

### The Evaluation Taxonomy

Evaluation approaches fall into two primary categories with distinct reliability profiles:

**Direct Scoring**: A single LLM rates one response on a defined scale.
- Best for: Objective criteria (factual accuracy, instruction following, toxicity)
- Reliability: Moderate to high for well-defined criteria
- Failure mode: Score calibration drift, inconsistent scale interpretation

**Pairwise Comparison**: An LLM compares two responses and selects the better one.
- Best for: Subjective preferences (tone, style, persuasiveness)
- Reliability: Higher than direct scoring for preferences