# MCP Extended GitLab - Client Setup Guide

This guide provides comprehensive instructions for integrating the MCP Extended GitLab server with various AI coding assistants and development tools.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Client Configuration](#client-configuration)
  - [Claude Desktop](#claude-desktop)
  - [Claude Code](#claude-code)
  - [Cursor](#cursor)
  - [VS Code](#vs-code)
  - [Windsurf](#windsurf)
  - [Cline](#cline)
  - [Zed](#zed)
  - [Other Clients](#other-clients)
- [Environment Variables](#environment-variables)
- [Available Tools](#available-tools)
- [Usage Examples](#usage-examples)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)
- [Support](#support)
- [Additional Resources](#additional-resources)

## Prerequisites

1. **Python 3.11 or higher** installed
2. **GitLab Account** with:
   - Personal Access Token (with `api` scope)
   - GitLab instance URL (default: https://gitlab.com)
3. **Git** installed on your system

## Installation

### Option 1: Install from GitHub (Development)

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

### Option 2: Install with pipx (Recommended for global use)

```bash
# Install pipx if not already installed
python -m pip install --user pipx
python -m pipx ensurepath

# Install MCP Extended GitLab
pipx install git+https://github.com/Xopoko/mcp-extended-gitlab.git
```

### Option 3: Install with uv

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install MCP Extended GitLab
uv tool install git+https://github.com/Xopoko/mcp-extended-gitlab.git
```

### Option 4: Direct pip install

```bash
pip install git+https://github.com/Xopoko/mcp-extended-gitlab.git
```

## Client Configuration

### Claude Desktop

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

**Config file location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

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

### Claude Code

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```bash
claude mcp add gitlab -- python -m mcp_extended_gitlab
```

Then set your environment variables:
```bash
claude mcp set-env gitlab GITLAB_PRIVATE_TOKEN=your-gitlab-token-here
claude mcp set-env gitlab GITLAB_BASE_URL=https://gitlab.com/api/v4
```

### Cursor

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

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

### VS Code

Add this to your VS Code settings. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

```json
{
  "mcp": {
    "servers": {
      "gitlab": {
        "type": "stdio",
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

### Windsurf

Add this to your Windsurf MCP config file. See [Windsurf MCP docs](https://docs.windsurf.com/windsurf/mcp) for more info.

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

### Cline

You can install MCP Extended GitLab through the Cline MCP Server Marketplace or manually:

#### Option 1: Manual installation
1. Open Cline
2. Click the hamburger menu icon (☰) to enter the MCP Servers section
3. Add the following configuration:

```json
{
  "gitlab": {
    "command": "python",
    "args": ["-m", "mcp_extended_gitlab"],
    "env": {
      "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
      "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
    }
  }
}
```

### Zed

Add this to your Zed `settings.json`. See [Zed Context Server docs](https://zed.dev/docs/assistant/context-servers) for more info.

```json
{
  "context_servers": {
    "gitlab": {
      "command": {
        "path": "python",
        "args": ["-m", "mcp_extended_gitlab"]
      },
      "settings": {
        "env": {
          "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
          "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
        }
      }
    }
  }
}
```

### Other Clients

#### BoltAI

Open the "Settings" page of the app, navigate to "Plugins," and enter the following JSON:

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

#### Continue (VS Code Extension)

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

#### Windows Configuration

On Windows, the configuration is slightly different:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "cmd",
      "args": ["/c", "python", "-m", "mcp_extended_gitlab"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
  }
}
```

#### Gemini CLI

See [Gemini CLI Configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md) for details.

1. Open the Gemini CLI settings file: `~/.gemini/settings.json`
2. Add the following to the `mcpServers` object:

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

#### Visual Studio 2022

See [Visual Studio MCP Servers documentation](https://learn.microsoft.com/visualstudio/ide/mcp-servers?view=vs-2022) for details.

Add this to your Visual Studio MCP config file:

```json
{
  "mcp": {
    "servers": {
      "gitlab": {
        "type": "stdio",
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

#### Augment Code

To configure MCP Extended GitLab in Augment Code:

1. Press Cmd/Ctrl Shift P or go to the hamburger menu in the Augment panel
2. Select Edit Settings
3. Under Advanced, click Edit in settings.json
4. Add the server configuration:

```json
{
  "augment.advanced": {
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
}
```

#### Roo Code

Add this to your Roo Code MCP configuration file. See [Roo Code MCP docs](https://docs.roocode.com/features/mcp/using-mcp-in-roo) for more info.

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

#### Docker

If you prefer to run the MCP server in a Docker container:

1. Create a `Dockerfile`:

```dockerfile
FROM python:3.11-alpine

WORKDIR /app

# Install git for cloning
RUN apk add --no-cache git

# Install the package
RUN pip install git+https://github.com/Xopoko/mcp-extended-gitlab.git

# Default command
CMD ["python", "-m", "mcp_extended_gitlab"]
```

2. Build the image:
```bash
docker build -t mcp-extended-gitlab .
```

3. Configure your MCP client to use Docker:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITLAB_PRIVATE_TOKEN", "-e", "GITLAB_BASE_URL", "mcp-extended-gitlab"],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your-gitlab-token-here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4"
      }
    }
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

## Available Tools

MCP Extended GitLab provides 478+ tools across 8 domains:

### Core Operations
- **Projects**: Create, manage, fork, star projects
- **Issues**: Create, update, manage issues and boards
- **Merge Requests**: Create, review, approve MRs
- **Commits**: View commits, create branches, manage tags
- **Users**: User management and preferences
- **Groups**: Group management and permissions

### CI/CD & DevOps
- **Pipelines**: Trigger, monitor, manage pipelines
- **Runners**: Manage GitLab runners
- **Environments**: Deploy environments and freeze periods
- **Deployments**: Track and manage deployments

### Registry & Security
- **Container Registry**: Manage Docker images
- **Package Registry**: Handle various package formats
- **Deploy Keys/Tokens**: Manage deployment credentials
- **Protected Branches**: Configure branch protection

### Monitoring & Admin
- **Analytics**: Access project analytics
- **Error Tracking**: Monitor application errors
- **System Hooks**: Admin-level webhooks
- **License Management**: GitLab license operations

## Usage Examples

Once configured, you can use natural language to interact with GitLab:

```
"List all open issues in project myorg/myrepo"
"Create a new merge request from feature-branch to main"
"Show pipeline status for the latest commit"
"Add user john@example.com as developer to project"
```

## Verification

After configuration, verify the setup:

### In Claude Desktop/Claude Code:
1. Restart the application
2. Type: "What GitLab tools are available?"
3. The assistant should list available GitLab operations

### In VS Code extensions:
1. Reload VS Code window
2. Check extension logs for MCP server connection
3. Try a simple command like "List my GitLab projects"

### Manual Testing:
```bash
# Test the server directly
python -m mcp_extended_gitlab

# With environment variables
GITLAB_PRIVATE_TOKEN=your-token GITLAB_BASE_URL=https://gitlab.com/api/v4 python -m mcp_extended_gitlab
```

### Using MCP Inspector:
```bash
npx @modelcontextprotocol/inspector python -m mcp_extended_gitlab
```

## Troubleshooting

### Common Issues

1. **"MCP server not found"**
   - Ensure Python is in your PATH
   - Verify installation with `pip show mcp-extended-gitlab`
   - Check file paths in configuration
   - Try using full path to Python executable

2. **"Authentication failed"**
   - Verify your GitLab token has `api` scope
   - Check token hasn't expired
   - Ensure token is correctly set in environment
   - Test token with: `curl -H "PRIVATE-TOKEN: your-token" https://gitlab.com/api/v4/user`

3. **"Connection refused"**
   - Check GitLab instance URL (should end with `/api/v4`)
   - Verify network connectivity
   - Check for proxy/firewall issues
   - Test API access: `curl https://gitlab.com/api/v4/version`

4. **"Module not found"**
   - Ensure virtual environment is activated
   - Reinstall with `pip install -e .`
   - Check Python version (3.11+)
   - Try alternative installation methods (pipx, uv)

5. **"ModuleNotFoundError: No module named 'fastmcp'"**
   - Dependencies not installed properly
   - Run: `pip install fastmcp httpx pydantic`
   - Or reinstall: `pip install --force-reinstall git+https://github.com/Xopoko/mcp-extended-gitlab.git`

### Platform-Specific Issues

#### Windows
- Use `cmd` instead of `python` directly in command
- Check Windows Defender/antivirus isn't blocking
- Use forward slashes in paths or escape backslashes

#### macOS
- Grant terminal/IDE full disk access in System Preferences
- Check if using system Python vs homebrew/pyenv
- Verify Xcode command line tools installed

#### Linux
- Check Python is python3 (not python2)
- Verify pip is pip3
- May need to use `python3` instead of `python` in configs

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

- **Claude Desktop**: 
  - macOS: `~/Library/Logs/Claude/`
  - Windows: `%APPDATA%\Claude\logs\`
  - Linux: `~/.config/Claude/logs/`
- **VS Code**: Output panel → Select "MCP" or extension name
- **Cursor**: Developer Tools (Cmd/Ctrl+Shift+I) → Console
- **Manual**: Terminal output when running directly

## Security Best Practices

1. **Never commit tokens**: Keep your GitLab token out of version control
2. **Use environment files**: Store tokens in `.env` files (git-ignored)
3. **Limit token scope**: Create tokens with minimum required permissions:
   - For read-only operations: `read_api`
   - For full access: `api`
   - Avoid `sudo` scope unless absolutely necessary
4. **Set token expiration**: Use short-lived tokens when possible
5. **Rotate tokens**: Regularly update your access tokens
6. **Use secure storage**: Consider using system keychains/credential managers
7. **Restrict token access**: Limit token to specific projects if possible

## Support

- **Issues**: https://github.com/Xopoko/mcp-extended-gitlab/issues
- **Documentation**: Check the README.md for detailed API usage
- **GitLab API Reference**: https://docs.gitlab.com/ee/api/
- **MCP Community**: https://modelcontextprotocol.io/community

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [GitLab Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Python Packaging Guide](https://packaging.python.org/)