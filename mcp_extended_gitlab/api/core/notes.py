"""GitLab Notes API - Comments and discussions management.

This module provides comprehensive access to GitLab's notes (comments) features,
enabling management of discussions on issues, merge requests, and snippets.
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
    """Register all Notes/Comments API tools.
    
    This function registers the following tools:
    - Issue notes/comments CRUD operations
    - Merge request notes/comments CRUD operations
    - Snippet notes/comments CRUD operations
    """
    
    @mcp.tool()
    async def list_issue_notes(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        sort: Optional[str] = Field(default=None, description="Return issue notes sorted in asc or desc order"),
        order_by: Optional[str] = Field(default=None, description="Return issue notes ordered by created_at or updated_at fields"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List issue notes."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "sort": sort,
            "order_by": order_by,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/notes", params=params)

    @mcp.tool()
    async def get_single_issue_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        note_id: str = Field(description="The ID of an issue note")) -> Dict[str, Any]:
        """Get a single issue note."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/notes/{note_id}")

    @mcp.tool()
    async def create_new_issue_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        body: str = Field(description="The content of a note"),
        confidential: Optional[bool] = Field(default=None, description="The confidential flag of a note"),
        internal: Optional[bool] = Field(default=None, description="The internal flag of a note"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted")) -> Dict[str, Any]:
        """Create new issue note."""
        client = await get_gitlab_client()
        data = {"body": body}
        for key, value in {
            "confidential": confidential,
            "internal": internal,
            "created_at": created_at
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/notes", json_data=data)

    @mcp.tool()
    async def modify_existing_issue_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        note_id: str = Field(description="The ID of a note"),
        body: str = Field(description="The content of a note"),
        confidential: Optional[bool] = Field(default=None, description="The confidential flag of a note")) -> Dict[str, Any]:
        """Modify existing issue note."""
        client = await get_gitlab_client()
        data = {"body": body}
        if confidential is not None:
            data["confidential"] = confidential
        return await client.put(f"/projects/{project_id}/issues/{issue_iid}/notes/{note_id}", json_data=data)

    @mcp.tool()
    async def delete_issue_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        note_id: str = Field(description="The ID of a note")) -> Dict[str, Any]:
        """Delete an issue note."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/issues/{issue_iid}/notes/{note_id}")

    @mcp.tool()
    async def list_merge_request_notes(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        sort: Optional[str] = Field(default=None, description="Return merge request notes sorted in asc or desc order"),
        order_by: Optional[str] = Field(default=None, description="Return merge request notes ordered by created_at or updated_at fields"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List merge request notes."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "sort": sort,
            "order_by": order_by,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/notes", params=params)

    @mcp.tool()
    async def get_single_merge_request_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        note_id: str = Field(description="The ID of a merge request note")) -> Dict[str, Any]:
        """Get a single merge request note."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/notes/{note_id}")

    @mcp.tool()
    async def create_new_merge_request_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        body: str = Field(description="The content of a note"),
        internal: Optional[bool] = Field(default=None, description="The internal flag of a note"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted")) -> Dict[str, Any]:
        """Create new merge request note."""
        client = await get_gitlab_client()
        data = {"body": body}
        for key, value in {
            "internal": internal,
            "created_at": created_at
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/notes", json_data=data)

    @mcp.tool()
    async def modify_existing_merge_request_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        note_id: str = Field(description="The ID of a note"),
        body: str = Field(description="The content of a note")) -> Dict[str, Any]:
        """Modify existing merge request note."""
        client = await get_gitlab_client()
        data = {"body": body}
        return await client.put(f"/projects/{project_id}/merge_requests/{merge_request_iid}/notes/{note_id}", json_data=data)

    @mcp.tool()
    async def delete_merge_request_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        note_id: str = Field(description="The ID of a note")) -> Dict[str, Any]:
        """Delete a merge request note."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/merge_requests/{merge_request_iid}/notes/{note_id}")

    @mcp.tool()
    async def list_snippet_notes(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a snippet"),
        sort: Optional[str] = Field(default=None, description="Return snippet notes sorted in asc or desc order"),
        order_by: Optional[str] = Field(default=None, description="Return snippet notes ordered by created_at or updated_at fields"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List snippet notes."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "sort": sort,
            "order_by": order_by,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/snippets/{snippet_id}/notes", params=params)

    @mcp.tool()
    async def get_single_snippet_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a snippet"),
        note_id: str = Field(description="The ID of a snippet note")) -> Dict[str, Any]:
        """Get a single snippet note."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/snippets/{snippet_id}/notes/{note_id}")

    @mcp.tool()
    async def create_new_snippet_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a snippet"),
        body: str = Field(description="The content of a note"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted")) -> Dict[str, Any]:
        """Create new snippet note."""
        client = await get_gitlab_client()
        data = {"body": body}
        if created_at:
            data["created_at"] = created_at
        return await client.post(f"/projects/{project_id}/snippets/{snippet_id}/notes", json_data=data)

    @mcp.tool()
    async def modify_existing_snippet_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a snippet"),
        note_id: str = Field(description="The ID of a note"),
        body: str = Field(description="The content of a note")) -> Dict[str, Any]:
        """Modify existing snippet note."""
        client = await get_gitlab_client()
        data = {"body": body}
        return await client.put(f"/projects/{project_id}/snippets/{snippet_id}/notes/{note_id}", json_data=data)

    @mcp.tool()
    async def delete_snippet_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        snippet_id: str = Field(description="The ID of a snippet"),
        note_id: str = Field(description="The ID of a note")) -> Dict[str, Any]:
        """Delete a snippet note."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/snippets/{snippet_id}/notes/{note_id}")