"""GitLab SSH Keys API - SSH key fingerprint and validation.

This module provides access to GitLab's SSH key validation features,
enabling fingerprint retrieval and key verification.
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
    """Register all SSH Keys API tools.
    
    This function registers the following tools:
    - SSH key fingerprint generation
    - SSH key details retrieval
    """
    
    @mcp.tool()
    async def get_ssh_key_fingerprint(
        ssh_key: str = Field(description="SSH key content")) -> Dict[str, Any]:
        """Get SSH key fingerprint."""
        client = await get_gitlab_client()
        data = {"key": ssh_key}
        return await client.post("/keys", json_data=data)

    @mcp.tool()
    async def get_ssh_key_details(
        fingerprint: str = Field(description="SSH key fingerprint (either MD5 or SHA256)")) -> Dict[str, Any]:
        """Get SSH key details by fingerprint."""
        client = await get_gitlab_client()
        return await client.get(f"/keys/{fingerprint}")