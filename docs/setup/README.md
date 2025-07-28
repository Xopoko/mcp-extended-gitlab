# Setup Documentation

This directory contains all setup and installation guides for MCP Extended GitLab.

## Quick Start

- **[Quick Start Guide](./QUICK_START.md)** - Get up and running in 5 minutes with Claude Desktop

## Detailed Setup Guides

- **[Installation Guide](./INSTALLATION.md)** - Complete installation instructions for all platforms
- **[MCP Client Setup](./MCP_CLIENT_SETUP.md)** - Setup instructions for various MCP clients
- **[Docker Setup](./DOCKER_SETUP.md)** - Docker installation and configuration
- **[Docker Usage](./DOCKER_USAGE.md)** - Using the Docker image effectively

## Platform-Specific Guides

- **[GitHub Setup](./GITHUB_SETUP.md)** - Special instructions for GitHub-hosted GitLab instances

## Setup Order

1. **Choose your installation method:**
   - Docker (recommended) - Follow [Docker Setup](./DOCKER_SETUP.md)
   - Local installation - Follow [Installation Guide](./INSTALLATION.md)

2. **Configure your MCP client:**
   - For Claude Desktop - Follow [Quick Start Guide](./QUICK_START.md)
   - For other clients - Follow [MCP Client Setup](./MCP_CLIENT_SETUP.md)

3. **Get your GitLab token:**
   - Go to GitLab → Settings → Access Tokens
   - Create a token with `api` scope
   - Save the token (starts with `glpat-`)

4. **Test your setup:**
   - Try listing projects: "List my GitLab projects"
   - Check the [Testing Tools Guide](../guides/TESTING_TOOLS.md) for more tests