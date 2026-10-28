---
name: sql-optimization
description: Use when debugging slow SQL queries, designing database indexes, or rewriting queries for better performance. For EXPLAIN analysis, index strategy, N+1 problem resolution, and query optimization patterns.
---

# SQL Optimization

Master SQL query performance through systematic analysis, strategic indexing, and proven optimization patterns.

## Overview

This skill helps you diagnose and fix slow database queries:
1. **Diagnose**: Identify bottlenecks with EXPLAIN analysis
2. **Optimize**: Design effective indexes and rewrite inefficient queries
3. **Validate**: Measure improvements and monitor performance

## Core Methodology

### Step 1: Analyze with EXPLAIN
Run EXPLAIN ANALYZE to see execution plan and actual timings.

### Step 2: Identify Bottlenecks
- Seq Scan = Missing index
- High rows removed = Non-selective filter
- Nested Loop on large tables = Inefficient join

### Step 3: Apply Patterns
- Index Strategies: composite, partial, covering, expression
- Query Rewrites: subquery→JOIN, IN→EXISTS, keyset pagination