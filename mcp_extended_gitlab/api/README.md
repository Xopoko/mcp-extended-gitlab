# GitLab MCP API Module Structure

This directory contains the organized GitLab API modules for the MCP server. The structure follows a domain-driven design approach, grouping related functionality into logical subdirectories.

## Directory Structure

### `/core/`
Core GitLab functionality that forms the foundation of the platform:
- `projects.py` - Project management and configuration
- `groups.py` - Group management and settings
- `users.py` - User management, authentication, and relationships
- `issues.py` - Issue tracking and management
- `merge_requests.py` - Merge request operations
- `commits.py` - Git commit operations
- `repository.py` - Repository file and tree operations
- `releases.py` - Release management
- `milestones.py` - Project and group milestones
- `labels.py` - Label management for issues and MRs
- `wikis.py` - Wiki page management
- `snippets.py` - Code snippet management
- `tags.py` - Git tag management
- `notes.py` - Comments on issues, MRs, and snippets
- `discussions.py` - Threaded discussions
- `webhooks.py` - Webhook management
- `search.py` - Global, group, and project search
- `preferences.py` - User preferences
- `todos.py` - Todo item management
- `notifications.py` - Notification settings
- `events.py` - Activity event tracking

### `/ci_cd/`
Continuous Integration and Deployment features:
- `pipelines.py` - CI/CD pipeline management
- `runners.py` - GitLab Runner management
- `variables.py` - CI/CD variable management
- `lint.py` - CI/CD configuration validation

### `/security/`
Security-related features:
- `protected_branches.py` - Branch protection rules
- `deploy_keys.py` - SSH deploy key management
- `deploy_tokens.py` - Deploy token management
- `keys.py` - SSH key validation and fingerprinting

### `/devops/`
DevOps and deployment features:
- `environments.py` - Deployment environment management
- `deployments.py` - Deployment tracking
- `feature_flags.py` - Feature flag management
- `feature_flag_user_lists.py` - Feature flag user targeting
- `dependency_proxy.py` - Docker image proxy
- `freeze_periods.py` - Deployment freeze periods

### `/registry/`
Package and container registry features:
- `packages.py` - Package registry operations
- `container.py` - Container registry management

### `/monitoring/`
Monitoring and analytics features:
- `statistics.py` - System and resource statistics
- `error_tracking.py` - Error monitoring and management
- `analytics.py` - DORA metrics and productivity analytics

### `/integrations/`
Third-party integrations:
- `services.py` - External service integrations

### `/admin/`
Administrative features:
- `license.py` - GitLab license management
- `hooks.py` - System-wide webhook management
- `flipper_features.py` - Internal feature flags

## Usage

Each module exports a single `register(mcp: FastMCP)` function that registers all related tools with the MCP server. This provides a consistent interface across all modules.

Example:
```python
from api.core.projects import register as register_projects_tools
register_projects_tools(mcp)
```

## Module Pattern

All modules follow the same pattern:
1. Module docstring describing the API section
2. Imports (typing, fastmcp, pydantic, client)
3. `get_gitlab_client()` helper function
4. `register(mcp: FastMCP)` function that registers all tools
5. Tool definitions using the `@mcp.tool()` decorator

This consistent structure makes the codebase easy to navigate and maintain.