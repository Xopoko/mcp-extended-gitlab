"""GitLab Snippets API - Code snippet management.

This module provides comprehensive access to GitLab's snippet features,
including both personal and project snippets for sharing code fragments.
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
    """Register all Snippets API tools.
    
    This function registers the following tools:
    - Personal snippet CRUD operations
    - Project snippet CRUD operations
    - Snippet content and repository access
    """
    
    @mcp.tool()
    async def list_all_snippets(
        created_after: Optional[str] = Field(default=None, description="Return snippets created after the specified date"),
        created_before: Optional[str] = Field(default=None, description="Return snippets created before the specified date"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List all public snippets."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "created_after": created_after,
            "created_before": created_before,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/snippets/public", params=params)

    @mcp.tool()
    async def list_snippets(
        created_after: Optional[str] = Field(default=None, description="Return snippets created after the specified date"),
        created_before: Optional[str] = Field(default=None, description="Return snippets created before the specified date"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List snippets for a user."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "created_after": created_after,
            "created_before": created_before,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/snippets", params=params)

    @mcp.tool()
    async def get_single_snippet(
        snippet_id: str = Field(description="The ID of a snippet")) -> Dict[str, Any]:
        """Get a single snippet."""
        client = await get_gitlab_client()
        return await client.get(f"/snippets/{snippet_id}")

    @mcp.tool()
    async def single_snippet_content(
        snippet_id: str = Field(description="The ID of a snippet")) -> Dict[str, Any]:
        """Get single snippet content."""
        client = await get_gitlab_client()
        return await client.get(f"/snippets/{snippet_id}/raw")

    @mcp.tool()
    async def create_snippet(
        title: str = Field(description="Title of a snippet"),
        visibility: str = Field(description="Snippet's visibility level"),
        files: List[Dict[str, str]] = Field(description="An array of snippet files"),
        description: Optional[str] = Field(default=None, description="Description of a snippet")) -> Dict[str, Any]:
        """Create new snippet."""
        client = await get_gitlab_client()
        data = {
            "title": title,
            "visibility": visibility,
            "files": files
        }
        if description:
            data["description"] = description
        return await client.post("/snippets", json_data=data)

    @mcp.tool()
    async def update_snippet(
        snippet_id: str = Field(description="The ID of a snippet"),
        title: Optional[str] = Field(default=None, description="Title of a snippet"),
        description: Optional[str] = Field(default=None, description="Description of a snippet"),
        visibility: Optional[str] = Field(default=None, description="Snippet's visibility level"),
        files: Optional[List[Dict[str, str]]] = Field(default=None, description="An array of snippet files")) -> Dict[str, Any]:
        """Update snippet."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "title": title,
            "description": description,
            "visibility": visibility,
            "files": files
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/snippets/{snippet_id}", json_data=data)

    @mcp.tool()
    async def delete_snippet(
        snippet_id: str = Field(description="The ID of a snippet")) -> Dict[str, Any]:
        """Delete snippet."""
        client = await get_gitlab_client()
        return await client.delete(f"/snippets/{snippet_id}")

    @mcp.tool()
    async def list_project_snippets(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List project snippets."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/snippets", params=params)

    @mcp.tool()
    async def get_single_project_snippet(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a project's snippet")) -> Dict[str, Any]:
        """Get a single project snippet."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/snippets/{snippet_id}")

    @mcp.tool()
    async def create_project_snippet(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        title: str = Field(description="Title of a snippet"),
        visibility: str = Field(description="Snippet's visibility level"),
        files: List[Dict[str, str]] = Field(description="An array of snippet files"),
        description: Optional[str] = Field(default=None, description="Description of a snippet")) -> Dict[str, Any]:
        """Create new project snippet."""
        client = await get_gitlab_client()
        data = {
            "title": title,
            "visibility": visibility,
            "files": files
        }
        if description:
            data["description"] = description
        return await client.post(f"/projects/{project_id}/snippets", json_data=data)

    @mcp.tool()
    async def update_project_snippet(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a project's snippet"),
        title: Optional[str] = Field(default=None, description="Title of a snippet"),
        description: Optional[str] = Field(default=None, description="Description of a snippet"),
        visibility: Optional[str] = Field(default=None, description="Snippet's visibility level"),
        files: Optional[List[Dict[str, str]]] = Field(default=None, description="An array of snippet files")) -> Dict[str, Any]:
        """Update project snippet."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "title": title,
            "description": description,
            "visibility": visibility,
            "files": files
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/snippets/{snippet_id}", json_data=data)

    @mcp.tool()
    async def delete_project_snippet(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a project's snippet")) -> Dict[str, Any]:
        """Delete project snippet."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/snippets/{snippet_id}")

    @mcp.tool()
    async def snippet_repository_file_content(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a project's snippet"),
        ref: str = Field(description="Reference to a tag or branch"),
        file_path: str = Field(description="URL-encoded path to the file")) -> Dict[str, Any]:
        """Get snippet repository file content."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/snippets/{snippet_id}/repository/files/{file_path}/raw?ref={ref}")