"""GitLab Error Tracking API - Error monitoring and management.

This module provides access to GitLab's error tracking features,
enabling monitoring, collection, and management of application errors.
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
    """Register all Error Tracking API tools.
    
    This function registers the following tools:
    - Error tracking settings management
    - Client key management
    - Error event collection
    - Error listing and status management
    - Error event details and stack traces
    """
    
    # Error Tracking Settings
    @mcp.tool()
    async def get_error_tracking_settings(
        project_id: str = Field(description="The ID or URL-encoded path of the project")) -> Dict[str, Any]:
        """Get error tracking settings for a project."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/error_tracking/settings")

    @mcp.tool()
    async def enable_or_disable_error_tracking(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        active: bool = Field(description="Pass true to enable the already configured error tracking settings"),
        api_url: Optional[str] = Field(default=None, description="The new API URL"),
        token: Optional[str] = Field(default=None, description="The new authentication token"),
        integrated: Optional[bool] = Field(default=None, description="Pass true to enable the integrated error tracking")) -> Dict[str, Any]:
        """Enable or disable the error tracking settings for a project."""
        client = await get_gitlab_client()
        data = {"active": active}
        for key, value in {
            "api_url": api_url,
            "token": token,
            "integrated": integrated
        }.items():
            if value is not None:
                data[key] = value
        return await client.patch(f"/projects/{project_id}/error_tracking/settings", json_data=data)

    # Error Tracking Client Keys
    @mcp.tool()
    async def list_project_client_keys(
        project_id: str = Field(description="The ID or URL-encoded path of the project")) -> Dict[str, Any]:
        """List project client keys."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/error_tracking/client_keys")

    @mcp.tool()
    async def create_client_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project")) -> Dict[str, Any]:
        """Create a client key."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/error_tracking/client_keys")

    @mcp.tool()
    async def delete_client_key(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key_id: str = Field(description="The ID of the client key")) -> Dict[str, Any]:
        """Delete a client key."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/error_tracking/client_keys/{key_id}")

    # Error Tracking Collector
    @mcp.tool()
    async def submit_error_tracking_event(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        event_data: Dict[str,
        Any] = Field(description="The error tracking event data")) -> Dict[str, Any]:
        """Submit an error tracking event."""
        client = await get_gitlab_client()
        return await client.post(f"/error_tracking/collector/api/{project_id}/store", json_data=event_data)

    @mcp.tool()
    async def get_error_tracking_collector_dsn(
        project_id: str = Field(description="The ID or URL-encoded path of the project")) -> Dict[str, Any]:
        """Get error tracking collector DSN."""
        client = await get_gitlab_client()
        return await client.get(f"/error_tracking/collector/api/{project_id}/envelope")

    # Integrated Error Tracking
    @mcp.tool()
    async def list_errors(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sort: Optional[str] = Field(default="last_seen", description="Sorts the results by the given field"),
        status: Optional[str] = Field(default=None, description="Searches for errors with the given status"),
        query: Optional[str] = Field(default=None, description="Searches for errors matching the given query"),
        cursor: Optional[str] = Field(default=None, description="Cursor for pagination"),
        limit: Optional[int] = Field(default=20, description="Number of errors to return")) -> Dict[str, Any]:
        """List errors for a project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "sort": sort,
            "status": status,
            "query": query,
            "cursor": cursor,
            "limit": limit
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/error_tracking/errors", params=params)

    @mcp.tool()
    async def get_error_details(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        fingerprint: str = Field(description="The error fingerprint")) -> Dict[str, Any]:
        """Get details of a specific error."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/error_tracking/errors/{fingerprint}")

    @mcp.tool()
    async def update_error_status(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        fingerprint: str = Field(description="The error fingerprint"),
        status: str = Field(description="The new status of the error (resolved, ignored, unresolved)")) -> Dict[str, Any]:
        """Update the status of an error."""
        client = await get_gitlab_client()
        data = {"status": status}
        return await client.put(f"/projects/{project_id}/error_tracking/errors/{fingerprint}", json_data=data)

    @mcp.tool()
    async def list_error_events(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        fingerprint: str = Field(description="The error fingerprint"),
        sort: Optional[str] = Field(default="occurred_at", description="Sorts the results by the given field"),
        cursor: Optional[str] = Field(default=None, description="Cursor for pagination"),
        limit: Optional[int] = Field(default=20, description="Number of events to return")) -> Dict[str, Any]:
        """List events for a specific error."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "sort": sort,
            "cursor": cursor,
            "limit": limit
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/error_tracking/errors/{fingerprint}/events", params=params)

    @mcp.tool()
    async def get_error_event_details(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        fingerprint: str = Field(description="The error fingerprint"),
        event_id: str = Field(description="The error event ID")) -> Dict[str, Any]:
        """Get details of a specific error event."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/error_tracking/errors/{fingerprint}/events/{event_id}")

    @mcp.tool()
    async def get_error_stack_trace(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        fingerprint: str = Field(description="The error fingerprint"),
        event_id: str = Field(description="The error event ID")) -> Dict[str, Any]:
        """Get stack trace of a specific error event."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/error_tracking/errors/{fingerprint}/events/{event_id}/stack_trace")