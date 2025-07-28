# Adding MCP Extended GitLab to Claude

This guide shows how to add the MCP Extended GitLab server to Claude Desktop or Claude Code using Docker.

## Prerequisites

1. **Docker Desktop** installed and running
2. **GitLab Personal Access Token** with appropriate permissions
3. **Claude Desktop** or **Claude Code CLI** installed

## Step 1: Build the Docker Image

Navigate to the project directory and build the image:

```bash
cd /mnt/d/Projects/mcp-extended-gitlab
docker build -t mcp-extended-gitlab:latest .
```

## Step 2: Test the Docker Image

First, let's verify the image works:

```bash
# Test with a simple command
docker run --rm mcp-extended-gitlab:latest --help

# Test in interactive mode (Ctrl+C to exit)
docker run -it --rm \
  -e GITLAB_PRIVATE_TOKEN="your_token_here" \
  mcp-extended-gitlab:latest
```

## Step 3: Add to Claude Desktop

### For Windows
Edit the configuration file at `%APPDATA%\Claude\claude_desktop_config.json`:

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

### For macOS
Edit the configuration file at `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

## Step 4: Add to Claude Code CLI

For Claude Code CLI, use the following command:

```bash
# Add the MCP server
claude mcp add gitlab-extended -- docker run -i --rm \
  -e GITLAB_PRIVATE_TOKEN \
  -e GITLAB_BASE_URL \
  -e GITLAB_ENABLED_TOOLS \
  mcp-extended-gitlab:latest

# Set your GitLab token
claude mcp update gitlab-extended \
  -e GITLAB_PRIVATE_TOKEN=your_gitlab_token \
  -e GITLAB_BASE_URL=https://gitlab.com/api/v4 \
  -e GITLAB_ENABLED_TOOLS=core
```

## Step 5: Tool Filtering Options

To reduce context usage, you can enable only specific tools:

### Available Presets

- **`minimal`** - Essential tools only (~15 tools)
- **`core`** - Core GitLab features (~80 tools)
- **`ci_cd`** - CI/CD pipeline tools (~40 tools)
- **`devops`** - DevOps and deployment tools (~35 tools)
- **`admin`** - Administrative tools (~25 tools)

### Examples

```bash
# Use minimal preset for basic operations
GITLAB_ENABLED_TOOLS="minimal"

# Enable specific tools only
GITLAB_ENABLED_TOOLS="list_projects,get_project,list_issues,create_issue"

# Use all tools (default - 478+ tools)
# Don't set GITLAB_ENABLED_TOOLS or set it to empty string
```

## Step 6: Verify Installation

### For Claude Desktop
1. Restart Claude Desktop after saving the configuration
2. Look for the MCP icon in the Claude interface
3. Click on the MCP icon to see "gitlab-extended" listed as running

### For Claude Code
```bash
# List MCP servers
claude mcp list

# Test the connection
claude mcp test gitlab-extended
```

## Step 7: Using the Tools

Once connected, you can ask Claude to:

```
"List my GitLab projects"
"Create an issue in project XYZ"
"Show recent merge requests"
"Check pipeline status for project ABC"
```

## Troubleshooting

### Docker Issues

```bash
# Check if Docker is running
docker --version

# Check if image was built
docker images | grep mcp-extended-gitlab

# Test the container manually
docker run -it --rm \
  -e GITLAB_PRIVATE_TOKEN="your_token" \
  -e GITLAB_BASE_URL="https://gitlab.com/api/v4" \
  -e GITLAB_ENABLED_TOOLS="minimal" \
  mcp-extended-gitlab:latest
```

### Claude Desktop Issues

1. Check logs:
   - Windows: `%APPDATA%\Claude\logs\`
   - macOS: `~/Library/Logs/Claude/`

2. Validate JSON configuration:
   ```bash
   # Use a JSON validator
   python -m json.tool < claude_desktop_config.json
   ```

3. Common fixes:
   - Ensure Docker Desktop is running
   - Check GitLab token has correct permissions
   - Try with "minimal" tools first
   - Restart Claude Desktop after config changes

### Claude Code Issues

```bash
# Check logs
claude mcp logs gitlab-extended

# Remove and re-add
claude mcp remove gitlab-extended
claude mcp add gitlab-extended -- docker run -i --rm -e GITLAB_PRIVATE_TOKEN mcp-extended-gitlab:latest

# Test with minimal tools
claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS=minimal
```

## Example Configuration with Self-Hosted GitLab

For self-hosted GitLab instances:

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
        "--add-host=gitlab.company.com:192.168.1.100",
        "mcp-extended-gitlab:latest"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_token",
        "GITLAB_BASE_URL": "https://gitlab.company.com/api/v4",
        "GITLAB_ENABLED_TOOLS": "core"
      }
    }
  }
}
```

## Security Considerations

1. **Never commit** your `claude_desktop_config.json` with tokens
2. **Use environment variables** where possible:
   ```json
   "env": {
     "GITLAB_PRIVATE_TOKEN": "${GITLAB_TOKEN}",
     "GITLAB_BASE_URL": "${GITLAB_URL}"
   }
   ```
3. **Limit token scope** to only necessary permissions
4. **Use tool filtering** to reduce attack surface

## Next Steps

1. Start with the `minimal` preset to test connectivity
2. Gradually enable more tools as needed
3. Create custom tool lists for specific workflows
4. Report issues at: https://github.com/yourusername/mcp-extended-gitlab/issues