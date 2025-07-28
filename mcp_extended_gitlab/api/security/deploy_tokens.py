"""GitLab Deploy Tokens API - Deploy token management.

This module provides access to GitLab's deploy tokens,
enabling automated deployment authentication for projects and groups.
"""

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
    """Register all Deploy Tokens API tools.
    
    This function registers the following tools:
    - Deploy token listing (system, project, and group level)
    - Deploy token CRUD operations
    - Token management and revocation
    """
    
    @mcp.tool()
    async def list_all_deploy_tokens() -> Dict[str, Any]:
        """List all deploy tokens."""
        client = await get_gitlab_client()
        return await client.get("/deploy_tokens")

    # Project-level deploy tokens
    @mcp.tool()
    async def list_project_deploy_tokens(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        active: Optional[bool] = Field(default=None, description="Limit by active status")) -> Dict[str, Any]:
        """List project deploy tokens."""
        client = await get_gitlab_client()
        params = {}
        if active is not None:
            params["active"] = active
        return await client.get(f"/projects/{project_id}/deploy_tokens", params=params)

    @mcp.tool()
    async def get_single_project_deploy_token(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        token_id: str = Field(description="The ID of the deploy token")) -> Dict[str, Any]:
        """Get a single project deploy token."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/deploy_tokens/{token_id}")

    @mcp.tool()
    async def create_project_deploy_token(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the deploy token"),
        scopes: List[str] = Field(description="Indicates the deploy token scopes"),
        expires_at: Optional[str] = Field(default=None, description="Expiration date of the deploy token (ISO 8601)"),
        username: Optional[str] = Field(default=None, description="A username for the deploy token")) -> Dict[str, Any]:
        """Create a project deploy token."""
        client = await get_gitlab_client()
        data = {
            "name": name,
            "scopes": scopes
        }
        for key, value in {
            "expires_at": expires_at,
            "username": username
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/deploy_tokens", json_data=data)

    @mcp.tool()
    async def delete_project_deploy_token(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        token_id: str = Field(description="The ID of the deploy token")) -> Dict[str, Any]:
        """Delete a project deploy token."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/deploy_tokens/{token_id}")

    # Group-level deploy tokens
    @mcp.tool()
    async def list_group_deploy_tokens(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        active: Optional[bool] = Field(default=None, description="Limit by active status")) -> Dict[str, Any]:
        """List group deploy tokens."""
        client = await get_gitlab_client()
        params = {}
        if active is not None:
            params["active"] = active
        return await client.get(f"/groups/{group_id}/deploy_tokens", params=params)

    @mcp.tool()
    async def get_single_group_deploy_token(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        token_id: str = Field(description="The ID of the deploy token")) -> Dict[str, Any]:
        """Get a single group deploy token."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/deploy_tokens/{token_id}")

    @mcp.tool()
    async def create_group_deploy_token(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        name: str = Field(description="The name of the deploy token"),
        scopes: List[str] = Field(description="Indicates the deploy token scopes"),
        expires_at: Optional[str] = Field(default=None, description="Expiration date of the deploy token (ISO 8601)"),
        username: Optional[str] = Field(default=None, description="A username for the deploy token")) -> Dict[str, Any]:
        """Create a group deploy token."""
        client = await get_gitlab_client()
        data = {
            "name": name,
            "scopes": scopes
        }
        for key, value in {
            "expires_at": expires_at,
            "username": username
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/groups/{group_id}/deploy_tokens", json_data=data)

    @mcp.tool()
    async def delete_group_deploy_token(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        token_id: str = Field(description="The ID of the deploy token")) -> Dict[str, Any]:
        """Delete a group deploy token."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/deploy_tokens/{token_id}")