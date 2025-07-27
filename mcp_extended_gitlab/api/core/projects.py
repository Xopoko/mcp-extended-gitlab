"""GitLab Projects API - Project management and operations.

This module provides comprehensive access to GitLab's project management features,
including project creation, configuration, members, forking, and more.
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
    """Register all Projects API tools.
    
    This function registers the following tools:
    - Project listing and search
    - Project CRUD operations
    - Project configuration (visibility, features, etc.)
    - Project members management
    - Project forking and starring
    - Project archiving and housekeeping
    - Project statistics and languages
    """
    
    @mcp.tool()
    async def list_projects(
        archived: Optional[bool] = Field(default=None, description="Limit by archived status"),
        visibility: Optional[str] = Field(default=None, description="Limit by visibility (public, internal, private)"),
        order_by: Optional[str] = Field(default=None, description="Return projects ordered by id, name, path, created_at, updated_at, last_activity_at fields"),
        sort: Optional[str] = Field(default=None, description="Return projects sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Return list of projects matching the search criteria"),
        simple: Optional[bool] = Field(default=None, description="Return only limited fields for each project"),
        owned: Optional[bool] = Field(default=None, description="Limit by projects explicitly owned by the current user"),
        membership: Optional[bool] = Field(default=None, description="Limit by projects that the current user is a member of"),
        starred: Optional[bool] = Field(default=None, description="Limit by projects starred by the current user"),
        statistics: Optional[bool] = Field(default=None, description="Include project statistics"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        with_issues_enabled: Optional[bool] = Field(default=None, description="Limit by enabled issues feature"),
        with_merge_requests_enabled: Optional[bool] = Field(default=None, description="Limit by enabled merge requests feature"),
        with_programming_language: Optional[str] = Field(default=None, description="Limit by projects which use the given programming language"),
        wiki_checksum_failed: Optional[bool] = Field(default=None, description="Limit projects where the wiki checksum calculation has failed"),
        repository_checksum_failed: Optional[bool] = Field(default=None, description="Limit projects where the repository checksum calculation has failed"),
        min_access_level: Optional[int] = Field(default=None, description="Limit by current user minimal access level"),
        id_after: Optional[int] = Field(default=None, description="Limit results to projects with IDs greater than the specified ID"),
        id_before: Optional[int] = Field(default=None, description="Limit results to projects with IDs less than the specified ID"),
        last_activity_after: Optional[str] = Field(default=None, description="Limit results to projects with last_activity after specified time"),
        last_activity_before: Optional[str] = Field(default=None, description="Limit results to projects with last_activity before specified time"),
        repository_storage: Optional[str] = Field(default=None, description="Limit results to projects stored on repository_storage"),
        topic: Optional[str] = Field(default=None, description="Limit results to projects with the assigned topic"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List all visible projects across GitLab for the authenticated user."""
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
            "membership": membership,
            "starred": starred,
            "statistics": statistics,
            "with_custom_attributes": with_custom_attributes,
            "with_issues_enabled": with_issues_enabled,
            "with_merge_requests_enabled": with_merge_requests_enabled,
            "with_programming_language": with_programming_language,
            "wiki_checksum_failed": wiki_checksum_failed,
            "repository_checksum_failed": repository_checksum_failed,
            "min_access_level": min_access_level,
            "id_after": id_after,
            "id_before": id_before,
            "last_activity_after": last_activity_after,
            "last_activity_before": last_activity_before,
            "repository_storage": repository_storage,
            "topic": topic,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/projects", params=params)

    @mcp.tool()
    async def list_user_projects(
        user_id: str = Field(description="The ID or username of the user"),
        archived: Optional[bool] = Field(default=None, description="Limit by archived status"),
        visibility: Optional[str] = Field(default=None, description="Limit by visibility"),
        order_by: Optional[str] = Field(default=None, description="Return projects ordered by field"),
        sort: Optional[str] = Field(default=None, description="Return projects sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Return list of projects matching the search criteria"),
        simple: Optional[bool] = Field(default=None, description="Return only limited fields for each project"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List projects for a specific user."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "archived": archived,
            "visibility": visibility,
            "order_by": order_by,
            "sort": sort,
            "search": search,
            "simple": simple,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/users/{user_id}/projects", params=params)

    @mcp.tool()
    async def list_starred_projects(
        user_id: str = Field(description="The ID or username of the user"),
        archived: Optional[bool] = Field(default=None, description="Limit by archived status"),
        visibility: Optional[str] = Field(default=None, description="Limit by visibility"),
        order_by: Optional[str] = Field(default=None, description="Return projects ordered by field"),
        sort: Optional[str] = Field(default=None, description="Return projects sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Return list of projects matching the search criteria"),
        simple: Optional[bool] = Field(default=None, description="Return only limited fields for each project"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List projects starred by a user."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "archived": archived,
            "visibility": visibility,
            "order_by": order_by,
            "sort": sort,
            "search": search,
            "simple": simple,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/users/{user_id}/starred_projects", params=params)

    @mcp.tool()
    async def get_single_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        statistics: Optional[bool] = Field(default=None, description="Include project statistics"),
        license: Optional[bool] = Field(default=None, description="Include project license data"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response")
    ) -> Dict[str, Any]:
        """Get a specific project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "statistics": statistics,
            "license": license,
            "with_custom_attributes": with_custom_attributes
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}", params=params)

    @mcp.tool()
    async def create_project(
        name: str = Field(description="The name of the new project"),
        path: Optional[str] = Field(default=None, description="Custom repository name for project"),
        namespace_id: Optional[int] = Field(default=None, description="Namespace for the new project (defaults to the current user's namespace)"),
        description: Optional[str] = Field(default=None, description="Short project description"),
        issues_enabled: Optional[bool] = Field(default=None, description="Enable issues for this project"),
        merge_requests_enabled: Optional[bool] = Field(default=None, description="Enable merge requests for this project"),
        jobs_enabled: Optional[bool] = Field(default=None, description="Enable jobs for this project"),
        wiki_enabled: Optional[bool] = Field(default=None, description="Enable wiki for this project"),
        snippets_enabled: Optional[bool] = Field(default=None, description="Enable snippets for this project"),
        resolve_outdated_diff_discussions: Optional[bool] = Field(default=None, description="Automatically resolve merge request diffs discussions on lines changed with a push"),
        container_registry_enabled: Optional[bool] = Field(default=None, description="Enable container registry for this project"),
        shared_runners_enabled: Optional[bool] = Field(default=None, description="Enable shared runners for this project"),
        visibility: Optional[str] = Field(default=None, description="See project visibility level"),
        import_url: Optional[str] = Field(default=None, description="URL to import repository from"),
        public_builds: Optional[bool] = Field(default=None, description="If true, jobs can be viewed by non-project-members"),
        only_allow_merge_if_pipeline_succeeds: Optional[bool] = Field(default=None, description="Set whether merge requests can only be merged with successful pipelines"),
        only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = Field(default=None, description="Set whether merge requests can only be merged when all the discussions are resolved"),
        merge_method: Optional[str] = Field(default=None, description="Set the merge method used"),
        forking_access_level: Optional[str] = Field(default=None, description="One of disabled, private or enabled"),
        remove_source_branch_after_merge: Optional[bool] = Field(default=None, description="Enable Delete source branch option by default for all new merge requests"),
        autoclose_referenced_issues: Optional[bool] = Field(default=None, description="Set whether auto-closing referenced issues on default branch"),
        build_timeout: Optional[int] = Field(default=None, description="The maximum amount of time in minutes that a job is able run"),
        default_branch: Optional[str] = Field(default=None, description="The default branch"),
        tags: Optional[List[str]] = Field(default=None, description="The list of tags for a project")
    ) -> Dict[str, Any]:
        """Create a new project."""
        client = await get_gitlab_client()
        data = {"name": name}
        for key, value in {
            "path": path,
            "namespace_id": namespace_id,
            "description": description,
            "issues_enabled": issues_enabled,
            "merge_requests_enabled": merge_requests_enabled,
            "jobs_enabled": jobs_enabled,
            "wiki_enabled": wiki_enabled,
            "snippets_enabled": snippets_enabled,
            "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
            "container_registry_enabled": container_registry_enabled,
            "shared_runners_enabled": shared_runners_enabled,
            "visibility": visibility,
            "import_url": import_url,
            "public_builds": public_builds,
            "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
            "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
            "merge_method": merge_method,
            "forking_access_level": forking_access_level,
            "remove_source_branch_after_merge": remove_source_branch_after_merge,
            "autoclose_referenced_issues": autoclose_referenced_issues,
            "build_timeout": build_timeout,
            "default_branch": default_branch,
            "tags": tags
        }.items():
            if value is not None:
                data[key] = value
        return await client.post("/projects", json_data=data)

    @mcp.tool()
    async def update_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        name: Optional[str] = Field(default=None, description="The name of the project"),
        path: Optional[str] = Field(default=None, description="Custom repository name for the project"),
        description: Optional[str] = Field(default=None, description="Short project description"),
        issues_enabled: Optional[bool] = Field(default=None, description="Enable issues for this project"),
        merge_requests_enabled: Optional[bool] = Field(default=None, description="Enable merge requests for this project"),
        jobs_enabled: Optional[bool] = Field(default=None, description="Enable jobs for this project"),
        wiki_enabled: Optional[bool] = Field(default=None, description="Enable wiki for this project"),
        snippets_enabled: Optional[bool] = Field(default=None, description="Enable snippets for this project"),
        resolve_outdated_diff_discussions: Optional[bool] = Field(default=None, description="Automatically resolve merge request diffs discussions on lines changed with a push"),
        container_registry_enabled: Optional[bool] = Field(default=None, description="Enable container registry for this project"),
        shared_runners_enabled: Optional[bool] = Field(default=None, description="Enable shared runners for this project"),
        visibility: Optional[str] = Field(default=None, description="See project visibility level"),
        public_builds: Optional[bool] = Field(default=None, description="If true, jobs can be viewed by non-project-members"),
        only_allow_merge_if_pipeline_succeeds: Optional[bool] = Field(default=None, description="Set whether merge requests can only be merged with successful pipelines"),
        only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = Field(default=None, description="Set whether merge requests can only be merged when all the discussions are resolved"),
        merge_method: Optional[str] = Field(default=None, description="Set the merge method used"),
        forking_access_level: Optional[str] = Field(default=None, description="One of disabled, private or enabled"),
        remove_source_branch_after_merge: Optional[bool] = Field(default=None, description="Enable Delete source branch option by default for all new merge requests"),
        autoclose_referenced_issues: Optional[bool] = Field(default=None, description="Set whether auto-closing referenced issues on default branch"),
        build_timeout: Optional[int] = Field(default=None, description="The maximum amount of time in minutes that a job is able run"),
        default_branch: Optional[str] = Field(default=None, description="The default branch"),
        tags: Optional[List[str]] = Field(default=None, description="The list of tags for a project")
    ) -> Dict[str, Any]:
        """Update a project."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "name": name,
            "path": path,
            "description": description,
            "issues_enabled": issues_enabled,
            "merge_requests_enabled": merge_requests_enabled,
            "jobs_enabled": jobs_enabled,
            "wiki_enabled": wiki_enabled,
            "snippets_enabled": snippets_enabled,
            "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
            "container_registry_enabled": container_registry_enabled,
            "shared_runners_enabled": shared_runners_enabled,
            "visibility": visibility,
            "public_builds": public_builds,
            "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
            "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
            "merge_method": merge_method,
            "forking_access_level": forking_access_level,
            "remove_source_branch_after_merge": remove_source_branch_after_merge,
            "autoclose_referenced_issues": autoclose_referenced_issues,
            "build_timeout": build_timeout,
            "default_branch": default_branch,
            "tags": tags
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/projects/{project_id}", json_data=data)

    @mcp.tool()
    async def fork_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        namespace: Optional[str] = Field(default=None, description="The ID or path of the namespace that the project is forked to"),
        namespace_id: Optional[int] = Field(default=None, description="The ID of the namespace that the project is forked to"),
        namespace_path: Optional[str] = Field(default=None, description="The path of the namespace that the project is forked to"),
        path: Optional[str] = Field(default=None, description="The path that is assigned to the resultant project after forking"),
        name: Optional[str] = Field(default=None, description="The name that is assigned to the resultant project after forking"),
        description: Optional[str] = Field(default=None, description="The description assigned to the resultant project after forking"),
        visibility: Optional[str] = Field(default=None, description="The visibility level assigned to the resultant project after forking")
    ) -> Dict[str, Any]:
        """Fork a project."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "namespace": namespace,
            "namespace_id": namespace_id,
            "namespace_path": namespace_path,
            "path": path,
            "name": name,
            "description": description,
            "visibility": visibility
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/fork", json_data=data)

    @mcp.tool()
    async def list_forks_of_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        archived: Optional[bool] = Field(default=None, description="Limit by archived status"),
        visibility: Optional[str] = Field(default=None, description="Limit by visibility"),
        order_by: Optional[str] = Field(default=None, description="Return projects ordered by field"),
        sort: Optional[str] = Field(default=None, description="Return projects sorted in asc or desc order"),
        search: Optional[str] = Field(default=None, description="Return list of projects matching the search criteria"),
        simple: Optional[bool] = Field(default=None, description="Return only limited fields for each project"),
        owned: Optional[bool] = Field(default=None, description="Limit by projects explicitly owned by the current user"),
        membership: Optional[bool] = Field(default=None, description="Limit by projects that the current user is a member of"),
        starred: Optional[bool] = Field(default=None, description="Limit by projects starred by the current user"),
        statistics: Optional[bool] = Field(default=None, description="Include project statistics"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        with_issues_enabled: Optional[bool] = Field(default=None, description="Limit by enabled issues feature"),
        with_merge_requests_enabled: Optional[bool] = Field(default=None, description="Limit by enabled merge requests feature"),
        min_access_level: Optional[int] = Field(default=None, description="Limit by current user minimal access level"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List forks of a project."""
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
            "membership": membership,
            "starred": starred,
            "statistics": statistics,
            "with_custom_attributes": with_custom_attributes,
            "with_issues_enabled": with_issues_enabled,
            "with_merge_requests_enabled": with_merge_requests_enabled,
            "min_access_level": min_access_level,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/forks", params=params)

    @mcp.tool()
    async def star_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Star a project."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/star")

    @mcp.tool()
    async def unstar_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Unstar a project."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/unstar")

    @mcp.tool()
    async def list_starrers(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        search: Optional[str] = Field(default=None, description="Search for starrers by name or username"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List the users who starred a project."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "search": search,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/starrers", params=params)

    @mcp.tool()
    async def archive_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Archive a project."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/archive")

    @mcp.tool()
    async def unarchive_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Unarchive a project."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/unarchive")

    @mcp.tool()
    async def delete_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        permanently_remove: Optional[bool] = Field(default=None, description="Permanently remove project instead of soft-delete")
    ) -> Dict[str, Any]:
        """Delete a project."""
        client = await get_gitlab_client()
        params = {}
        if permanently_remove is not None:
            params["permanently_remove"] = permanently_remove
        return await client.delete(f"/projects/{project_id}", params=params)

    @mcp.tool()
    async def restore_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Restore project marked for deletion."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/restore")

    @mcp.tool()
    async def upload_file(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        file_content: str = Field(description="File content to upload"),
        file_name: str = Field(description="Name of the file")
    ) -> Dict[str, Any]:
        """Upload a file to the project."""
        client = await get_gitlab_client()
        # Note: In real implementation, this would need multipart form data
        files = {"file": (file_name, file_content)}
        return await client.post(f"/projects/{project_id}/uploads", files=files)

    @mcp.tool()
    async def share_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        group_id: int = Field(description="The ID of the group to share with"),
        group_access: int = Field(description="The access level to grant"),
        expires_at: Optional[str] = Field(default=None, description="Share expiration date in ISO 8601 format")
    ) -> Dict[str, Any]:
        """Share project with a group."""
        client = await get_gitlab_client()
        data = {
            "group_id": group_id,
            "group_access": group_access
        }
        if expires_at is not None:
            data["expires_at"] = expires_at
        return await client.post(f"/projects/{project_id}/share", json_data=data)

    @mcp.tool()
    async def delete_shared_project_link(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        group_id: int = Field(description="The ID of the group")
    ) -> Dict[str, Any]:
        """Delete a shared project link within a group."""
        client = await get_gitlab_client()
        return await client.delete(f"/projects/{project_id}/share/{group_id}")

    @mcp.tool()
    async def project_housekeeping(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Start the housekeeping task for a project."""
        client = await get_gitlab_client()
        return await client.post(f"/projects/{project_id}/housekeeping")

    @mcp.tool()
    async def transfer_project(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        namespace: str = Field(description="The ID or path of the namespace to transfer to")
    ) -> Dict[str, Any]:
        """Transfer a project to a new namespace."""
        client = await get_gitlab_client()
        data = {"namespace": namespace}
        return await client.put(f"/projects/{project_id}/transfer", json_data=data)

    @mcp.tool()
    async def get_project_push_rules(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Get project push rules."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/push_rule")

    @mcp.tool()
    async def add_project_push_rule(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        deny_delete_tag: Optional[bool] = Field(default=None, description="Deny deleting a tag"),
        member_check: Optional[bool] = Field(default=None, description="Restrict commits by author (email) to existing GitLab users"),
        prevent_secrets: Optional[bool] = Field(default=None, description="GitLab rejects any files that are likely to contain secrets"),
        commit_message_regex: Optional[str] = Field(default=None, description="All commit messages must match this regex"),
        commit_message_negative_regex: Optional[str] = Field(default=None, description="No commit message is allowed to match this regex"),
        branch_name_regex: Optional[str] = Field(default=None, description="All branch names must match this regex"),
        author_email_regex: Optional[str] = Field(default=None, description="All commit author emails must match this regex"),
        file_name_regex: Optional[str] = Field(default=None, description="All committed filenames must not match this regex"),
        max_file_size: Optional[int] = Field(default=None, description="Maximum file size (MB)"),
        commit_committer_check: Optional[bool] = Field(default=None, description="Users can only push commits to this repository that were committed with one of their own verified emails"),
        reject_unsigned_commits: Optional[bool] = Field(default=None, description="Reject commit when it is not signed through GPG")
    ) -> Dict[str, Any]:
        """Add project push rule."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "deny_delete_tag": deny_delete_tag,
            "member_check": member_check,
            "prevent_secrets": prevent_secrets,
            "commit_message_regex": commit_message_regex,
            "commit_message_negative_regex": commit_message_negative_regex,
            "branch_name_regex": branch_name_regex,
            "author_email_regex": author_email_regex,
            "file_name_regex": file_name_regex,
            "max_file_size": max_file_size,
            "commit_committer_check": commit_committer_check,
            "reject_unsigned_commits": reject_unsigned_commits
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/push_rule", json_data=data)

    @mcp.tool()
    async def list_project_members(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        query: Optional[str] = Field(default=None, description="A query string to search for members"),
        user_ids: Optional[List[int]] = Field(default=None, description="Filter the results on the given user IDs"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Gets a list of project members viewable by the authenticated user."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "query": query,
            "user_ids": user_ids,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/members", params=params)

    @mcp.tool()
    async def list_project_members_all(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        query: Optional[str] = Field(default=None, description="A query string to search for members"),
        user_ids: Optional[List[int]] = Field(default=None, description="Filter the results on the given user IDs"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Gets a list of project members viewable by the authenticated user, including inherited members."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "query": query,
            "user_ids": user_ids,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/projects/{project_id}/members/all", params=params)

    @mcp.tool()
    async def get_project_member(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        user_id: str = Field(description="The user ID of the member")
    ) -> Dict[str, Any]:
        """Gets a member of a project."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/members/{user_id}")

    @mcp.tool()
    async def add_project_member(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        user_id: str = Field(description="The user ID of the new member"),
        access_level: int = Field(description="A valid access level"),
        expires_at: Optional[str] = Field(default=None, description="A date string in the format YEAR-MONTH-DAY")
    ) -> Dict[str, Any]:
        """Adds a member to a project."""
        client = await get_gitlab_client()
        data = {
            "user_id": user_id,
            "access_level": access_level
        }
        if expires_at is not None:
            data["expires_at"] = expires_at
        return await client.post(f"/projects/{project_id}/members", json_data=data)

    @mcp.tool()
    async def edit_project_member(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        user_id: str = Field(description="The user ID of the member"),
        access_level: int = Field(description="A valid access level"),
        expires_at: Optional[str] = Field(default=None, description="A date string in the format YEAR-MONTH-DAY")
    ) -> Dict[str, Any]:
        """Updates a member of a project."""
        client = await get_gitlab_client()
        data = {"access_level": access_level}
        if expires_at is not None:
            data["expires_at"] = expires_at
        return await client.put(f"/projects/{project_id}/members/{user_id}", json_data=data)

    @mcp.tool()
    async def remove_project_member(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        user_id: str = Field(description="The user ID of the member"),
        unassign_issuables: Optional[bool] = Field(default=None, description="Whether to unassign the user from issues and merge requests")
    ) -> Dict[str, Any]:
        """Removes a user from a project."""
        client = await get_gitlab_client()
        params = {}
        if unassign_issuables is not None:
            params["unassign_issuables"] = unassign_issuables
        return await client.delete(f"/projects/{project_id}/members/{user_id}", params=params)

    @mcp.tool()
    async def project_languages(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """Get languages used in a project with percentage value."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/languages")