---
name: aws-serverless
description: Specialized skill for building production-ready serverless
  applications on AWS. Covers Lambda functions, API Gateway, DynamoDB, SQS/SNS
  event-driven patterns, SAM/CDK deployment, and cold start optimization.
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# AWS Serverless

Specialized skill for building production-ready serverless applications on AWS.
Covers Lambda functions, API Gateway, DynamoDB, SQS/SNS event-driven patterns,
SAM/CDK deployment, and cold start optimization.

## Principles

- Right-size memory and timeout (measure before optimizing)
- Minimize cold starts for latency-sensitive workloads
- Use SnapStart for Java/.NET functions
- Prefer HTTP API over REST API for simple use cases
- Design for failure with DLQs and retries
- Keep deployment packages small
- Use environment variables for configuration
- Implement structured logging with correlation IDs

## Patterns

### Lambda Handler Pattern

Proper Lambda function structure with error handling

**When to use**: Any Lambda function implementation,API handlers, event processors, scheduled tasks

```javascript
// Node.js Lambda Handler
// handler.js

// Initialize outside handler (reused across invocations)
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

// Handler function
exports.handler = async (event, context) => {
  // Optional: Don't wait for event loop to clear (Node.js)
  context.callbackWaitsForEmptyEventLoop = false;

  try {
    // Parse input based on event source
    const body = typeof event.body === 'string'
      ? JSON.parse(event.body)
      : event.body;

    // Business logic
    const result = await processRequest(body);

    // Return API Gateway compatible response
    return {
      statusCode: 200,