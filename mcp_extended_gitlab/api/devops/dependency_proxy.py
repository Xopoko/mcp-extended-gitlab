"""GitLab Dependency Proxy API - Docker image proxy management.

This module provides access to GitLab's dependency proxy features,
enabling caching and management of Docker images from external registries.
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
    """Register all Dependency Proxy API tools.
    
    This function registers the following tools:
    - Dependency proxy settings management
    - Cache management and purging
    - Blob and manifest management
    """
    
    @mcp.tool()
    async def get_dependency_proxy_settings(
        group_id: str = Field(description="The ID or URL-encoded path of the group")) -> Dict[str, Any]:
        """Get dependency proxy settings for a group."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/dependency_proxy")

    @mcp.tool()
    async def update_dependency_proxy_settings(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        enabled: Optional[bool] = Field(default=None, description="Enable or disable the dependency proxy"),
        ttl_policy: Optional[str] = Field(default=None, description="The TTL policy for dependency proxy"),
        keep_n_most_recent_files: Optional[int] = Field(default=None, description="The number of files to keep")) -> Dict[str, Any]:
        """Update dependency proxy settings for a group."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "enabled": enabled,
            "ttl_policy": ttl_policy,
            "keep_n_most_recent_files": keep_n_most_recent_files
        }.items():
            if value is not None:
                data[key] = value
        return await client.patch(f"/groups/{group_id}/dependency_proxy", json_data=data)

    @mcp.tool()
    async def purge_dependency_proxy_cache(
        group_id: str = Field(description="The ID or URL-encoded path of the group")) -> Dict[str, Any]:
        """Purge the dependency proxy cache for a group."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/dependency_proxy/cache")

    @mcp.tool()
    async def list_dependency_proxy_for_group(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        order_by: Optional[str] = Field(default="created_at", description="Return images ordered by created_at or updated_at fields"),
        sort: Optional[str] = Field(default="desc", description="Return images sorted in asc or desc order"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List dependency proxy for a group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/dependency_proxy/blobs", params=params)

    @mcp.tool()
    async def delete_dependency_proxy_blob(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        blob_id: str = Field(description="The ID of the dependency proxy blob")) -> Dict[str, Any]:
        """Delete a dependency proxy blob."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/dependency_proxy/blobs/{blob_id}")

    @mcp.tool()
    async def list_dependency_proxy_manifests(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        order_by: Optional[str] = Field(default="created_at", description="Return manifests ordered by created_at or updated_at fields"),
        sort: Optional[str] = Field(default="desc", description="Return manifests sorted in asc or desc order"),
        page: Optional[int] = Field(default=None, description="Page number"),
        per_page: Optional[int] = Field(default=None, description="Number of items per page")) -> Dict[str, Any]:
        """List dependency proxy manifests for a group."""
        client = await get_gitlab_client()
        params = {}
        for key, value in {
            "order_by": order_by,
            "sort": sort,
            "page": page,
            "per_page": per_page
        }.items():
            if value is not None:
                params[key] = value
        return await client.get(f"/groups/{group_id}/dependency_proxy/manifests", params=params)

    @mcp.tool()
    async def delete_dependency_proxy_manifest(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        manifest_id: str = Field(description="The ID of the dependency proxy manifest")) -> Dict[str, Any]:
        """Delete a dependency proxy manifest."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/dependency_proxy/manifests/{manifest_id}")