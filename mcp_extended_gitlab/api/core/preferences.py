"""GitLab User Preferences API - User settings management.

This module provides access to GitLab's user preferences features,
enabling management of personal settings and UI preferences.
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
    """Register all User Preferences API tools.
    
    This function registers the following tools:
    - User preference retrieval
    - User preference updates
    """
    
    @mcp.tool()
    async def get_current_user_settings() -> Dict[str, Any]:
        """Get current user settings."""
        client = await get_gitlab_client()
        return await client.get("/user/preferences")

    @mcp.tool()
    async def update_current_user_settings(
        color_scheme_id: Optional[int] = Field(default=None, description="The color scheme ID"),
        diff_view: Optional[str] = Field(default=None, description="Flag indicating the user sees either the side-by-side diff view or the inline diff view"),
        theme_id: Optional[int] = Field(default=None, description="The theme ID"),
        tab_size: Optional[int] = Field(default=None, description="The number of spaces a tab is equal to"),
        sourcegraph_enabled: Optional[bool] = Field(default=None, description="Enable integrated code intelligence on code views"),
        setup_for_company: Optional[bool] = Field(default=None, description="Indicates the purpose for which this account is being used"),
        render_whitespace_in_code: Optional[bool] = Field(default=None, description="Render whitespace characters in the Web IDE"),
        use_legacy_web_ide: Optional[bool] = Field(default=None, description="Use the legacy Web IDE"),
        keyboard_shortcuts_enabled: Optional[bool] = Field(default=None, description="Enable keyboard shortcuts")) -> Dict[str, Any]:
        """Update current user settings."""
        client = await get_gitlab_client()
        data = {}
        for key, value in {
            "color_scheme_id": color_scheme_id,
            "diff_view": diff_view,
            "theme_id": theme_id,
            "tab_size": tab_size,
            "sourcegraph_enabled": sourcegraph_enabled,
            "setup_for_company": setup_for_company,
            "render_whitespace_in_code": render_whitespace_in_code,
            "use_legacy_web_ide": use_legacy_web_ide,
            "keyboard_shortcuts_enabled": keyboard_shortcuts_enabled
        }.items():
            if value is not None:
                data[key] = value
        return await client.put("/user/preferences", json_data=data)