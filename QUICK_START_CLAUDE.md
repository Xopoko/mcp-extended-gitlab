# Quick Start - Adding MCP Extended GitLab to Claude

## Step 1: Build Docker Image

```bash
cd /mnt/d/Projects/mcp-extended-gitlab
docker build -t mcp-extended-gitlab:latest .
```

## Step 2: Get Your GitLab Token

1. Go to GitLab → Settings → Access Tokens
2. Create a token with `api` scope
3. Copy the token (starts with `glpat-`)

## Step 3: Add to Claude Desktop (Windows)

1. Open file: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add this configuration:

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
        "GITLAB_PRIVATE_TOKEN": "glpat-YOUR_TOKEN_HERE",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4",
        "GITLAB_ENABLED_TOOLS": "core"
      }
    }
  }
}
```

3. Replace `glpat-YOUR_TOKEN_HERE` with your actual token
4. Save the file
5. Restart Claude Desktop

## Step 4: Verify

In Claude Desktop, you should see:
- MCP icon appears in the interface
- Click MCP icon → "gitlab-extended" should show as running

## Step 5: Use It!

Ask Claude:
- "List my GitLab projects"
- "Show recent issues in project XYZ"
- "Create a new issue"
- "Check pipeline status"

## Tool Filtering Options

- `"GITLAB_ENABLED_TOOLS": "minimal"` - 15 essential tools only
- `"GITLAB_ENABLED_TOOLS": "core"` - 80 core tools (recommended)
- `"GITLAB_ENABLED_TOOLS": "ci_cd"` - CI/CD tools
- `"GITLAB_ENABLED_TOOLS": ""` - All 478+ tools (may use lots of context)

## Troubleshooting

If it doesn't work:
1. Check Docker Desktop is running
2. Verify JSON syntax is correct
3. Check logs at `%APPDATA%\Claude\logs\`
4. Try with `"GITLAB_ENABLED_TOOLS": "minimal"` first

## Important Notes

- **Don't use `docker compose up`** - MCP servers don't work that way
- The container only runs when Claude needs it
- It's normal for the container to exit when not in use