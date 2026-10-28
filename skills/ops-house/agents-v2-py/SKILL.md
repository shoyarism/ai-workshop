---
name: agents-v2-py
description: "Build container-based Foundry Agents with Azure AI Projects SDK (ImageBasedHostedAgentDefinition). Use when creating hosted agents with custom container images in Azure AI Foundry."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure AI Hosted Agents (Python)

Build container-based hosted agents using `ImageBasedHostedAgentDefinition` from the Azure AI Projects SDK.

## Installation

```bash
pip install azure-ai-projects>=2.0.0b3 azure-identity
```

**Minimum SDK Version:** `2.0.0b3` or later required for hosted agent support.

## Environment Variables

```bash
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
```

## Prerequisites

Before creating hosted agents:

1. **Container Image** - Build and push to Azure Container Registry (ACR)
2. **ACR Pull Permissions** - Grant your project's managed identity `AcrPull` role on the ACR
3. **Capability Host** - Account-level capability host with `enablePublicHostingEnvironment=true`
4. **SDK Version** - Ensure `azure-ai-projects>=2.0.0b3`

## Authentication

Always use `DefaultAzureCredential`:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

credential = DefaultAzureCredential()
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=credential
)
```

## Core Workflow

### 1. Imports

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)
```

### 2. Create Hosted Agent

```python
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

agent = client.agents.create_version(
    agent_name="my-hosted-agent",
    definition=ImageBasedHostedAgentDefinition(