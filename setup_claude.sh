#!/bin/bash
# Quick setup script for adding MCP Extended GitLab to Claude

echo "🚀 MCP Extended GitLab - Claude Setup Script"
echo "==========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t mcp-extended-gitlab:latest . || {
    echo "❌ Failed to build Docker image"
    exit 1
}

echo "✅ Docker image built successfully"
echo ""

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    PLATFORM="macOS"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    CONFIG_PATH="$APPDATA/Claude/claude_desktop_config.json"
    PLATFORM="Windows"
else
    CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
    PLATFORM="Linux"
fi

echo "🖥️  Detected platform: $PLATFORM"
echo "📁 Configuration file: $CONFIG_PATH"
echo ""

# Check if using Claude Desktop or Claude Code
read -p "Are you using Claude Desktop (D) or Claude Code CLI (C)? [D/C]: " claude_type

if [[ "$claude_type" == "C" ]] || [[ "$claude_type" == "c" ]]; then
    echo ""
    echo "📝 For Claude Code CLI, run these commands:"
    echo ""
    echo "# Add the MCP server"
    echo "claude mcp add gitlab-extended -- docker run -i --rm -e GITLAB_PRIVATE_TOKEN -e GITLAB_BASE_URL -e GITLAB_ENABLED_TOOLS mcp-extended-gitlab:latest"
    echo ""
    echo "# Set your GitLab token"
    echo "claude mcp update gitlab-extended -e GITLAB_PRIVATE_TOKEN=your_gitlab_token"
    echo ""
    echo "# Optional: Use tool filtering (recommended)"
    echo "claude mcp update gitlab-extended -e GITLAB_ENABLED_TOOLS=core"
else
    echo ""
    echo "📝 For Claude Desktop, add this to your config file:"
    echo "Location: $CONFIG_PATH"
    echo ""
    cat << 'EOF'
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
        "GITLAB_PRIVATE_TOKEN": "your_gitlab_token_here",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4",
        "GITLAB_ENABLED_TOOLS": "core"
      }
    }
  }
}
EOF
    echo ""
    echo "⚠️  Don't forget to:"
    echo "1. Replace 'your_gitlab_token_here' with your actual GitLab token"
    echo "2. Restart Claude Desktop after saving the configuration"
fi

echo ""
echo "📚 Tool Filtering Options:"
echo "- minimal: ~15 essential tools"
echo "- core: ~80 core GitLab features (recommended)"
echo "- ci_cd: ~40 CI/CD tools"
echo "- devops: ~35 DevOps tools"
echo "- admin: ~25 admin tools"
echo "- (empty/unset): All 478+ tools"
echo ""
echo "✨ Setup complete! Check CLAUDE_SETUP.md for detailed instructions."