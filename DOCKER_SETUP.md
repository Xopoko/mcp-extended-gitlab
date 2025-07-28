# Docker Setup for MCP Extended GitLab

This guide explains how to run the MCP Extended GitLab server using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for using docker-compose.yml)
- GitLab Personal Access Token

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/your-repo/mcp-extended-gitlab.git
cd mcp-extended-gitlab
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Edit the `.env` file and add your GitLab Personal Access Token:
```bash
GITLAB_BASE_URL=https://gitlab.com/api/v4
GITLAB_PRIVATE_TOKEN=your-actual-token-here
```

4. Start the MCP server:
```bash
docker-compose up -d
```

The MCP server will be available at `http://localhost:8000`.

### Using Docker CLI

1. Build the Docker image:
```bash
docker build -t mcp-extended-gitlab .
```

2. Run the container:
```bash
docker run -d \
  --name mcp-gitlab \
  -p 8000:8000 \
  -e GITLAB_BASE_URL=https://gitlab.com/api/v4 \
  -e GITLAB_PRIVATE_TOKEN=your-token-here \
  mcp-extended-gitlab
```

## Configuration

### Environment Variables

- `GITLAB_BASE_URL`: The GitLab API URL (default: `https://gitlab.com/api/v4`)
- `GITLAB_PRIVATE_TOKEN`: Your GitLab Personal Access Token (required)

### Custom GitLab Instance

If you're using a self-hosted GitLab instance, update the `GITLAB_BASE_URL`:

```bash
GITLAB_BASE_URL=https://gitlab.example.com/api/v4
```

### Using with Proxy (Optional)

To use the included Nginx proxy configuration:

```bash
docker-compose --profile with-proxy up -d
```

This will start both the MCP server and an Nginx reverse proxy.

## Managing the Container

### View logs:
```bash
docker-compose logs -f mcp-gitlab
# or
docker logs -f mcp-gitlab
```

### Stop the server:
```bash
docker-compose down
# or
docker stop mcp-gitlab
```

### Restart the server:
```bash
docker-compose restart
# or
docker restart mcp-gitlab
```

### Update the image:
```bash
docker-compose pull
docker-compose up -d
# or
docker pull mcp-extended-gitlab:latest
docker stop mcp-gitlab
docker rm mcp-gitlab
docker run -d ... (with your parameters)
```

## Health Check

The container includes a health check that verifies the MCP server is running. You can check the health status:

```bash
docker inspect mcp-gitlab --format='{{.State.Health.Status}}'
```

## Volumes

The docker-compose.yml mounts the `.env` file as read-only. You can add additional volume mounts if needed:

```yaml
volumes:
  - ./custom-config:/app/config:ro
  - ./logs:/app/logs
```

## Troubleshooting

### Container won't start

1. Check if the port 8000 is already in use:
```bash
sudo lsof -i :8000
```

2. Check container logs:
```bash
docker logs mcp-gitlab
```

### Authentication errors

Ensure your GitLab Personal Access Token has the necessary scopes:
- `api` - Full API access
- `read_api` - Read-only API access (minimum required)

### Connection issues

If using a self-hosted GitLab:
1. Ensure the GitLab instance is accessible from the Docker container
2. Check if SSL certificates are valid
3. You might need to add custom CA certificates to the container

## Security Considerations

1. Never commit your `.env` file with real tokens
2. Use Docker secrets for production deployments
3. Consider using a reverse proxy with SSL for production
4. Regularly update the Docker image for security patches

## Building for Different Architectures

To build for ARM64 (e.g., Apple Silicon):

```bash
docker buildx build --platform linux/arm64 -t mcp-extended-gitlab:arm64 .
```

## Integration with MCP Clients

Once the server is running, you can connect any MCP-compatible client to `http://localhost:8000`. Refer to the main documentation for client setup instructions.