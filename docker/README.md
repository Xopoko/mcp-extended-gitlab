# MCP Extended GitLab Docker Image

Official Docker image for the MCP Extended GitLab server, providing 478+ GitLab API tools through the Model Context Protocol.

## Quick Start

### With Claude Code CLI

```bash
# Add the MCP server
claude mcp add gitlab-extended -- docker run -i --rm -e GITLAB_PRIVATE_TOKEN ghcr.io/yourusername/mcp-extended-gitlab

# Configure your GitLab token
claude mcp update gitlab-extended -e GITLAB_PRIVATE_TOKEN=your_token_here
```

### With Claude Desktop

Add to your `claude_desktop_config.json`:

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
        "ghcr.io/yourusername/mcp-extended-gitlab"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token"
      }
    }
  }
}
```

## Environment Variables

- `GITLAB_PRIVATE_TOKEN` (required): Your GitLab Personal Access Token
- `GITLAB_BASE_URL` (optional): GitLab API URL (default: `https://gitlab.com/api/v4`)

## Self-Hosted GitLab

For self-hosted GitLab instances:

```bash
claude mcp update gitlab-extended \
  -e GITLAB_PRIVATE_TOKEN=your_token \
  -e GITLAB_BASE_URL=https://gitlab.example.com/api/v4
```

## Available Tags

- `latest`: Latest stable release
- `v1.0.0`, `v1.0`, `v1`: Semantic versioning
- `main`: Latest development build

## Features

- 478+ GitLab API tools
- Full async support
- Type-safe with Pydantic
- Supports all GitLab editions
- Works with self-hosted instances

## Documentation

- [GitHub Repository](https://github.com/yourusername/mcp-extended-gitlab)
- [Installation Guide](https://github.com/yourusername/mcp-extended-gitlab/blob/main/INSTALLATION.md)
- [API Documentation](https://github.com/yourusername/mcp-extended-gitlab/blob/main/README.md)

## License

MIT License - see [LICENSE](https://github.com/yourusername/mcp-extended-gitlab/blob/main/LICENSE) for details.