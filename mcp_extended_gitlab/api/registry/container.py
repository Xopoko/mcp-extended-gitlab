"""GitLab Container Registry API - Container image management.

This module provides access to GitLab's container registry features,
enabling management of Docker container images and repositories.
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
    """Register all Container Registry API tools.
    
    This function registers the following tools:
    - Repository listing (project and group level)
    - Repository CRUD operations
    - Tag management and bulk operations
    - Registry event tracking
    """
    
    # Project-level container registry tools
    @mcp.tool()
    async def list_registry_repositories_in_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        tags: Optional[bool] = Field(default=False, description="If true, include tag information"),
        tags_count: Optional[bool] = Field(default=False, description="If true, include tags count"),
        name: Optional[str] = Field(default=None, description="Filter repositories by name"),
        sort: Optional[str] = Field(default="created_at", description="Sort field"),
        order: Optional[str] = Field(default="desc", description="Sort order"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List registry repositories in a project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "tags": tags,
            "tags_count": tags_count,
            "name": name,
            "sort": sort,
            "order": order,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/registry/repositories", params=params)

    @mcp.tool()
    async def get_details_of_registry_repository(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        repository_id: str = Field(description="The ID of registry repository"),
        tags: Optional[bool] = Field(default=False, description="If true, include tag information"),
        tags_count: Optional[bool] = Field(default=False, description="If true, include tags count")
    ) -> Dict[str, Any]:
        """Get details of a registry repository."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "tags": tags,
            "tags_count": tags_count
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/registry/repositories/{repository_id}", params=params)

    @mcp.tool()
    async def delete_registry_repository(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        repository_id: str = Field(description="The ID of registry repository")
    ) -> Dict[str, Any]:
        """Delete a registry repository."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/registry/repositories/{repository_id}")

    @mcp.tool()
    async def list_registry_repository_tags(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        repository_id: str = Field(description="The ID of registry repository"),
        name: Optional[str] = Field(default=None, description="Filter tags by name"),
        sort: Optional[str] = Field(default="name", description="Sort field"),
        order: Optional[str] = Field(default="asc", description="Sort order"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List tags of a registry repository."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "name": name,
            "sort": sort,
            "order": order,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/registry/repositories/{repository_id}/tags", params=params)

    @mcp.tool()
    async def get_details_of_registry_repository_tag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        repository_id: str = Field(description="The ID of registry repository"),
        tag_name: str = Field(description="The name of tag")
    ) -> Dict[str, Any]:
        """Get details of a registry repository tag."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/registry/repositories/{repository_id}/tags/{tag_name}")

    @mcp.tool()
    async def delete_registry_repository_tag(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        repository_id: str = Field(description="The ID of registry repository"),
        tag_name: str = Field(description="The name of tag")
    ) -> Dict[str, Any]:
        """Delete a registry repository tag."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/registry/repositories/{repository_id}/tags/{tag_name}")

    @mcp.tool()
    async def delete_registry_repository_tags_in_bulk(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        repository_id: str = Field(description="The ID of registry repository"),
        name_regex_delete: Optional[str] = Field(default=None, description="The tag name regexp to delete"),
        name_regex_keep: Optional[str] = Field(default=None, description="The tag name regexp to retain"),
        keep_n: Optional[int] = Field(default=None, description="The amount of latest tags to keep"),
        older_than: Optional[str] = Field(default=None, description="Tags to delete that are older than the given time")
    ) -> Dict[str, Any]:
        """Delete registry repository tags in bulk."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "name_regex_delete": name_regex_delete,
            "name_regex_keep": name_regex_keep,
            "keep_n": keep_n,
            "older_than": older_than
        }.items():
            if value is not None:
                data[key] = value
        return await client.delete(f"/projects/{project_id}/registry/repositories/{repository_id}/tags", json_data=data)

    # Group-level container registry tools
    @mcp.tool()
    async def list_registry_repositories_in_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        tags: Optional[bool] = Field(default=False, description="If true, include tag information"),
        tags_count: Optional[bool] = Field(default=False, description="If true, include tags count"),
        name: Optional[str] = Field(default=None, description="Filter repositories by name"),
        sort: Optional[str] = Field(default="created_at", description="Sort field"),
        order: Optional[str] = Field(default="desc", description="Sort order"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List registry repositories in a group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "tags": tags,
            "tags_count": tags_count,
            "name": name,
            "sort": sort,
            "order": order,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/registry/repositories", params=params)

    # Container registry events
    @mcp.tool()
    async def get_container_registry_events(
        target: Optional[str] = Field(default=None, description="Filter events by target"),
        action: Optional[str] = Field(default=None, description="Filter events by action"),
        from_date: Optional[str] = Field(default=None, description="Filter events from this date"),
        to_date: Optional[str] = Field(default=None, description="Filter events to this date"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Get container registry events."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "target": target,
            "action": action,
            "from": from_date,
            "to": to_date,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/admin/container_registry_events", params=params)