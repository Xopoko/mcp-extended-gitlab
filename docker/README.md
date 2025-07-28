# Docker Configuration

This directory contains Docker-related files for building and running MCP Extended GitLab.

## Files

- **Dockerfile.simple** - Simplified Dockerfile for basic deployments
- **docker-entrypoint.sh** - Entrypoint script for the Docker container
- **docker-compose.dev.yml** - Development Docker Compose configuration

## Usage

### Building the Docker Image

From the project root:

```bash
# Using the main Dockerfile
docker build -t mcp-extended-gitlab .

# Using the simple Dockerfile
docker build -f docker/Dockerfile.simple -t mcp-extended-gitlab:simple .
```

### Running with Docker Compose

For development:

```bash
docker-compose -f docker/docker-compose.dev.yml up
```

For production (using root docker-compose.yml):

```bash
docker-compose up -d
```

See [Docker Setup Guide](../docs/setup/DOCKER_SETUP.md) for detailed instructions.