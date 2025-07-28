"""GitLab Deployments API - Deployment tracking and management.

This module provides access to GitLab's deployment features,
enabling tracking and management of application deployments.
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
    """Register all Deployments API tools.
    
    This function registers the following tools:
    - Deployment listing and filtering
    - Deployment CRUD operations
    - Deployment status management
    - Deployment approval workflows
    - Associated merge requests
    """
    
    @mcp.tool()
    async def list_project_deployments(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        order_by: Optional[str] = Field(default="id", description="Return deployments ordered by id or iid or created_at or updated_at or ref fields"),
        sort: Optional[str] = Field(default="asc", description="Return deployments sorted in asc or desc order"),
        finished_after: Optional[str] = Field(default=None, description="Return deployments finished after the specified date"),
        finished_before: Optional[str] = Field(default=None, description="Return deployments finished before the specified date"),
        environment: Optional[str] = Field(default=None, description="The name of the environment to filter deployments by"),
        status: Optional[str] = Field(default=None, description="The status to filter deployments by"),
        updated_after: Optional[str] = Field(default=None, description="Return deployments updated after the specified date"),
        updated_before: Optional[str] = Field(default=None, description="Return deployments updated before the specified date"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List project deployments."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort,
            "finished_after": finished_after,
            "finished_before": finished_before,
            "environment": environment,
            "status": status,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/deployments", params=params)

    @mcp.tool()
    async def get_single_deployment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        deployment_id: str = Field(description="The ID of the deployment")) -> Dict[str, Any]:
        """Get a single deployment."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/deployments/{deployment_id}")

    @mcp.tool()
    async def create_deployment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        environment: str = Field(description="The name of the environment to deploy to"),
        sha: str = Field(description="The SHA of the commit that is deployed"),
        ref: str = Field(description="The name of the branch or tag that is deployed"),
        tag: Optional[bool] = Field(default=False, description="A boolean that indicates if the deployed ref is a tag"),
        status: Optional[str] = Field(default="created", description="The status to filter deployments by")) -> Dict[str, Any]:
        """Create a deployment."""
        client = await get_gitlab_client()
        data = {
            "environment": environment,
            "sha": sha,
            "ref": ref
        }
        for key, value in {
            "tag": tag,
            "status": status
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/deployments", json_data=data)

    @mcp.tool()
    async def update_deployment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        deployment_id: str = Field(description="The ID of the deployment"),
        status: str = Field(description="The new status of the deployment")) -> Dict[str, Any]:
        """Update a deployment."""
        client = await get_gitlab_client()
        data = {"status": status}
        return await client.put(f"/projects/{project_id}/deployments/{deployment_id}", json_data=data)

    @mcp.tool()
    async def delete_deployment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        deployment_id: str = Field(description="The ID of the deployment")) -> Dict[str, Any]:
        """Delete a deployment."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/deployments/{deployment_id}")

    @mcp.tool()
    async def list_deployment_merge_requests(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        deployment_id: str = Field(description="The ID of the deployment")) -> Dict[str, Any]:
        """List merge requests associated with a deployment."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/deployments/{deployment_id}/merge_requests")

    @mcp.tool()
    async def approve_blocked_deployment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        deployment_id: str = Field(description="The ID of the deployment"),
        status: str = Field(description="The status of the approval (approved or rejected)"),
        comment: Optional[str] = Field(default=None, description="A comment to associate with the manual approval"),
        represented_as: Optional[str] = Field(default=None, description="The name of the User/Group/Role to use for the approval")) -> Dict[str, Any]:
        """Approve or reject a blocked deployment."""
        client = await get_gitlab_client()
        data = {"status": status}
        for key, value in {
            "comment": comment,
            "represented_as": represented_as
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/deployments/{deployment_id}/approval", json_data=data)

    @mcp.tool()
    async def list_merge_requests_for_deployment(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        deployment_id: str = Field(description="The ID of the deployment"),
        environment: Optional[str] = Field(default=None, description="The name of the environment")) -> Dict[str, Any]:
        """List the merge requests associated with a deployment."""
        client = await get_gitlab_client()
        params = {}
        if environment is not None:
            params["environment"] = environment
        return await client.get(f"/projects/{project_id}/deployments/{deployment_id}/merge_requests", params=params)