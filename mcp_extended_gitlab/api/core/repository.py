"""GitLab Repository API - File and repository operations.

This module provides comprehensive access to GitLab's repository features,
including file management, tree browsing, archives, and comparisons.
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
    """Register all Repository API tools.
    
    This function registers the following tools:
    - Repository tree browsing
    - File operations (CRUD)
    - File content retrieval (raw, blame)
    - Repository metadata (contributors, archive)
    - Branch/tag/commit comparisons
    """
    
    @mcp.tool()
    async def list_repository_tree(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        path: Optional[str] = Field(default=None, description="The path inside repository. Used to get content of subdirectories"),
        ref: Optional[str] = Field(default=None, description="The name of a repository branch or tag or if not given the default branch"),
        recursive: Optional[bool] = Field(default=False, description="Boolean value used to get a recursive tree (false by default)"),
        per_page: Optional[int] = Field(default=None, description="Number of results to show"),
        page: Optional[int] = Field(default=None, description="Page number")) -> Dict[str, Any]:
        """Get a list of repository files and directories in a project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "path": path,
            "ref": ref,
            "recursive": recursive,
            "per_page": per_page,
            "page": page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/repository/tree", params=params)

    @mcp.tool()
    async def get_raw_file(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_path: str = Field(description="URL-encoded full path to new file"),
        ref: Optional[str] = Field(default=None, description="The name of branch, tag or commit")) -> Dict[str, Any]:
        """Get raw file from repository."""
        client = await get_gitlab_client()
        params = {}
        if ref:
            params["ref"] = ref
        return await client.get(f"/projects/{project_id}/repository/files/{file_path}/raw", params=params)

    @mcp.tool()
    async def get_file_from_repository(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_path: str = Field(description="URL-encoded full path to new file"),
        ref: str = Field(description="The name of branch, tag or commit")) -> Dict[str, Any]:
        """Get file from repository."""
        client = await get_gitlab_client()
        params = {"ref": ref}
        return await client.get(f"/projects/{project_id}/repository/files/{file_path}", params=params)

    @mcp.tool()
    async def get_file_blame(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_path: str = Field(description="URL-encoded full path to new file"),
        ref: str = Field(description="The name of branch, tag or commit"),
        range_start: Optional[int] = Field(default=None, description="The first line of the range to blame"),
        range_end: Optional[int] = Field(default=None, description="The last line of the range to blame")) -> Dict[str, Any]:
        """Get file blame from repository."""
        client = await get_gitlab_client()
        params = {"ref": ref}
        if range_start:
            params["range[start]"] = range_start
        if range_end:
            params["range[end]"] = range_end
        return await client.get(f"/projects/{project_id}/repository/files/{file_path}/blame", params=params)

    @mcp.tool()
    async def create_file(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_path: str = Field(description="URL-encoded full path to new file"),
        branch: str = Field(description="Name of the new branch to create"),
        content: str = Field(description="File content"),
        commit_message: str = Field(description="Commit message"),
        start_branch: Optional[str] = Field(default=None, description="Name of the base branch to create the new branch from"),
        encoding: Optional[str] = Field(default="text", description="Change encoding to base64. Default is text"),
        author_email: Optional[str] = Field(default=None, description="Specify the commit author's email address"),
        author_name: Optional[str] = Field(default=None, description="Specify the commit author's name"),
        execute_filemode: Optional[bool] = Field(default=False, description="Enables or disables the execute flag on the file")) -> Dict[str, Any]:
        """Create new file in repository."""
        client = await get_gitlab_client()
        data = {
            "branch": branch,
            "content": content,
            "commit_message": commit_message
        }
        for key, value in {
            "start_branch": start_branch,
            "encoding": encoding,
            "author_email": author_email,
            "author_name": author_name,
            "execute_filemode": execute_filemode
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/repository/files/{file_path}", json_data=data)

    @mcp.tool()
    async def update_existing_file(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_path: str = Field(description="URL-encoded full path to new file"),
        branch: str = Field(description="Name of the new branch to create"),
        content: str = Field(description="File content"),
        commit_message: str = Field(description="Commit message"),
        start_branch: Optional[str] = Field(default=None, description="Name of the base branch to create the new branch from"),
        encoding: Optional[str] = Field(default="text", description="Change encoding to base64. Default is text"),
        author_email: Optional[str] = Field(default=None, description="Specify the commit author's email address"),
        author_name: Optional[str] = Field(default=None, description="Specify the commit author's name"),
        last_commit_id: Optional[str] = Field(default=None, description="Last known file commit ID"),
        execute_filemode: Optional[bool] = Field(default=None, description="Enables or disables the execute flag on the file")) -> Dict[str, Any]:
        """Update existing file in repository."""
        client = await get_gitlab_client()
        data = {
            "branch": branch,
            "content": content,
            "commit_message": commit_message
        }
        for key, value in {
            "start_branch": start_branch,
            "encoding": encoding,
            "author_email": author_email,
            "author_name": author_name,
            "last_commit_id": last_commit_id,
            "execute_filemode": execute_filemode
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}/repository/files/{file_path}", json_data=data)

    @mcp.tool()
    async def delete_existing_file(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_path: str = Field(description="URL-encoded full path to new file"),
        branch: str = Field(description="Name of the new branch to create"),
        commit_message: str = Field(description="Commit message"),
        start_branch: Optional[str] = Field(default=None, description="Name of the base branch to create the new branch from"),
        author_email: Optional[str] = Field(default=None, description="Specify the commit author's email address"),
        author_name: Optional[str] = Field(default=None, description="Specify the commit author's name"),
        last_commit_id: Optional[str] = Field(default=None, description="Last known file commit ID")) -> Dict[str, Any]:
        """Delete existing file in repository."""
        client = await get_gitlab_client()
        data = {
            "branch": branch,
            "commit_message": commit_message
        }
        for key, value in {
            "start_branch": start_branch,
            "author_email": author_email,
            "author_name": author_name,
            "last_commit_id": last_commit_id
        }.items():
            if value is not None:
                data[key] = value
        return await client.delete(f"/projects/{project_id}/repository/files/{file_path}", json_data=data)

    @mcp.tool()
    async def list_repository_contributors(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        order_by: Optional[str] = Field(default=None, description="Return contributors ordered by name, email, or commits fields"),
        sort: Optional[str] = Field(default=None, description="Return contributors sorted in asc or desc order")) -> Dict[str, Any]:
        """Get repository contributors list."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/repository/contributors", params=params)

    @mcp.tool()
    async def get_repository_archive(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        sha: Optional[str] = Field(default=None, description="The commit SHA to download. A tag, branch reference, or SHA can be used"),
        format: Optional[str] = Field(default="tar.gz", description="The archive format. Default is tar.gz")) -> Dict[str, Any]:
        """Get an archive of the repository."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "sha": sha,
            "format": format
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/repository/archive", params=params)

    @mcp.tool()
    async def compare_branches_tags_commits(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        from_ref: str = Field(description="The commit SHA or branch name"),
        to_ref: str = Field(description="The commit SHA or branch name"),
        straight: Optional[bool] = Field(default=False, description="Comparison method, true for direct comparison between from and to (from..to), false to compare using merge base (from...to)")) -> Dict[str, Any]:
        """Compare branches, tags or commits."""
        client = await get_gitlab_client()
        params = {
            "from": from_ref,
            "to": to_ref
        }
        if straight is not None:
            params["straight"] = straight
        return await client.get(f"/projects/{project_id}/repository/compare", params=params)

    @mcp.tool()
    async def list_repository_submodules(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        ref: Optional[str] = Field(default=None, description="The commit SHA or branch name")) -> Dict[str, Any]:
        """List repository submodules."""
        client = await get_gitlab_client()
        params = {}
        if ref:
            params["ref"] = ref
        return await client.get(f"/projects/{project_id}/repository/submodules", params=params)

    @mcp.tool()
    async def get_repository_changelog(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        version: str = Field(description="The version to generate changelog for"),
        from_ref: Optional[str] = Field(default=None, description="The SHA or branch name to start from"),
        to_ref: Optional[str] = Field(default=None, description="The SHA or branch name to end at"),
        date: Optional[str] = Field(default=None, description="The date and time of the release")) -> Dict[str, Any]:
        """Generate changelog data for a repository."""
        client = await get_gitlab_client()
        params = {"version": version}
        for key, value in {
            "from": from_ref,
            "to": to_ref,
            "date": date
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/repository/changelog", params=params)

    @mcp.tool()
    async def create_repository_changelog(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        version: str = Field(description="The version to generate changelog for"),
        branch: Optional[str] = Field(default=None, description="The branch to commit the changelog changes to"),
        config_file: Optional[str] = Field(default=None, description="The path of changelog configuration file"),
        date: Optional[str] = Field(default=None, description="The date and time of the release"),
        file: Optional[str] = Field(default="CHANGELOG.md", description="The file to commit the changelog changes to"),
        from_ref: Optional[str] = Field(default=None, description="The SHA or branch name to start from"),
        message: Optional[str] = Field(default=None, description="The commit message to use when committing the changelog"),
        to_ref: Optional[str] = Field(default=None, description="The SHA or branch name to end at"),
        trailer: Optional[str] = Field(default=None, description="The Git trailer to use for including commits")) -> Dict[str, Any]:
        """Generate changelog data for a repository and commit it."""
        client = await get_gitlab_client()
        data = {"version": version}
        for key, value in {
            "branch": branch,
            "config_file": config_file,
            "date": date,
            "file": file,
            "from": from_ref,
            "message": message,
            "to": to_ref,
            "trailer": trailer
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/repository/changelog", json_data=data)