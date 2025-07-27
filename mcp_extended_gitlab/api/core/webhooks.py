"""GitLab Webhooks API - HTTP callback management.

This module provides comprehensive access to GitLab's webhooks features,
enabling management of project, group, and system hooks for event notifications.
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
    """Register all Webhooks API tools.
    
    This function registers the following tools:
    - Project webhook CRUD operations
    - Group webhook CRUD operations
    - System webhook management
    - Webhook testing functionality
    """
    
    @mcp.tool()
    async def list_project_hooks(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """List project hooks."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/hooks")

    @mcp.tool()
    async def get_project_hook(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        hook_id: str = Field(description="The ID of a project hook")
    ) -> Dict[str, Any]:
        """Get project hook."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/hooks/{hook_id}")

    @mcp.tool()
    async def add_project_hook(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        url: str = Field(description="The URL to which the hook will send HTTP POST requests"),
        push_events: Optional[bool] = Field(default=True, description="Trigger hook on push events"),
        issues_events: Optional[bool] = Field(default=False, description="Trigger hook on issues events"),
        confidential_issues_events: Optional[bool] = Field(default=False, description="Trigger hook on confidential issues events"),
        merge_requests_events: Optional[bool] = Field(default=False, description="Trigger hook on merge requests events"),
        tag_push_events: Optional[bool] = Field(default=False, description="Trigger hook on tag push events"),
        note_events: Optional[bool] = Field(default=False, description="Trigger hook on note events"),
        confidential_note_events: Optional[bool] = Field(default=False, description="Trigger hook on confidential note events"),
        job_events: Optional[bool] = Field(default=False, description="Trigger hook on job events"),
        pipeline_events: Optional[bool] = Field(default=False, description="Trigger hook on pipeline events"),
        wiki_page_events: Optional[bool] = Field(default=False, description="Trigger hook on wiki page events"),
        deployment_events: Optional[bool] = Field(default=False, description="Trigger hook on deployment events"),
        releases_events: Optional[bool] = Field(default=False, description="Trigger hook on release events"),
        subgroup_events: Optional[bool] = Field(default=False, description="Trigger hook on subgroup events"),
        enable_ssl_verification: Optional[bool] = Field(default=True, description="Do SSL verification when triggering the hook"),
        token: Optional[str] = Field(default=None, description="Secret token to validate received payloads"),
        push_events_branch_filter: Optional[str] = Field(default=None, description="Push events branch filter"),
        custom_webhook_template: Optional[str] = Field(default=None, description="Custom webhook template")
    ) -> Dict[str, Any]:
        """Add project hook."""
        client = await get_gitlab_client()
        data = {"url": url}
        for key, value in {
            "push_events": push_events,
            "issues_events": issues_events,
            "confidential_issues_events": confidential_issues_events,
            "merge_requests_events": merge_requests_events,
            "tag_push_events": tag_push_events,
            "note_events": note_events,
            "confidential_note_events": confidential_note_events,
            "job_events": job_events,
            "pipeline_events": pipeline_events,
            "wiki_page_events": wiki_page_events,
            "deployment_events": deployment_events,
            "releases_events": releases_events,
            "subgroup_events": subgroup_events,
            "enable_ssl_verification": enable_ssl_verification,
            "token": token,
            "push_events_branch_filter": push_events_branch_filter,
            "custom_webhook_template": custom_webhook_template
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/hooks", json_data=data)

    @mcp.tool()
    async def edit_project_hook(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        hook_id: str = Field(description="The ID of the project hook"),
        url: str = Field(description="The URL to which the hook will send HTTP POST requests"),
        push_events: Optional[bool] = Field(default=None, description="Trigger hook on push events"),
        issues_events: Optional[bool] = Field(default=None, description="Trigger hook on issues events"),
        confidential_issues_events: Optional[bool] = Field(default=None, description="Trigger hook on confidential issues events"),
        merge_requests_events: Optional[bool] = Field(default=None, description="Trigger hook on merge requests events"),
        tag_push_events: Optional[bool] = Field(default=None, description="Trigger hook on tag push events"),
        note_events: Optional[bool] = Field(default=None, description="Trigger hook on note events"),
        confidential_note_events: Optional[bool] = Field(default=None, description="Trigger hook on confidential note events"),
        job_events: Optional[bool] = Field(default=None, description="Trigger hook on job events"),
        pipeline_events: Optional[bool] = Field(default=None, description="Trigger hook on pipeline events"),
        wiki_page_events: Optional[bool] = Field(default=None, description="Trigger hook on wiki page events"),
        deployment_events: Optional[bool] = Field(default=None, description="Trigger hook on deployment events"),
        releases_events: Optional[bool] = Field(default=None, description="Trigger hook on release events"),
        subgroup_events: Optional[bool] = Field(default=None, description="Trigger hook on subgroup events"),
        enable_ssl_verification: Optional[bool] = Field(default=None, description="Do SSL verification when triggering the hook"),
        token: Optional[str] = Field(default=None, description="Secret token to validate received payloads"),
        push_events_branch_filter: Optional[str] = Field(default=None, description="Push events branch filter"),
        custom_webhook_template: Optional[str] = Field(default=None, description="Custom webhook template")
    ) -> Dict[str, Any]:
        """Edit project hook."""
        client = await get_gitlab_client()
        data = {"url": url}
        for key, value in {
            "push_events": push_events,
            "issues_events": issues_events,
            "confidential_issues_events": confidential_issues_events,
            "merge_requests_events": merge_requests_events,
            "tag_push_events": tag_push_events,
            "note_events": note_events,
            "confidential_note_events": confidential_note_events,
            "job_events": job_events,
            "pipeline_events": pipeline_events,
            "wiki_page_events": wiki_page_events,
            "deployment_events": deployment_events,
            "releases_events": releases_events,
            "subgroup_events": subgroup_events,
            "enable_ssl_verification": enable_ssl_verification,
            "token": token,
            "push_events_branch_filter": push_events_branch_filter,
            "custom_webhook_template": custom_webhook_template
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/hooks/{hook_id}", json_data=data)

    @mcp.tool()
    async def delete_project_hook(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        hook_id: str = Field(description="The ID of the project hook")
    ) -> Dict[str, Any]:
        """Delete project hook."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/hooks/{hook_id}")

    @mcp.tool()
    async def test_project_hook(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        hook_id: str = Field(description="The ID of the project hook")
    ) -> Dict[str, Any]:
        """Test project hook."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/hooks/{hook_id}/test/push_events")

    @mcp.tool()
    async def list_system_hooks() -> Dict[str, Any]:
        """List system hooks."""
        client = await get_gitlab_client()
        return await client.get("/hooks")

    @mcp.tool()
    async def add_new_system_hook(
        url: str = Field(description="The URL to do an HTTP POST request on"),
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
        hook_id: str = Field(description="The ID of the system hook")
    ) -> Dict[str, Any]:
        """Test system hook."""
        client = await get_gitlab_client()
        return await client.post(f"/hooks/{hook_id}")

    @mcp.tool()
    async def delete_system_hook(
        hook_id: str = Field(description="The ID of the system hook")
    ) -> Dict[str, Any]:
        """Delete system hook."""
        client = await get_gitlab_client()
        return await client.delete(f"/hooks/{hook_id}")

    @mcp.tool()
    async def list_group_hooks(
        group_id: str = Field(description="The ID or URL-encoded path of the group")
    ) -> Dict[str, Any]:
        """List group hooks."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/hooks")

    @mcp.tool()
    async def get_group_hook(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        hook_id: str = Field(description="The ID of a group hook")
    ) -> Dict[str, Any]:
        """Get group hook."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/hooks/{hook_id}")

    @mcp.tool()
    async def add_group_hook(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        url: str = Field(description="The URL to which the hook will send HTTP POST requests"),
        push_events: Optional[bool] = Field(default=True, description="Trigger hook on push events"),
        issues_events: Optional[bool] = Field(default=True, description="Trigger hook on issues events"),
        confidential_issues_events: Optional[bool] = Field(default=True, description="Trigger hook on confidential issues events"),
        merge_requests_events: Optional[bool] = Field(default=True, description="Trigger hook on merge requests events"),
        tag_push_events: Optional[bool] = Field(default=True, description="Trigger hook on tag push events"),
        note_events: Optional[bool] = Field(default=True, description="Trigger hook on note events"),
        job_events: Optional[bool] = Field(default=True, description="Trigger hook on job events"),
        pipeline_events: Optional[bool] = Field(default=True, description="Trigger hook on pipeline events"),
        wiki_page_events: Optional[bool] = Field(default=True, description="Trigger hook on wiki page events"),
        deployment_events: Optional[bool] = Field(default=True, description="Trigger hook on deployment events"),
        releases_events: Optional[bool] = Field(default=True, description="Trigger hook on release events"),
        subgroup_events: Optional[bool] = Field(default=True, description="Trigger hook on subgroup events"),
        enable_ssl_verification: Optional[bool] = Field(default=True, description="Do SSL verification when triggering the hook"),
        token: Optional[str] = Field(default=None, description="Secret token to validate received payloads"),
        push_events_branch_filter: Optional[str] = Field(default=None, description="Push events branch filter"),
        custom_webhook_template: Optional[str] = Field(default=None, description="Custom webhook template")
    ) -> Dict[str, Any]:
        """Add group hook."""
        client = await get_gitlab_client()
        data = {"url": url}
        for key, value in {
            "push_events": push_events,
            "issues_events": issues_events,
            "confidential_issues_events": confidential_issues_events,
            "merge_requests_events": merge_requests_events,
            "tag_push_events": tag_push_events,
            "note_events": note_events,
            "job_events": job_events,
            "pipeline_events": pipeline_events,
            "wiki_page_events": wiki_page_events,
            "deployment_events": deployment_events,
            "releases_events": releases_events,
            "subgroup_events": subgroup_events,
            "enable_ssl_verification": enable_ssl_verification,
            "token": token,
            "push_events_branch_filter": push_events_branch_filter,
            "custom_webhook_template": custom_webhook_template
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/groups/{group_id}/hooks", json_data=data)

    @mcp.tool()
    async def edit_group_hook(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        hook_id: str = Field(description="The ID of the group hook"),
        url: str = Field(description="The URL to which the hook will send HTTP POST requests"),
        push_events: Optional[bool] = Field(default=None, description="Trigger hook on push events"),
        issues_events: Optional[bool] = Field(default=None, description="Trigger hook on issues events"),
        confidential_issues_events: Optional[bool] = Field(default=None, description="Trigger hook on confidential issues events"),
        merge_requests_events: Optional[bool] = Field(default=None, description="Trigger hook on merge requests events"),
        tag_push_events: Optional[bool] = Field(default=None, description="Trigger hook on tag push events"),
        note_events: Optional[bool] = Field(default=None, description="Trigger hook on note events"),
        job_events: Optional[bool] = Field(default=None, description="Trigger hook on job events"),
        pipeline_events: Optional[bool] = Field(default=None, description="Trigger hook on pipeline events"),
        wiki_page_events: Optional[bool] = Field(default=None, description="Trigger hook on wiki page events"),
        deployment_events: Optional[bool] = Field(default=None, description="Trigger hook on deployment events"),
        releases_events: Optional[bool] = Field(default=None, description="Trigger hook on release events"),
        subgroup_events: Optional[bool] = Field(default=None, description="Trigger hook on subgroup events"),
        enable_ssl_verification: Optional[bool] = Field(default=None, description="Do SSL verification when triggering the hook"),
        token: Optional[str] = Field(default=None, description="Secret token to validate received payloads"),
        push_events_branch_filter: Optional[str] = Field(default=None, description="Push events branch filter"),
        custom_webhook_template: Optional[str] = Field(default=None, description="Custom webhook template")
    ) -> Dict[str, Any]:
        """Edit group hook."""
        client = await get_gitlab_client()
        data = {"url": url}
        for key, value in {
            "push_events": push_events,
            "issues_events": issues_events,
            "confidential_issues_events": confidential_issues_events,
            "merge_requests_events": merge_requests_events,
            "tag_push_events": tag_push_events,
            "note_events": note_events,
            "job_events": job_events,
            "pipeline_events": pipeline_events,
            "wiki_page_events": wiki_page_events,
            "deployment_events": deployment_events,
            "releases_events": releases_events,
            "subgroup_events": subgroup_events,
            "enable_ssl_verification": enable_ssl_verification,
            "token": token,
            "push_events_branch_filter": push_events_branch_filter,
            "custom_webhook_template": custom_webhook_template
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/groups/{group_id}/hooks/{hook_id}", json_data=data)

    @mcp.tool()
    async def delete_group_hook(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        hook_id: str = Field(description="The ID of the group hook")
    ) -> Dict[str, Any]:
        """Delete group hook."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/hooks/{hook_id}")

    @mcp.tool()
    async def test_group_hook(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        hook_id: str = Field(description="The ID of the group hook"),
        trigger: Optional[str] = Field(default="push_events", description="The trigger event type")
    ) -> Dict[str, Any]:
        """Test group hook."""
        client = await get_gitlab_client()
        return await client.post(f"/groups/{group_id}/hooks/{hook_id}/test/{trigger}")