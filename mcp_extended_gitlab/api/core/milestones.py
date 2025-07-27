"""GitLab Milestones API - Project and group milestone management.

This module provides comprehensive access to GitLab's milestone features,
including project and group milestones, associated issues and merge requests.
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
    """Register all Milestones API tools.
    
    This function registers the following tools:
    - Project milestone CRUD operations
    - Group milestone CRUD operations
    - Milestone associations (issues, MRs)
    - Milestone promotion
    """
    
    @mcp.tool()
    async def list_project_milestones(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        iids: Optional[List[int]] = Field(default=None, description="Return only the milestones having the given iid"),
        state: Optional[str] = Field(default=None, description="Return only active or closed milestones"),
        title: Optional[str] = Field(default=None, description="Return only the milestones having the given title"),
        search: Optional[str] = Field(default=None, description="Return only milestones with a title or description matching the provided string"),
        include_parent_milestones: Optional[bool] = Field(default=None, description="Include group milestones from parent group and its ancestors"),
        updated_before: Optional[str] = Field(default=None, description="Return only milestones updated before the given datetime"),
        updated_after: Optional[str] = Field(default=None, description="Return only milestones updated after the given datetime"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List project milestones."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "iids": iids,
            "state": state,
            "title": title,
            "search": search,
            "include_parent_milestones": include_parent_milestones,
            "updated_before": updated_before,
            "updated_after": updated_after,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/milestones", params=params)

    @mcp.tool()
    async def get_single_milestone(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        milestone_id: str = Field(description="The ID of the project milestone")
    ) -> Dict[str, Any]:
        """Get single milestone."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/milestones/{milestone_id}")

    @mcp.tool()
    async def create_new_milestone(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        title: str = Field(description="The title of a milestone"),
        description: Optional[str] = Field(default=None, description="The description of the milestone"),
        due_date: Optional[str] = Field(default=None, description="The due date of the milestone"),
        start_date: Optional[str] = Field(default=None, description="The start date of the milestone")
    ) -> Dict[str, Any]:
        """Create a new milestone."""
        client = await get_gitlab_client()
        data = {"title": title}
        for key, value in {
            "description": description,
            "due_date": due_date,
            "start_date": start_date
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/milestones", json_data=data)

    @mcp.tool()
    async def edit_milestone(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        milestone_id: str = Field(description="The ID of the project milestone"),
        title: Optional[str] = Field(default=None, description="The title of a milestone"),
        description: Optional[str] = Field(default=None, description="The description of the milestone"),
        due_date: Optional[str] = Field(default=None, description="The due date of the milestone"),
        start_date: Optional[str] = Field(default=None, description="The start date of the milestone"),
        state_event: Optional[str] = Field(default=None, description="The state event of the milestone")
    ) -> Dict[str, Any]:
        """Edit milestone."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "title": title,
            "description": description,
            "due_date": due_date,
            "start_date": start_date,
            "state_event": state_event
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/milestones/{milestone_id}", json_data=data)

    @mcp.tool()
    async def delete_milestone(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        milestone_id: str = Field(description="The ID of the project milestone")
    ) -> Dict[str, Any]:
        """Delete milestone."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/milestones/{milestone_id}")

    @mcp.tool()
    async def get_all_issues_assigned_to_milestone(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        milestone_id: str = Field(description="The ID of the project milestone")
    ) -> Dict[str, Any]:
        """Get all issues assigned to a single milestone."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/milestones/{milestone_id}/issues")

    @mcp.tool()
    async def get_all_merge_requests_assigned_to_milestone(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        milestone_id: str = Field(description="The ID of the project milestone")
    ) -> Dict[str, Any]:
        """Get all merge requests assigned to a single milestone."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/milestones/{milestone_id}/merge_requests")

    @mcp.tool()
    async def promote_project_milestone_to_group_milestone(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        milestone_id: str = Field(description="The ID of the project milestone")
    ) -> Dict[str, Any]:
        """Promote project milestone to group milestone."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/milestones/{milestone_id}/promote")

    @mcp.tool()
    async def list_group_milestones(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        iids: Optional[List[int]] = Field(default=None, description="Return only the milestones having the given iid"),
        state: Optional[str] = Field(default=None, description="Return only active or closed milestones"),
        title: Optional[str] = Field(default=None, description="Return only the milestones having the given title"),
        search: Optional[str] = Field(default=None, description="Return only milestones with a title or description matching the provided string"),
        include_descendants: Optional[bool] = Field(default=None, description="Include milestones from descendant subgroups and projects"),
        updated_before: Optional[str] = Field(default=None, description="Return only milestones updated before the given datetime"),
        updated_after: Optional[str] = Field(default=None, description="Return only milestones updated after the given datetime"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List group milestones."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "iids": iids,
            "state": state,
            "title": title,
            "search": search,
            "include_descendants": include_descendants,
            "updated_before": updated_before,
            "updated_after": updated_after,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/milestones", params=params)

    @mcp.tool()
    async def get_single_group_milestone(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        milestone_id: str = Field(description="The ID of the group milestone")
    ) -> Dict[str, Any]:
        """Get single group milestone."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/milestones/{milestone_id}")

    @mcp.tool()
    async def create_new_group_milestone(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        title: str = Field(description="The title of a milestone"),
        description: Optional[str] = Field(default=None, description="The description of the milestone"),
        due_date: Optional[str] = Field(default=None, description="The due date of the milestone"),
        start_date: Optional[str] = Field(default=None, description="The start date of the milestone")
    ) -> Dict[str, Any]:
        """Create a new group milestone."""
        client = await get_gitlab_client()
        data = {"title": title}
        for key, value in {
            "description": description,
            "due_date": due_date,
            "start_date": start_date
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/groups/{group_id}/milestones", json_data=data)

    @mcp.tool()
    async def edit_group_milestone(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        milestone_id: str = Field(description="The ID of the group milestone"),
        title: Optional[str] = Field(default=None, description="The title of a milestone"),
        description: Optional[str] = Field(default=None, description="The description of the milestone"),
        due_date: Optional[str] = Field(default=None, description="The due date of the milestone"),
        start_date: Optional[str] = Field(default=None, description="The start date of the milestone"),
        state_event: Optional[str] = Field(default=None, description="The state event of the milestone")
    ) -> Dict[str, Any]:
        """Edit group milestone."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "title": title,
            "description": description,
            "due_date": due_date,
            "start_date": start_date,
            "state_event": state_event
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/groups/{group_id}/milestones/{milestone_id}", json_data=data)

    @mcp.tool()
    async def delete_group_milestone(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        milestone_id: str = Field(description="The ID of the group milestone")
    ) -> Dict[str, Any]:
        """Delete group milestone."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/milestones/{milestone_id}")

    @mcp.tool()
    async def get_all_issues_assigned_to_group_milestone(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        milestone_id: str = Field(description="The ID of the group milestone")
    ) -> Dict[str, Any]:
        """Get all issues assigned to a single group milestone."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/milestones/{milestone_id}/issues")

    @mcp.tool()
    async def get_all_merge_requests_assigned_to_group_milestone(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        milestone_id: str = Field(description="The ID of the group milestone")
    ) -> Dict[str, Any]:
        """Get all merge requests assigned to a single group milestone."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/milestones/{milestone_id}/merge_requests")