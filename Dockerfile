# ==============================================================================
# WORKSHOP OS: Universal Agent Sandboxed Runtime Container
# ==============================================================================
FROM python:3.12-slim

# Prevent interactive prompts and Python output buffering
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install essential runtime tools (git, curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy packaging configuration first for layer caching
COPY pyproject.toml /app/

# Install build backend and package dependencies
RUN pip install --no-cache-dir hatchling uv && \
    pip install --no-cache-dir pyyaml pydantic requests ruff pytest

# Copy full application tree
COPY . /app/

# Install workshop console entrypoint
RUN pip install --no-cache-dir -e .

# Expose standard Workshop gateway ports
EXPOSE 7860 7861 7862

# Default execution: run comprehensive health diagnostics
CMD ["workshop", "doctor"]
