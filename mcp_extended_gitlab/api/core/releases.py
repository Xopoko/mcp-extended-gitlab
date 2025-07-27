"""GitLab Releases API - Software release management.

This module provides comprehensive access to GitLab's release management features,
including creating releases, managing release assets, and associating milestones.
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
    """Register all Releases API tools.
    
    This function registers the following tools:
    - Release listing and search
    - Release CRUD operations
    - Release asset management
    - Milestone associations
    """
    
    @mcp.tool()
    async def list_releases(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        order_by: Optional[str] = Field(default="created_at", description="The field to use as order. Either created_at or released_at"),
        sort: Optional[str] = Field(default="desc", description="The direction of the order. Either desc or asc"),
        include_html_description: Optional[bool] = Field(default=None, description="If true, a response includes HTML rendered markdown of the release description"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List releases."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort,
            "include_html_description": include_html_description,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/releases", params=params)

    @mcp.tool()
    async def get_release_by_tag_name(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The Git tag the release is associated with"),
        include_html_description: Optional[bool] = Field(default=None, description="If true, a response includes HTML rendered markdown of the release description")
    ) -> Dict[str, Any]:
        """Get a release by a tag name."""
        client = await get_gitlab_client()
        params = {}
        if include_html_description:
            params["include_html_description"] = include_html_description
        return await client.get(f"/projects/{project_id}/releases/{tag_name}", params=params)

    @mcp.tool()
    async def create_release(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The release name"),
        tag_name: str = Field(description="The tag where the release is created from"),
        description: str = Field(description="The description of the release"),
        ref: Optional[str] = Field(default=None, description="If a tag specified in tag_name doesn't exist, the release is created from ref and tagged with tag_name"),
        milestones: Optional[List[str]] = Field(default=None, description="The title of each milestone the release is associated with"),
        assets: Optional[Dict[str, Any]] = Field(default=None, description="An assets object"),
        released_at: Optional[str] = Field(default=None, description="The date when the release is/was ready")
    ) -> Dict[str, Any]:
        """Create a release."""
        client = await get_gitlab_client()
        data = {
            "name": name,
            "tag_name": tag_name,
            "description": description
        }
        for key, value in {
            "ref": ref,
            "milestones": milestones,
            "assets": assets,
            "released_at": released_at
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/releases", json_data=data)

    @mcp.tool()
    async def update_release(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The Git tag the release is associated with"),
        name: Optional[str] = Field(default=None, description="The release name"),
        description: Optional[str] = Field(default=None, description="The description of the release"),
        milestones: Optional[List[str]] = Field(default=None, description="The title of each milestone to associate with the release"),
        released_at: Optional[str] = Field(default=None, description="The date when the release is/was ready")
    ) -> Dict[str, Any]:
        """Update a release."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "name": name,
            "description": description,
            "milestones": milestones,
            "released_at": released_at
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/releases/{tag_name}", json_data=data)

    @mcp.tool()
    async def delete_release(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The Git tag the release is associated with")
    ) -> Dict[str, Any]:
        """Delete a release."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/releases/{tag_name}")