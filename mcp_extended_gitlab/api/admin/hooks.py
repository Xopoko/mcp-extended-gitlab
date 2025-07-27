"""GitLab System Hooks API - System-wide webhook management.

This module provides access to GitLab's system hooks features,
enabling management of system-level webhooks.
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
    """Register all System Hooks API tools.
    
    This function registers the following tools:
    - System hook listing
    - System hook creation
    - System hook testing
    - System hook deletion
    """
    
    @mcp.tool()
    async def list_system_hooks() -> Dict[str, Any]:
        """List system hooks."""
        client = await get_gitlab_client()
        return await client.get("/hooks")

    @mcp.tool()
    async def add_new_system_hook(
        url: str = Field(description="The URL to do a POST request"),
        token: Optional[str] = Field(default=None, description="Secret token to validate received payloads"),
        push_events: Optional[bool] = Field(default=True, description="When true, the hook fires on push events"),
        tag_push_events: Optional[bool] = Field(default=True, description="When true, the hook fires on new tags being pushed"),
        merge_requests_events: Optional[bool] = Field(default=True, description="Trigger hook on merge requests events"),
        repository_update_events: Optional[bool] = Field(default=True, description="Trigger hook on repository update events"),
        enable_ssl_verification: Optional[bool] = Field(default=True, description="Do SSL verification when triggering the hook")
    ) -> Dict[str, Any]:
        """Add new system hook."""
        client = await get_gitlab_client()
        data = {"url": url}
        for key, value in {
            "token": token,
            "push_events": push_events,
            "tag_push_events": tag_push_events,
            "merge_requests_events": merge_requests_events,
            "repository_update_events": repository_update_events,
            "enable_ssl_verification": enable_ssl_verification
        }.items():
            if value is not None:
                data[key] = value
        return await client.post("/hooks", json_data=data)

    @mcp.tool()
    async def test_system_hook(
        hook_id: str = Field(description="The ID of the hook")
    ) -> Dict[str, Any]:
        """Test system hook."""
        client = await get_gitlab_client()
        return await client.post(f"/hooks/{hook_id}")

    @mcp.tool()
    async def delete_system_hook(
        hook_id: str = Field(description="The ID of the hook")
    ) -> Dict[str, Any]:
        """Delete system hook."""
        client = await get_gitlab_client()
        return await client.delete(f"/hooks/{hook_id}")