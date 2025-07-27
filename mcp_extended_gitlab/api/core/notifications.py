"""GitLab Notifications API - Notification settings management.

This module provides access to GitLab's notification settings features,
enabling management of notification preferences at global, group, and project levels.
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
    """Register all Notifications API tools.
    
    This function registers the following tools:
    - Global notification settings management
    - Group notification settings
    - Project notification settings
    """
    
    @mcp.tool()
    async def get_notification_settings() -> Dict[str, Any]:
        """Get global notification settings."""
        client = await get_gitlab_client()
        return await client.get("/notification_settings")

    @mcp.tool()
    async def update_global_notification_settings(
        level: Optional[str] = Field(default=None, description="The global notification level"),
        notification_email: Optional[str] = Field(default=None, description="The email address to send notifications"),
        new_note: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        new_issue: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        reopen_issue: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        close_issue: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        reassign_issue: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        issue_due: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        new_merge_request: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        push_to_merge_request: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        reopen_merge_request: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        close_merge_request: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        reassign_merge_request: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        merge_merge_request: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        failed_pipeline: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        fixed_pipeline: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        success_pipeline: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        moved_project: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        merge_when_pipeline_succeeds: Optional[bool] = Field(default=None, description="Enable/disable this notification"),
        new_epic: Optional[bool] = Field(default=None, description="Enable/disable this notification")
    ) -> Dict[str, Any]:
        """Update global notification settings."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "level": level,
            "notification_email": notification_email,
            "new_note": new_note,
            "new_issue": new_issue,
            "reopen_issue": reopen_issue,
            "close_issue": close_issue,
            "reassign_issue": reassign_issue,
            "issue_due": issue_due,
            "new_merge_request": new_merge_request,
            "push_to_merge_request": push_to_merge_request,
            "reopen_merge_request": reopen_merge_request,
            "close_merge_request": close_merge_request,
            "reassign_merge_request": reassign_merge_request,
            "merge_merge_request": merge_merge_request,
            "failed_pipeline": failed_pipeline,
            "fixed_pipeline": fixed_pipeline,
            "success_pipeline": success_pipeline,
            "moved_project": moved_project,
            "merge_when_pipeline_succeeds": merge_when_pipeline_succeeds,
            "new_epic": new_epic
        }.items():
            if value is not None:
                data[key] = value
        return await client.put("/notification_settings", json_data=data)

    @mcp.tool()
    async def get_group_notification_settings(
        group_id: str = Field(description="The group ID or URL-encoded path")
    ) -> Dict[str, Any]:
        """Get group notification settings."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/notification_settings")

    @mcp.tool()
    async def get_project_notification_settings(
        project_id: str = Field(description="The project ID or URL-encoded path")
    ) -> Dict[str, Any]:
        """Get project notification settings."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/notification_settings")