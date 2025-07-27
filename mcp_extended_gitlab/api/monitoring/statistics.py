"""GitLab Statistics API - System and resource statistics.

This module provides access to GitLab's statistics features,
enabling retrieval of system, project, and group statistics.
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
    """Register all Statistics API tools.
    
    This function registers the following tools:
    - Application statistics
    - Project statistics
    - Group statistics
    """
    
    @mcp.tool()
    async def get_gitlab_statistics() -> Dict[str, Any]:
        """Get application statistics."""
        client = await get_gitlab_client()
        return await client.get("/application/statistics")

    @mcp.tool()
    async def get_project_statistics(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Get project statistics."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/statistics")

    @mcp.tool()
    async def get_group_statistics(
        group_id: str = Field(description="The ID or URL-encoded path of the group")
    ) -> Dict[str, Any]:
        """Get group statistics."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/statistics")