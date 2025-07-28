# API Reference

This directory contains API reference documentation for MCP Extended GitLab.

## Available Documentation

- **[Tool Names](./TOOL_NAMES.md)** - Complete list of all 478+ available GitLab API tools
- **[Unimplemented APIs](./unimplemented_apis_analysis.md)** - Analysis of GitLab APIs not yet implemented

## Tool Categories

The 478+ tools are organized into these categories:

### Core (200+ tools)
- Projects management
- Groups management  
- Users and members
- Issues and merge requests
- Commits and repository operations
- Releases and milestones
- Labels and wikis
- Snippets and tags
- Notes and discussions
- Search and preferences

### CI/CD (50+ tools)
- Pipelines and jobs
- Runners configuration
- CI/CD variables
- Configuration validation

### Security (40+ tools)
- Protected branches
- Deploy keys and tokens
- SSH key management

### DevOps (40+ tools)
- Environments
- Deployments
- Feature flags
- Dependency proxy

### Registry (20+ tools)
- Package registry
- Container registry

### Monitoring (30+ tools)
- Analytics
- Error tracking
- Statistics

### Integrations (10+ tools)
- External service integrations

### Admin (20+ tools)
- License management
- System hooks
- Admin-level operations

## Finding the Right Tool

1. Check [Tool Names](./TOOL_NAMES.md) for the complete alphabetical list
2. Use Ctrl+F to search for keywords
3. Tools follow naming conventions:
   - `list_*` - Get multiple items
   - `get_*` - Get single item
   - `create_*` - Create new item
   - `update_*` - Update existing item
   - `delete_*` - Remove item

## Tool Usage

Each tool accepts specific parameters as documented in the tool list. Common patterns:

- **Authentication**: All tools use the GitLab private token from environment
- **Project identification**: Use either numeric ID or URL-encoded path
- **Pagination**: List operations support `page` and `per_page` parameters
- **Optional parameters**: Most creation/update tools have many optional parameters