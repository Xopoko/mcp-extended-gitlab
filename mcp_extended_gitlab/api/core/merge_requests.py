"""GitLab Merge Requests API - Code review and merge management.

This module provides comprehensive access to GitLab's merge request system,
including MR creation, reviews, approvals, merging, and associated workflows.
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
    """Register all Merge Requests API tools.
    
    This function registers the following tools:
    - MR CRUD operations (list, get, create, update, delete)
    - MR workflow (accept, merge, rebase, approve)
    - MR relationships (commits, changes, pipelines)
    - MR reviews (reviewers, participants, discussions)
    - MR management (subscribe, todos, time tracking)
    """
    
    @mcp.tool()
    async def list_merge_requests(
        state: Optional[str] = Field(default=None, description="Return all merge requests or just those that are opened, closed, locked, or merged"),
        order_by: Optional[str] = Field(default=None, description="Return merge requests ordered by created_at, updated_at, priority, due_date, relative_position, label_priority, milestone_due, popularity, weight fields"),
        sort: Optional[str] = Field(default=None, description="Return merge requests sorted in asc or desc order"),
        milestone: Optional[str] = Field(default=None, description="Return merge requests for a specific milestone"),
        view: Optional[str] = Field(default=None, description="If simple, returns the iid, URL, title, description, and basic state of merge request"),
        labels: Optional[str] = Field(default=None, description="Return merge requests matching a comma separated list of labels"),
        with_labels_details: Optional[bool] = Field(default=None, description="If true, response returns more details for each label in labels field"),
        with_merge_status_recheck: Optional[bool] = Field(default=None, description="If true, this projection requests the latest merge status recheck"),
        created_after: Optional[str] = Field(default=None, description="Return merge requests created on or after the given time"),
        created_before: Optional[str] = Field(default=None, description="Return merge requests created on or before the given time"),
        updated_after: Optional[str] = Field(default=None, description="Return merge requests updated on or after the given time"),
        updated_before: Optional[str] = Field(default=None, description="Return merge requests updated on or before the given time"),
        scope: Optional[str] = Field(default=None, description="Return merge requests for the given scope: created_by_me, assigned_to_me or all"),
        author_id: Optional[int] = Field(default=None, description="Returns merge requests created by the given user id"),
        author_username: Optional[str] = Field(default=None, description="Returns merge requests created by the given username"),
        assignee_id: Optional[int] = Field(default=None, description="Returns merge requests assigned to the given user id"),
        assignee_username: Optional[str] = Field(default=None, description="Returns merge requests assigned to the given username"),
        reviewer_id: Optional[int] = Field(default=None, description="Returns merge requests which have the user as a reviewer with the given user id"),
        reviewer_username: Optional[str] = Field(default=None, description="Returns merge requests which have the user as a reviewer with the given username"),
        my_reaction_emoji: Optional[str] = Field(default=None, description="Return merge requests reacted by the authenticated user by the given emoji"),
        source_branch: Optional[str] = Field(default=None, description="Return merge requests with the given source branch"),
        target_branch: Optional[str] = Field(default=None, description="Return merge requests with the given target branch"),
        search: Optional[str] = Field(default=None, description="Search merge requests against their title and description"),
        in_: Optional[str] = Field(default=None, alias="in", description="Modify the scope of the search attribute"),
        wip: Optional[str] = Field(default=None, description="Filter merge requests against their wip status"),
        not_author_id: Optional[int] = Field(default=None, description="Return merge requests not created by the given user id"),
        not_author_username: Optional[str] = Field(default=None, description="Return merge requests not created by the given username"),
        not_assignee_id: Optional[int] = Field(default=None, description="Return merge requests not assigned to the given user id"),
        not_assignee_username: Optional[str] = Field(default=None, description="Return merge requests not assigned to the given username"),
        not_reviewer_id: Optional[int] = Field(default=None, description="Return merge requests which do not have the user as a reviewer"),
        not_reviewer_username: Optional[str] = Field(default=None, description="Return merge requests which do not have the user as a reviewer"),
        not_labels: Optional[str] = Field(default=None, description="Return merge requests that do not match a comma separated list of labels"),
        not_milestone: Optional[str] = Field(default=None, description="Return merge requests that do not have a milestone"),
        not_my_reaction_emoji: Optional[str] = Field(default=None, description="Return merge requests not reacted by the authenticated user"),
        deployment_status: Optional[str] = Field(default=None, description="Return merge requests with the given deployment status"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List all merge requests the authenticated user has access to."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "state": state,
            "order_by": order_by,
            "sort": sort,
            "milestone": milestone,
            "view": view,
            "labels": labels,
            "with_labels_details": with_labels_details,
            "with_merge_status_recheck": with_merge_status_recheck,
            "created_after": created_after,
            "created_before": created_before,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "scope": scope,
            "author_id": author_id,
            "author_username": author_username,
            "assignee_id": assignee_id,
            "assignee_username": assignee_username,
            "reviewer_id": reviewer_id,
            "reviewer_username": reviewer_username,
            "my_reaction_emoji": my_reaction_emoji,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "search": search,
            "in": in_,
            "wip": wip,
            "not[author_id]": not_author_id,
            "not[author_username]": not_author_username,
            "not[assignee_id]": not_assignee_id,
            "not[assignee_username]": not_assignee_username,
            "not[reviewer_id]": not_reviewer_id,
            "not[reviewer_username]": not_reviewer_username,
            "not[labels]": not_labels,
            "not[milestone]": not_milestone,
            "not[my_reaction_emoji]": not_my_reaction_emoji,
            "deployment_status": deployment_status,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/merge_requests", params=params)

    @mcp.tool()
    async def list_project_merge_requests(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        iids: Optional[List[int]] = Field(default=None, description="Return the request having the given iid"),
        state: Optional[str] = Field(default=None, description="Return all merge requests or just those that are opened, closed, locked, or merged"),
        order_by: Optional[str] = Field(default=None, description="Return requests ordered by created_at or updated_at fields"),
        sort: Optional[str] = Field(default=None, description="Return requests sorted in asc or desc order"),
        milestone: Optional[str] = Field(default=None, description="Return merge requests for a specific milestone"),
        view: Optional[str] = Field(default=None, description="If simple, returns the iid, URL, title, description, and basic state of merge request"),
        labels: Optional[str] = Field(default=None, description="Return merge requests matching a comma separated list of labels"),
        with_labels_details: Optional[bool] = Field(default=None, description="If true, response returns more details for each label in labels field"),
        with_merge_status_recheck: Optional[bool] = Field(default=None, description="If true, this projection requests the latest merge status recheck"),
        created_after: Optional[str] = Field(default=None, description="Return merge requests created on or after the given time"),
        created_before: Optional[str] = Field(default=None, description="Return merge requests created on or before the given time"),
        updated_after: Optional[str] = Field(default=None, description="Return merge requests updated on or after the given time"),
        updated_before: Optional[str] = Field(default=None, description="Return merge requests updated on or before the given time"),
        scope: Optional[str] = Field(default=None, description="Return merge requests for the given scope"),
        author_id: Optional[int] = Field(default=None, description="Returns merge requests created by the given user id"),
        assignee_id: Optional[int] = Field(default=None, description="Returns merge requests assigned to the given user id"),
        reviewer_id: Optional[int] = Field(default=None, description="Returns merge requests which have the user as a reviewer"),
        my_reaction_emoji: Optional[str] = Field(default=None, description="Return merge requests reacted by the authenticated user by the given emoji"),
        source_branch: Optional[str] = Field(default=None, description="Return merge requests with the given source branch"),
        target_branch: Optional[str] = Field(default=None, description="Return merge requests with the given target branch"),
        search: Optional[str] = Field(default=None, description="Search merge requests against their title and description"),
        wip: Optional[str] = Field(default=None, description="Filter merge requests against their wip status"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Get all merge requests for this project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "iids": iids,
            "state": state,
            "order_by": order_by,
            "sort": sort,
            "milestone": milestone,
            "view": view,
            "labels": labels,
            "with_labels_details": with_labels_details,
            "with_merge_status_recheck": with_merge_status_recheck,
            "created_after": created_after,
            "created_before": created_before,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "scope": scope,
            "author_id": author_id,
            "assignee_id": assignee_id,
            "reviewer_id": reviewer_id,
            "my_reaction_emoji": my_reaction_emoji,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "search": search,
            "wip": wip,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/merge_requests", params=params)

    @mcp.tool()
    async def list_group_merge_requests(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        state: Optional[str] = Field(default=None, description="Return all merge requests or just those that are opened, closed, locked, or merged"),
        order_by: Optional[str] = Field(default=None, description="Return merge requests ordered by created_at or updated_at fields"),
        sort: Optional[str] = Field(default=None, description="Return merge requests sorted in asc or desc order"),
        milestone: Optional[str] = Field(default=None, description="Return merge requests for a specific milestone"),
        view: Optional[str] = Field(default=None, description="If simple, returns the iid, URL, title, description, and basic state of merge request"),
        labels: Optional[str] = Field(default=None, description="Return merge requests matching a comma separated list of labels"),
        created_after: Optional[str] = Field(default=None, description="Return merge requests created on or after the given time"),
        created_before: Optional[str] = Field(default=None, description="Return merge requests created on or before the given time"),
        updated_after: Optional[str] = Field(default=None, description="Return merge requests updated on or after the given time"),
        updated_before: Optional[str] = Field(default=None, description="Return merge requests updated on or before the given time"),
        scope: Optional[str] = Field(default=None, description="Return merge requests for the given scope"),
        author_id: Optional[int] = Field(default=None, description="Returns merge requests created by the given user id"),
        assignee_id: Optional[int] = Field(default=None, description="Returns merge requests assigned to the given user id"),
        my_reaction_emoji: Optional[str] = Field(default=None, description="Return merge requests reacted by the authenticated user by the given emoji"),
        source_branch: Optional[str] = Field(default=None, description="Return merge requests with the given source branch"),
        target_branch: Optional[str] = Field(default=None, description="Return merge requests with the given target branch"),
        search: Optional[str] = Field(default=None, description="Search merge requests against their title and description"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Get all merge requests for this group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "state": state,
            "order_by": order_by,
            "sort": sort,
            "milestone": milestone,
            "view": view,
            "labels": labels,
            "created_after": created_after,
            "created_before": created_before,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "scope": scope,
            "author_id": author_id,
            "assignee_id": assignee_id,
            "my_reaction_emoji": my_reaction_emoji,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "search": search,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/merge_requests", params=params)

    @mcp.tool()
    async def get_single_mr(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        render_html: Optional[bool] = Field(default=None, description="If true response includes rendered HTML for title and description"),
        include_diverged_commits_count: Optional[bool] = Field(default=None, description="If true response includes the commits behind the target branch"),
        include_rebase_in_progress: Optional[bool] = Field(default=None, description="If true response includes whether a rebase operation is in progress")
    ) -> Dict[str, Any]:
        """Shows information about a single merge request."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "render_html": render_html,
            "include_diverged_commits_count": include_diverged_commits_count,
            "include_rebase_in_progress": include_rebase_in_progress
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}", params=params)

    @mcp.tool()
    async def get_single_mr_participants(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Get list of merge request participants."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/participants")

    @mcp.tool()
    async def get_single_mr_commits(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Get list of merge request commits."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/commits")

    @mcp.tool()
    async def get_single_mr_reviewers(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Get list of merge request reviewers."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/reviewers")

    @mcp.tool()
    async def get_single_mr_changes(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        access_raw_diffs: Optional[bool] = Field(default=None, description="Retrieve change diffs via Gitaly")
    ) -> Dict[str, Any]:
        """Shows information about the merge request including its files and changes."""
        client = await get_gitlab_client()
        params = {}
        if access_raw_diffs is not None:
            params["access_raw_diffs"] = access_raw_diffs
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/changes", params=params)

    @mcp.tool()
    async def list_mr_pipelines(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Get a list of merge request pipelines."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/pipelines")

    @mcp.tool()
    async def create_mr_pipeline(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Create MR pipeline."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/pipelines")

    @mcp.tool()
    async def create_merge_request(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        source_branch: str = Field(description="The source branch"),
        target_branch: str = Field(description="The target branch"),
        title: str = Field(description="Title of MR"),
        assignee_id: Optional[int] = Field(default=None, description="Assignee user ID"),
        assignee_ids: Optional[List[int]] = Field(default=None, description="The ID of the user(s) to assign the MR to"),
        reviewer_ids: Optional[List[int]] = Field(default=None, description="The ID of the user(s) to review the MR"),
        description: Optional[str] = Field(default=None, description="Description of MR"),
        target_project_id: Optional[int] = Field(default=None, description="The target project"),
        labels: Optional[str] = Field(default=None, description="Labels for MR as a comma-separated list"),
        milestone_id: Optional[int] = Field(default=None, description="The global ID of a milestone"),
        remove_source_branch: Optional[bool] = Field(default=None, description="Flag indicating if a merge request should remove the source branch when merging"),
        allow_collaboration: Optional[bool] = Field(default=None, description="Allow commits from members who can merge to the target branch"),
        allow_maintainer_to_push: Optional[bool] = Field(default=None, description="Deprecated, use allow_collaboration"),
        squash: Optional[bool] = Field(default=None, description="Squash commits into a single commit when merging")
    ) -> Dict[str, Any]:
        """Creates a new merge request."""
        client = await get_gitlab_client()
        data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title
        }
        for key, value in {
            "assignee_id": assignee_id,
            "assignee_ids": assignee_ids,
            "reviewer_ids": reviewer_ids,
            "description": description,
            "target_project_id": target_project_id,
            "labels": labels,
            "milestone_id": milestone_id,
            "remove_source_branch": remove_source_branch,
            "allow_collaboration": allow_collaboration,
            "allow_maintainer_to_push": allow_maintainer_to_push,
            "squash": squash
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/merge_requests", json_data=data)

    @mcp.tool()
    async def update_mr(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        target_branch: Optional[str] = Field(default=None, description="The target branch"),
        title: Optional[str] = Field(default=None, description="Title of MR"),
        assignee_id: Optional[int] = Field(default=None, description="The ID of the user to assign the merge request to"),
        assignee_ids: Optional[List[int]] = Field(default=None, description="The ID of the user(s) to assign the MR to"),
        reviewer_ids: Optional[List[int]] = Field(default=None, description="The ID of the user(s) to review the MR"),
        milestone_id: Optional[int] = Field(default=None, description="The global ID of a milestone to assign the merge request to"),
        labels: Optional[str] = Field(default=None, description="Comma-separated label names for an MR"),
        add_labels: Optional[str] = Field(default=None, description="Comma-separated label names to add to an MR"),
        remove_labels: Optional[str] = Field(default=None, description="Comma-separated label names to remove from an MR"),
        description: Optional[str] = Field(default=None, description="Description of MR"),
        state_event: Optional[str] = Field(default=None, description="New state (close/reopen)"),
        remove_source_branch: Optional[bool] = Field(default=None, description="Flag indicating if a merge request should remove the source branch when merging"),
        squash: Optional[bool] = Field(default=None, description="Squash commits into a single commit when merging"),
        discussion_locked: Optional[bool] = Field(default=None, description="Flag indicating if the merge request's discussion is locked"),
        allow_collaboration: Optional[bool] = Field(default=None, description="Allow commits from members who can merge to the target branch"),
        allow_maintainer_to_push: Optional[bool] = Field(default=None, description="Deprecated, use allow_collaboration")
    ) -> Dict[str, Any]:
        """Updates an existing merge request."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "target_branch": target_branch,
            "title": title,
            "assignee_id": assignee_id,
            "assignee_ids": assignee_ids,
            "reviewer_ids": reviewer_ids,
            "milestone_id": milestone_id,
            "labels": labels,
            "add_labels": add_labels,
            "remove_labels": remove_labels,
            "description": description,
            "state_event": state_event,
            "remove_source_branch": remove_source_branch,
            "squash": squash,
            "discussion_locked": discussion_locked,
            "allow_collaboration": allow_collaboration,
            "allow_maintainer_to_push": allow_maintainer_to_push
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/merge_requests/{merge_request_iid}", json_data=data)

    @mcp.tool()
    async def delete_merge_request(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Only for admins and project owners. Deletes the merge request in question."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/merge_requests/{merge_request_iid}")

    @mcp.tool()
    async def accept_mr(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        merge_commit_message: Optional[str] = Field(default=None, description="Custom merge commit message"),
        squash_commit_message: Optional[str] = Field(default=None, description="Custom squash commit message"),
        squash: Optional[bool] = Field(default=None, description="if true the commits are squashed into a single commit on merge"),
        should_remove_source_branch: Optional[bool] = Field(default=None, description="if true removes the source branch"),
        merge_when_pipeline_succeeds: Optional[bool] = Field(default=None, description="if true the MR is merged when the pipeline succeeds"),
        sha: Optional[str] = Field(default=None, description="if present, then this SHA must match the HEAD of the source branch, otherwise the merge fails")
    ) -> Dict[str, Any]:
        """Accept and merge changes submitted with merge request using this API."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "merge_commit_message": merge_commit_message,
            "squash_commit_message": squash_commit_message,
            "squash": squash,
            "should_remove_source_branch": should_remove_source_branch,
            "merge_when_pipeline_succeeds": merge_when_pipeline_succeeds,
            "sha": sha
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/merge_requests/{merge_request_iid}/merge", json_data=data)

    @mcp.tool()
    async def merge_ref(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Merge the changes between the merge request source and target branches into refs/merge-requests/:iid/merge ref."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/merge_ref")

    @mcp.tool()
    async def cancel_merge_when_pipeline_succeeds(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Cancel Merge When Pipeline Succeeds."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/cancel_merge_when_pipeline_succeeds")

    @mcp.tool()
    async def rebase_merge_request(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        skip_ci: Optional[bool] = Field(default=None, description="Set to true to skip creating a CI pipeline")
    ) -> Dict[str, Any]:
        """Automatically rebase the source_branch of the merge request against its target_branch."""
        client = await get_gitlab_client()
        data = {}
        if skip_ci is not None:
            data["skip_ci"] = skip_ci
        return await client.put(f"/projects/{project_id}/merge_requests/{merge_request_iid}/rebase", json_data=data)

    @mcp.tool()
    async def get_merge_request_diff_versions(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Get a list of merge request diff versions."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/versions")

    @mcp.tool()
    async def get_single_mr_diff_version(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        version_id: str = Field(description="The ID of the merge request diff version")
    ) -> Dict[str, Any]:
        """Get a single merge request diff version."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/versions/{version_id}")

    @mcp.tool()
    async def set_mr_time_estimate(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        duration: str = Field(description="The duration in human format. e.g: 3h30m")
    ) -> Dict[str, Any]:
        """Sets an estimated time of work for this merge request."""
        client = await get_gitlab_client()
        data = {"duration": duration}
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/time_estimate", json_data=data)

    @mcp.tool()
    async def reset_mr_time_estimate(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Resets the estimated time for this merge request to 0 seconds."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/reset_time_estimate")

    @mcp.tool()
    async def add_mr_spent_time(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request"),
        duration: str = Field(description="The duration in human format. e.g: 3h30m")
    ) -> Dict[str, Any]:
        """Adds spent time for this merge request."""
        client = await get_gitlab_client()
        data = {"duration": duration}
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/add_spent_time", json_data=data)

    @mcp.tool()
    async def reset_mr_spent_time(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Resets the total spent time for this merge request to 0 seconds."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/reset_spent_time")

    @mcp.tool()
    async def get_mr_time_stats(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Show time stats for a merge request."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/time_stats")

    @mcp.tool()
    async def subscribe_to_mr(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Subscribes the authenticated user to a merge request to receive notifications."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/subscribe")

    @mcp.tool()
    async def unsubscribe_from_mr(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Unsubscribes the authenticated user from a merge request to not receive notifications."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/unsubscribe")

    @mcp.tool()
    async def create_mr_todo(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Manually creates a todo for the current user on a merge request."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/merge_requests/{merge_request_iid}/todo")

    @mcp.tool()
    async def get_mr_issues_that_will_close(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        merge_request_iid: str = Field(description="The internal ID of the merge request")
    ) -> Dict[str, Any]:
        """Get all the issues that would be closed by merging the provided merge request."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/merge_requests/{merge_request_iid}/closes_issues")