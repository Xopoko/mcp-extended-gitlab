# Project Structure

This document describes the organization of the MCP Extended GitLab project.

## Directory Layout

```
mcp-extended-gitlab/
├── mcp_extended_gitlab/       # Main Python package
│   ├── api/                   # GitLab API implementations (478+ tools)
│   │   ├── core/              # Core functionality (projects, issues, MRs, etc.)
│   │   ├── ci_cd/             # CI/CD features
│   │   ├── security/          # Security features
│   │   ├── devops/            # DevOps tools
│   │   ├── registry/          # Package/container registries
│   │   ├── monitoring/        # Analytics and monitoring
│   │   ├── integrations/      # External integrations
│   │   └── admin/             # Administrative features
│   ├── client.py              # GitLab API client
│   ├── server.py              # MCP server implementation
│   ├── filtered_mcp.py        # Tool filtering logic
│   └── tool_registry.py       # Tool presets and mappings
│
├── docs/                      # Documentation
│   ├── setup/                 # Installation and setup guides
│   ├── guides/                # User guides and tutorials
│   └── api/                   # API reference
│
├── scripts/                   # Utility scripts
│   ├── test_*.py              # Testing scripts
│   ├── verify_*.py            # Verification scripts
│   └── *.sh                   # Shell scripts
│
├── tests/                     # Test suite
│   ├── test_*.py              # Unit and integration tests
│   └── conftest.py            # Test configuration
│
├── config/                    # Configuration files
│   └── nginx.conf.example     # Example Nginx config
│
├── docker/                    # Docker-related files
│   ├── Dockerfile.simple      # Simplified Dockerfile
│   ├── docker-entrypoint.sh   # Container entrypoint
│   └── docker-compose.dev.yml # Development compose file
│
├── examples/                  # Example configurations
│   └── claude_config_example.json
│
├── Dockerfile                 # Main Docker image
├── docker-compose.yml         # Production compose file
├── pyproject.toml             # Python project configuration
├── Makefile                   # Development commands
├── README.md                  # Project overview
├── CLAUDE.md                  # Claude-specific instructions
└── LICENSE                    # MIT License
```

## Key Files

### Root Directory
- **README.md** - Main project documentation
- **CLAUDE.md** - Instructions for Claude when working with the codebase
- **Dockerfile** - Production Docker image definition
- **docker-compose.yml** - Production deployment configuration
- **pyproject.toml** - Python package configuration and dependencies
- **Makefile** - Development automation commands

### Package Structure
- **mcp_extended_gitlab/** - Main Python package
  - **server.py** - MCP server that registers all tools
  - **client.py** - Async GitLab API client
  - **filtered_mcp.py** - Tool filtering implementation
  - **tool_registry.py** - Tool presets and module mappings

### Documentation
- **docs/setup/** - Installation and configuration guides
- **docs/guides/** - How-to guides for common tasks
- **docs/api/** - API reference and tool listings

### Scripts
- **scripts/test_all_tools.py** - Comprehensive tool testing framework
- **scripts/test_inline_comment.py** - Test inline comments
- **scripts/test_suggestions.py** - Test GitLab suggestions

### Tests
- **tests/** - Unit and integration tests
- **pytest.ini** - Pytest configuration

## Development Workflow

1. **Setup**: `make dev` - Install with development dependencies
2. **Test**: `make test` - Run test suite
3. **Lint**: `make lint` - Check code quality
4. **Format**: `make format` - Format code with black
5. **Docker**: `make build` - Build Docker image

## Tool Organization

The 478+ GitLab API tools are organized into logical domains:

- **Core** (~200 tools): Projects, issues, merge requests, users, etc.
- **CI/CD** (~50 tools): Pipelines, runners, variables, lint
- **Security** (~40 tools): Protected branches, deploy keys/tokens
- **DevOps** (~40 tools): Environments, deployments, feature flags
- **Registry** (~20 tools): Package and container registries
- **Monitoring** (~30 tools): Analytics, error tracking, statistics
- **Integrations** (~10 tools): External service integrations
- **Admin** (~20 tools): License, system hooks, admin operations

## Configuration

- **Environment Variables**: See `.env.template` or `make dev-env`
- **Docker**: See `docker-compose.yml` for container configuration
- **Claude Desktop**: See `examples/claude_config_example.json`

## Quick Start

```bash
# Install dependencies
make install

# Run tests
make test

# Build Docker image
make build

# Run with tool filtering
make run-minimal
```

For detailed setup instructions, see [docs/setup/QUICK_START.md](docs/setup/QUICK_START.md).