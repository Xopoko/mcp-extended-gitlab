"""GitLab Pipelines API - CI/CD pipeline management.

This module provides comprehensive access to GitLab's CI/CD pipeline features,
including pipeline creation, monitoring, retry/cancel operations, and test reports.
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
    """Register all Pipelines API tools.
    
    This function registers the following tools:
    - Pipeline listing and filtering
    - Pipeline CRUD operations
    - Pipeline status and variables
    - Test reports and summaries
    - Pipeline control (retry, cancel)
    """
    
    @mcp.tool()
    async def list_project_pipelines(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        scope: Optional[str] = Field(default=None, description="The scope of pipelines, one of: running, pending, finished, branches, tags"),
        status: Optional[str] = Field(default=None, description="The status of pipelines, one of: created, waiting_for_resource, preparing, pending, running, success, failed, canceled, skipped, manual, scheduled"),
        source: Optional[str] = Field(default=None, description="How the pipeline was triggered"),
        ref: Optional[str] = Field(default=None, description="The ref of pipelines"),
        sha: Optional[str] = Field(default=None, description="The SHA of pipelines"),
        yaml_errors: Optional[bool] = Field(default=None, description="Returns pipelines with invalid configurations"),
        username: Optional[str] = Field(default=None, description="The username of the user who triggered pipelines"),
        updated_after: Optional[str] = Field(default=None, description="Return pipelines updated after the specified date"),
        updated_before: Optional[str] = Field(default=None, description="Return pipelines updated before the specified date"),
        order_by: Optional[str] = Field(default="id", description="Order pipelines by id, status, ref, updated_at or user_id"),
        sort: Optional[str] = Field(default="desc", description="Sort pipelines in asc or desc order"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List project pipelines."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "scope": scope,
            "status": status,
            "source": source,
            "ref": ref,
            "sha": sha,
            "yaml_errors": yaml_errors,
            "username": username,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "order_by": order_by,
            "sort": sort,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/pipelines", params=params)

    @mcp.tool()
    async def get_single_pipeline(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        pipeline_id: str = Field(description="The ID of a pipeline")) -> Dict[str, Any]:
        """Get a single pipeline."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/pipelines/{pipeline_id}")

    @mcp.tool()
    async def get_pipeline_variables(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        pipeline_id: str = Field(description="The ID of a pipeline")) -> Dict[str, Any]:
        """Get variables of a pipeline."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/pipelines/{pipeline_id}/variables")

    @mcp.tool()
    async def get_pipeline_test_report(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        pipeline_id: str = Field(description="The ID of a pipeline")) -> Dict[str, Any]:
        """Get a pipeline's test report."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/pipelines/{pipeline_id}/test_report")

    @mcp.tool()
    async def get_pipeline_test_report_summary(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        pipeline_id: str = Field(description="The ID of a pipeline")) -> Dict[str, Any]:
        """Get a pipeline's test report summary."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/pipelines/{pipeline_id}/test_report_summary")

    @mcp.tool()
    async def create_pipeline(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        ref: str = Field(description="The branch or tag to run the pipeline on"),
        variables: Optional[List[Dict[str,
        str]]] = Field(default=None, description="An array containing the variables available in the pipeline")) -> Dict[str, Any]:
        """Create a new pipeline."""
        client = await get_gitlab_client()
        data = {"ref": ref}
        if variables:
            data["variables"] = variables
        return await client.post(f"/projects/{project_id}/pipeline", json_data=data)

    @mcp.tool()
    async def retry_jobs_in_pipeline(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        pipeline_id: str = Field(description="The ID of a pipeline")) -> Dict[str, Any]:
        """Retry jobs in a pipeline."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/pipelines/{pipeline_id}/retry")

    @mcp.tool()
    async def cancel_pipeline_jobs(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        pipeline_id: str = Field(description="The ID of a pipeline")) -> Dict[str, Any]:
        """Cancel a pipeline's jobs."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/pipelines/{pipeline_id}/cancel")

    @mcp.tool()
    async def delete_pipeline(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        pipeline_id: str = Field(description="The ID of a pipeline")) -> Dict[str, Any]:
        """Delete a pipeline."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/pipelines/{pipeline_id}")