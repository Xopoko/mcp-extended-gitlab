"""GitLab Integrations API - Third-party service integrations.

This module provides access to GitLab's integrations features,
enabling management of external service integrations.
"""

from typing import Any, Dict
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
    """Register all Integrations API tools.
    
    This function registers the following tools:
    - Integration listing
    - Integration configuration
    - Integration activation/deactivation
    """
    
    @mcp.tool()
    async def list_project_integrations(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """List project integrations."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/integrations")

    @mcp.tool()
    async def get_project_integration(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        integration: str = Field(description="The name of the integration")
    ) -> Dict[str, Any]:
        """Get project integration."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/integrations/{integration}")

    @mcp.tool()
    async def activate_integration(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        integration: str = Field(description="The name of the integration"),
        **kwargs
    ) -> Dict[str, Any]:
        """Activate a project integration."""
        client = await get_gitlab_client()
        return await client.put(f"/projects/{project_id}/integrations/{integration}", json_data=kwargs)

    @mcp.tool()
    async def disable_integration(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        integration: str = Field(description="The name of the integration")
    ) -> Dict[str, Any]:
        """Disable a project integration."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/integrations/{integration}")