"""GitLab Todos API - Task management.

This module provides access to GitLab's todos features,
enabling management of personal task items and action reminders.
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
    """Register all Todos API tools.
    
    This function registers the following tools:
    - Todo listing and filtering
    - Todo completion management
    """
    
    @mcp.tool()
    async def list_todos(
        action: Optional[str] = Field(default=None, description="The action to be filtered"),
        author_id: Optional[int] = Field(default=None, description="The ID of an author"),
        project_id: Optional[int] = Field(default=None, description="The ID of a project"),
        group_id: Optional[int] = Field(default=None, description="The ID of a group"),
        state: Optional[str] = Field(default=None, description="The state of the todo"),
        type: Optional[str] = Field(default=None, description="The type of a todo"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """Get a list of todos."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "action": action,
            "author_id": author_id,
            "project_id": project_id,
            "group_id": group_id,
            "state": state,
            "type": type,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/todos", params=params)

    @mcp.tool()
    async def mark_todo_as_done(
        todo_id: str = Field(description="The ID of a todo")) -> Dict[str, Any]:
        """Mark a todo as done."""
        client = await get_gitlab_client()
        return await client.post(f"/todos/{todo_id}/mark_as_done")

    @mcp.tool()
    async def mark_all_todos_as_done() -> Dict[str, Any]:
        """Mark all todos as done."""
        client = await get_gitlab_client()
        return await client.post("/todos/mark_as_done")

    @mcp.tool()
    async def get_single_todo(
        todo_id: str = Field(description="The ID of a todo")) -> Dict[str, Any]:
        """Get a single todo."""
        client = await get_gitlab_client()
        return await client.get(f"/todos/{todo_id}")