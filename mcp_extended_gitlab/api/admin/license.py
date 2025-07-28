"""GitLab License API - License management.

This module provides access to GitLab's license features,
enabling management of GitLab Enterprise licenses.
"""

from typing import Any, Dict
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
    """Register all License API tools.
    
    This function registers the following tools:
    - License information retrieval
    - License addition
    - License deletion
    """
    
    @mcp.tool()
    async def retrieve_license_information() -> Dict[str, Any]:
        """Retrieve information about the current license."""
        client = await get_gitlab_client()
        return await client.get("/license")

    @mcp.tool()
    async def add_new_license(
        license: str = Field(description="The license string")) -> Dict[str, Any]:
        """Add a new license."""
        client = await get_gitlab_client()
        data = {"license": license}
        return await client.post("/license", json_data=data)

    @mcp.tool()
    async def delete_license() -> Dict[str, Any]:
        """Delete current license."""
        client = await get_gitlab_client()
        return await client.delete("/license")