"""GitLab Wikis API - Project wiki management.

This module provides comprehensive access to GitLab's wiki features,
including creating, reading, updating, and deleting wiki pages.
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
    """Register all Wikis API tools.
    
    This function registers the following tools:
    - Wiki page listing
    - Wiki page CRUD operations
    - Wiki attachments
    """
    
    @mcp.tool()
    async def list_wiki_pages(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        with_content: Optional[bool] = Field(default=False, description="Include page content in response")) -> Dict[str, Any]:
        """List all wiki pages."""
        client = await get_gitlab_client()
        params = {}
        if with_content is not None:
            params["with_content"] = with_content
        return await client.get(f"/projects/{project_id}/wikis", params=params)

    @mcp.tool()
    async def get_wiki_page(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        slug: str = Field(description="URL-encoded slug (a unique string) of the wiki page"),
        version: Optional[str] = Field(default=None, description="Wiki page version sha"),
        render_html: Optional[bool] = Field(default=False, description="Return the rendered HTML of the wiki page")) -> Dict[str, Any]:
        """Get a wiki page."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "version": version,
            "render_html": render_html
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/wikis/{slug}", params=params)

    @mcp.tool()
    async def create_wiki_page(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        title: str = Field(description="The title of a wiki page"),
        content: str = Field(description="The content of a wiki page"),
        format: Optional[str] = Field(default="markdown", description="The format of the wiki page. Available formats are: markdown (default), rdoc, asciidoc and org")) -> Dict[str, Any]:
        """Create a new wiki page."""
        client = await get_gitlab_client()
        data = {
            "title": title,
            "content": content,
            "format": format
        }
        return await client.post(f"/projects/{project_id}/wikis", json_data=data)

    @mcp.tool()
    async def edit_existing_wiki_page(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        slug: str = Field(description="URL-encoded slug (a unique string) of the wiki page"),
        title: Optional[str] = Field(default=None, description="The title of a wiki page"),
        content: Optional[str] = Field(default=None, description="The content of a wiki page"),
        format: Optional[str] = Field(default=None, description="The format of the wiki page")) -> Dict[str, Any]:
        """Edit an existing wiki page."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "title": title,
            "content": content,
            "format": format
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/wikis/{slug}", json_data=data)

    @mcp.tool()
    async def delete_wiki_page(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        slug: str = Field(description="URL-encoded slug (a unique string) of the wiki page")) -> Dict[str, Any]:
        """Delete a wiki page."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/wikis/{slug}")

    @mcp.tool()
    async def upload_attachment_to_wiki_repository(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_path: str = Field(description="Path to the file to upload"),
        branch: Optional[str] = Field(default="master", description="The name of the branch")) -> Dict[str, Any]:
        """Upload an attachment to the wiki repository."""
        client = await get_gitlab_client()
        data = {}
        if branch:
            data["branch"] = branch
        # Note: File upload would need special handling in real implementation
        return await client.post(f"/projects/{project_id}/wikis/attachments", data={"file": file_path, **data})