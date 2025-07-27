"""GitLab Search API - Global and scoped search functionality.

This module provides comprehensive access to GitLab's search features,
enabling searching across various resources at global, group, and project levels.
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
    """Register all Search API tools.
    
    This function registers the following tools:
    - Global search across GitLab
    - Group-scoped search
    - Project-scoped search
    """
    
    @mcp.tool()
    async def search_globally(
        scope: str = Field(description="The scope to search in"),
        search: str = Field(description="The search query"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Search globally across GitLab."""
        client = await get_gitlab_client()
        params = {
            "scope": scope,
            "search": search
        }
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/search", params=params)

    @mcp.tool()
    async def search_within_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        scope: str = Field(description="The scope to search in"),
        search: str = Field(description="The search query"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Search within a specific group."""
        client = await get_gitlab_client()
        params = {
            "scope": scope,
            "search": search
        }
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/search", params=params)

    @mcp.tool()
    async def search_within_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        scope: str = Field(description="The scope to search in"),
        search: str = Field(description="The search query"),
        ref: Optional[str] = Field(default=None, description="The name of a repository branch or tag to search on"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Search within a specific project."""
        client = await get_gitlab_client()
        params = {
            "scope": scope,
            "search": search
        }
        for key, value in {
            "ref": ref,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/search", params=params)