"""GitLab Commits API - Git commit operations and information.

This module provides comprehensive access to GitLab's commit management features,
including creating commits, cherry-picking, reverting, and commit metadata.
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
    """Register all Commits API tools.
    
    This function registers the following tools:
    - Commit listing and search
    - Commit creation with multiple file operations
    - Commit information (diff, status, GPG signature)
    - Commit operations (cherry-pick, revert)
    - Commit comments and discussions
    - Commit build statuses
    """
    
    @mcp.tool()
    async def list_repository_commits(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        ref_name: Optional[str] = Field(default=None, description="The name of a repository branch, tag or revision range, or if not given the default branch"),
        since: Optional[str] = Field(default=None, description="Only commits after or on this date will be returned in ISO 8601 format"),
        until: Optional[str] = Field(default=None, description="Only commits before or on this date will be returned in ISO 8601 format"),
        path: Optional[str] = Field(default=None, description="The file path"),
        author: Optional[str] = Field(default=None, description="Search commits by author name"),
        all: Optional[bool] = Field(default=None, description="Retrieve every commit from the repository"),
        with_stats: Optional[bool] = Field(default=None, description="Stats about each commit will be added to the response"),
        first_parent: Optional[bool] = Field(default=None, description="Follow only the first parent commit upon seeing a merge commit"),
        order: Optional[str] = Field(default=None, description="List commits in order. Possible values: default, topo"),
        trailers: Optional[bool] = Field(default=None, description="Parse and include Git trailers for each commit"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List repository commits."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "ref_name": ref_name,
            "since": since,
            "until": until,
            "path": path,
            "author": author,
            "all": all,
            "with_stats": with_stats,
            "first_parent": first_parent,
            "order": order,
            "trailers": trailers,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/repository/commits", params=params)

    @mcp.tool()
    async def create_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        branch: str = Field(description="Name of the branch to commit into"),
        commit_message: str = Field(description="Commit message"),
        start_branch: Optional[str] = Field(default=None, description="Name of the branch to start the new commit from"),
        start_sha: Optional[str] = Field(default=None, description="SHA of the commit to start the new commit from"),
        start_project: Optional[str] = Field(default=None, description="The project ID or URL-encoded path of the project to start the new commit from"),
        actions: List[Dict[str, Any]] = Field(description="An array of action hashes to commit as a batch"),
        author_email: Optional[str] = Field(default=None, description="Specify the commit author's email address"),
        author_name: Optional[str] = Field(default=None, description="Specify the commit author's name"),
        stats: Optional[bool] = Field(default=True, description="Include commit stats"),
        force: Optional[bool] = Field(default=False, description="When true overwrites the target branch with a new commit based on the start_branch or start_sha")
    ) -> Dict[str, Any]:
        """Create a commit with multiple files and actions."""
        client = await get_gitlab_client()
        data = {
            "branch": branch,
            "commit_message": commit_message,
            "actions": actions
        }
        for key, value in {
            "start_branch": start_branch,
            "start_sha": start_sha,
            "start_project": start_project,
            "author_email": author_email,
            "author_name": author_name,
            "stats": stats,
            "force": force
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/repository/commits", json_data=data)

    @mcp.tool()
    async def get_single_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash or name of a repository branch or tag"),
        stats: Optional[bool] = Field(default=True, description="Include commit stats")
    ) -> Dict[str, Any]:
        """Get a single commit."""
        client = await get_gitlab_client()
        params = {}
        if stats is not None:
            params["stats"] = stats
        return await client.get(f"/projects/{project_id}/repository/commits/{sha}", params=params)

    @mcp.tool()
    async def get_references_commit_is_pushed_to(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash"),
        type: Optional[str] = Field(default="all", description="The scope of commits. Possible values branch, tag, all. Default is all.")
    ) -> Dict[str, Any]:
        """Get references a commit is pushed to."""
        client = await get_gitlab_client()
        params = {}
        if type:
            params["type"] = type
        return await client.get(f"/projects/{project_id}/repository/commits/{sha}/refs", params=params)

    @mcp.tool()
    async def cherry_pick_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash"),
        branch: str = Field(description="The name of the branch")
    ) -> Dict[str, Any]:
        """Cherry-pick a commit."""
        client = await get_gitlab_client()
        data = {"branch": branch}
        return await client.post(f"/projects/{project_id}/repository/commits/{sha}/cherry_pick", json_data=data)

    @mcp.tool()
    async def revert_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash"),
        branch: str = Field(description="The name of the branch")
    ) -> Dict[str, Any]:
        """Revert a commit."""
        client = await get_gitlab_client()
        data = {"branch": branch}
        return await client.post(f"/projects/{project_id}/repository/commits/{sha}/revert", json_data=data)

    @mcp.tool()
    async def get_diff_of_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash")
    ) -> Dict[str, Any]:
        """Get the diff of a commit."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/repository/commits/{sha}/diff")

    @mcp.tool()
    async def get_comments_of_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash")
    ) -> Dict[str, Any]:
        """Get the comments of a commit."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/repository/commits/{sha}/comments")

    @mcp.tool()
    async def post_comment_to_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash"),
        note: str = Field(description="The text of the comment"),
        path: Optional[str] = Field(default=None, description="The file path relative to the repository"),
        line: Optional[int] = Field(default=None, description="The line number where the comment should be placed"),
        line_type: Optional[str] = Field(default=None, description="The line type. Takes new or old as arguments")
    ) -> Dict[str, Any]:
        """Post comment to commit."""
        client = await get_gitlab_client()
        data = {"note": note}
        for key, value in {
            "path": path,
            "line": line,
            "line_type": line_type
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/repository/commits/{sha}/comments", json_data=data)

    @mcp.tool()
    async def get_commit_statuses(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit SHA"),
        ref: Optional[str] = Field(default=None, description="The name of a repository branch or tag or, if not given, the default branch"),
        stage: Optional[str] = Field(default=None, description="Filter by build stage"),
        name: Optional[str] = Field(default=None, description="Filter by job name"),
        all: Optional[bool] = Field(default=None, description="Return all statuses, not only the latest ones")
    ) -> Dict[str, Any]:
        """Get statuses of a commit."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "ref": ref,
            "stage": stage,
            "name": name,
            "all": all
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/statuses/{sha}", params=params)

    @mcp.tool()
    async def post_build_status_to_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit SHA"),
        state: str = Field(description="The state of the status. Can be one of the following: pending, running, success, failed, canceled"),
        ref: Optional[str] = Field(default=None, description="The ref (branch or tag) to which the status refers"),
        name: Optional[str] = Field(default=None, description="The label to differentiate this status from the status of other systems"),
        target_url: Optional[str] = Field(default=None, description="The target URL to associate with this status"),
        description: Optional[str] = Field(default=None, description="The short description of the status"),
        coverage: Optional[float] = Field(default=None, description="The total code coverage"),
        pipeline_id: Optional[int] = Field(default=None, description="The ID of the pipeline to set status")
    ) -> Dict[str, Any]:
        """Post build status to commit."""
        client = await get_gitlab_client()
        data = {"state": state}
        for key, value in {
            "ref": ref,
            "name": name,
            "target_url": target_url,
            "description": description,
            "coverage": coverage,
            "pipeline_id": pipeline_id
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/statuses/{sha}", json_data=data)

    @mcp.tool()
    async def list_merge_requests_associated_with_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit SHA")
    ) -> Dict[str, Any]:
        """List merge requests associated with a commit."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/repository/commits/{sha}/merge_requests")

    @mcp.tool()
    async def get_gpg_signature_of_commit(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: str = Field(description="The commit hash")
    ) -> Dict[str, Any]:
        """Get GPG signature of a commit."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/repository/commits/{sha}/signature")