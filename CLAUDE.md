# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
```bash
# Install dependencies
pip install -e .
pip install -e ".[dev]"

# Run the MCP server
python -m mcp_extended_gitlab
# or
mcp-extended-gitlab

# Run tests
pytest tests/
# Run specific test category
pytest -m unit
pytest -m integration
pytest -m openapi

# Code quality
black mcp_extended_gitlab/         # Format code
ruff check mcp_extended_gitlab/    # Lint code

# Docker operations (via Makefile)
make build    # Build Docker image
make up       # Start containers
make down     # Stop containers
make logs     # View logs
make shell    # Open container shell
make status   # Show container status

# Run with tool filtering
GITLAB_ENABLED_TOOLS=minimal python -m mcp_extended_gitlab
GITLAB_ENABLED_TOOLS=core docker run -e GITLAB_PRIVATE_TOKEN -e GITLAB_ENABLED_TOOLS mcp-extended-gitlab

# List available tools
python scripts/list_tools.py

# Development tools via Makefile
make list-tools    # List all tools
make list-presets  # Show tool presets
make stats         # Project statistics
```

### Environment Setup
```bash
# Required environment variable
export GITLAB_PRIVATE_TOKEN="your_gitlab_private_token"

# Optional: for self-hosted GitLab
export GITLAB_BASE_URL="https://gitlab.com/api/v4"

# Optional: tool filtering to reduce context usage
export GITLAB_ENABLED_TOOLS="minimal"  # Use preset: minimal, core, ci_cd, devops, admin
# Or specify tools explicitly
export GITLAB_ENABLED_TOOLS="list_projects,get_project,list_issues,create_issue"
# Or use JSON array
export GITLAB_ENABLED_TOOLS='["list_projects","get_project","list_issues"]'
```

## Architecture

This is an MCP (Model Context Protocol) server providing 478+ tools for GitLab's REST API, built with FastMCP. The codebase follows a domain-driven design.

### Tool Filtering

Due to the large number of tools (478+), the server supports filtering to reduce Claude's context usage:

- **Environment Variable**: `GITLAB_ENABLED_TOOLS`
- **Presets**: `minimal`, `core`, `ci_cd`, `devops`, `admin`
- **Custom Lists**: Comma-separated tool names or JSON array
- **Implementation**: Uses `FilteredMCP` wrapper that conditionally registers tools
- **Default**: All tools enabled if `GITLAB_ENABLED_TOOLS` not set

### Core Structure
- **`mcp_extended_gitlab/server.py`** - Main MCP server that registers all tools and runs in stdio mode
- **`mcp_extended_gitlab/client.py`** - GitLab API client with async HTTP operations and error handling
- **`mcp_extended_gitlab/filtered_mcp.py`** - FilteredMCP wrapper for conditional tool registration
- **`mcp_extended_gitlab/tool_registry.py`** - Tool presets and module mappings
- **`mcp_extended_gitlab/api/`** - Domain-organized API modules across 8 domains

### Domain Organization
API modules are organized by functionality:
- **`core/`** - Essential GitLab features (projects, groups, users, issues, merge requests, etc.)
- **`ci_cd/`** - CI/CD features (pipelines, runners, variables, lint)
- **`security/`** - Security features (protected branches, deploy keys/tokens)
- **`devops/`** - DevOps features (environments, deployments, feature flags)
- **`registry/`** - Package and container registries
- **`monitoring/`** - Analytics, error tracking, statistics
- **`integrations/`** - Third-party service integrations
- **`admin/`** - Administrative features (license, system hooks)

### Module Pattern
Every API module follows this consistent pattern:
1. Module docstring describing the API section
2. Imports (typing, fastmcp, pydantic, client)
3. `get_gitlab_client()` helper function
4. `register(mcp: FastMCP)` function that registers all tools
5. Tool definitions using `@mcp.tool()` decorator
6. Pydantic Field() for parameter descriptions and defaults

### Tool Registration Flow
1. `server.py` creates a `FilteredMCP` instance (wraps FastMCP)
2. `FilteredMCP` checks `GITLAB_ENABLED_TOOLS` environment variable
3. All register functions from API modules are called
4. `FilteredMCP.tool()` decorator conditionally registers tools based on filter
5. Skipped tools are tracked but not registered (zero context usage)
6. The server runs in stdio mode for Claude Desktop/CLI compatibility

### Adding New Tools
1. Identify the appropriate domain in `mcp_extended_gitlab/api/`
2. Add tool to existing module or create new module following the pattern
3. Import and call the register function in `server.py`
4. Use consistent parameter descriptions and return types
5. Update `tool_registry.py` if:
   - Creating new modules (add to `MODULE_REGISTRY`)
   - Adding tools to presets (update `TOOL_PRESETS`)
   - Creating new categories (update `get_tools_by_category`)

## Key Considerations

- The server runs in stdio mode by default for Claude integration
- All API calls are async using httpx
- GitLabClient handles authentication, rate limiting, and error responses
- Tools use URL-encoded paths or numeric IDs for project/group identification
- Most list operations support pagination via page/per_page parameters
- Many create/update operations use optional parameters with Pydantic Field defaults
- Tool filtering is applied at registration time, not runtime
- Filtered tools consume zero context in Claude

## Testing

### Running Tests
```bash
# Run all tests
make test

# Run specific test categories
pytest -m unit
pytest -m integration

# Test coverage
make coverage
```

### Testing Tools
```bash
# Test all tools
python scripts/test_all_tools.py

# Test specific tools
python scripts/test_all_tools.py -t list_projects -t get_project

# Test by category
python scripts/test_all_tools.py -c core --verbose

# Quick test
scripts/run_tool_tests.sh quick
```

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed project organization.