"""GitLab Freeze Periods API - Deployment freeze management.

This module provides access to GitLab's freeze periods features,
enabling scheduled deployment restrictions for projects.
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
    """Register all Freeze Periods API tools.
    
    This function registers the following tools:
    - Freeze period listing
    - Freeze period CRUD operations
    - Cron-based freeze scheduling
    """
    
    @mcp.tool()
    async def list_freeze_periods(
        project_id: str = Field(description="The ID or URL-encoded path of the project")) -> Dict[str, Any]:
        """List freeze periods for a project."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/freeze_periods")

    @mcp.tool()
    async def get_single_freeze_period(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        freeze_period_id: str = Field(description="The ID of the freeze period")) -> Dict[str, Any]:
        """Get a single freeze period."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/freeze_periods/{freeze_period_id}")

    @mcp.tool()
    async def create_freeze_period(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        freeze_start: str = Field(description="Start of the freeze period in cron format"),
        freeze_end: str = Field(description="End of the freeze period in cron format"),
        cron_timezone: Optional[str] = Field(default=None, description="The timezone for the cron fields")) -> Dict[str, Any]:
        """Create a freeze period."""
        client = await get_gitlab_client()
        data = {
            "freeze_start": freeze_start,
            "freeze_end": freeze_end
        }
        if cron_timezone is not None:
            data["cron_timezone"] = cron_timezone
        return await client.post(f"/projects/{project_id}/freeze_periods", json_data=data)

    @mcp.tool()
    async def update_freeze_period(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        freeze_period_id: str = Field(description="The ID of the freeze period"),
        freeze_start: Optional[str] = Field(default=None, description="Start of the freeze period in cron format"),
        freeze_end: Optional[str] = Field(default=None, description="End of the freeze period in cron format"),
        cron_timezone: Optional[str] = Field(default=None, description="The timezone for the cron fields")) -> Dict[str, Any]:
        """Update a freeze period."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "freeze_start": freeze_start,
            "freeze_end": freeze_end,
            "cron_timezone": cron_timezone
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/freeze_periods/{freeze_period_id}", json_data=data)

    @mcp.tool()
    async def delete_freeze_period(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        freeze_period_id: str = Field(description="The ID of the freeze period")) -> Dict[str, Any]:
        """Delete a freeze period."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/freeze_periods/{freeze_period_id}")