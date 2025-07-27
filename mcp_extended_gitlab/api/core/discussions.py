"""GitLab Discussions API - Threaded conversations management.

This module provides comprehensive access to GitLab's discussions features,
enabling management of threaded conversations on issues, merge requests, and other resources.
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
    """Register all Discussions API tools.
    
    This function registers the following tools:
    - Issue discussions management
    - Merge request discussions management
    - Commit discussions management
    - Thread and note operations
    """
    
    @mcp.tool()
    async def list_issue_discussions(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List issue discussions."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/discussions", params=params)

    @mcp.tool()
    async def get_single_issue_discussion(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        discussion_id: str = Field(description="The ID of a discussion")
    ) -> Dict[str, Any]:
        """Get single issue discussion."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}")

    @mcp.tool()
    async def create_new_issue_thread(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        body: str = Field(description="The content of the thread"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted"),
        position: Optional[Dict[str, Any]] = Field(default=None, description="Position when creating a diff note")
    ) -> Dict[str, Any]:
        """Create new issue thread."""
        client = await get_gitlab_client()
        data = {"body": body}
        for key, value in {
            "created_at": created_at,
            "position": position
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/discussions", json_data=data)

    @mcp.tool()
    async def add_note_to_existing_issue_thread(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note"),
        body: str = Field(description="The content of the note/reply"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted")
    ) -> Dict[str, Any]:
        """Add note to existing issue thread."""
        client = await get_gitlab_client()
        data = {"body": body}
        if created_at:
            data["created_at"] = created_at
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/notes", json_data=data)

    @mcp.tool()
    async def modify_existing_issue_thread_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note"),
        body: str = Field(description="The content of the note/reply")
    ) -> Dict[str, Any]:
        """Modify existing issue thread note."""
        client = await get_gitlab_client()
        data = {"body": body}
        return await client.put(f"/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/notes/{note_id}", json_data=data)

    @mcp.tool()
    async def delete_issue_thread_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The IID of an issue"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note")
    ) -> Dict[str, Any]:
        """Delete issue thread note."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/notes/{note_id}")

    @mcp.tool()
    async def list_merge_request_discussions(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List merge request discussions."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/discussions", params=params)

    @mcp.tool()
    async def get_single_merge_request_discussion(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        discussion_id: str = Field(description="The ID of a discussion")
    ) -> Dict[str, Any]:
        """Get single merge request discussion."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/discussions/{discussion_id}")

    @mcp.tool()
    async def create_new_merge_request_thread(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        body: str = Field(description="The content of the thread"),
        commit_id: Optional[str] = Field(default=None, description="SHA referencing commit to start this thread on"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted"),
        position: Optional[Dict[str, Any]] = Field(default=None, description="Position when creating a diff note")
    ) -> Dict[str, Any]:
        """Create new merge request thread."""
        client = await get_gitlab_client()
        data = {"body": body}
        for key, value in {
            "commit_id": commit_id,
            "created_at": created_at,
            "position": position
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/discussions", json_data=data)

    @mcp.tool()
    async def resolve_merge_request_thread(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        discussion_id: str = Field(description="The ID of a thread"),
        resolved: bool = Field(description="Resolve/unresolve the discussion")
    ) -> Dict[str, Any]:
        """Resolve merge request thread."""
        client = await get_gitlab_client()
        data = {"resolved": resolved}
        return await client.put(f"/projects/{project_id}/merge_requests/{merge_request_iid}/discussions/{discussion_id}", json_data=data)

    @mcp.tool()
    async def add_note_to_existing_merge_request_thread(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note"),
        body: str = Field(description="The content of the note/reply"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted")
    ) -> Dict[str, Any]:
        """Add note to existing merge request thread."""
        client = await get_gitlab_client()
        data = {"body": body}
        if created_at:
            data["created_at"] = created_at
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/discussions/{discussion_id}/notes", json_data=data)

    @mcp.tool()
    async def modify_existing_merge_request_thread_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note"),
        body: str = Field(description="The content of the note/reply"),
        resolved: Optional[bool] = Field(default=None, description="Resolve/unresolve the discussion")
    ) -> Dict[str, Any]:
        """Modify existing merge request thread note."""
        client = await get_gitlab_client()
        data = {"body": body}
        if resolved is not None:
            data["resolved"] = resolved
        return await client.put(f"/projects/{project_id}/merge_requests/{merge_request_iid}/discussions/{discussion_id}/notes/{note_id}", json_data=data)

    @mcp.tool()
    async def delete_merge_request_thread_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The IID of a merge request"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note")
    ) -> Dict[str, Any]:
        """Delete merge request thread note."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/merge_requests/{merge_request_iid}/discussions/{discussion_id}/notes/{note_id}")

    @mcp.tool()
    async def list_commit_discussions(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        commit_id: str = Field(description="The ID of a commit"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List commit discussions."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/commits/{commit_id}/discussions", params=params)

    @mcp.tool()
    async def get_single_commit_discussion(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        commit_id: str = Field(description="The ID of a commit"),
        discussion_id: str = Field(description="The ID of a discussion")
    ) -> Dict[str, Any]:
        """Get single commit discussion."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/commits/{commit_id}/discussions/{discussion_id}")

    @mcp.tool()
    async def create_new_commit_thread(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        commit_id: str = Field(description="The ID of a commit"),
        body: str = Field(description="The content of the thread"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted"),
        position: Optional[Dict[str, Any]] = Field(default=None, description="Position when creating a diff note")
    ) -> Dict[str, Any]:
        """Create new commit thread."""
        client = await get_gitlab_client()
        data = {"body": body}
        for key, value in {
            "created_at": created_at,
            "position": position
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/commits/{commit_id}/discussions", json_data=data)

    @mcp.tool()
    async def add_note_to_existing_commit_thread(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        commit_id: str = Field(description="The ID of a commit"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note"),
        body: str = Field(description="The content of the note/reply"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted")
    ) -> Dict[str, Any]:
        """Add note to existing commit thread."""
        client = await get_gitlab_client()
        data = {"body": body}
        if created_at:
            data["created_at"] = created_at
        return await client.post(f"/projects/{project_id}/commits/{commit_id}/discussions/{discussion_id}/notes", json_data=data)

    @mcp.tool()
    async def modify_existing_commit_thread_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        commit_id: str = Field(description="The ID of a commit"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note"),
        body: str = Field(description="The content of the note/reply")
    ) -> Dict[str, Any]:
        """Modify existing commit thread note."""
        client = await get_gitlab_client()
        data = {"body": body}
        return await client.put(f"/projects/{project_id}/commits/{commit_id}/discussions/{discussion_id}/notes/{note_id}", json_data=data)

    @mcp.tool()
    async def delete_commit_thread_note(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        commit_id: str = Field(description="The ID of a commit"),
        discussion_id: str = Field(description="The ID of a thread"),
        note_id: str = Field(description="The ID of a thread note")
    ) -> Dict[str, Any]:
        """Delete a commit thread note."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/commits/{commit_id}/discussions/{discussion_id}/notes/{note_id}")