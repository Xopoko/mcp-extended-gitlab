"""GitLab Groups API - Group management and operations.

This module provides comprehensive access to GitLab's group management features,
including group creation, subgroups, members, and group-level settings.
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
    """Register all Groups API tools.
    
    This function registers the following tools:
    - Group listing and search
    - Group CRUD operations
    - Group configuration (visibility, permissions, etc.)
    - Group members management
    - Subgroups management
    - Group projects listing
    """
    
    @mcp.tool()
    async def list_groups(
        skip_groups: Optional[List[int]] = Field(default=None, description="Skip the group IDs passed"),
        all_available: Optional[bool] = Field(default=None, description="Show all the groups you have access to"),
        search: Optional[str] = Field(default=None, description="Return the list of authorized groups matching the search criteria"),
        order_by: Optional[str] = Field(default=None, description="Order groups by name, path, id, or similarity"),
        sort: Optional[str] = Field(default=None, description="Order groups in asc or desc order"),
        statistics: Optional[bool] = Field(default=None, description="Include group statistics"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        owned: Optional[bool] = Field(default=None, description="Limit to groups explicitly owned by the current user"),
        min_access_level: Optional[int] = Field(default=None, description="Limit to groups where current user has at least this access level"),
        top_level_only: Optional[bool] = Field(default=None, description="Limit to top level groups, excluding all subgroups"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List groups."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "skip_groups": skip_groups,
            "all_available": all_available,
            "search": search,
            "order_by": order_by,
            "sort": sort,
            "statistics": statistics,
            "with_custom_attributes": with_custom_attributes,
            "owned": owned,
            "min_access_level": min_access_level,
            "top_level_only": top_level_only,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/groups", params=params)

    @mcp.tool()
    async def list_subgroups(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        skip_groups: Optional[List[int]] = Field(default=None, description="Skip the group IDs passed"),
        all_available: Optional[bool] = Field(default=None, description="Show all the groups you have access to"),
        search: Optional[str] = Field(default=None, description="Return the list of authorized groups matching the search criteria"),
        order_by: Optional[str] = Field(default=None, description="Order groups by name, path, id, or similarity"),
        sort: Optional[str] = Field(default=None, description="Order groups in asc or desc order"),
        statistics: Optional[bool] = Field(default=None, description="Include group statistics"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        owned: Optional[bool] = Field(default=None, description="Limit to groups explicitly owned by the current user"),
        min_access_level: Optional[int] = Field(default=None, description="Limit to groups where current user has at least this access level"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List subgroups of a group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "skip_groups": skip_groups,
            "all_available": all_available,
            "search": search,
            "order_by": order_by,
            "sort": sort,
            "statistics": statistics,
            "with_custom_attributes": with_custom_attributes,
            "owned": owned,
            "min_access_level": min_access_level,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/subgroups", params=params)

    @mcp.tool()
    async def list_group_projects(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        archived: Optional[bool] = Field(default=None, description="Limit by archived status"),
        visibility: Optional[str] = Field(default=None, description="Limit by visibility"),
        order_by: Optional[str] = Field(default=None, description="Return projects ordered by field"),
        sort: Optional[str] = Field(default=None, description="Return projects sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Return list of projects matching the search criteria"),
        simple: Optional[bool] = Field(default=None, description="Return only limited fields for each project"),
        owned: Optional[bool] = Field(default=None, description="Limit by projects explicitly owned by the current user"),
        starred: Optional[bool] = Field(default=None, description="Limit by projects starred by the current user"),
        with_issues_enabled: Optional[bool] = Field(default=None, description="Limit by enabled issues feature"),
        with_merge_requests_enabled: Optional[bool] = Field(default=None, description="Limit by enabled merge requests feature"),
        with_shared: Optional[bool] = Field(default=True, description="Include projects shared to this group"),
        include_subgroups: Optional[bool] = Field(default=False, description="Include projects in subgroups of this group"),
        min_access_level: Optional[int] = Field(default=None, description="Limit by current user minimal access level"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        with_security_reports: Optional[bool] = Field(default=None, description="Return only projects that have security reports artifacts present"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List group projects."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "archived": archived,
            "visibility": visibility,
            "order_by": order_by,
            "sort": sort,
            "search": search,
            "simple": simple,
            "owned": owned,
            "starred": starred,
            "with_issues_enabled": with_issues_enabled,
            "with_merge_requests_enabled": with_merge_requests_enabled,
            "with_shared": with_shared,
            "include_subgroups": include_subgroups,
            "min_access_level": min_access_level,
            "with_custom_attributes": with_custom_attributes,
            "with_security_reports": with_security_reports,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/projects", params=params)

    @mcp.tool()
    async def get_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        with_projects: Optional[bool] = Field(default=True, description="Include details from projects that belong to the specified group")
    ) -> Dict[str, Any]:
        """Get group details."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "with_custom_attributes": with_custom_attributes,
            "with_projects": with_projects
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}", params=params)

    @mcp.tool()
    async def create_group(
        name: str = Field(description="The name of the group"),
        path: str = Field(description="The path of the group"),
        description: Optional[str] = Field(default=None, description="The group's description"),
        membership_lock: Optional[bool] = Field(default=False, description="Prevent adding new members to project membership within this group"),
        visibility: Optional[str] = Field(default="private", description="The group's visibility"),
        share_with_group_lock: Optional[bool] = Field(default=False, description="Prevent sharing a project with another group within this group"),
        require_two_factor_authentication: Optional[bool] = Field(default=False, description="Require all users in this group to setup Two-factor authentication"),
        two_factor_grace_period: Optional[int] = Field(default=48, description="Time before Two-factor authentication is enforced (in hours)"),
        project_creation_level: Optional[str] = Field(default=None, description="Determine if developers can create projects in the group"),
        auto_devops_enabled: Optional[bool] = Field(default=None, description="Default to Auto DevOps pipeline for all projects within this group"),
        subgroup_creation_level: Optional[str] = Field(default=None, description="Allowed to create subgroups"),
        emails_disabled: Optional[bool] = Field(default=None, description="Disable email notifications"),
        avatar: Optional[str] = Field(default=None, description="Image file for avatar of the group"),
        mentions_disabled: Optional[bool] = Field(default=None, description="Disable the capability of a group from getting mentioned"),
        lfs_enabled: Optional[bool] = Field(default=True, description="Enable/disable Large File Storage (LFS) for the projects in this group"),
        request_access_enabled: Optional[bool] = Field(default=True, description="Allow users to request member access"),
        parent_id: Optional[int] = Field(default=None, description="The parent group ID for creating nested group"),
        default_branch_protection: Optional[int] = Field(default=None, description="Determine if developers can push to the default branch"),
        shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Pipeline minutes quota for this group"),
        extra_shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Extra pipeline minutes quota for this group")
    ) -> Dict[str, Any]:
        """Create a new group."""
        client = await get_gitlab_client()
        data = {
            "name": name,
            "path": path
        }
        for key, value in {
            "description": description,
            "membership_lock": membership_lock,
            "visibility": visibility,
            "share_with_group_lock": share_with_group_lock,
            "require_two_factor_authentication": require_two_factor_authentication,
            "two_factor_grace_period": two_factor_grace_period,
            "project_creation_level": project_creation_level,
            "auto_devops_enabled": auto_devops_enabled,
            "subgroup_creation_level": subgroup_creation_level,
            "emails_disabled": emails_disabled,
            "avatar": avatar,
            "mentions_disabled": mentions_disabled,
            "lfs_enabled": lfs_enabled,
            "request_access_enabled": request_access_enabled,
            "parent_id": parent_id,
            "default_branch_protection": default_branch_protection,
            "shared_runners_minutes_limit": shared_runners_minutes_limit,
            "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit
        }.items():
            if value is not None:
                data[key] = value
        return await client.post("/groups", json_data=data)

    @mcp.tool()
    async def update_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        name: Optional[str] = Field(default=None, description="The name of the group"),
        path: Optional[str] = Field(default=None, description="The path of the group"),
        description: Optional[str] = Field(default=None, description="The group's description"),
        membership_lock: Optional[bool] = Field(default=None, description="Prevent adding new members to project membership within this group"),
        share_with_group_lock: Optional[bool] = Field(default=None, description="Prevent sharing a project with another group within this group"),
        visibility: Optional[str] = Field(default=None, description="The group's visibility"),
        require_two_factor_authentication: Optional[bool] = Field(default=None, description="Require all users in this group to setup Two-factor authentication"),
        two_factor_grace_period: Optional[int] = Field(default=None, description="Time before Two-factor authentication is enforced (in hours)"),
        project_creation_level: Optional[str] = Field(default=None, description="Determine if developers can create projects in the group"),
        auto_devops_enabled: Optional[bool] = Field(default=None, description="Default to Auto DevOps pipeline for all projects within this group"),
        subgroup_creation_level: Optional[str] = Field(default=None, description="Allowed to create subgroups"),
        emails_disabled: Optional[bool] = Field(default=None, description="Disable email notifications"),
        avatar: Optional[str] = Field(default=None, description="Image file for avatar of the group"),
        mentions_disabled: Optional[bool] = Field(default=None, description="Disable the capability of a group from getting mentioned"),
        lfs_enabled: Optional[bool] = Field(default=None, description="Enable/disable Large File Storage (LFS) for the projects in this group"),
        request_access_enabled: Optional[bool] = Field(default=None, description="Allow users to request member access"),
        default_branch_protection: Optional[int] = Field(default=None, description="Determine if developers can push to the default branch"),
        file_template_project_id: Optional[int] = Field(default=None, description="The ID of a project to load custom file templates from"),
        shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Pipeline minutes quota for this group"),
        extra_shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Extra pipeline minutes quota for this group"),
        prevent_forking_outside_group: Optional[bool] = Field(default=None, description="When enabled, users can not fork projects from this group to external namespaces")
    ) -> Dict[str, Any]:
        """Update a group."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "name": name,
            "path": path,
            "description": description,
            "membership_lock": membership_lock,
            "share_with_group_lock": share_with_group_lock,
            "visibility": visibility,
            "require_two_factor_authentication": require_two_factor_authentication,
            "two_factor_grace_period": two_factor_grace_period,
            "project_creation_level": project_creation_level,
            "auto_devops_enabled": auto_devops_enabled,
            "subgroup_creation_level": subgroup_creation_level,
            "emails_disabled": emails_disabled,
            "avatar": avatar,
            "mentions_disabled": mentions_disabled,
            "lfs_enabled": lfs_enabled,
            "request_access_enabled": request_access_enabled,
            "default_branch_protection": default_branch_protection,
            "file_template_project_id": file_template_project_id,
            "shared_runners_minutes_limit": shared_runners_minutes_limit,
            "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit,
            "prevent_forking_outside_group": prevent_forking_outside_group
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/groups/{group_id}", json_data=data)

    @mcp.tool()
    async def delete_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        permanently_remove: Optional[bool] = Field(default=False, description="Immediately deletes a group marked for deletion"),
        full_path: Optional[str] = Field(default=None, description="Full path of the group")
    ) -> Dict[str, Any]:
        """Delete a group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "permanently_remove": permanently_remove,
            "full_path": full_path
        }.items():
            if value is not None:
                params[key] = value
        return await client.delete(f"/groups/{group_id}", params=params)

    @mcp.tool()
    async def restore_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group")
    ) -> Dict[str, Any]:
        """Restore a group marked for deletion."""
        client = await get_gitlab_client()
        return await client.post(f"/groups/{group_id}/restore")

    @mcp.tool()
    async def list_group_members(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        query: Optional[str] = Field(default=None, description="A query string to search for members"),
        user_ids: Optional[List[int]] = Field(default=None, description="Filter the results on the given user IDs"),
        skip_users: Optional[List[int]] = Field(default=None, description="Filter the results to exclude the given user IDs"),
        show_seat_info: Optional[bool] = Field(default=None, description="Show seat information for members"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List group members."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "query": query,
            "user_ids": user_ids,
            "skip_users": skip_users,
            "show_seat_info": show_seat_info,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/members", params=params)

    @mcp.tool()
    async def list_all_group_members(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        query: Optional[str] = Field(default=None, description="A query string to search for members"),
        user_ids: Optional[List[int]] = Field(default=None, description="Filter the results on the given user IDs"),
        skip_users: Optional[List[int]] = Field(default=None, description="Filter the results to exclude the given user IDs"),
        show_seat_info: Optional[bool] = Field(default=None, description="Show seat information for members"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List all group members including inherited members."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "query": query,
            "user_ids": user_ids,
            "skip_users": skip_users,
            "show_seat_info": show_seat_info,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/members/all", params=params)

    @mcp.tool()
    async def get_group_member(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        user_id: str = Field(description="The user ID or username of the member")
    ) -> Dict[str, Any]:
        """Get a group member."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/members/{user_id}")

    @mcp.tool()
    async def add_group_member(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        user_id: str = Field(description="The user ID to add"),
        access_level: int = Field(description="A valid access level"),
        expires_at: Optional[str] = Field(default=None, description="A date string in the format YYYY-MM-DD")
    ) -> Dict[str, Any]:
        """Add a member to a group."""
        client = await get_gitlab_client()
        data = {
            "user_id": user_id,
            "access_level": access_level
        }
        if expires_at:
            data["expires_at"] = expires_at
        return await client.post(f"/groups/{group_id}/members", json_data=data)

    @mcp.tool()
    async def update_group_member(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        user_id: str = Field(description="The user ID or username of the member"),
        access_level: Optional[int] = Field(default=None, description="A valid access level"),
        expires_at: Optional[str] = Field(default=None, description="A date string in the format YYYY-MM-DD")
    ) -> Dict[str, Any]:
        """Update a group member."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "access_level": access_level,
            "expires_at": expires_at
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/groups/{group_id}/members/{user_id}", json_data=data)

    @mcp.tool()
    async def remove_group_member(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        user_id: str = Field(description="The user ID or username of the member"),
        skip_subresources: Optional[bool] = Field(default=False, description="Whether the deletion of direct memberships of the removed member in subgroups and projects should be skipped"),
        unassign_issuables: Optional[bool] = Field(default=False, description="Whether the removed member should be unassigned from any issues or merge requests inside a given group or project")
    ) -> Dict[str, Any]:
        """Remove a member from a group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "skip_subresources": skip_subresources,
            "unassign_issuables": unassign_issuables
        }.items():
            if value is not None:
                params[key] = value
        return await client.delete(f"/groups/{group_id}/members/{user_id}", params=params)

    @mcp.tool()
    async def share_group_with_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        group_id_to_share: int = Field(description="The ID of the group to share with"),
        group_access: int = Field(description="The access level to grant"),
        expires_at: Optional[str] = Field(default=None, description="Share expiration date in ISO 8601 format")
    ) -> Dict[str, Any]:
        """Share group with another group."""
        client = await get_gitlab_client()
        data = {
            "group_id": group_id_to_share,
            "group_access": group_access
        }
        if expires_at:
            data["expires_at"] = expires_at
        return await client.post(f"/groups/{group_id}/share", json_data=data)

    @mcp.tool()
    async def unshare_group_with_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        group_id_to_unshare: int = Field(description="The ID of the group to unshare with")
    ) -> Dict[str, Any]:
        """Unshare group with another group."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/share/{group_id_to_unshare}")

    @mcp.tool()
    async def list_group_descendants(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        skip_groups: Optional[List[int]] = Field(default=None, description="Skip the group IDs passed"),
        all_available: Optional[bool] = Field(default=None, description="Show all the groups you have access to"),
        search: Optional[str] = Field(default=None, description="Return the list of authorized groups matching the search criteria"),
        order_by: Optional[str] = Field(default=None, description="Order groups by name, path, id, or similarity"),
        sort: Optional[str] = Field(default=None, description="Order groups in asc or desc order"),
        statistics: Optional[bool] = Field(default=None, description="Include group statistics"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        owned: Optional[bool] = Field(default=None, description="Limit to groups explicitly owned by the current user"),
        min_access_level: Optional[int] = Field(default=None, description="Limit to groups where current user has at least this access level"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List group descendants."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "skip_groups": skip_groups,
            "all_available": all_available,
            "search": search,
            "order_by": order_by,
            "sort": sort,
            "statistics": statistics,
            "with_custom_attributes": with_custom_attributes,
            "owned": owned,
            "min_access_level": min_access_level,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/descendant_groups", params=params)

    @mcp.tool()
    async def transfer_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        group_id_to_transfer_to: int = Field(description="The ID of the group to transfer to")
    ) -> Dict[str, Any]:
        """Transfer a group to a new parent group."""
        client = await get_gitlab_client()
        data = {"group_id": group_id_to_transfer_to}
        return await client.post(f"/groups/{group_id}/transfer", json_data=data)