"""GitLab Runners API - CI/CD runner management.

This module provides comprehensive access to GitLab's runners features,
enabling management of CI/CD runners at various levels (instance, group, project).
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
    """Register all Runners API tools.
    
    This function registers the following tools:
    - Runner listing and management
    - Runner job operations
    - Project and group runner associations
    """
    
    @mcp.tool()
    async def list_owned_runners(
        type: Optional[str] = Field(default=None, description="The type of runners to return"),
        status: Optional[str] = Field(default=None, description="The status of runners to return"),
        paused: Optional[bool] = Field(default=None, description="Whether to include only runners that are accepting or ignoring new jobs"),
        tag_list: Optional[List[str]] = Field(default=None, description="List of the runner's tags")) -> Dict[str, Any]:
        """List owned runners."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "type": type,
            "status": status,
            "paused": paused,
            "tag_list": tag_list
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/runners", params=params)

    @mcp.tool()
    async def list_all_runners(
        scope: Optional[str] = Field(default=None, description="Deprecated: Use type or status instead"),
        type: Optional[str] = Field(default=None, description="The type of runners to return"),
        status: Optional[str] = Field(default=None, description="The status of runners to return"),
        paused: Optional[bool] = Field(default=None, description="Whether to include only runners that are accepting or ignoring new jobs"),
        tag_list: Optional[List[str]] = Field(default=None, description="List of the runner's tags")) -> Dict[str, Any]:
        """List all runners (specific runners are listed if the user has admin privileges)."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "scope": scope,
            "type": type,
            "status": status,
            "paused": paused,
            "tag_list": tag_list
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/runners/all", params=params)

    @mcp.tool()
    async def get_runner_details(
        runner_id: str = Field(description="The ID of a runner")) -> Dict[str, Any]:
        """Get runner's details."""
        client = await get_gitlab_client()
        return await client.get(f"/runners/{runner_id}")

    @mcp.tool()
    async def update_runner_details(
        runner_id: str = Field(description="The ID of a runner"),
        description: Optional[str] = Field(default=None, description="The description of a runner"),
        active: Optional[bool] = Field(default=None, description="The state of a runner; can be set to true or false"),
        paused: Optional[bool] = Field(default=None, description="Whether the runner should ignore new jobs"),
        tag_list: Optional[List[str]] = Field(default=None, description="The list of tags for a runner"),
        run_untagged: Optional[bool] = Field(default=None, description="Flag indicating the runner can execute untagged jobs"),
        locked: Optional[bool] = Field(default=None, description="Flag indicating the runner is locked"),
        access_level: Optional[str] = Field(default=None, description="The access_level of the runner"),
        maximum_timeout: Optional[int] = Field(default=None, description="Maximum timeout set when this runner handles the job")) -> Dict[str, Any]:
        """Update runner's details."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "description": description,
            "active": active,
            "paused": paused,
            "tag_list": tag_list,
            "run_untagged": run_untagged,
            "locked": locked,
            "access_level": access_level,
            "maximum_timeout": maximum_timeout
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/runners/{runner_id}", json_data=data)

    @mcp.tool()
    async def delete_runner(
        runner_id: str = Field(description="The ID of a runner")) -> Dict[str, Any]:
        """Delete a runner."""
        client = await get_gitlab_client()
        return await client.delete(f"/runners/{runner_id}")

    @mcp.tool()
    async def list_runner_jobs(
        runner_id: str = Field(description="The ID of a runner"),
        status: Optional[str] = Field(default=None, description="Status of the job"),
        order_by: Optional[str] = Field(default="id", description="Order jobs by field"),
        sort: Optional[str] = Field(default="desc", description="Sort jobs in asc or desc order")) -> Dict[str, Any]:
        """List runner's jobs."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "status": status,
            "order_by": order_by,
            "sort": sort
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/runners/{runner_id}/jobs", params=params)

    @mcp.tool()
    async def list_project_runners(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        scope: Optional[str] = Field(default=None, description="Deprecated: Use type or status instead"),
        type: Optional[str] = Field(default=None, description="The type of runners to return"),
        status: Optional[str] = Field(default=None, description="The status of runners to return"),
        paused: Optional[bool] = Field(default=None, description="Whether to include only runners that are accepting or ignoring new jobs"),
        tag_list: Optional[List[str]] = Field(default=None, description="List of the runner's tags")) -> Dict[str, Any]:
        """List project's runners."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "scope": scope,
            "type": type,
            "status": status,
            "paused": paused,
            "tag_list": tag_list
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/runners", params=params)

    @mcp.tool()
    async def enable_runner_in_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        runner_id: str = Field(description="The ID of a runner")) -> Dict[str, Any]:
        """Enable a runner in project."""
        client = await get_gitlab_client()
        data = {"runner_id": runner_id}
        return await client.post(f"/projects/{project_id}/runners", json_data=data)

    @mcp.tool()
    async def disable_runner_from_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        runner_id: str = Field(description="The ID of a runner")) -> Dict[str, Any]:
        """Disable a runner from project."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/runners/{runner_id}")

    @mcp.tool()
    async def list_group_runners(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        type: Optional[str] = Field(default=None, description="The type of runners to return"),
        status: Optional[str] = Field(default=None, description="The status of runners to return"),
        paused: Optional[bool] = Field(default=None, description="Whether to include only runners that are accepting or ignoring new jobs"),
        tag_list: Optional[List[str]] = Field(default=None, description="List of the runner's tags")) -> Dict[str, Any]:
        """List group's runners."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "type": type,
            "status": status,
            "paused": paused,
            "tag_list": tag_list
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/runners", params=params)