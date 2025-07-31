"""Tool registry for mapping tool names to modules."""

from typing import Dict, List, Set, Tuple
import inspect
from .api.core import (
    projects, groups, users, issues, merge_requests, commits, repository,
    releases, milestones, labels, wikis, snippets, tags, notes, discussions,
    search, preferences, todos, notifications, events, webhooks
)
from .api.ci_cd import pipelines, runners, variables, lint
from .api.security import protected_branches, deploy_keys, keys, deploy_tokens
from .api.devops import (
    environments, feature_flags, feature_flag_user_lists, deployments,
    dependency_proxy, freeze_periods
)
from .api.registry import packages, container
from .api.integrations import services
from .api.monitoring import statistics, error_tracking, analytics
from .api.admin import license, hooks, flipper_features


# Module registry with all available modules
MODULE_REGISTRY = {
    # Core modules
    "projects": projects,
    "groups": groups,
    "users": users,
    "issues": issues,
    "merge_requests": merge_requests,
    "commits": commits,
    "repository": repository,
    "releases": releases,
    "milestones": milestones,
    "labels": labels,
    "wikis": wikis,
    "snippets": snippets,
    "tags": tags,
    "notes": notes,
    "discussions": discussions,
    "search": search,
    "preferences": preferences,
    "todos": todos,
    "notifications": notifications,
    "events": events,
    "webhooks": webhooks,
    
    # CI/CD modules
    "pipelines": pipelines,
    "runners": runners,
    "variables": variables,
    "lint": lint,
    
    # Security modules
    "protected_branches": protected_branches,
    "deploy_keys": deploy_keys,
    "keys": keys,
    "deploy_tokens": deploy_tokens,
    
    # DevOps modules
    "environments": environments,
    "feature_flags": feature_flags,
    "feature_flag_user_lists": feature_flag_user_lists,
    "deployments": deployments,
    "dependency_proxy": dependency_proxy,
    "freeze_periods": freeze_periods,
    
    # Registry modules
    "packages": packages,
    "container": container,
    
    # Integrations
    "services": services,
    
    # Monitoring modules
    "statistics": statistics,
    "error_tracking": error_tracking,
    "analytics": analytics,
    
    # Admin modules
    "license": license,
    "hooks": hooks,
    "flipper_features": flipper_features,
}


def get_module_tools(module) -> List[str]:
    """Extract tool names from a module by inspecting its register function."""
    tool_names = []
    
    # Get the register function
    if hasattr(module, 'register'):
        register_func = module.register
        
        # Get the source code of the register function
        try:
            source = inspect.getsource(register_func)
            
            # Look for @mcp.tool() decorators followed by function definitions
            lines = source.split('\n')
            for i, line in enumerate(lines):
                if '@mcp.tool()' in line:
                    # Look for the next function definition
                    for j in range(i + 1, min(i + 10, len(lines))):
                        if lines[j].strip().startswith('async def '):
                            # Extract function name
                            func_line = lines[j].strip()
                            func_name = func_line.split('async def ')[1].split('(')[0]
                            tool_names.append(func_name)
                            break
        except:
            pass
    
    return tool_names


def build_tool_to_module_map() -> Dict[str, str]:
    """Build a mapping from tool names to module names."""
    tool_map = {}
    
    for module_name, module in MODULE_REGISTRY.items():
        tools = get_module_tools(module)
        for tool in tools:
            tool_map[tool] = module_name
    
    return tool_map


def get_enabled_modules(enabled_tools: List[str]) -> Set[str]:
    """Get the set of modules that need to be enabled based on tool names."""
    tool_map = build_tool_to_module_map()
    enabled_modules = set()
    
    for tool in enabled_tools:
        if tool in tool_map:
            enabled_modules.add(tool_map[tool])
    
    return enabled_modules


def get_all_tools() -> List[str]:
    """Get all available tool names."""
    tool_map = build_tool_to_module_map()
    return sorted(list(tool_map.keys()))


def get_tools_by_category() -> Dict[str, List[str]]:
    """Get tools organized by category."""
    tools_by_category = {
        "core": [],
        "ci_cd": [],
        "security": [],
        "devops": [],
        "registry": [],
        "integrations": [],
        "monitoring": [],
        "admin": [],
        "server": []  # Tools defined in server.py
    }
    
    tool_map = build_tool_to_module_map()
    
    # Categorize by module path
    for tool, module_name in tool_map.items():
        if module_name in ["projects", "groups", "users", "issues", "merge_requests", 
                          "commits", "repository", "releases", "milestones", "labels",
                          "wikis", "snippets", "tags", "notes", "discussions", "search",
                          "preferences", "todos", "notifications", "events", "webhooks"]:
            tools_by_category["core"].append(tool)
        elif module_name in ["pipelines", "runners", "variables", "lint"]:
            tools_by_category["ci_cd"].append(tool)
        elif module_name in ["protected_branches", "deploy_keys", "keys", "deploy_tokens"]:
            tools_by_category["security"].append(tool)
        elif module_name in ["environments", "feature_flags", "feature_flag_user_lists",
                            "deployments", "dependency_proxy", "freeze_periods"]:
            tools_by_category["devops"].append(tool)
        elif module_name in ["packages", "container"]:
            tools_by_category["registry"].append(tool)
        elif module_name in ["services"]:
            tools_by_category["integrations"].append(tool)
        elif module_name in ["statistics", "error_tracking", "analytics"]:
            tools_by_category["monitoring"].append(tool)
        elif module_name in ["license", "hooks", "flipper_features"]:
            tools_by_category["admin"].append(tool)
    
    # Sort tools in each category
    for category in tools_by_category:
        tools_by_category[category].sort()
    
    return tools_by_category


# Common tool presets
TOOL_PRESETS = {
    "minimal": [
        # Essential project operations
        "list_projects", "get_single_project", "create_project",
        # Essential issue operations
        "list_issues", "get_single_project_issue", "create_issue", "update_issue",
        # Essential MR operations
        "list_merge_requests", "get_single_merge_request", "create_merge_request",
        # Essential user operations
        "get_current_user", "list_users",
        # Essential search
        "search_globally"
    ],
    
    "core": [
        # All project tools
        "list_projects", "get_single_project", "create_project", "update_project", "delete_project",
        "fork_project", "star_project", "unstar_project", "project_languages",
        "list_project_members", "add_project_member", "edit_project_member", "remove_project_member",
        
        # All issue tools
        "list_issues", "get_single_project_issue", "create_issue", "update_issue", "delete_issue",
        "move_issue", "subscribe_to_issue", "unsubscribe_from_issue", "list_issue_links",
        
        # All MR tools
        "list_merge_requests", "get_single_merge_request", "create_merge_request", "update_merge_request",
        "delete_merge_request", "accept_merge_request", "cancel_merge_when_pipeline_succeeds",
        "rebase_merge_request",
        
        # Repository tools
        "list_repository_tree", "get_file_from_repository", "get_file_blame", "compare_branches_tags_commits",
        "list_repository_contributors",
        
        # Commit tools
        "list_repository_commits", "get_single_commit", "get_diff_of_commit", "get_comments_of_commit",
        "post_comment_to_commit", "get_commit_statuses",
        
        # User/Group tools
        "get_current_user", "list_users", "get_user", "list_groups", "get_group",
        
        # Search
        "search_globally", "search_within_project", "search_within_group"
    ],
    
    "ci_cd": [
        # Pipeline tools
        "list_project_pipelines", "get_single_pipeline", "create_pipeline", "retry_jobs_in_pipeline", "cancel_pipeline_jobs",
        "delete_pipeline", "get_pipeline_test_report",
        
        # Job tools
        "list_project_jobs", "get_project_job", "cancel_project_job", "retry_project_job",
        "erase_project_job", "play_project_job",
        
        # Runner tools
        "list_owned_runners", "list_all_runners", "get_runner_details", "update_runner_details", 
        "delete_runner", "list_runner_jobs", "list_project_runners", "enable_runner_in_project",
        "disable_runner_from_project", "list_group_runners",
        
        # Variable tools
        "list_project_variables", "get_project_variable", "create_project_variable",
        "update_project_variable", "delete_project_variable",
        
        # CI lint
        "get_lint_result"
    ],
    
    "devops": [
        # Environment tools
        "list_environments", "get_single_environment", "create_environment", "edit_existing_environment",
        "delete_environment", "stop_environment",
        
        # Deployment tools
        "list_project_deployments", "get_single_deployment", "create_deployment", "update_deployment",
        "delete_deployment", "list_deployment_merge_requests", "approve_blocked_deployment",
        "list_merge_requests_for_deployment",
        
        # Feature flag tools
        "list_feature_flags", "get_single_feature_flag", "create_feature_flag", "edit_feature_flag",
        "delete_feature_flag",
        
        # Package registry
        "list_packages_within_group", "list_packages_within_project", "get_project_package", 
        "delete_project_package", "list_package_files", "delete_package_file"
    ],
    
    "admin": [
        # License tools
        "retrieve_license_information", "add_new_license", "delete_license",
        
        # System hooks
        "list_system_hooks", "add_new_system_hook", "test_system_hook", "delete_system_hook",
        
        # Admin CI variables
        "list_admin_ci_variables", "get_admin_ci_variable", "create_admin_ci_variable",
        "update_admin_ci_variable", "delete_admin_ci_variable",
        
        # Flipper features
        "list_all_features", "set_or_create_feature", "delete_feature"
    ]
}