# Install MCP Extended GitLab Server in Claude Applications

This guide covers installation of the MCP Extended GitLab server for Claude Code CLI, Claude Desktop, and Claude Web applications.

## Claude Web (claude.ai)

Claude Web supports remote MCP servers through the Integrations built-in feature.

### Prerequisites

1. Claude Pro, Team, or Enterprise account (Integrations not available on free plan)
2. [GitLab Personal Access Token](https://gitlab.com/-/user_settings/personal_access_tokens)

### Installation

**Note**: As of January 2025, Claude Web primarily supports official remote MCP servers from providers like Atlassian, Zapier, and Notion. For self-hosted MCP servers like MCP Extended GitLab, we recommend using Claude Desktop or Claude Code CLI for the best experience.

**Alternative**: Use Claude Desktop or Claude Code CLI for reliable MCP Extended GitLab integration.

---

## Claude Code CLI

Claude Code CLI provides command-line access to Claude with MCP server integration.

### Prerequisites

1. Claude Code CLI installed
2. [GitLab Personal Access Token](https://gitlab.com/-/user_settings/personal_access_tokens)
3. [Docker](https://www.docker.com/) installed and running

### Installation

Run the following command to add the MCP Extended GitLab server using Docker:

```bash
# Simple one-liner installation (recommended)
claude mcp add gitlab-extended -- docker run -i --rm -e GITLAB_PRIVATE_TOKEN ghcr.io/yourusername/mcp-extended-gitlab
```

Then set your GitLab token:
```bash
claude mcp update gitlab-extended -e GITLAB_PRIVATE_TOKEN=your_gitlab_token
```

For self-hosted GitLab instances, also add the base URL:
```bash
claude mcp update gitlab-extended -e GITLAB_PRIVATE_TOKEN=your_gitlab_token -e GITLAB_BASE_URL=https://gitlab.example.com/api/v4
```

### Tool Filtering (Reducing Context Usage)

The MCP Extended GitLab server supports tool filtering to reduce context usage. This is especially useful since the server provides 478+ tools.

#### Using Presets

```bash
# Use minimal preset (essential tools only)
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS=minimal

# Use core preset (all core GitLab features)
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS=core

# Use CI/CD preset (pipeline and job management)
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS=ci_cd

# Use DevOps preset (environments, deployments, feature flags)
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS=devops

# Use admin preset (administrative tools)
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS=admin
```

#### Using Custom Tool Lists

```bash
# Enable specific tools by name (comma-separated)
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS="list_projects,get_project,list_issues,create_issue"

# Or use JSON array format
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS='["list_projects","get_project","list_issues","create_issue"]'
```

### For Development/Local Build

If you're building the Docker image locally:

```bash
# Build the image first
cd mcp-extended-gitlab
docker build -t mcp-extended-gitlab:local .

# Add to Claude Code
claude mcp add-json gitlab-extended '{"command": "docker", "args": ["run", "-i", "--rm", "-e", "GITLAB_PRIVATE_TOKEN", "-e", "GITLAB_BASE_URL", "-p", "8000:8000", "mcp-extended-gitlab:local"], "env": {"GITLAB_PRIVATE_TOKEN": "your_gitlab_token", "GITLAB_BASE_URL": "https://gitlab.com/api/v4"}}'
```

### Configuration Options

- Use `-s user` to add the server to your user configuration (available across all projects)
- Use `-s project` to add the server to project-specific configuration (shared via `.mcp.json`)
- Default scope is `local` (available only to you in the current project)

### For Self-Hosted GitLab

Add the GitLab URL to the environment:
```bash
claude mcp update gitlab-extended -e GITLAB_BASE_URL=https://gitlab.example.com/api/v4
```

### Verification

Run the following command to verify the installation:
```bash
claude mcp list
```

Use the `/mcp` command within Claude Code to check the available tools:
```
/mcp gitlab-extended
```

---

## Claude Desktop

Claude Desktop provides a graphical interface for interacting with the MCP Extended GitLab Server.

### Prerequisites

1. Claude Desktop installed
2. [GitLab Personal Access Token](https://gitlab.com/-/user_settings/personal_access_tokens)
3. [Docker](https://www.docker.com/) installed and running

### Configuration File Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json` (unofficial support)

### Installation

Add the following to your `claude_desktop_config.json`:

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
        "ghcr.io/yourusername/mcp-extended-gitlab"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

### Tool Filtering (Reducing Context Usage)

To reduce Claude's context usage, you can enable only specific tools:

#### Using Presets

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
        "ghcr.io/yourusername/mcp-extended-gitlab"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4",
        "GITLAB_ENABLED_TOOLS": "minimal"  // Options: minimal, core, ci_cd, devops, admin
      }
    }
  }
}
```

#### Using Custom Tool Lists

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
        "ghcr.io/yourusername/mcp-extended-gitlab"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4",
        "GITLAB_ENABLED_TOOLS": "list_projects,get_project,list_issues,create_issue"
      }
    }
  }
}
```

### For Local Development Build

If you're using a locally built image:

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
        "mcp-extended-gitlab:local"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

### Using Environment Variables

Claude Desktop supports environment variable references. You can use:

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
        "ghcr.io/yourusername/mcp-extended-gitlab"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "$GITLAB_TOKEN",
        "GITLAB_BASE_URL": "$GITLAB_URL"
      }
    }
  }
}
```

Then set the environment variables in your system before starting Claude Desktop.

### Installation Steps

1. Open Claude Desktop
2. Go to Settings (from the Claude menu) → Developer → Edit Config
3. Add your chosen configuration
4. Save the file
5. Restart Claude Desktop

### Verification

After restarting, you should see:
- An MCP icon in the Claude Desktop interface
- The GitLab Extended server listed as "running" in Developer settings
- Access to 478+ GitLab tools when chatting with Claude

---

## Direct Python Installation (Alternative)

If you prefer not to use Docker, you can run the server directly with Python:

### Claude Code CLI

```bash
# Install the package
pip install mcp-extended-gitlab

# Add to Claude Code
claude mcp add gitlab-extended -- python -m mcp_extended_gitlab.server
claude mcp update gitlab-extended -e GITLAB_PRIVATE_TOKEN=your_gitlab_token
```

### Claude Desktop

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "python",
      "args": ["-m", "mcp_extended_gitlab.server"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

---

## Troubleshooting

### Claude Web
- Self-hosted MCP servers are not directly supported
- Use Claude Desktop or Claude Code CLI for MCP Extended GitLab
- Consider deploying as a remote MCP server with proper authentication

### Claude Code CLI
- Verify Docker is running: `docker --version`
- Check if port 8000 is available: `lsof -i :8000`
- Use `/mcp` command within Claude Code to check server status
- Check logs: `claude mcp logs gitlab-extended`

### Claude Desktop
- Check logs at:
  - **macOS**: `~/Library/Logs/Claude/`
  - **Windows**: `%APPDATA%\Claude\logs\`
- Look for `mcp-server-gitlab-extended.log` for server-specific errors
- Ensure configuration file is valid JSON
- Try running the Docker command manually in terminal to diagnose issues

### Common Issues

#### Invalid JSON
Validate your configuration at [jsonlint.com](https://jsonlint.com)

#### Token Issues
Ensure your GitLab Personal Access Token has required scopes:
- `api` - Full API access (recommended)
- `read_api` - Read-only API access (minimum)

#### Docker Not Found
Install Docker Desktop and ensure it's running

#### Port Already in Use
Check if port 8000 is already occupied:
```bash
# macOS/Linux
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

#### Connection to Self-Hosted GitLab
- Ensure the GitLab instance is accessible from Docker
- Check SSL certificates (may need `--insecure` flag for self-signed certs)
- Verify network connectivity from within Docker

---

## Security Best Practices

- **Protect configuration files**: Set appropriate file permissions
  ```bash
  # macOS/Linux
  chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json
  ```
- **Use environment variables** when possible instead of hardcoding tokens
- **Limit token scope** to only necessary permissions
- **Regularly rotate** your GitLab Personal Access Tokens
- **Never commit** configuration files containing tokens to version control
- **Use `.env` files** for local development with proper `.gitignore` entries

---

## Available Tools

Once installed, you'll have access to 478+ GitLab tools organized into categories:

### Core Features (120+ tools)
- Projects, Groups, Users
- Issues, Merge Requests
- Commits, Repository operations
- Releases, Milestones, Labels

### CI/CD (40+ tools)
- Pipelines, Jobs, Runners
- Variables, Lint validation

### DevOps (30+ tools)
- Environments, Deployments
- Feature Flags, Dependency Proxy

### Security (25+ tools)
- Protected Branches, Deploy Keys
- Access Tokens, SSH Keys

### And many more...

Use the `/mcp` command in Claude Code or check the MCP icon in Claude Desktop to explore all available tools.

## Tool Presets

To optimize context usage, the following presets are available:

### Minimal Preset
Essential operations only (~15 tools):
- `list_projects`, `get_project`, `create_project`
- `list_issues`, `get_issue`, `create_issue`, `update_issue`
- `list_merge_requests`, `get_merge_request`, `create_merge_request`
- `get_current_user`, `list_users`
- `search_globally`

### Core Preset
All core GitLab features (~80 tools):
- All project management tools
- Complete issue and merge request operations
- Repository browsing and commit tools
- User and group management
- Search functionality

### CI/CD Preset
Continuous integration and deployment (~40 tools):
- Pipeline management
- Job control and monitoring
- Runner configuration
- CI/CD variables
- YAML validation

### DevOps Preset
Deployment and operations (~35 tools):
- Environment management
- Deployment tracking
- Feature flags
- Package registry

### Admin Preset
Administrative functions (~25 tools):
- License management
- System hooks
- Admin variables
- Flipper features

---

## Additional Resources

- [MCP Extended GitLab Repository](https://github.com/yourusername/mcp-extended-gitlab)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Claude Code MCP Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [Docker Installation Guide](https://docs.docker.com/get-docker/)