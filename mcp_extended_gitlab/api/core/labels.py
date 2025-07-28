"""GitLab Labels API - Issue and MR label management.

This module provides comprehensive access to GitLab's label management features,
including project and group labels, subscriptions, and label promotion.
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
    """Register all Labels API tools.
    
    This function registers the following tools:
    - Project label CRUD operations
    - Group label CRUD operations
    - Label subscriptions
    - Label promotion from project to group
    """
    
    @mcp.tool()
    async def list_project_labels(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        with_counts: Optional[bool] = Field(default=False, description="Whether or not to include issue and merge request counts"),
        include_ancestor_groups: Optional[bool] = Field(default=True, description="Include ancestor groups"),
        search: Optional[str] = Field(default=None, description="Keyword to filter labels by name"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List project labels."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "with_counts": with_counts,
            "include_ancestor_groups": include_ancestor_groups,
            "search": search,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/labels", params=params)

    @mcp.tool()
    async def get_single_project_label(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        label_id: str = Field(description="The ID or title of a project's label"),
        include_ancestor_groups: Optional[bool] = Field(default=True, description="Include ancestor groups")) -> Dict[str, Any]:
        """Get a single project label."""
        client = await get_gitlab_client()
        params = {}
        if include_ancestor_groups is not None:
            params["include_ancestor_groups"] = include_ancestor_groups
        return await client.get(f"/projects/{project_id}/labels/{label_id}", params=params)

    @mcp.tool()
    async def create_new_label(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: str = Field(description="The name of the label"),
        color: str = Field(description="The color of the label given in 6-digit hex notation with leading '#' sign"),
        description: Optional[str] = Field(default=None, description="The description of the label"),
        priority: Optional[int] = Field(default=None, description="The priority of the label")) -> Dict[str, Any]:
        """Create a new label."""
        client = await get_gitlab_client()
        data = {
            "name": name,
            "color": color
        }
        for key, value in {
            "description": description,
            "priority": priority
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/labels", json_data=data)

    @mcp.tool()
    async def delete_label(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        label_id: str = Field(description="The ID or title of a project's label")) -> Dict[str, Any]:
        """Delete a label."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/labels/{label_id}")

    @mcp.tool()
    async def edit_existing_label(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        label_id: str = Field(description="The ID or title of a project's label"),
        new_name: Optional[str] = Field(default=None, description="The new name of the label"),
        color: Optional[str] = Field(default=None, description="The color of the label given in 6-digit hex notation"),
        description: Optional[str] = Field(default=None, description="The new description of the label"),
        priority: Optional[int] = Field(default=None, description="The new priority of the label")) -> Dict[str, Any]:
        """Edit an existing label."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "new_name": new_name,
            "color": color,
            "description": description,
            "priority": priority
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/labels/{label_id}", json_data=data)

    @mcp.tool()
    async def promote_project_label_to_group_label(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        label_id: str = Field(description="The ID or title of a project's label")) -> Dict[str, Any]:
        """Promote a project label to group label."""
        client = await get_gitlab_client()
        return await client.put(f"/projects/{project_id}/labels/{label_id}/promote")

    @mcp.tool()
    async def subscribe_to_label(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        label_id: str = Field(description="The ID or title of a project's label")) -> Dict[str, Any]:
        """Subscribe to a label."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/labels/{label_id}/subscribe")

    @mcp.tool()
    async def unsubscribe_from_label(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        label_id: str = Field(description="The ID or title of a project's label")) -> Dict[str, Any]:
        """Unsubscribe from a label."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/labels/{label_id}/unsubscribe")

    @mcp.tool()
    async def list_group_labels(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        with_counts: Optional[bool] = Field(default=False, description="Whether or not to include issue and merge request counts"),
        include_ancestor_groups: Optional[bool] = Field(default=True, description="Include ancestor groups"),
        include_descendant_groups: Optional[bool] = Field(default=False, description="Include descendant groups"),
        only_group_labels: Optional[bool] = Field(default=False, description="Toggle to include only group labels or also project labels"),
        search: Optional[str] = Field(default=None, description="Keyword to filter labels by name"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List group labels."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "with_counts": with_counts,
            "include_ancestor_groups": include_ancestor_groups,
            "include_descendant_groups": include_descendant_groups,
            "only_group_labels": only_group_labels,
            "search": search,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/labels", params=params)

    @mcp.tool()
    async def get_single_group_label(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        label_id: str = Field(description="The ID or title of a group's label"),
        include_ancestor_groups: Optional[bool] = Field(default=True, description="Include ancestor groups"),
        include_descendant_groups: Optional[bool] = Field(default=False, description="Include descendant groups")) -> Dict[str, Any]:
        """Get a single group label."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "include_ancestor_groups": include_ancestor_groups,
            "include_descendant_groups": include_descendant_groups
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/labels/{label_id}", params=params)

    @mcp.tool()
    async def create_new_group_label(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        name: str = Field(description="The name of the label"),
        color: str = Field(description="The color of the label given in 6-digit hex notation with leading '#' sign"),
        description: Optional[str] = Field(default=None, description="The description of the label")) -> Dict[str, Any]:
        """Create a new group label."""
        client = await get_gitlab_client()
        data = {
            "name": name,
            "color": color
        }
        if description:
            data["description"] = description
        return await client.post(f"/groups/{group_id}/labels", json_data=data)

    @mcp.tool()
    async def update_group_label(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        label_id: str = Field(description="The ID or title of a group's label"),
        new_name: Optional[str] = Field(default=None, description="The new name of the label"),
        color: Optional[str] = Field(default=None, description="The color of the label given in 6-digit hex notation"),
        description: Optional[str] = Field(default=None, description="The new description of the label")) -> Dict[str, Any]:
        """Update a group label."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "new_name": new_name,
            "color": color,
            "description": description
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/groups/{group_id}/labels/{label_id}", json_data=data)

    @mcp.tool()
    async def delete_group_label(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        label_id: str = Field(description="The ID or title of a group's label")) -> Dict[str, Any]:
        """Delete a group label."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/labels/{label_id}")

    @mcp.tool()
    async def subscribe_to_group_label(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        label_id: str = Field(description="The ID or title of a group's label")) -> Dict[str, Any]:
        """Subscribe to a group label."""
        client = await get_gitlab_client()
        return await client.post(f"/groups/{group_id}/labels/{label_id}/subscribe")

    @mcp.tool()
    async def unsubscribe_from_group_label(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        label_id: str = Field(description="The ID or title of a group's label")) -> Dict[str, Any]:
        """Unsubscribe from a group label."""
        client = await get_gitlab_client()
        return await client.post(f"/groups/{group_id}/labels/{label_id}/unsubscribe")