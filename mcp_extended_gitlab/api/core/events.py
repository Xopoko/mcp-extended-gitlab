"""GitLab Events API - Activity event tracking.

This module provides access to GitLab's events features,
enabling tracking of user activities and contributions.
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
    """Register all Events API tools.
    
    This function registers the following tools:
    - User event listing
    - Project event listing
    - Contribution event tracking
    """
    
    @mcp.tool()
    async def list_events(
        action: Optional[str] = Field(default=None, description="Include only events of a particular action type"),
        target_type: Optional[str] = Field(default=None, description="Include only events of a particular target type"),
        before: Optional[str] = Field(default=None, description="Include only events created before a particular date"),
        after: Optional[str] = Field(default=None, description="Include only events created after a particular date"),
        sort: Optional[str] = Field(default="desc", description="Sort events in asc or desc order by created_at"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List currently authenticated user's events."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "action": action,
            "target_type": target_type,
            "before": before,
            "after": after,
            "sort": sort,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/events", params=params)

    @mcp.tool()
    async def list_user_contribution_events(
        user_id: str = Field(description="The ID or username of the user"),
        action: Optional[str] = Field(default=None, description="Include only events of a particular action type"),
        target_type: Optional[str] = Field(default=None, description="Include only events of a particular target type"),
        before: Optional[str] = Field(default=None, description="Include only events created before a particular date"),
        after: Optional[str] = Field(default=None, description="Include only events created after a particular date"),
        sort: Optional[str] = Field(default="desc", description="Sort events in asc or desc order by created_at"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """Get user contribution events."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "action": action,
            "target_type": target_type,
            "before": before,
            "after": after,
            "sort": sort,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/users/{user_id}/events", params=params)

    @mcp.tool()
    async def list_project_events(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        action: Optional[str] = Field(default=None, description="Include only events of a particular action type"),
        target_type: Optional[str] = Field(default=None, description="Include only events of a particular target type"),
        before: Optional[str] = Field(default=None, description="Include only events created before a particular date"),
        after: Optional[str] = Field(default=None, description="Include only events created after a particular date"),
        sort: Optional[str] = Field(default="desc", description="Sort events in asc or desc order by created_at"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List project events."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "action": action,
            "target_type": target_type,
            "before": before,
            "after": after,
            "sort": sort,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/events", params=params)