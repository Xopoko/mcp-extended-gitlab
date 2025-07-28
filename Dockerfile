FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir build && \
    pip install --no-cache-dir -e .

# Copy the application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 mcp && \
    chown -R mcp:mcp /app

USER mcp

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the MCP server in stdio mode for Claude integration
ENTRYPOINT ["python", "-m", "mcp_extended_gitlab.server"]