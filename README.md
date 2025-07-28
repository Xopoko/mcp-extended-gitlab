# MCP Extended GitLab 🚀

A comprehensive Model Context Protocol (MCP) server that provides AI agents with complete access to GitLab's REST API through 478+ specialized tools.

[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)](https://github.com/jlowin/fastmcp)
[![GitLab API](https://img.shields.io/badge/GitLab%20API-v4-orange)](https://docs.gitlab.com/ee/api/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://www.python.org/)

## 🌟 Overview

MCP Extended GitLab enables AI agents to interact with GitLab programmatically through the Model Context Protocol. With **478 MCP tools** covering **38+ API categories**, this server provides comprehensive access to GitLab's functionality, from basic repository operations to advanced DevOps workflows.

### ✨ Key Features

- **🔧 478 MCP Tools**: Complete implementation of GitLab's REST API endpoints
- **🏗️ Built with FastMCP**: Leverages the powerful FastMCP framework for robust MCP server development
- **🎛️ Tool Filtering**: Reduce context usage by enabling only the tools you need
- **🔐 Secure Authentication**: Support for GitLab private tokens with configurable scopes
- **⚡ Async Operations**: High-performance async HTTP client for efficient API calls
- **🛡️ Error Handling**: Comprehensive error handling with detailed error messages
- **📝 Type Safety**: Full Pydantic models for request/response validation
- **🎯 Domain-Driven Architecture**: Tools organized into focused modules across 8 logical domains
- **📦 Modular Design**: Easy to maintain, extend, and understand codebase structure

## 📦 Installation


### Using Docker (Recommended)

#### Quick Install with Claude Code CLI

```bash
# One-liner installation
claude mcp add gitlab-extended -- docker run -i --rm -e GITLAB_PRIVATE_TOKEN ghcr.io/yourusername/mcp-extended-gitlab

# Set your GitLab token
claude mcp update gitlab-extended -e GITLAB_PRIVATE_TOKEN=your_gitlab_token
```

#### Using Docker Compose

For production deployments or development:

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-extended-gitlab.git
cd mcp-extended-gitlab

# Copy and configure environment variables
cp .env.example .env
# Edit .env and add your GITLAB_PRIVATE_TOKEN

# Start the server
docker-compose up -d
```

For detailed Docker setup instructions, see [DOCKER_SETUP.md](./DOCKER_SETUP.md).

For installation in Claude applications (Claude Code CLI, Claude Desktop), see [INSTALLATION.md](./INSTALLATION.md).

### From Source

```bash
git clone https://github.com/yourusername/mcp-extended-gitlab.git
cd mcp-extended-gitlab
pip install -e .
```

### Dependencies

```bash
pip install fastmcp httpx pydantic python-dotenv
```

## 🔧 Configuration

### Environment Variables

Configure your GitLab connection using environment variables:

```bash
# Required: Your GitLab private token
export GITLAB_PRIVATE_TOKEN="your_gitlab_private_token"

# Optional: GitLab instance URL (defaults to gitlab.com)
export GITLAB_BASE_URL="https://gitlab.com/api/v4"

# Optional: Tool filtering to reduce context usage (478 tools can overwhelm Claude's context)
export GITLAB_ENABLED_TOOLS="minimal"  # Use preset: minimal, core, ci_cd, devops, admin
# Or specify tools explicitly:
export GITLAB_ENABLED_TOOLS="list_projects,get_project,list_issues,create_issue"
```

### Tool Filtering (Recommended)

With 478+ tools available, enabling all tools can consume significant context in Claude. Use tool filtering to enable only the tools you need:

#### Available Presets

- **`minimal`** (~15 tools): Essential operations only - projects, issues, merge requests
- **`core`** (~80 tools): All core GitLab features - complete project management
- **`ci_cd`** (~40 tools): Pipeline, job, runner, and CI/CD variable management
- **`devops`** (~35 tools): Environments, deployments, feature flags, packages
- **`admin`** (~25 tools): Administrative functions, system hooks, licenses

#### Examples

```bash
# Use minimal preset for basic operations
export GITLAB_ENABLED_TOOLS="minimal"

# Use CI/CD preset for pipeline management
export GITLAB_ENABLED_TOOLS="ci_cd"

# Enable specific tools
export GITLAB_ENABLED_TOOLS="list_projects,get_project,list_pipelines,get_pipeline"

# Use JSON array format
export GITLAB_ENABLED_TOOLS='["list_projects","create_issue","list_merge_requests"]'
```

### Generating a GitLab Token

1. Go to your GitLab profile settings
2. Navigate to **Access Tokens**
3. Create a new token with appropriate scopes:
   - `api` - Full API access (recommended for all features)
   - `read_api` - Read-only API access
   - `read_user` - Read user information
   - `read_repository` - Read repository data

## 🚀 Usage

### Starting the Server

```bash
# Using the installed command
mcp-extended-gitlab

# Or run directly with Python
python -m mcp_extended_gitlab.server
```

The server will start on `http://127.0.0.1:8000` by default.

### Example MCP Client Usage

```python
# Example of using the MCP server with an AI agent
# The AI agent can call any of the 478 available tools

# List all projects
projects = await mcp_client.call_tool("list_projects", {
    "owned": True,
    "simple": True
})

# Create a new issue
issue = await mcp_client.call_tool("create_issue", {
    "project_id": "my-project",
    "title": "Bug: Login fails on mobile",
    "description": "Users report login failures on iOS devices",
    "labels": ["bug", "mobile", "high-priority"]
})

# Deploy to production
deployment = await mcp_client.call_tool("create_deployment", {
    "project_id": "my-project",
    "environment": "production",
    "sha": "abc123def456",
    "ref": "main"
})
```

## 📊 API Coverage Overview

### 🎯 Core Features (100+ tools)

| Category | Tools | Description |
|----------|-------|-------------|
| 📁 **Projects** | 30+ | Complete project lifecycle management |
| 👥 **Groups** | 20+ | Group and subgroup operations |
| 👤 **Users** | 25+ | User management and profiles |
| 🐛 **Issues** | 25+ | Issue tracking and management |
| 🔀 **Merge Requests** | 30+ | Code review and merging |

### 🔧 Development Tools (100+ tools)

| Category | Tools | Description |
|----------|-------|-------------|
| 📝 **Commits** | 15+ | Commit operations and history |
| 📂 **Repository** | 15+ | File and tree operations |
| 🔄 **Pipelines** | 10+ | CI/CD pipeline management |
| 🚀 **Releases** | 5+ | Release management |
| 🎯 **Milestones** | 15+ | Project planning |

### 🛡️ Security & Operations (150+ tools)

| Category | Tools | Description |
|----------|-------|-------------|
| 🔑 **Deploy Keys** | 8 | SSH key management |
| 🌍 **Environments** | 6 | Environment configuration |
| 🚩 **Feature Flags** | 12 | Feature toggle management |
| 📦 **Container Registry** | 11 | Docker image management |
| 🐛 **Error Tracking** | 12 | Error monitoring |

### 📈 Analytics & Monitoring (50+ tools)

| Category | Tools | Description |
|----------|-------|-------------|
| 📊 **DORA Metrics** | 8 | DevOps performance metrics |
| 🔍 **Search** | 3 | Global search capabilities |
| 📦 **Package Registry** | 6 | Package management |
| ⚙️ **System APIs** | 50+ | Admin and system operations |

## 📋 Complete API Categories

<details>
<summary>Click to see all 38+ implemented categories</summary>

### Administrative Tools
- 🔐 **Access Requests** (8 tools) - Manage access requests for projects and groups
- 🛠️ **Admin Operations** (5 tools) - Database and system administration
- 🚨 **Alert Management** (6 tools) - Alert metric images and management
- 📱 **Application Settings** (7 tools) - Instance appearance and limits

### Project Management
- 📁 **Projects** (30+ tools) - Full project lifecycle management
- 👥 **Groups** (20+ tools) - Group hierarchy and permissions
- 👤 **Users** (25+ tools) - User profiles and management
- 🏆 **Badges** (12 tools) - Project and group badges

### Development Workflow
- 🐛 **Issues** (25+ tools) - Issue tracking with time tracking and links
- 🔀 **Merge Requests** (30+ tools) - Code review with approvals
- 📝 **Commits** (15+ tools) - Commit management and cherry-picking
- 📂 **Repository** (15+ tools) - File operations and blame

### CI/CD & DevOps
- 🔄 **Pipelines** (10+ tools) - Pipeline execution and management
- 🚀 **Releases** (5+ tools) - Release creation and assets
- 🌍 **Environments** (6 tools) - Environment management
- 🚀 **Deployments** (8 tools) - Deployment lifecycle

### Security & Access
- 🔑 **Deploy Keys** (8 tools) - SSH key management
- 🔑 **Deploy Tokens** (10 tools) - Token-based authentication
- 🌿 **Protected Branches** (8 tools) - Branch protection rules
- 🔐 **Variables** (10 tools) - CI/CD variable management

### Advanced Features
- 🚩 **Feature Flags** (12 tools) - Feature toggle management
- 📦 **Container Registry** (11 tools) - Docker registry operations
- 🐛 **Error Tracking** (12 tools) - Error monitoring and management
- 🔗 **Dependency Proxy** (11 tools) - Package proxy management

### Collaboration Tools
- 🏷️ **Labels** (10 tools) - Label management
- 📝 **Notes** (15 tools) - Comments and discussions
- 💬 **Discussions** (8 tools) - Thread management
- 📖 **Wikis** (8 tools) - Documentation management
- ✂️ **Snippets** (10 tools) - Code snippet sharing

### Monitoring & Analytics
- 📊 **DORA Metrics** (8 tools) - DevOps performance metrics
- 📈 **Analytics** (5 tools) - Issue and MR analytics
- 📊 **Statistics** (3 tools) - Project and group statistics
- 🔍 **Search** (3 tools) - Global search functionality

### System Integration
- 🔗 **Webhooks** (10 tools) - Event notifications
- 🔌 **Integrations** (4 tools) - Third-party integrations
- 🪝 **System Hooks** (4 tools) - System-level webhooks
- 📦 **Package Registry** (6 tools) - Package management

### Additional Tools
- 🔧 **Jobs** (6 tools) - CI job management
- 🏃 **Runners** (15 tools) - GitLab Runner management
- 🏷️ **Tags** (8 tools) - Git tag operations
- 📊 **Metadata** (2 tools) - Instance information
- 🗝️ **License** (3 tools) - License management

</details>

## 🏗️ Architecture

### Project Structure

The project follows a clean, domain-driven architecture that organizes 478+ tools into logical API modules:

```
mcp-extended-gitlab/
├── mcp_extended_gitlab/
│   ├── __init__.py
│   ├── server.py              # Main MCP server registration
│   ├── client.py              # GitLab API client wrapper
│   ├── filtered_mcp.py        # Tool filtering wrapper
│   ├── tool_registry.py       # Tool presets and mappings
│   └── api/                   # Organized API modules
│       ├── core/              # Core GitLab functionality
│       │   ├── __init__.py
│       │   ├── projects.py    # Project management (30+ tools)
│       │   ├── groups.py      # Group management (20+ tools)
│       │   ├── users.py       # User management (25+ tools)
│       │   ├── issues.py      # Issue tracking (25+ tools)
│       │   ├── merge_requests.py # Code review (30+ tools)
│       │   ├── commits.py     # Git commits (15+ tools)
│       │   ├── repository.py  # File operations (15+ tools)
│       │   ├── releases.py    # Release management
│       │   ├── milestones.py  # Planning tools
│       │   ├── labels.py      # Label management
│       │   ├── wikis.py       # Documentation
│       │   ├── snippets.py    # Code snippets
│       │   ├── tags.py        # Git tags
│       │   ├── notes.py       # Comments
│       │   ├── discussions.py # Threaded discussions
│       │   ├── webhooks.py    # Event notifications
│       │   ├── search.py      # Search functionality
│       │   ├── preferences.py # User preferences
│       │   ├── todos.py       # Todo management
│       │   ├── notifications.py # Notification settings
│       │   └── events.py      # Activity tracking
│       ├── ci_cd/             # CI/CD features
│       │   ├── __init__.py
│       │   ├── pipelines.py   # Pipeline management
│       │   ├── runners.py     # Runner configuration
│       │   ├── variables.py   # CI/CD variables
│       │   └── lint.py        # Config validation
│       ├── security/          # Security features
│       │   ├── __init__.py
│       │   ├── protected_branches.py # Branch protection
│       │   ├── deploy_keys.py # SSH deploy keys
│       │   ├── deploy_tokens.py # Deploy tokens
│       │   └── keys.py        # SSH key validation
│       ├── devops/            # DevOps features
│       │   ├── __init__.py
│       │   ├── environments.py # Environment management
│       │   ├── deployments.py # Deployment tracking
│       │   ├── feature_flags.py # Feature toggles
│       │   ├── feature_flag_user_lists.py # User targeting
│       │   ├── dependency_proxy.py # Docker proxy
│       │   └── freeze_periods.py # Deployment freezes
│       ├── registry/          # Package and container registry
│       │   ├── __init__.py
│       │   ├── packages.py    # Package registry
│       │   └── container.py   # Container registry
│       ├── monitoring/        # Analytics and monitoring
│       │   ├── __init__.py
│       │   ├── statistics.py  # Usage statistics
│       │   ├── error_tracking.py # Error monitoring
│       │   └── analytics.py   # DORA metrics
│       ├── integrations/      # Third-party integrations
│       │   ├── __init__.py
│       │   └── services.py    # External services
│       └── admin/             # Administrative features
│           ├── __init__.py
│           ├── license.py     # License management
│           ├── hooks.py       # System hooks
│           └── flipper_features.py # Internal flags
├── pyproject.toml
├── README.md
└── openapi.yaml               # GitLab OpenAPI specification
```

### Key Components

1. **GitLabClient**: Async HTTP client with authentication and error handling
2. **Domain-Driven Modules**: Focused modules organized by functionality
3. **FastMCP Integration**: Consistent tool registration pattern across all modules
4. **Pydantic Models**: Type-safe parameter validation for all tools
5. **FilteredMCP**: Dynamic tool filtering based on environment configuration

### Architecture Benefits

- **🎯 Clear Organization**: Tools grouped by domain for easy discovery
- **📦 Modular Design**: Each module has a single responsibility
- **🔧 Consistent Pattern**: All modules follow the same structure
- **📈 Scalable**: Easy to add new features in appropriate domains
- **🧪 Maintainable**: Focused modules are easier to test and update
- **⚡ Performance**: Tool filtering reduces context usage for better performance

## 🧪 Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black mcp_extended_gitlab/

# Lint code
ruff check mcp_extended_gitlab/

# Type checking
mypy mcp_extended_gitlab/
```

### Adding New Tools

1. Identify the appropriate domain directory in `mcp_extended_gitlab/api/`
2. Create or update a module in the relevant subdirectory
3. Define tools using the `@mcp.tool()` decorator within a `register()` function
4. Import and call the register function in `server.py`
5. Update the tool count in README.md

Example for adding a new tool:
```python
# In api/core/new_feature.py
from typing import Any, Dict
from fastmcp import FastMCP
from pydantic import Field
from ...client import GitLabClient

async def get_gitlab_client() -> GitLabClient:
    """Get or create GitLab client instance."""
    import os
    from ...client import GitLabConfig
    
    config = GitLabConfig(
        base_url=os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4"),
        private_token=os.getenv("GITLAB_PRIVATE_TOKEN")
    )
    return GitLabClient(config)

def register(mcp: FastMCP):
    """Register all New Feature API tools."""
    
    @mcp.tool()
    async def new_feature_action(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Perform new feature action."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/new_feature")
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) - The awesome MCP framework
- GitLab API documentation and OpenAPI specification
- The Model Context Protocol community

## 🚧 Roadmap

### Recently Completed ✅

- [x] **Architecture Refactoring**: Migrated from flat structure to domain-driven design with focused modules
- [x] **Tool Filtering**: Added support for enabling only needed tools to reduce context usage
- [x] **Improved Organization**: Tools now grouped into 8 logical domains for better discoverability
- [x] **Consistent Patterns**: All modules follow the same structure and registration pattern

### Future Enhancements

- [ ] Add support for GraphQL API endpoints
- [ ] Implement webhook server for real-time events
- [ ] Add batch operations for improved performance
- [ ] Create specialized tool bundles for common workflows
- [ ] Add support for GitLab-specific package registries
- [ ] Add comprehensive test coverage for all modules
- [ ] Create domain-specific client wrappers for common use cases

### Potential API Additions

The GitLab API continues to evolve. Future implementations could include:
- Terraform module registry
- Advanced package management (NPM, Maven, etc.)
- Geo replication APIs
- Advanced analytics and insights
- AI-powered features integration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mcp-extended-gitlab/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mcp-extended-gitlab/discussions)
- **Documentation**: [GitLab API Docs](https://docs.gitlab.com/ee/api/)

---

**Made with ❤️ for the MCP and GitLab communities**