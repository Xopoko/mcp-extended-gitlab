# MCP Extended GitLab - Client Setup Guide

This guide provides comprehensive instructions for integrating the MCP Extended GitLab server with various AI coding assistants and development tools.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Client Configuration](#client-configuration)
  - [Claude Desktop](#claude-desktop)
  - [Claude Code](#claude-code)
  - [Cursor](#cursor)
  - [VS Code with Continue](#vs-code-with-continue)
  - [Windsurf](#windsurf)
  - [Cline (Claude Dev)](#cline-claude-dev)
  - [Other MCP Clients](#other-mcp-clients)
- [Environment Variables](#environment-variables)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

1. **Python 3.11 or higher** installed
2. **GitLab Account** with:
   - Personal Access Token (with `api` scope)
   - GitLab instance URL (default: https://gitlab.com)
3. **Git** installed on your system

## Installation

### Option 1: Install from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/Xopoko/mcp-extended-gitlab.git
cd mcp-extended-gitlab

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package
pip install -e .
```

### Option 2: Install with pipx (System-wide)

```bash
# Install pipx if not already installed
python -m pip install --user pipx
python -m pipx ensurepath

# Install MCP Extended GitLab
pipx install git+https://github.com/Xopoko/mcp-extended-gitlab.git
```

### Option 3: Install with uv (Fast Python package installer)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install MCP Extended GitLab
uv tool install git+https://github.com/Xopoko/mcp-extended-gitlab.git
```

## Client Configuration

### Claude Desktop

Claude Desktop supports MCP servers through configuration files.

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "python",
      "args": ["-m", "mcp_extended_gitlab"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

If installed with pipx or uv:
```json
{
  "mcpServers": {
    "gitlab": {
      "command": "mcp-extended-gitlab",
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

### Claude Code

Claude Code uses the same configuration format as Claude Desktop.

**Location**: `~/.claudecode/settings.json`

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "python",
      "args": ["-m", "mcp_extended_gitlab"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

### Cursor

Cursor supports MCP through its settings file.

1. Open Cursor Settings (`Cmd/Ctrl + ,`)
2. Search for "MCP" or "Model Context Protocol"
3. Add server configuration:

```json
{
  "mcp.servers": {
    "gitlab": {
      "command": "python",
      "args": ["-m", "mcp_extended_gitlab"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

### VS Code with Continue

Continue extension for VS Code supports MCP servers.

1. Install Continue extension from VS Code marketplace
2. Open Continue settings: `~/.continue/config.json`
3. Add MCP server configuration:

```json
{
  "models": [...],
  "mcpServers": [
    {
      "name": "gitlab",
      "command": "python",
      "args": ["-m", "mcp_extended_gitlab"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  ]
}
```

### Windsurf

Windsurf IDE supports MCP servers through its configuration.

**Location**: `~/.windsurf/settings.json`

```json
{
  "mcp": {
    "servers": {
      "gitlab": {
        "command": "python",
        "args": ["-m", "mcp_extended_gitlab"],
        "env": {
          "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
          "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
        }
      }
    }
  }
}
```

### Cline (Claude Dev)

Cline is a VS Code extension that supports MCP.

1. Install Cline from VS Code marketplace
2. Open VS Code settings (`Cmd/Ctrl + ,`)
3. Search for "Cline MCP"
4. Add server configuration in settings.json:

```json
{
  "cline.mcpServers": {
    "gitlab": {
      "command": "python",
      "args": ["-m", "mcp_extended_gitlab"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

### Other MCP Clients

For any MCP-compatible client, use these standard settings:

```json
{
  "command": "python",
  "args": ["-m", "mcp_extended_gitlab"],
  "env": {
    "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
    "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
  }
}
```

Or if installed globally:
```json
{
  "command": "mcp-extended-gitlab",
  "env": {
    "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
    "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
  }
}
```

## Environment Variables

The MCP server supports the following environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GITLAB_PRIVATE_TOKEN` | GitLab Personal Access Token | Yes | None |
| `GITLAB_BASE_URL` | GitLab API base URL | No | `https://gitlab.com/api/v4` |
| `MCP_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No | INFO |

### Creating a GitLab Personal Access Token

1. Go to GitLab → User Settings → Access Tokens
2. Create a new token with:
   - Name: `MCP Extended GitLab`
   - Expiration: Set as needed
   - Scopes: Select `api` (full API access)
3. Copy the token immediately (it won't be shown again)

## Verification

After configuration, verify the setup:

### In Claude Desktop/Claude Code:
1. Restart the application
2. Type: "What GitLab tools are available?"
3. The assistant should list available GitLab operations

### In VS Code extensions:
1. Reload VS Code window
2. Check extension logs for MCP server connection
3. Try using GitLab-related commands

### Manual Testing:
```bash
# Test the server directly
python -m mcp_extended_gitlab --help

# Run in development mode
GITLAB_PRIVATE_TOKEN=your-token python -m mcp_extended_gitlab
```

## Troubleshooting

### Common Issues

1. **"MCP server not found"**
   - Ensure Python is in your PATH
   - Verify installation with `pip show mcp-extended-gitlab`
   - Check file paths in configuration

2. **"Authentication failed"**
   - Verify your GitLab token has `api` scope
   - Check token hasn't expired
   - Ensure token is correctly set in environment

3. **"Connection refused"**
   - Check GitLab instance URL
   - Verify network connectivity
   - Check for proxy/firewall issues

4. **"Module not found"**
   - Ensure virtual environment is activated
   - Reinstall with `pip install -e .`
   - Check Python version (3.11+)

### Debug Mode

Enable debug logging by setting:
```json
{
  "env": {
    "MCP_LOG_LEVEL": "DEBUG",
    "GITLAB_PRIVATE_TOKEN": "your-token",
    "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
  }
}
```

### Log Locations

- **Claude Desktop**: `~/Library/Logs/Claude/` (macOS), `%APPDATA%\Claude\logs\` (Windows)
- **VS Code**: Output panel → Select "MCP" or extension name
- **Manual**: Check terminal output when running directly

## Security Best Practices

1. **Never commit tokens**: Keep your GitLab token out of version control
2. **Use environment files**: Store tokens in `.env` files (git-ignored)
3. **Limit token scope**: Create tokens with minimum required permissions
4. **Rotate tokens**: Regularly update your access tokens
5. **Use secure storage**: Consider using system keychains/credential managers

## Support

- **Issues**: https://github.com/Xopoko/mcp-extended-gitlab/issues
- **Documentation**: Check the README.md for API usage
- **GitLab API Reference**: https://docs.gitlab.com/ee/api/

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)