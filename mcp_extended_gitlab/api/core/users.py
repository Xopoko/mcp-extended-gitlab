"""GitLab Users API - User management and authentication.

This module provides comprehensive access to GitLab's user management features,
including user creation, SSH keys, blocking/unblocking, and user relationships.
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
    """Register all Users API tools.
    
    This function registers the following tools:
    - User listing and search
    - User CRUD operations
    - User authentication (SSH keys)
    - User blocking/deactivation
    - User relationships (following, followers)
    - User memberships and contributed projects
    """
    
    @mcp.tool()
    async def list_users(
        active: Optional[bool] = Field(default=None, description="Return only active users"),
        blocked: Optional[bool] = Field(default=None, description="Return only blocked users"),
        external: Optional[bool] = Field(default=None, description="Return only external users"),
        exclude_external: Optional[bool] = Field(default=None, description="Return only non-external users"),
        exclude_internal: Optional[bool] = Field(default=None, description="Return users excluding internal users"),
        without_projects: Optional[bool] = Field(default=None, description="Return only users without projects"),
        admins: Optional[bool] = Field(default=None, description="Return only admin users"),
        two_factor: Optional[str] = Field(default=None, description="Return users with or without two-factor authentication enabled"),
        identity_provider: Optional[str] = Field(default=None, description="Return users created by the specified external identity provider"),
        extern_uid: Optional[str] = Field(default=None, description="Return users with the specified external identity provider UID"),
        provider: Optional[str] = Field(default=None, description="Return users for the specified provider"),
        search: Optional[str] = Field(default=None, description="Search for users by name, username, or email"),
        username: Optional[str] = Field(default=None, description="Return user with a specific username"),
        order_by: Optional[str] = Field(default=None, description="Order users by name, username, id, created_at, or updated_at"),
        sort: Optional[str] = Field(default=None, description="Sort users in asc or desc order"),
        created_before: Optional[str] = Field(default=None, description="Return users created before the specified date"),
        created_after: Optional[str] = Field(default=None, description="Return users created after the specified date"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List users."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "active": active,
            "blocked": blocked,
            "external": external,
            "exclude_external": exclude_external,
            "exclude_internal": exclude_internal,
            "without_projects": without_projects,
            "admins": admins,
            "two_factor": two_factor,
            "identity_provider": identity_provider,
            "extern_uid": extern_uid,
            "provider": provider,
            "search": search,
            "username": username,
            "order_by": order_by,
            "sort": sort,
            "created_before": created_before,
            "created_after": created_after,
            "with_custom_attributes": with_custom_attributes,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get("/users", params=params)

    @mcp.tool()
    async def get_user(
        user_id: str = Field(description="The ID or username of the user"),
        with_custom_attributes: Optional[bool] = Field(default=None, description="Include custom attributes in response")
    ) -> Dict[str, Any]:
        """Get a single user."""
        client = await get_gitlab_client()
        params = {}
        if with_custom_attributes:
            params["with_custom_attributes"] = with_custom_attributes
        return await client.get(f"/users/{user_id}", params=params)

    @mcp.tool()
    async def create_user(
        email: str = Field(description="Email address"),
        password: str = Field(description="Password"),
        username: str = Field(description="Username"),
        name: str = Field(description="Name"),
        skype: Optional[str] = Field(default=None, description="Skype ID"),
        linkedin: Optional[str] = Field(default=None, description="LinkedIn profile"),
        twitter: Optional[str] = Field(default=None, description="Twitter account"),
        website_url: Optional[str] = Field(default=None, description="Website URL"),
        organization: Optional[str] = Field(default=None, description="Organization name"),
        projects_limit: Optional[int] = Field(default=None, description="Number of projects user can create"),
        extern_uid: Optional[str] = Field(default=None, description="External UID"),
        provider: Optional[str] = Field(default=None, description="External provider name"),
        bio: Optional[str] = Field(default=None, description="User's biography"),
        location: Optional[str] = Field(default=None, description="User's location"),
        admin: Optional[bool] = Field(default=False, description="User is admin"),
        can_create_group: Optional[bool] = Field(default=True, description="User can create groups"),
        skip_confirmation: Optional[bool] = Field(default=False, description="Skip confirmation"),
        external: Optional[bool] = Field(default=False, description="Flags the user as external"),
        avatar: Optional[str] = Field(default=None, description="Image file for user's avatar"),
        private_profile: Optional[bool] = Field(default=False, description="User's profile is private"),
        color_scheme_id: Optional[int] = Field(default=None, description="User's color scheme for the file viewer"),
        theme_id: Optional[int] = Field(default=None, description="GitLab theme for the user"),
        note: Optional[str] = Field(default=None, description="Admin notes for this user"),
        shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Pipeline minutes quota for this user"),
        extra_shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Extra pipeline minutes quota for this user")
    ) -> Dict[str, Any]:
        """Create a new user."""
        client = await get_gitlab_client()
        data = {
            "email": email,
            "password": password,
            "username": username,
            "name": name
        }
        for key, value in {
            "skype": skype,
            "linkedin": linkedin,
            "twitter": twitter,
            "website_url": website_url,
            "organization": organization,
            "projects_limit": projects_limit,
            "extern_uid": extern_uid,
            "provider": provider,
            "bio": bio,
            "location": location,
            "admin": admin,
            "can_create_group": can_create_group,
            "skip_confirmation": skip_confirmation,
            "external": external,
            "avatar": avatar,
            "private_profile": private_profile,
            "color_scheme_id": color_scheme_id,
            "theme_id": theme_id,
            "note": note,
            "shared_runners_minutes_limit": shared_runners_minutes_limit,
            "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit
        }.items():
            if value is not None:
                data[key] = value
        return await client.post("/users", json_data=data)

    @mcp.tool()
    async def update_user(
        user_id: str = Field(description="The ID or username of the user"),
        email: Optional[str] = Field(default=None, description="Email address"),
        password: Optional[str] = Field(default=None, description="Password"),
        username: Optional[str] = Field(default=None, description="Username"),
        name: Optional[str] = Field(default=None, description="Name"),
        skype: Optional[str] = Field(default=None, description="Skype ID"),
        linkedin: Optional[str] = Field(default=None, description="LinkedIn profile"),
        twitter: Optional[str] = Field(default=None, description="Twitter account"),
        website_url: Optional[str] = Field(default=None, description="Website URL"),
        organization: Optional[str] = Field(default=None, description="Organization name"),
        projects_limit: Optional[int] = Field(default=None, description="Number of projects user can create"),
        extern_uid: Optional[str] = Field(default=None, description="External UID"),
        provider: Optional[str] = Field(default=None, description="External provider name"),
        bio: Optional[str] = Field(default=None, description="User's biography"),
        location: Optional[str] = Field(default=None, description="User's location"),
        admin: Optional[bool] = Field(default=None, description="User is admin"),
        can_create_group: Optional[bool] = Field(default=None, description="User can create groups"),
        skip_reconfirmation: Optional[bool] = Field(default=None, description="Skip reconfirmation"),
        external: Optional[bool] = Field(default=None, description="Flags the user as external"),
        avatar: Optional[str] = Field(default=None, description="Image file for user's avatar"),
        private_profile: Optional[bool] = Field(default=None, description="User's profile is private"),
        color_scheme_id: Optional[int] = Field(default=None, description="User's color scheme for the file viewer"),
        theme_id: Optional[int] = Field(default=None, description="GitLab theme for the user"),
        note: Optional[str] = Field(default=None, description="Admin notes for this user"),
        shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Pipeline minutes quota for this user"),
        extra_shared_runners_minutes_limit: Optional[int] = Field(default=None, description="Extra pipeline minutes quota for this user"),
        commit_email: Optional[str] = Field(default=None, description="Default email for commits")
    ) -> Dict[str, Any]:
        """Update an existing user."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "email": email,
            "password": password,
            "username": username,
            "name": name,
            "skype": skype,
            "linkedin": linkedin,
            "twitter": twitter,
            "website_url": website_url,
            "organization": organization,
            "projects_limit": projects_limit,
            "extern_uid": extern_uid,
            "provider": provider,
            "bio": bio,
            "location": location,
            "admin": admin,
            "can_create_group": can_create_group,
            "skip_reconfirmation": skip_reconfirmation,
            "external": external,
            "avatar": avatar,
            "private_profile": private_profile,
            "color_scheme_id": color_scheme_id,
            "theme_id": theme_id,
            "note": note,
            "shared_runners_minutes_limit": shared_runners_minutes_limit,
            "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit,
            "commit_email": commit_email
        }.items():
            if value is not None:
                data[key] = value
        return await client.put(f"/users/{user_id}", json_data=data)

    @mcp.tool()
    async def delete_user(
        user_id: str = Field(description="The ID or username of the user"),
        hard_delete: Optional[bool] = Field(default=False, description="If true, contributions that would usually be moved to the ghost user will be deleted instead, as well as groups owned solely by this user")
    ) -> Dict[str, Any]:
        """Delete a user."""
        client = await get_gitlab_client()
        params = {}
        if hard_delete:
            params["hard_delete"] = hard_delete
        return await client.delete(f"/users/{user_id}", params=params)

    @mcp.tool()
    async def get_current_user() -> Dict[str, Any]:
        """Get current user details."""
        client = await get_gitlab_client()
        return await client.get("/user")

    @mcp.tool()
    async def list_current_user_ssh_keys() -> Dict[str, Any]:
        """List SSH keys for current user."""
        client = await get_gitlab_client()
        return await client.get("/user/keys")

    @mcp.tool()
    async def list_user_ssh_keys(
        user_id: str = Field(description="The ID or username of the user")
    ) -> Dict[str, Any]:
        """List SSH keys for a user."""
        client = await get_gitlab_client()
        return await client.get(f"/users/{user_id}/keys")

    @mcp.tool()
    async def get_user_ssh_key(
        key_id: str = Field(description="The ID of the SSH key")
    ) -> Dict[str, Any]:
        """Get a single SSH key."""
        client = await get_gitlab_client()
        return await client.get(f"/user/keys/{key_id}")

    @mcp.tool()
    async def add_ssh_key_for_current_user(
        title: str = Field(description="The title of the SSH key"),
        key: str = Field(description="The SSH key"),
        expires_at: Optional[str] = Field(default=None, description="The expiration date of the SSH key in ISO 8601 format")
    ) -> Dict[str, Any]:
        """Add SSH key for current user."""
        client = await get_gitlab_client()
        data = {
            "title": title,
            "key": key
        }
        if expires_at:
            data["expires_at"] = expires_at
        return await client.post("/user/keys", json_data=data)

    @mcp.tool()
    async def add_ssh_key_for_user(
        user_id: str = Field(description="The ID or username of the user"),
        title: str = Field(description="The title of the SSH key"),
        key: str = Field(description="The SSH key"),
        expires_at: Optional[str] = Field(default=None, description="The expiration date of the SSH key in ISO 8601 format")
    ) -> Dict[str, Any]:
        """Add SSH key for a user."""
        client = await get_gitlab_client()
        data = {
            "title": title,
            "key": key
        }
        if expires_at:
            data["expires_at"] = expires_at
        return await client.post(f"/users/{user_id}/keys", json_data=data)

    @mcp.tool()
    async def delete_ssh_key_for_current_user(
        key_id: str = Field(description="The ID of the SSH key")
    ) -> Dict[str, Any]:
        """Delete SSH key for current user."""
        client = await get_gitlab_client()
        return await client.delete(f"/user/keys/{key_id}")

    @mcp.tool()
    async def delete_ssh_key_for_user(
        user_id: str = Field(description="The ID or username of the user"),
        key_id: str = Field(description="The ID of the SSH key")
    ) -> Dict[str, Any]:
        """Delete SSH key for a user."""
        client = await get_gitlab_client()
        return await client.delete(f"/users/{user_id}/keys/{key_id}")

    @mcp.tool()
    async def block_user(
        user_id: str = Field(description="The ID or username of the user")
    ) -> Dict[str, Any]:
        """Block a user."""
        client = await get_gitlab_client()
        return await client.post(f"/users/{user_id}/block")

    @mcp.tool()
    async def unblock_user(
        user_id: str = Field(description="The ID or username of the user")
    ) -> Dict[str, Any]:
        """Unblock a user."""
        client = await get_gitlab_client()
        return await client.post(f"/users/{user_id}/unblock")

    @mcp.tool()
    async def deactivate_user(
        user_id: str = Field(description="The ID or username of the user")
    ) -> Dict[str, Any]:
        """Deactivate a user."""
        client = await get_gitlab_client()
        return await client.post(f"/users/{user_id}/deactivate")

    @mcp.tool()
    async def activate_user(
        user_id: str = Field(description="The ID or username of the user")
    ) -> Dict[str, Any]:
        """Activate a user."""
        client = await get_gitlab_client()
        return await client.post(f"/users/{user_id}/activate")

    @mcp.tool()
    async def get_user_memberships(
        user_id: str = Field(description="The ID or username of the user"),
        type: Optional[str] = Field(default=None, description="Filter memberships by type (Project or Namespace)"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """Get user memberships."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "type": type,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/users/{user_id}/memberships", params=params)

    @mcp.tool()
    async def list_user_contributed_projects(
        user_id: str = Field(description="The ID or username of the user"),
        order_by: Optional[str] = Field(default=None, description="Return projects ordered by field"),
        sort: Optional[str] = Field(default=None, description="Return projects sorted in asc or desc order"),
        simple: Optional[bool] = Field(default=None, description="Return only limited fields for each project"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List projects a user has contributed to."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort,
            "simple": simple,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/users/{user_id}/contributed_projects", params=params)

    @mcp.tool()
    async def list_user_starred_projects(
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
    async def follow_user(
        user_id: str = Field(description="The ID or username of the user")
    ) -> Dict[str, Any]:
        """Follow a user."""
        client = await get_gitlab_client()
        return await client.post(f"/users/{user_id}/follow")

    @mcp.tool()
    async def unfollow_user(
        user_id: str = Field(description="The ID or username of the user")
    ) -> Dict[str, Any]:
        """Unfollow a user."""
        client = await get_gitlab_client()
        return await client.post(f"/users/{user_id}/unfollow")

    @mcp.tool()
    async def list_user_followers(
        user_id: str = Field(description="The ID or username of the user"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List followers of a user."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/users/{user_id}/followers", params=params)

    @mcp.tool()
    async def list_user_following(
        user_id: str = Field(description="The ID or username of the user"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")
    ) -> Dict[str, Any]:
        """List users followed by a user."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/users/{user_id}/following", params=params)