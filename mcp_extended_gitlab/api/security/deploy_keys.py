"""GitLab Deploy Keys API - SSH key management for deployments.

This module provides comprehensive access to GitLab's deploy keys features,
enabling management of read-only SSH keys for repository access.
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
    """Register all Deploy Keys API tools.
    
    This function registers the following tools:
    - Deploy key listing and management
    - Deploy key CRUD operations
    - Deploy key enable/disable functionality
    """
    
    @mcp.tool()
    async def list_all_deploy_keys() -> Dict[str, Any]:
        """List all deploy keys for the authenticated user."""
        client = await get_gitlab_client()
        return await client.get("/deploy_keys")

    @mcp.tool()
    async def list_project_deploy_keys(
        project_id: str = Field(description="The ID or URL-encoded path of the project")) -> Dict[str, Any]:
        """List project deploy keys."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/deploy_keys")

    @mcp.tool()
    async def get_single_deploy_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key_id: str = Field(description="The ID of the deploy key")) -> Dict[str, Any]:
        """Get a single deploy key."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/deploy_keys/{key_id}")

    @mcp.tool()
    async def add_deploy_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        title: str = Field(description="New deploy key's title"),
        key: str = Field(description="New deploy key"),
        can_push: Optional[bool] = Field(default=False, description="Can deploy key push to the project's repository")) -> Dict[str, Any]:
        """Add a deploy key."""
        client = await get_gitlab_client()
        data = {
            "title": title,
            "key": key,
            "can_push": can_push
        }
        return await client.post(f"/projects/{project_id}/deploy_keys", json_data=data)

    @mcp.tool()
    async def update_deploy_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key_id: str = Field(description="The ID of the deploy key"),
        title: Optional[str] = Field(default=None, description="New deploy key's title"),
        can_push: Optional[bool] = Field(default=None, description="Can deploy key push to the project's repository")) -> Dict[str, Any]:
        """Update a deploy key."""
        client = await get_gitlab_client()
        data = {}
        for key_name, value in {
            "title": title,
            "can_push": can_push
        }.items():
            if value is not None:
                data[key_name] = value
        return await client.put(f"/projects/{project_id}/deploy_keys/{key_id}", json_data=data)

    @mcp.tool()
    async def delete_deploy_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key_id: str = Field(description="The ID of the deploy key")) -> Dict[str, Any]:
        """Delete a deploy key."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/deploy_keys/{key_id}")

    @mcp.tool()
    async def enable_deploy_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key_id: str = Field(description="The ID of the deploy key")) -> Dict[str, Any]:
        """Enable a deploy key."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/deploy_keys/{key_id}/enable")

    @mcp.tool()
    async def disable_deploy_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key_id: str = Field(description="The ID of the deploy key")) -> Dict[str, Any]:
        """Disable a deploy key."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/deploy_keys/{key_id}/disable")