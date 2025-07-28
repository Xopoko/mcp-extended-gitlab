"""GitLab Feature Flag User Lists API - User list management for feature flags.

This module provides access to GitLab's feature flag user lists,
enabling targeted feature rollouts to specific user groups.
"""

from typing import Any, Dict, Optional
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
    """Register all Feature Flag User Lists API tools.
    
    This function registers the following tools:
    - User list listing and search
    - User list CRUD operations
    """
    
    @mcp.tool()
    async def list_feature_flag_user_lists(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        search: Optional[str] = Field(default=None, description="Return user lists with a name matching the search term"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List feature flag user lists for a project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "search": search,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/feature_flags_user_lists", params=params)

    @mcp.tool()
    async def create_feature_flag_user_list(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the user list"),
        user_xids: str = Field(description="A comma separated list of user IDs")) -> Dict[str, Any]:
        """Create a feature flag user list."""
        client = await get_gitlab_client()
        data = {
            "name": name,
            "user_xids": user_xids
        }
        return await client.post(f"/projects/{project_id}/feature_flags_user_lists", json_data=data)

    @mcp.tool()
    async def get_single_feature_flag_user_list(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        iid: str = Field(description="The internal ID of the user list")) -> Dict[str, Any]:
        """Get a single feature flag user list."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/feature_flags_user_lists/{iid}")

    @mcp.tool()
    async def update_feature_flag_user_list(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        iid: str = Field(description="The internal ID of the user list"),
        name: Optional[str] = Field(default=None, description="The name of the user list"),
        user_xids: Optional[str] = Field(default=None, description="A comma separated list of user IDs")) -> Dict[str, Any]:
        """Update a feature flag user list."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "name": name,
            "user_xids": user_xids
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/feature_flags_user_lists/{iid}", json_data=data)

    @mcp.tool()
    async def delete_feature_flag_user_list(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        iid: str = Field(description="The internal ID of the user list")) -> Dict[str, Any]:
        """Delete a feature flag user list."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/feature_flags_user_lists/{iid}")