"""GitLab Variables API - CI/CD variable management.

This module provides comprehensive access to GitLab's CI/CD variables features,
enabling management of environment variables at project and group levels.
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
    """Register all Variables API tools.
    
    This function registers the following tools:
    - Project variable CRUD operations
    - Group variable CRUD operations
    - Variable masking and protection
    """
    
    @mcp.tool()
    async def list_project_variables(
        project_id: str = Field(description="The ID or URL-encoded path of the project")
    ) -> Dict[str, Any]:
        """List project variables."""
        client = await get_gitlab_client()
        return await client.get(f"/projects/{project_id}/variables")

    @mcp.tool()
    async def get_project_variable(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key: str = Field(description="The key of a variable"),
        filter: Optional[Dict[str, str]] = Field(default=None, description="Hash of attributes to narrow the search")
    ) -> Dict[str, Any]:
        """Get project variable."""
        client = await get_gitlab_client()
        params = {}
        if filter:
            params.update(filter)
        return await client.get(f"/projects/{project_id}/variables/{key}", params=params)

    @mcp.tool()
    async def create_project_variable(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key: str = Field(description="The key of a variable"),
        value: str = Field(description="The value of a variable"),
        variable_type: Optional[str] = Field(default="env_var", description="The type of a variable. Available types are: env_var (default) and file"),
        protected: Optional[bool] = Field(default=False, description="Whether the variable is protected"),
        masked: Optional[bool] = Field(default=False, description="Whether the variable is masked"),
        raw: Optional[bool] = Field(default=False, description="Whether the variable is treated as a raw string"),
        environment_scope: Optional[str] = Field(default="*", description="The environment_scope of the variable"),
        description: Optional[str] = Field(default=None, description="The description of the variable")
    ) -> Dict[str, Any]:
        """Create project variable."""
        client = await get_gitlab_client()
        data = {
            "key": key,
            "value": value,
            "variable_type": variable_type,
            "protected": protected,
            "masked": masked,
            "raw": raw,
            "environment_scope": environment_scope
        }
        if description:
            data["description"] = description
        return await client.post(f"/projects/{project_id}/variables", json_data=data)

    @mcp.tool()
    async def update_project_variable(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key: str = Field(description="The key of a variable"),
        value: Optional[str] = Field(default=None, description="The value of a variable"),
        variable_type: Optional[str] = Field(default=None, description="The type of a variable"),
        protected: Optional[bool] = Field(default=None, description="Whether the variable is protected"),
        masked: Optional[bool] = Field(default=None, description="Whether the variable is masked"),
        raw: Optional[bool] = Field(default=None, description="Whether the variable is treated as a raw string"),
        environment_scope: Optional[str] = Field(default=None, description="The environment_scope of the variable"),
        description: Optional[str] = Field(default=None, description="The description of the variable"),
        filter: Optional[Dict[str, str]] = Field(default=None, description="Hash of attributes to narrow the search")
    ) -> Dict[str, Any]:
        """Update project variable."""
        client = await get_gitlab_client()
        data = {}
        for key_name, value_item in {
            "value": value,
            "variable_type": variable_type,
            "protected": protected,
            "masked": masked,
            "raw": raw,
            "environment_scope": environment_scope,
            "description": description
        }.items():
            if value_item is not None:
                data[key_name] = value_item
        if filter:
            data.update(filter)
        return await client.put(f"/projects/{project_id}/variables/{key}", json_data=data)

    @mcp.tool()
    async def delete_project_variable(
        project_id: str = Field(description="The ID or URL-encoded path of the project"),
        key: str = Field(description="The key of a variable"),
        filter: Optional[Dict[str, str]] = Field(default=None, description="Hash of attributes to narrow the search")
    ) -> Dict[str, Any]:
        """Delete project variable."""
        client = await get_gitlab_client()
        params = {}
        if filter:
            params.update(filter)
        return await client.delete(f"/projects/{project_id}/variables/{key}", params=params)

    @mcp.tool()
    async def list_group_variables(
        group_id: str = Field(description="The ID or URL-encoded path of the group")
    ) -> Dict[str, Any]:
        """List group variables."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/variables")

    @mcp.tool()
    async def get_group_variable(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        key: str = Field(description="The key of a variable")
    ) -> Dict[str, Any]:
        """Get group variable."""
        client = await get_gitlab_client()
        return await client.get(f"/groups/{group_id}/variables/{key}")

    @mcp.tool()
    async def create_group_variable(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        key: str = Field(description="The key of a variable"),
        value: str = Field(description="The value of a variable"),
        variable_type: Optional[str] = Field(default="env_var", description="The type of a variable"),
        protected: Optional[bool] = Field(default=False, description="Whether the variable is protected"),
        masked: Optional[bool] = Field(default=False, description="Whether the variable is masked"),
        raw: Optional[bool] = Field(default=False, description="Whether the variable is treated as a raw string"),
        environment_scope: Optional[str] = Field(default="*", description="The environment_scope of the variable"),
        description: Optional[str] = Field(default=None, description="The description of the variable")
    ) -> Dict[str, Any]:
        """Create group variable."""
        client = await get_gitlab_client()
        data = {
            "key": key,
            "value": value,
            "variable_type": variable_type,
            "protected": protected,
            "masked": masked,
            "raw": raw,
            "environment_scope": environment_scope
        }
        if description:
            data["description"] = description
        return await client.post(f"/groups/{group_id}/variables", json_data=data)

    @mcp.tool()
    async def update_group_variable(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        key: str = Field(description="The key of a variable"),
        value: Optional[str] = Field(default=None, description="The value of a variable"),
        variable_type: Optional[str] = Field(default=None, description="The type of a variable"),
        protected: Optional[bool] = Field(default=None, description="Whether the variable is protected"),
        masked: Optional[bool] = Field(default=None, description="Whether the variable is masked"),
        raw: Optional[bool] = Field(default=None, description="Whether the variable is treated as a raw string"),
        environment_scope: Optional[str] = Field(default=None, description="The environment_scope of the variable"),
        description: Optional[str] = Field(default=None, description="The description of the variable")
    ) -> Dict[str, Any]:
        """Update group variable."""
        client = await get_gitlab_client()
        data = {}
        for key_name, value_item in {
            "value": value,
            "variable_type": variable_type,
            "protected": protected,
            "masked": masked,
            "raw": raw,
            "environment_scope": environment_scope,
            "description": description
        }.items():
            if value_item is not None:
                data[key_name] = value_item
        return await client.put(f"/groups/{group_id}/variables/{key}", json_data=data)

    @mcp.tool()
    async def delete_group_variable(
        group_id: str = Field(description="The ID or URL-encoded path of the group"),
        key: str = Field(description="The key of a variable")
    ) -> Dict[str, Any]:
        """Delete group variable."""
        client = await get_gitlab_client()
        return await client.delete(f"/groups/{group_id}/variables/{key}")