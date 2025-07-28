# Claude Desktop Quick Start Guide

This guide helps you set up MCP Extended GitLab with Claude Desktop in just a few minutes.

## Prerequisites

- Docker Desktop installed and running
- Claude Desktop installed
- GitLab account with API access

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your GitLab Token

1. Go to GitLab → Settings → Access Tokens
2. Create a token with `api` scope
3. Copy the token (starts with `glpat-`)

### Step 2: Build Docker Image

```bash
cd /path/to/mcp-extended-gitlab
docker build -t mcp-extended-gitlab:latest .
```

### Step 3: Configure Claude Desktop

#### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITLAB_PRIVATE_TOKEN=glpat-YOUR_TOKEN_HERE",
        "mcp-extended-gitlab:latest"
      ]
    }
  }
}
```

#### macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITLAB_PRIVATE_TOKEN=glpat-YOUR_TOKEN_HERE",
        "mcp-extended-gitlab:latest"
      ]
    }
  }
}
```

### Step 4: Restart Claude

1. Completely quit Claude Desktop
2. Start Claude Desktop again
3. Look for the 🔌 icon showing MCP is connected

### Step 5: Test It!

Try these commands in Claude:
- "List my GitLab projects"
- "Show my recent merge requests"
- "What issues are assigned to me?"

## 🛠️ Advanced Configuration

### Using Environment Variables

Instead of hardcoding your token:

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITLAB_PRIVATE_TOKEN",
        "-e", "GITLAB_BASE_URL",
        "mcp-extended-gitlab:latest"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "glpat-YOUR_TOKEN_HERE",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

### Tool Filtering

To reduce Claude's context usage, enable only specific tools:

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITLAB_PRIVATE_TOKEN",
        "-e", "GITLAB_ENABLED_TOOLS=minimal",
        "mcp-extended-gitlab:latest"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "glpat-YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Tool presets:
- `minimal` - Essential tools only (~15 tools)
- `core` - Core features (~100 tools)
- `ci_cd` - CI/CD tools (~50 tools)
- `devops` - DevOps tools (~40 tools)
- `admin` - Admin tools (~20 tools)

### Self-Hosted GitLab

For self-hosted GitLab instances:

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITLAB_PRIVATE_TOKEN",
        "-e", "GITLAB_BASE_URL=https://gitlab.company.com/api/v4",
        "mcp-extended-gitlab:latest"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "glpat-YOUR_TOKEN_HERE"
      }
    }
  }
}
```

## 🔧 Troubleshooting

### "MCP server gitlab-extended is not responsive"

1. **Check Docker is running**: Open Docker Desktop
2. **Verify the image exists**: `docker images | grep mcp-extended-gitlab`
3. **Test manually**: 
   ```bash
   docker run --rm -e GITLAB_PRIVATE_TOKEN="your_token" mcp-extended-gitlab:latest
   ```

### "Authentication error"

1. **Verify your token**: Ensure it starts with `glpat-`
2. **Check token permissions**: Must have `api` scope
3. **Test token**:
   ```bash
   curl -H "PRIVATE-TOKEN: your_token" https://gitlab.com/api/v4/user
   ```

### Tools not appearing

1. **Restart Claude completely**: Quit and restart, don't just close the window
2. **Check the 🔌 icon**: Should show "1 MCP server connected"
3. **Try a simple command**: "What GitLab tools are available?"

## 📖 Next Steps

- See [Testing Tools Guide](../guides/TESTING_TOOLS.md) to test all features
- Check [Tool Names](../api/TOOL_NAMES.md) for the complete tool list
- Read [Docker Usage](./DOCKER_USAGE.md) for advanced Docker configuration

## 🆘 Need Help?

- Check the [Installation Guide](./INSTALLATION.md) for detailed instructions
- See [MCP Client Setup](./MCP_CLIENT_SETUP.md) for other MCP clients
- Review [Docker Setup](./DOCKER_SETUP.md) for Docker-specific issues