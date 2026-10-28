---
name: bullmq-specialist
description: BullMQ expert for Redis-backed job queues, background processing,
  and reliable async execution in Node.js/TypeScript applications.
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# BullMQ Specialist

BullMQ expert for Redis-backed job queues, background processing, and
reliable async execution in Node.js/TypeScript applications.

## Principles

- Jobs are fire-and-forget from the producer side - let the queue handle delivery
- Always set explicit job options - defaults rarely match your use case
- Idempotency is your responsibility - jobs may run more than once
- Backoff strategies prevent thundering herds - exponential beats linear
- Dead letter queues are not optional - failed jobs need a home
- Concurrency limits protect downstream services - start conservative
- Job data should be small - pass IDs, not payloads
- Graceful shutdown prevents orphaned jobs - handle SIGTERM properly

## Capabilities

- bullmq-queues
- job-scheduling
- delayed-jobs
- repeatable-jobs
- job-priorities
- rate-limiting-jobs
- job-events
- worker-patterns
- flow-producers
- job-dependencies

## Scope

- redis-infrastructure -> redis-specialist
- serverless-queues -> upstash-qstash
- workflow-orchestration -> temporal-craftsman
- event-sourcing -> event-architect
- email-delivery -> email-systems

## Tooling

### Core

- bullmq
- ioredis

### Hosting

- upstash
- redis-cloud
- elasticache
- railway

### Monitoring

- bull-board
- arena
- bullmq-pro

### Patterns

- delayed-jobs
- repeatable-jobs
- job-flows
- rate-limiting
- sandboxed-processors

## Patterns

### Basic Queue Setup

Production-ready BullMQ queue with proper configuration

**When to use**: Starting any new queue implementation

import { Queue, Worker, QueueEvents } from 'bullmq';
import IORedis from 'ioredis';

// Shared connection for all queues
const connection = new IORedis(process.env.REDIS_URL, {