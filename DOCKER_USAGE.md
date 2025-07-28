# Docker Usage for MCP Extended GitLab

## Important: MCP Servers and Docker

MCP (Model Context Protocol) servers communicate via **stdio** (standard input/output), which means:
- They cannot run as traditional web services
- Docker Compose is not suitable for running MCP servers
- The server must be launched by Claude, not independently

## Correct Usage

### 1. Build the Docker Image

```bash
docker build -t mcp-extended-gitlab:latest .
```

### 2. Add to Claude Desktop

Edit your Claude Desktop configuration file and add:

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITLAB_PRIVATE_TOKEN",
        "-e",
        "GITLAB_BASE_URL",
        "-e",
        "GITLAB_ENABLED_TOOLS",
        "mcp-extended-gitlab:latest"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4",
        "GITLAB_ENABLED_TOOLS": "core"
      }
    }
  }
}
```

### 3. Add to Claude Code CLI

```bash
claude mcp add gitlab-extended -- docker run -i --rm \
  -e GITLAB_PRIVATE_TOKEN \
  -e GITLAB_BASE_URL \
  -e GITLAB_ENABLED_TOOLS \
  mcp-extended-gitlab:latest

claude mcp update gitlab-extended -e GITLAB_PRIVATE_TOKEN=your_token
```

## Why `docker compose up` Doesn't Work

When you run `docker compose up`, the container starts and immediately exits because:

1. **No stdin connection**: The MCP server expects to communicate via stdin/stdout
2. **No MCP client**: Without Claude connecting to it, the server has nothing to do
3. **Immediate exit**: The server exits when there's no input stream

The warnings you see are cosmetic issues that don't affect functionality.

## Development and Testing

For development purposes, we provide `docker-compose.dev.yml`:

```bash
# Build and show setup instructions
docker compose -f docker-compose.dev.yml up --build

# Test the image interactively (Ctrl+C to exit)
docker run -it --rm \
  -e GITLAB_PRIVATE_TOKEN="test_token" \
  -e GITLAB_ENABLED_TOOLS="minimal" \
  mcp-extended-gitlab:latest
```

## Key Points

✅ **DO**: Use Docker to package the MCP server for Claude
✅ **DO**: Let Claude launch the Docker container
✅ **DO**: Use environment variables for configuration

❌ **DON'T**: Try to run the MCP server standalone
❌ **DON'T**: Use docker-compose for production
❌ **DON'T**: Expect the container to stay running on its own

## Architecture

```
Claude Desktop/Code → Docker → MCP Server
       ↑                           ↓
       └──────── stdio ────────────┘
```

Claude launches the Docker container and communicates with it via stdio pipes.