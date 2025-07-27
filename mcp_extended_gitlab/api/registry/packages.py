"""GitLab Package Registry API - Package management.

This module provides comprehensive access to GitLab's package registry features,
enabling management of various package types (NPM, Maven, PyPI, etc.).
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
    """Register all Package Registry API tools.
    
    This function registers the following tools:
    - Package listing at group and project levels
    - Package CRUD operations
    - Package file management
    """
    
    @mcp.tool()
    async def list_packages_within_group(
        group_id: str = Field(description="ID or URL-encoded path of the group"),
        exclude_subgroups: Optional[bool] = Field(default=False, description="If the parameter is included as true, packages from projects from subgroups are not listed"),
        order_by: Optional[str] = Field(default="created_at", description="The field to use as order"),
        sort: Optional[str] = Field(default="asc", description="The direction of the order"),
        package_type: Optional[str] = Field(default=None, description="Filter the returned packages by type"),
        package_name: Optional[str] = Field(default=None, description="Filter the project packages with a fuzzy search by name"),
        include_versionless: Optional[bool] = Field(default=False, description="When set to true, versionless packages are included in the response"),
        status: Optional[str] = Field(default=None, description="Filter the returned packages by status"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List packages within a group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "exclude_subgroups": exclude_subgroups,
            "order_by": order_by,
            "sort": sort,
            "package_type": package_type,
            "package_name": package_name,
            "include_versionless": include_versionless,
            "status": status,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/packages", params=params)

    @mcp.tool()
    async def list_packages_within_project(
        project_id: str = Field(description="ID or URL-encoded path of the project"),
        order_by: Optional[str] = Field(default="created_at", description="The field to use as order"),
        sort: Optional[str] = Field(default="asc", description="The direction of the order"),
        package_type: Optional[str] = Field(default=None, description="Filter the returned packages by type"),
        package_name: Optional[str] = Field(default=None, description="Filter the project packages with a fuzzy search by name"),
        include_versionless: Optional[bool] = Field(default=False, description="When set to true, versionless packages are included in the response"),
        status: Optional[str] = Field(default=None, description="Filter the returned packages by status"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List packages within a project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort,
            "package_type": package_type,
            "package_name": package_name,
            "include_versionless": include_versionless,
            "status": status,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/packages", params=params)

    @mcp.tool()
    async def get_project_package(
        project_id: str = Field(description="ID or URL-encoded path of the project"),
        package_id: str = Field(description="ID of a package")
    ) -> Dict[str, Any]:
        """Get a project package."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/packages/{package_id}")

    @mcp.tool()
    async def list_package_files(
        project_id: str = Field(description="ID or URL-encoded path of the project"),
        package_id: str = Field(description="ID of a package")
    ) -> Dict[str, Any]:
        """List package files."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/packages/{package_id}/package_files")

    @mcp.tool()
    async def delete_project_package(
        project_id: str = Field(description="ID or URL-encoded path of the project"),
        package_id: str = Field(description="ID of a package")
    ) -> Dict[str, Any]:
        """Delete a project package."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/packages/{package_id}")

    @mcp.tool()
    async def delete_package_file(
        project_id: str = Field(description="ID or URL-encoded path of the project"),
        package_id: str = Field(description="ID of a package"),
        package_file_id: str = Field(description="ID of a package file")
    ) -> Dict[str, Any]:
        """Delete a package file."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/packages/{package_id}/package_files/{package_file_id}")