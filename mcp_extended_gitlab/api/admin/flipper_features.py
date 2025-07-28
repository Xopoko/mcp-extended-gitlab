"""GitLab Flipper Features API - Internal feature flag management.

This module provides access to GitLab's internal Flipper feature flags,
which control GitLab instance features.
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
    """Register all Flipper Features API tools.
    
    This function registers the following tools:
    - Feature listing
    - Feature creation and configuration
    - Feature deletion
    """
    
    @mcp.tool()
    async def list_all_features() -> Dict[str, Any]:
        """List all persisted features."""
        client = await get_gitlab_client()
        return await client.get("/features")

    @mcp.tool()
    async def set_or_create_feature(
        name: str = Field(description="Name of the feature"),
        value: Optional[str] = Field(default=None, description="Value to set for the feature (percentage, boolean, etc.)"),
        feature_group: Optional[str] = Field(default=None, description="A feature group name"),
        user: Optional[str] = Field(default=None, description="A GitLab username or email"),
        project: Optional[str] = Field(default=None, description="A projects path, for example 'gitlab-org/gitlab-ce'"),
        group: Optional[str] = Field(default=None, description="A group's path, for example 'gitlab-org'")) -> Dict[str, Any]:
        """Set or create a feature."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "value": value,
            "feature_group": feature_group,
            "user": user,
            "project": project,
            "group": group
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/features/{name}", json_data=data)

    @mcp.tool()
    async def delete_feature(
        name: str = Field(description="Name of the feature")) -> Dict[str, Any]:
        """Delete a feature."""
        client = await get_gitlab_client()
        return await client.delete(f"/features/{name}")