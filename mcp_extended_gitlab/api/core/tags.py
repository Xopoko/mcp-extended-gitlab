"""GitLab Tags API - Git tag management.

This module provides comprehensive access to GitLab's tag features,
including creating, listing, and managing Git tags and associated releases.
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
    """Register all Tags API tools.
    
    This function registers the following tools:
    - Repository tag listing and search
    - Tag CRUD operations
    - Release creation and management for tags
    """
    
    @mcp.tool()
    async def list_project_repository_tags(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        order_by: Optional[str] = Field(default="updated", description="Return tags ordered by name or updated fields"),
        sort: Optional[str] = Field(default="desc", description="Return tags sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Return list of tags matching the search criteria"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List project repository tags."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort,
            "search": search,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/repository/tags", params=params)

    @mcp.tool()
    async def get_single_repository_tag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The name of the tag")
    ) -> Dict[str, Any]:
        """Get a single repository tag."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/repository/tags/{tag_name}")

    @mcp.tool()
    async def create_new_tag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The name of a tag"),
        ref: str = Field(description="Create tag using commit SHA, another tag name, or branch name"),
        message: Optional[str] = Field(default=None, description="Creates annotated tag"),
        release_description: Optional[str] = Field(default=None, description="Add release notes to the Git tag and store it in the GitLab database")
    ) -> Dict[str, Any]:
        """Create a new tag."""
        client = await get_gitlab_client()
        data = {
            "tag_name": tag_name,
            "ref": ref
        }
        for key, value in {
            "message": message,
            "release_description": release_description
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/repository/tags", json_data=data)

    @mcp.tool()
    async def delete_tag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The name of a tag")
    ) -> Dict[str, Any]:
        """Delete a tag."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/repository/tags/{tag_name}")

    @mcp.tool()
    async def create_new_release(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The name of a tag"),
        description: str = Field(description="Release notes with markdown support")
    ) -> Dict[str, Any]:
        """Create a new release."""
        client = await get_gitlab_client()
        data = {
            "tag_name": tag_name,
            "description": description
        }
        return await client.post(f"/projects/{project_id}/repository/tags/{tag_name}/release", json_data=data)

    @mcp.tool()
    async def update_release(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tag_name: str = Field(description="The name of a tag"),
        description: str = Field(description="Release notes with markdown support")
    ) -> Dict[str, Any]:
        """Update a release."""
        client = await get_gitlab_client()
        data = {"description": description}
        return await client.put(f"/projects/{project_id}/repository/tags/{tag_name}/release", json_data=data)