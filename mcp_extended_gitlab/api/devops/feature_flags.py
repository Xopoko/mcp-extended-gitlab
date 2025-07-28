"""GitLab Feature Flags API - Feature flag management.

This module provides access to GitLab's feature flags functionality,
enabling controlled feature rollouts and A/B testing.
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
    """Register all Feature Flags API tools.
    
    This function registers the following tools:
    - Feature flag listing
    - Feature flag CRUD operations
    - Feature flag user lists management
    """
    
    @mcp.tool()
    async def list_feature_flags(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        scope: Optional[str] = Field(default=None, description="The condition of feature flags, one of: enabled, disabled"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List feature flags for a project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "scope": scope,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/feature_flags", params=params)

    @mcp.tool()
    async def create_feature_flag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the feature flag"),
        description: Optional[str] = Field(default=None, description="The description of the feature flag"),
        active: Optional[bool] = Field(default=True, description="The active state of the flag"),
        strategies: Optional[str] = Field(default=None, description="The feature flag strategies as JSON string. Example: '[{\"name\": \"userWithId\", \"parameters\": {\"userIds\": \"1,2,3\"}}]'")
    ) -> Dict[str, Any]:
        """Create a feature flag for a project."""
        client = await get_gitlab_client()
        data = {"name": name}
        for key, value in {
            "description": description,
            "active": active
        }.items():
            if value is not None:
                data[key] = value
        
        # Parse strategies JSON if provided
        if strategies:
            try:
                data["strategies"] = json.loads(strategies)
            except json.JSONDecodeError:
                pass
        return await client.post(f"/projects/{project_id}/feature_flags", json_data=data)

    @mcp.tool()
    async def get_single_feature_flag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        feature_flag_name: str = Field(description="The name of the feature flag")) -> Dict[str, Any]:
        """Get a single feature flag."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/feature_flags/{feature_flag_name}")

    @mcp.tool()
    async def edit_feature_flag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        feature_flag_name: str = Field(description="The name of the feature flag"),
        name: Optional[str] = Field(default=None, description="The name of the feature flag"),
        description: Optional[str] = Field(default=None, description="The description of the feature flag"),
        active: Optional[bool] = Field(default=None, description="The active state of the flag"),
        strategies: Optional[str] = Field(default=None, description="The feature flag strategies as JSON string. Example: '[{\"name\": \"userWithId\", \"parameters\": {\"userIds\": \"1,2,3\"}}]'")
    ) -> Dict[str, Any]:
        """Edit a feature flag for a project."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "name": name,
            "description": description,
            "active": active,
            "strategies": strategies
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/feature_flags/{feature_flag_name}", json_data=data)

    @mcp.tool()
    async def delete_feature_flag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        feature_flag_name: str = Field(description="The name of the feature flag")) -> Dict[str, Any]:
        """Delete a feature flag."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/feature_flags/{feature_flag_name}")