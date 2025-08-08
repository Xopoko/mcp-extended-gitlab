"""GitLab Protected Branches API - Branch protection management.

This module provides comprehensive access to GitLab's protected branches features,
enabling management of branch protection rules and access controls.
"""

import json
from typing import Any, Dict, List, Optional
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
    """Register all Protected Branches API tools.
    
    This function registers the following tools:
    - Protected branch listing and search
    - Branch protection management
    - Access level configuration
    """
    
    @mcp.tool()
    async def list_protected_branches(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        search: Optional[str] = Field(default=None, description="Name or part of the name of protected branches to be searched for")) -> Dict[str, Any]:
        """List protected branches."""
        client = await get_gitlab_client()
        params = {}
        if search:
            params["search"] = search
        return await client.get(f"/projects/{project_id}/protected_branches", params=params)

    @mcp.tool()
    async def get_single_protected_branch(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the branch or wildcard")) -> Dict[str, Any]:
        """Get a single protected branch or wildcard protected branch."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/protected_branches/{name}")

    @mcp.tool()
    async def protect_repository_branch(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the branch or wildcard"),
        push_access_level: Optional[int] = Field(default=40, description="Access levels allowed to push (defaults to 40, maintainer access level)"),
        merge_access_level: Optional[int] = Field(default=40, description="Access levels allowed to merge (defaults to 40, maintainer access level)"),
        unprotect_access_level: Optional[int] = Field(default=40, description="Access levels allowed to unprotect (defaults to 40, maintainer access level)"),
        allow_force_push: Optional[bool] = Field(default=False, description="Allow all users with push access to force push"),
        code_owner_approval_required: Optional[bool] = Field(default=False, description="Prevent pushes to this branch if it matches an item in the CODEOWNERS file"),
        allowed_to_push: Optional[str] = Field(default=None, description="Array of access levels allowed to push as JSON string. Example: '[{\"access_level\": 40}]'"),
        allowed_to_merge: Optional[str] = Field(default=None, description="Array of access levels allowed to merge as JSON string. Example: '[{\"access_level\": 40}]'"),
        allowed_to_unprotect: Optional[str] = Field(default=None, description="Array of access levels allowed to unprotect as JSON string")
    ) -> Dict[str, Any]:
        """Protect repository branch."""
        client = await get_gitlab_client()
        data = {"name": name}
        
        # Parse JSON strings for allowed_to_* parameters
        allowed_to_push_parsed = None
        allowed_to_merge_parsed = None
        allowed_to_unprotect_parsed = None
        
        if isinstance(allowed_to_push, str):
            try:
                allowed_to_push_parsed = json.loads(allowed_to_push)
            except json.JSONDecodeError:
                pass
                
        if isinstance(allowed_to_merge, str):
            try:
                allowed_to_merge_parsed = json.loads(allowed_to_merge)
            except json.JSONDecodeError:
                pass
                
        if isinstance(allowed_to_unprotect, str):
            try:
                allowed_to_unprotect_parsed = json.loads(allowed_to_unprotect)
            except json.JSONDecodeError:
                pass
        
        for key, value in {
            "push_access_level": push_access_level,
            "merge_access_level": merge_access_level,
            "unprotect_access_level": unprotect_access_level,
            "allow_force_push": allow_force_push,
            "allowed_to_push": allowed_to_push_parsed,
            "allowed_to_merge": allowed_to_merge_parsed,
            "allowed_to_unprotect": allowed_to_unprotect_parsed,
            "code_owner_approval_required": code_owner_approval_required
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/protected_branches", json_data=data)

    @mcp.tool()
    async def unprotect_repository_branch(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the branch")) -> Dict[str, Any]:
        """Unprotect repository branch."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/protected_branches/{name}")

    @mcp.tool()
    async def update_protected_branch(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the branch"),
        allow_force_push: Optional[bool] = Field(default=None, description="Allow all users with push access to force push"),
        code_owner_approval_required: Optional[bool] = Field(default=None, description="Prevent pushes to this branch if it matches an item in the CODEOWNERS file"),
        allowed_to_push: Optional[str] = Field(default=None, description="Array of access levels allowed to push as JSON string. Example: '[{\"access_level\": 40}]'"),
        allowed_to_merge: Optional[str] = Field(default=None, description="Array of access levels allowed to merge as JSON string. Example: '[{\"access_level\": 40}]'"),
        allowed_to_unprotect: Optional[str] = Field(default=None, description="Array of access levels allowed to unprotect as JSON string")
    ) -> Dict[str, Any]:
        """Update a protected branch."""
        client = await get_gitlab_client()
        data = {}
        
        # Parse JSON strings for allowed_to_* parameters
        allowed_to_push_parsed = None
        allowed_to_merge_parsed = None
        allowed_to_unprotect_parsed = None
        
        if allowed_to_push:
            try:
                allowed_to_push_parsed = json.loads(allowed_to_push)
            except json.JSONDecodeError:
                pass
                
        if allowed_to_merge:
            try:
                allowed_to_merge_parsed = json.loads(allowed_to_merge)
            except json.JSONDecodeError:
                pass
                
        if allowed_to_unprotect:
            try:
                allowed_to_unprotect_parsed = json.loads(allowed_to_unprotect)
            except json.JSONDecodeError:
                pass
        
        for key, value in {
            "allow_force_push": allow_force_push,
            "allowed_to_push": allowed_to_push_parsed,
            "allowed_to_merge": allowed_to_merge_parsed,
            "allowed_to_unprotect": allowed_to_unprotect_parsed,
            "code_owner_approval_required": code_owner_approval_required
        }.items():
            if value is not None:
                data[key] = value
        return await client.patch(f"/projects/{project_id}/protected_branches/{name}", json_data=data)
