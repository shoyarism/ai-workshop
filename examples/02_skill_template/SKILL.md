---
name: example-resilient-service
description: Reference implementation template demonstrating zero-slop structural invariants, strict error handling, and type-safe architecture for Workshop OS skills.
domain: software-engineering
subdomain: backend-architecture
tags:
  - tdd
  - clean-architecture
  - type-safety
  - error-boundaries
version: "1.0.0"
author: workshop-architect
license: Apache-2.0
---

# Example Resilient Service

## Overview
This skill provides an authoritative, zero-slop reference implementation for building backend services with deterministic error handling and strict boundary validation.

## Prerequisites
- Python 3.11+
- Virtual environment with strict typing enabled (`mypy`)

## Implementation Invariants
1. **Zero Bare Exceptions**: Every exception must be specifically typed and either handled with appropriate logging or explicitly re-raised.
2. **Complete Code Deliveries**: No `// TODO`, `/* implement later */`, or `# rest unchanged` placeholders.
3. **Deterministic Verification**: Every skill must provide concrete test assertions verifying both the positive execution path and error boundary conditions.

## Reference Code
```python
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    """Base exception for service domain failures."""
    pass

class ResourceNotFoundError(ServiceError):
    """Raised when the requested resource ID does not exist."""
    pass

@dataclass(frozen=True)
class ServicePayload:
    resource_id: str
    action: str
    metadata: Optional[dict[str, str]] = None

def execute_service_action(payload: ServicePayload) -> dict[str, str]:
    """Execute an action with explicit input validation and logging."""
    if not payload.resource_id:
        raise ValueError("resource_id cannot be empty")
    
    logger.info("Executing action '%s' for resource: %s", payload.action, payload.resource_id)
    return {"status": "success", "resource_id": payload.resource_id}
```

## Verification
```bash
python -m unittest tests/test_example_service.py
```
