# MCP Extended GitLab - Tool Names Reference

## Important: How Tool Filtering Works

When you set `GITLAB_ENABLED_TOOLS`, you must use the **exact tool names**, not category names.

❌ **Wrong**: `GITLAB_ENABLED_TOOLS="projects,groups,users"`
✅ **Correct**: `GITLAB_ENABLED_TOOLS="list_projects,get_project,list_groups"`

## Tool Presets (Recommended)

Instead of listing individual tools, use presets:

```bash
# Minimal set (~15 tools)
GITLAB_ENABLED_TOOLS="minimal"

# Core features (~80 tools) 
GITLAB_ENABLED_TOOLS="core"

# CI/CD tools (~40 tools)
GITLAB_ENABLED_TOOLS="ci_cd"
```

## Custom Tool Selection

For your use case with projects, groups, users, merge requests, notes, discussions, and repository:

```bash
# Option 1: Use comma-separated list
GITLAB_ENABLED_TOOLS="list_projects,get_single_project,create_project,update_project,delete_project,list_groups,get_group,create_group,update_group,list_users,get_user,get_current_user,list_merge_requests,get_single_merge_request,create_merge_request,update_merge_request,accept_merge_request,list_merge_request_notes,create_merge_request_note,list_merge_request_discussions,create_new_merge_request_thread,list_repository_tree,get_file_from_repository,create_new_file,update_existing_file"

# Option 2: Use JSON array (easier to read)
GITLAB_ENABLED_TOOLS='[
  "list_projects",
  "get_single_project",
  "create_project",
  "update_project",
  "list_groups",
  "get_group",
  "create_group",
  "list_users",
  "get_user",
  "get_current_user",
  "list_merge_requests",
  "get_single_merge_request",
  "create_merge_request",
  "update_merge_request",
  "accept_merge_request",
  "list_merge_request_notes",
  "create_merge_request_note",
  "list_merge_request_discussions",
  "create_new_merge_request_thread",
  "list_repository_tree",
  "get_file_from_repository",
  "create_new_file",
  "update_existing_file"
]'
```

## Common Tool Names by Category

### Projects
- `list_projects` - List all projects
- `get_single_project` - Get project details
- `create_project` - Create new project
- `update_project` - Update project settings
- `delete_project` - Delete project
- `fork_project` - Fork a project
- `star_project` / `unstar_project` - Star/unstar projects

### Groups
- `list_groups` - List all groups
- `get_group` - Get group details
- `create_group` - Create new group
- `update_group` - Update group settings
- `delete_group` - Delete group
- `list_subgroups` - List subgroups

### Users
- `list_users` - List all users
- `get_user` - Get user details
- `get_current_user` - Get authenticated user
- `create_user` - Create new user (admin)
- `update_user` - Update user (admin)
- `block_user` / `unblock_user` - Block/unblock users

### Merge Requests
- `list_merge_requests` - List project merge requests
- `get_single_merge_request` - Get MR details
- `create_merge_request` - Create new MR
- `update_merge_request` - Update MR
- `accept_merge_request` - Accept/merge MR
- `merge_request_changes` - Get MR diff
- `list_merge_request_approvals` - List approvals

### Issues
- `list_issues` - List project issues
- `get_single_issue` - Get issue details
- `create_issue` - Create new issue
- `update_issue` - Update issue
- `delete_issue` - Delete issue

### Notes (Comments)
- `list_merge_request_notes` - List MR comments
- `create_merge_request_note` - Add MR comment
- `update_merge_request_note` - Edit comment
- `delete_merge_request_note` - Delete comment
- `list_issue_notes` - List issue comments
- `create_issue_note` - Add issue comment

### Discussions
- `list_merge_request_discussions` - List MR discussions
- `create_new_merge_request_thread` - Start new thread
- `add_note_to_merge_request_discussion` - Reply to thread
- `resolve_merge_request_discussion` - Resolve thread
- `list_issue_discussions` - List issue discussions

### Repository
- `list_repository_tree` - List files/folders
- `get_file_from_repository` - Get file content
- `get_raw_file` - Get raw file content
- `create_new_file` - Create file
- `update_existing_file` - Update file
- `delete_existing_file` - Delete file
- `list_repository_commits` - List commits

### Commits
- `list_repository_commits` - List commits
- `get_single_commit` - Get commit details
- `create_commit` - Create new commit
- `list_commit_refs` - Get commit references
- `cherry_pick_commit` - Cherry-pick commit
- `revert_commit` - Revert commit

## Finding Tool Names

To find exact tool names:

1. Look at the error logs when a tool is not found
2. Check the MCP server output when starting
3. Use the "minimal" preset first to see basic tool names
4. Gradually add more tools as needed

## Example Docker Configuration

```json
{
  "mcpServers": {
    "gitlab-extended": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITLAB_PRIVATE_TOKEN",
        "-e", "GITLAB_BASE_URL",
        "-e", "GITLAB_ENABLED_TOOLS",
        "mcp-extended-gitlab:latest"
      ],
      "env": {
        "GITLAB_PRIVATE_TOKEN": "your_token",
        "GITLAB_BASE_URL": "https://gitlab.com/api/v4",
        "GITLAB_ENABLED_TOOLS": '["list_projects","get_single_project","list_issues","create_issue"]'
      }
    }
  }
}
```