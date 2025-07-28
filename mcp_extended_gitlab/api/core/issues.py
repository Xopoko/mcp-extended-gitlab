"""GitLab Issues API - Issue tracking and management.

This module provides comprehensive access to GitLab's issue tracking system,
including issue creation, updates, time tracking, links, and relationships.
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
    """Register all Issues API tools.
    
    This function registers the following tools:
    - Issue CRUD operations (list, get, create, update, delete)
    - Issue time tracking (estimates, time spent)
    - Issue relationships (links, related issues)
    - Issue metadata (participants, user agent details)
    - Issue management (move, reorder, subscribe)
    """
    
    @mcp.tool()
    async def list_issues(
        state: Optional[str] = Field(default=None, description="Return all issues or just those that are opened or closed"),
        labels: Optional[str] = Field(default=None, description="Comma-separated list of label names"),
        milestone: Optional[str] = Field(default=None, description="The milestone title"),
        scope: Optional[str] = Field(default=None, description="Return issues for the given scope: created_by_me, assigned_to_me or all"),
        author_id: Optional[int] = Field(default=None, description="Return issues created by the given user id"),
        author_username: Optional[str] = Field(default=None, description="Return issues created by the given username"),
        assignee_id: Optional[int] = Field(default=None, description="Return issues assigned to the given user id"),
        assignee_username: Optional[str] = Field(default=None, description="Return issues assigned to the given username"),
        my_reaction_emoji: Optional[str] = Field(default=None, description="Return issues reacted by the authenticated user by the given emoji"),
        weight: Optional[int] = Field(default=None, description="Return issues with the specified weight"),
        iids: Optional[List[int]] = Field(default=None, description="Return only the issues having the given iid"),
        order_by: Optional[str] = Field(default=None, description="Return issues ordered by created_at, updated_at, priority, due_date, relative_position, label_priority, milestone_due, popularity, weight fields"),
        sort: Optional[str] = Field(default=None, description="Return issues sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Search issues against their title and description"),
        created_after: Optional[str] = Field(default=None, description="Return issues created on or after the given time"),
        created_before: Optional[str] = Field(default=None, description="Return issues created on or before the given time"),
        updated_after: Optional[str] = Field(default=None, description="Return issues updated on or after the given time"),
        updated_before: Optional[str] = Field(default=None, description="Return issues updated on or before the given time"),
        confidential: Optional[bool] = Field(default=None, description="Filter confidential or public issues"),
        not_labels: Optional[str] = Field(default=None, description="Comma-separated list of label names"),
        not_milestone: Optional[str] = Field(default=None, description="The milestone title"),
        not_author_id: Optional[int] = Field(default=None, description="Return issues not created by the given user id"),
        not_author_username: Optional[str] = Field(default=None, description="Return issues not created by the given username"),
        not_assignee_id: Optional[int] = Field(default=None, description="Return issues not assigned to the given user id"),
        not_assignee_username: Optional[str] = Field(default=None, description="Return issues not assigned to the given username"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List all issues the authenticated user has access to."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "state": state,
            "labels": labels,
            "milestone": milestone,
            "scope": scope,
            "author_id": author_id,
            "author_username": author_username,
            "assignee_id": assignee_id,
            "assignee_username": assignee_username,
            "my_reaction_emoji": my_reaction_emoji,
            "weight": weight,
            "iids": iids,
            "order_by": order_by,
            "sort": sort,
            "search": search,
            "created_after": created_after,
            "created_before": created_before,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "confidential": confidential,
            "not[labels]": not_labels,
            "not[milestone]": not_milestone,
            "not[author_id]": not_author_id,
            "not[author_username]": not_author_username,
            "not[assignee_id]": not_assignee_id,
            "not[assignee_username]": not_assignee_username,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/issues", params=params)

    @mcp.tool()
    async def list_group_issues(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        state: Optional[str] = Field(default=None, description="Return all issues or just those that are opened or closed"),
        labels: Optional[str] = Field(default=None, description="Comma-separated list of label names"),
        iids: Optional[List[int]] = Field(default=None, description="Return only the issues having the given iid"),
        milestone: Optional[str] = Field(default=None, description="The milestone title"),
        scope: Optional[str] = Field(default=None, description="Return issues for the given scope"),
        author_id: Optional[int] = Field(default=None, description="Return issues created by the given user id"),
        assignee_id: Optional[int] = Field(default=None, description="Return issues assigned to the given user id"),
        my_reaction_emoji: Optional[str] = Field(default=None, description="Return issues reacted by the authenticated user by the given emoji"),
        order_by: Optional[str] = Field(default=None, description="Return issues ordered by created_at or updated_at fields"),
        sort: Optional[str] = Field(default=None, description="Return issues sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Search group issues against their title and description"),
        created_after: Optional[str] = Field(default=None, description="Return issues created on or after the given time"),
        created_before: Optional[str] = Field(default=None, description="Return issues created on or before the given time"),
        updated_after: Optional[str] = Field(default=None, description="Return issues updated on or after the given time"),
        updated_before: Optional[str] = Field(default=None, description="Return issues updated on or before the given time"),
        confidential: Optional[bool] = Field(default=None, description="Filter confidential or public issues"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """Get a list of group issues."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "state": state,
            "labels": labels,
            "iids": iids,
            "milestone": milestone,
            "scope": scope,
            "author_id": author_id,
            "assignee_id": assignee_id,
            "my_reaction_emoji": my_reaction_emoji,
            "order_by": order_by,
            "sort": sort,
            "search": search,
            "created_after": created_after,
            "created_before": created_before,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "confidential": confidential,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/issues", params=params)

    @mcp.tool()
    async def list_project_issues(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        iids: Optional[List[int]] = Field(default=None, description="Return only the issues having the given iid"),
        state: Optional[str] = Field(default=None, description="Return all issues or just those that are opened or closed"),
        labels: Optional[str] = Field(default=None, description="Comma-separated list of label names"),
        milestone: Optional[str] = Field(default=None, description="The milestone title"),
        scope: Optional[str] = Field(default=None, description="Return issues for the given scope"),
        author_id: Optional[int] = Field(default=None, description="Return issues created by the given user id"),
        assignee_id: Optional[int] = Field(default=None, description="Return issues assigned to the given user id"),
        my_reaction_emoji: Optional[str] = Field(default=None, description="Return issues reacted by the authenticated user by the given emoji"),
        weight: Optional[int] = Field(default=None, description="Return issues with the specified weight"),
        order_by: Optional[str] = Field(default=None, description="Return issues ordered by created_at or updated_at fields"),
        sort: Optional[str] = Field(default=None, description="Return issues sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Search project issues against their title and description"),
        created_after: Optional[str] = Field(default=None, description="Return issues created on or after the given time"),
        created_before: Optional[str] = Field(default=None, description="Return issues created on or before the given time"),
        updated_after: Optional[str] = Field(default=None, description="Return issues updated on or after the given time"),
        updated_before: Optional[str] = Field(default=None, description="Return issues updated on or before the given time"),
        confidential: Optional[bool] = Field(default=None, description="Filter confidential or public issues"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """Get a list of project issues."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "iids": iids,
            "state": state,
            "labels": labels,
            "milestone": milestone,
            "scope": scope,
            "author_id": author_id,
            "assignee_id": assignee_id,
            "my_reaction_emoji": my_reaction_emoji,
            "weight": weight,
            "order_by": order_by,
            "sort": sort,
            "search": search,
            "created_after": created_after,
            "created_before": created_before,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "confidential": confidential,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/issues", params=params)

    @mcp.tool()
    async def get_single_issue(
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Get a single issue."""
        client = await get_gitlab_client()
        return await client.get(f"/issues/{issue_iid}")

    @mcp.tool()
    async def get_single_project_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Get a single project issue."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}")

    @mcp.tool()
    async def create_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        title: str = Field(description="The title of an issue"),
        description: Optional[str] = Field(default=None, description="The description of an issue"),
        confidential: Optional[bool] = Field(default=None, description="Set an issue to be confidential"),
        assignee_ids: Optional[List[int]] = Field(default=None, description="The ID of the user to assign the issue to"),
        milestone_id: Optional[int] = Field(default=None, description="The global ID of a milestone to assign the issue to"),
        labels: Optional[str] = Field(default=None, description="Comma-separated label names for an issue"),
        created_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted"),
        due_date: Optional[str] = Field(default=None, description="Date time string in the format YYYY-MM-DD"),
        merge_request_to_resolve_discussions_of: Optional[int] = Field(default=None, description="The IID of a merge request in which to resolve all issues"),
        discussion_to_resolve: Optional[str] = Field(default=None, description="The ID of a discussion to resolve"),
        weight: Optional[int] = Field(default=None, description="The weight of the issue"),
        epic_id: Optional[int] = Field(default=None, description="ID of the epic to add the issue to")) -> Dict[str, Any]:
        """Create a new issue."""
        client = await get_gitlab_client()
        data = {"title": title}
        for key, value in {
            "description": description,
            "confidential": confidential,
            "assignee_ids": assignee_ids,
            "milestone_id": milestone_id,
            "labels": labels,
            "created_at": created_at,
            "due_date": due_date,
            "merge_request_to_resolve_discussions_of": merge_request_to_resolve_discussions_of,
            "discussion_to_resolve": discussion_to_resolve,
            "weight": weight,
            "epic_id": epic_id
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/issues", json_data=data)

    @mcp.tool()
    async def update_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue"),
        title: Optional[str] = Field(default=None, description="The title of an issue"),
        description: Optional[str] = Field(default=None, description="The description of an issue"),
        confidential: Optional[bool] = Field(default=None, description="Set an issue to be confidential"),
        assignee_ids: Optional[List[int]] = Field(default=None, description="The ID of the user to assign the issue to"),
        milestone_id: Optional[int] = Field(default=None, description="The global ID of a milestone to assign the issue to"),
        labels: Optional[str] = Field(default=None, description="Comma-separated label names for an issue"),
        add_labels: Optional[str] = Field(default=None, description="Comma-separated label names to add to an issue"),
        remove_labels: Optional[str] = Field(default=None, description="Comma-separated label names to remove from an issue"),
        state_event: Optional[str] = Field(default=None, description="The state event of an issue. Set close to close the issue and reopen to reopen it"),
        updated_at: Optional[str] = Field(default=None, description="Date time string, ISO 8601 formatted"),
        due_date: Optional[str] = Field(default=None, description="Date time string in the format YYYY-MM-DD"),
        weight: Optional[int] = Field(default=None, description="The weight of the issue"),
        discussion_locked: Optional[bool] = Field(default=None, description="Flag indicating if the issue's discussion is locked")) -> Dict[str, Any]:
        """Update an issue."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "title": title,
            "description": description,
            "confidential": confidential,
            "assignee_ids": assignee_ids,
            "milestone_id": milestone_id,
            "labels": labels,
            "add_labels": add_labels,
            "remove_labels": remove_labels,
            "state_event": state_event,
            "updated_at": updated_at,
            "due_date": due_date,
            "weight": weight,
            "discussion_locked": discussion_locked
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/issues/{issue_iid}", json_data=data)

    @mcp.tool()
    async def delete_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Delete an issue."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/issues/{issue_iid}")

    @mcp.tool()
    async def reorder_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue"),
        move_after_id: Optional[int] = Field(default=None, description="The ID of a project's issue to move this issue after"),
        move_before_id: Optional[int] = Field(default=None, description="The ID of a project's issue to move this issue before")) -> Dict[str, Any]:
        """Reorder an issue."""
        client = await get_gitlab_client()
        data = {}
        if move_after_id is not None:
            data["move_after_id"] = move_after_id
        if move_before_id is not None:
            data["move_before_id"] = move_before_id
        return await client.put(f"/projects/{project_id}/issues/{issue_iid}/reorder", json_data=data)

    @mcp.tool()
    async def move_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue"),
        to_project_id: str = Field(description="The ID or URL-encoded path of the project to move the issue to")) -> Dict[str, Any]:
        """Move an issue."""
        client = await get_gitlab_client()
        data = {"to_project_id": to_project_id}
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/move", json_data=data)

    @mcp.tool()
    async def subscribe_to_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Subscribe to an issue."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/subscribe")

    @mcp.tool()
    async def unsubscribe_from_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Unsubscribe from an issue."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/unsubscribe")

    @mcp.tool()
    async def create_todo_for_issue(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Create a todo for the current user on an issue."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/todo")

    @mcp.tool()
    async def get_issue_user_agent_details(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Get user agent details for an issue."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/user_agent_detail")

    @mcp.tool()
    async def list_issue_participants(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """List participants on an issue."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/participants")

    @mcp.tool()
    async def list_issue_links(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """List links for an issue."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/links")

    @mcp.tool()
    async def create_issue_link(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue"),
        target_project_id: str = Field(description="The ID or URL-encoded path of the project of a target issue"),
        target_issue_iid: str = Field(description="The internal ID of a target project's issue"),
        link_type: Optional[str] = Field(default=None, description="The type of the link (relates_to, blocks, is_blocked_by)")) -> Dict[str, Any]:
        """Create an issue link."""
        client = await get_gitlab_client()
        data = {
            "target_project_id": target_project_id,
            "target_issue_iid": target_issue_iid
        }
        if link_type:
            data["link_type"] = link_type
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/links", json_data=data)

    @mcp.tool()
    async def delete_issue_link(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue"),
        issue_link_id: str = Field(description="The ID of an issue link")) -> Dict[str, Any]:
        """Delete an issue link."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/issues/{issue_iid}/links/{issue_link_id}")

    @mcp.tool()
    async def list_related_issues(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """List related issues of an issue."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/related_issues")

    @mcp.tool()
    async def set_issue_time_estimate(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue"),
        duration: str = Field(description="The duration in human format. e.g: 3h30m")) -> Dict[str, Any]:
        """Set a time estimate for an issue."""
        client = await get_gitlab_client()
        data = {"duration": duration}
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/time_estimate", json_data=data)

    @mcp.tool()
    async def reset_issue_time_estimate(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Reset the time estimate for an issue."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/reset_time_estimate")

    @mcp.tool()
    async def add_issue_spent_time(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue"),
        duration: str = Field(description="The duration in human format. e.g: 3h30m")) -> Dict[str, Any]:
        """Add spent time for an issue."""
        client = await get_gitlab_client()
        data = {"duration": duration}
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/add_spent_time", json_data=data)

    @mcp.tool()
    async def reset_issue_spent_time(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Reset spent time for an issue."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/issues/{issue_iid}/reset_spent_time")

    @mcp.tool()
    async def get_issue_time_stats(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """Get time tracking stats for an issue."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/time_stats")

    @mcp.tool()
    async def list_issue_closed_by(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        issue_iid: str = Field(description="The internal ID of a project's issue")) -> Dict[str, Any]:
        """List merge requests that will close issue on merge."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/issues/{issue_iid}/closed_by")