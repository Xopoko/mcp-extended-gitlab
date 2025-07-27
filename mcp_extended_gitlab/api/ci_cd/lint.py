"""GitLab CI/CD Lint API - Configuration validation.

This module provides access to GitLab's CI/CD configuration linting features,
enabling validation of .gitlab-ci.yml files.
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
    """Register all CI/CD Lint API tools.
    
    This function registers the following tools:
    - CI/CD configuration linting and validation
    """
    
    @mcp.tool()
    async def get_lint_result(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        content: str = Field(description="The CI/CD configuration content"),
        include_merged_yaml: Optional[bool] = Field(default=False, description="If the expanded CI configuration should be included in the response"),
        include_jobs: Optional[bool] = Field(default=False, description="If the list of jobs should be included in the response"),
        ref: Optional[str] = Field(default=None, description="When specified, the CI/CD configuration is fetched from this reference"),
        dry_run: Optional[bool] = Field(default=False, description="Run validation only")
    ) -> Dict[str, Any]:
        """Lint CI/CD configuration."""
        client = await get_gitlab_client()
        data = {"content": content}
        for key, value in {
            "include_merged_yaml": include_merged_yaml,
            "include_jobs": include_jobs,
            "ref": ref,
            "dry_run": dry_run
        }.items():
            if value is not None:
                data[key] = value
        return await client.post(f"/projects/{project_id}/ci/lint", json_data=data)