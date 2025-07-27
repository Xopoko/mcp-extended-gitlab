"""GitLab Environments API - Deployment environment management.

This module provides comprehensive access to GitLab's environments features,
enabling management of deployment environments and their configurations.
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
    """Register all Environments API tools.
    
    This function registers the following tools:
    - Environment listing and search
    - Environment CRUD operations
    - Environment lifecycle management (stop/start)
    """
    
    @mcp.tool()
    async def list_environments(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: Optional[str] = Field(default=None, description="Return the environment with this name"),
        search: Optional[str] = Field(default=None, description="Return list of environments matching the search criteria"),
        states: Optional[str] = Field(default=None, description="List all environments that match a specific state")
    ) -> Dict[str, Any]:
        """List environments."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "name": name,
            "search": search,
            "states": states
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/environments", params=params)

    @mcp.tool()
    async def create_new_environment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the environment"),
        external_url: Optional[str] = Field(default=None, description="Place to link to for this environment"),
        tier: Optional[str] = Field(default=None, description="The tier of the new environment")
    ) -> Dict[str, Any]:
        """Create a new environment."""
        client = await get_gitlab_client()
        data = {"name": name}
        for key, value in {
            "external_url": external_url,
            "tier": tier
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/environments", json_data=data)

    @mcp.tool()
    async def edit_existing_environment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        environment_id: str = Field(description="The ID of the environment"),
        name: Optional[str] = Field(default=None, description="The new name of the environment"),
        external_url: Optional[str] = Field(default=None, description="The new external_url"),
        tier: Optional[str] = Field(default=None, description="The new tier of the environment")
    ) -> Dict[str, Any]:
        """Edit an existing environment."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "name": name,
            "external_url": external_url,
            "tier": tier
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/environments/{environment_id}", json_data=data)

    @mcp.tool()
    async def delete_environment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        environment_id: str = Field(description="The ID of the environment")
    ) -> Dict[str, Any]:
        """Delete an environment."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/environments/{environment_id}")

    @mcp.tool()
    async def stop_environment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        environment_id: str = Field(description="The ID of the environment")
    ) -> Dict[str, Any]:
        """Stop an environment."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/environments/{environment_id}/stop")

    @mcp.tool()
    async def get_single_environment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        environment_id: str = Field(description="The ID of the environment")
    ) -> Dict[str, Any]:
        """Get a specific environment."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/environments/{environment_id}")