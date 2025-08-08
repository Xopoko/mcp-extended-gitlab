"""GitLab Analytics API - DevOps and productivity analytics.

This module provides access to GitLab's analytics features,
including DORA metrics, issue analytics, and code review analytics.
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
    """Register all Analytics API tools.
    # Ensure tests using FastMCP can inspect tool names via mcp._tools
    try:
        if not hasattr(mcp, '_tools'):
            setattr(mcp, '_tools', {})  # type: ignore[attr-defined]
        _orig_tool = mcp.tool
        def _recording_tool(*dargs, **dkwargs):
            def _decorator(func):
                registered = _orig_tool(*dargs, **dkwargs)(func)
                try:
                    name = dkwargs.get('name') or func.__name__
                    mcp._tools[name] = func  # type: ignore[attr-defined]
                except Exception:
                    pass
                return registered
            return _decorator
        mcp.tool = _recording_tool  # type: ignore[assignment]
    except Exception:
        pass

    This function registers the following tools:
    - DORA metrics (project and group level)
    - Issue analytics
    - Merge request analytics
    - Repository analytics
    - Code review analytics
    """
    
    # DORA Metrics
    @mcp.tool()
    async def get_project_dora_metrics(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        metric: str = Field(description="The DORA metric type (deployment_frequency, lead_time_for_changes, time_to_restore_service, change_failure_rate)"),
        start_date: Optional[str] = Field(default=None, description="Date range to start from (ISO 8601 format)"),
        end_date: Optional[str] = Field(default=None, description="Date range to end at (ISO 8601 format)"),
        interval: Optional[str] = Field(default="all", description="The bucketing interval (all, monthly, daily)"),
        environment_tiers: Optional[List[str]] = Field(default=None, description="The tiers of the deployment environments")) -> Dict[str, Any]:
        """Get project-level DORA metrics."""
        client = await get_gitlab_client()
        params = {"metric": metric}
        for key, value in {
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval,
            "environment_tiers": environment_tiers
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/dora/metrics", params=params)

    @mcp.tool()
    async def get_group_dora_metrics(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        metric: str = Field(description="The DORA metric type (deployment_frequency, lead_time_for_changes, time_to_restore_service, change_failure_rate)"),
        start_date: Optional[str] = Field(default=None, description="Date range to start from (ISO 8601 format)"),
        end_date: Optional[str] = Field(default=None, description="Date range to end at (ISO 8601 format)"),
        interval: Optional[str] = Field(default="all", description="The bucketing interval (all, monthly, daily)"),
        environment_tiers: Optional[List[str]] = Field(default=None, description="The tiers of the deployment environments")) -> Dict[str, Any]:
        """Get group-level DORA metrics."""
        client = await get_gitlab_client()
        params = {"metric": metric}
        for key, value in {
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval,
            "environment_tiers": environment_tiers
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/dora/metrics", params=params)

    # Issue Analytics
    @mcp.tool()
    async def get_group_issue_analytics(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        issue_analytics_start_date: Optional[str] = Field(default=None, description="Date range to start from (ISO 8601 format)"),
        issue_analytics_end_date: Optional[str] = Field(default=None, description="Date range to end at (ISO 8601 format)")) -> Dict[str, Any]:
        """Get group issue analytics."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "issue_analytics_start_date": issue_analytics_start_date,
            "issue_analytics_end_date": issue_analytics_end_date
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/issues_analytics", params=params)

    @mcp.tool()
    async def get_project_issue_analytics(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_analytics_start_date: Optional[str] = Field(default=None, description="Date range to start from (ISO 8601 format)"),
        issue_analytics_end_date: Optional[str] = Field(default=None, description="Date range to end at (ISO 8601 format)")) -> Dict[str, Any]:
        """Get project issue analytics."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "issue_analytics_start_date": issue_analytics_start_date,
            "issue_analytics_end_date": issue_analytics_end_date
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/issues_analytics", params=params)

    # Merge Request Analytics
    @mcp.tool()
    async def get_group_merge_request_analytics(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        merge_request_analytics_start_date: Optional[str] = Field(default=None, description="Date range to start from (ISO 8601 format)"),
        merge_request_analytics_end_date: Optional[str] = Field(default=None, description="Date range to end at (ISO 8601 format)")) -> Dict[str, Any]:
        """Get group merge request analytics."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "merge_request_analytics_start_date": merge_request_analytics_start_date,
            "merge_request_analytics_end_date": merge_request_analytics_end_date
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/merge_requests_analytics", params=params)

    # Repository Analytics
    @mcp.tool()
    async def get_project_repository_analytics(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        from_date: Optional[str] = Field(default=None, description="Date range to start from (ISO 8601 format)"),
        to_date: Optional[str] = Field(default=None, description="Date range to end at (ISO 8601 format)")) -> Dict[str, Any]:
        """Get project repository analytics."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "from": from_date,
            "to": to_date
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/repository/analytics", params=params)

    # Code Review Analytics
    @mcp.tool()
    async def get_project_code_review_analytics(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        milestone_title: Optional[str] = Field(default=None, description="Filter results by milestone title"),
        label_name: Optional[List[str]] = Field(default=None, description="Filter results by label names"),
        from_date: Optional[str] = Field(default=None, description="Date range to start from (ISO 8601 format)"),
        to_date: Optional[str] = Field(default=None, description="Date range to end at (ISO 8601 format)")) -> Dict[str, Any]:
        """Get project code review analytics."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "milestone_title": milestone_title,
            "label_name": label_name,
            "from": from_date,
            "to": to_date
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/analytics/code_review", params=params)
