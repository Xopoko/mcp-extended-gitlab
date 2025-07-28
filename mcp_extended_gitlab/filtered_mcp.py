"""Filtered MCP wrapper that conditionally registers tools."""

import os
import json
from typing import Set, Optional, Callable, Any
from fastmcp import FastMCP
from functools import wraps

from .tool_registry import TOOL_PRESETS


class FilteredMCP:
    """Wrapper around FastMCP that filters tool registration."""
    
    def __init__(self, name: str):
        self._mcp = FastMCP(name)
        self.enabled_tools = self._get_enabled_tools()
        self._skipped_tools = []
        
    def _get_enabled_tools(self) -> Optional[Set[str]]:
        """Get the set of enabled tools from environment."""
        enabled_tools_env = os.getenv("GITLAB_ENABLED_TOOLS", "")
        
        if not enabled_tools_env:
            # If no tools specified, enable all
            return None
        
        # Check if it's a preset
        if enabled_tools_env in TOOL_PRESETS:
            return set(TOOL_PRESETS[enabled_tools_env])
        
        # Parse as JSON array or comma-separated list
        try:
            # Try parsing as JSON array first
            enabled_tools = json.loads(enabled_tools_env)
            if isinstance(enabled_tools, list):
                return set(enabled_tools)
        except json.JSONDecodeError:
            # Fall back to comma-separated list
            enabled_tools = [t.strip() for t in enabled_tools_env.split(",") if t.strip()]
            return set(enabled_tools)
        
        return None
    
    def tool(self, **kwargs):
        """Filtered tool decorator."""
        def decorator(func: Callable) -> Callable:
            tool_name = func.__name__
            
            # Check if tool should be registered
            if self.enabled_tools is None or tool_name in self.enabled_tools:
                # Register the tool
                return self._mcp.tool(**kwargs)(func)
            else:
                # Skip registration but return the function unchanged
                self._skipped_tools.append(tool_name)
                return func
        
        return decorator
    
    def run(self, **kwargs):
        """Run the MCP server."""
        # Log statistics
        if self.enabled_tools:
            import sys
            # Access the internal tools dictionary properly
            enabled_count = len(getattr(self._mcp, '_tools', {}))
            total_tools = enabled_count + len(self._skipped_tools)
            print(f"GitLab MCP: Enabled {enabled_count} of {total_tools} tools", file=sys.stderr)
            
            # List enabled presets if any match
            for preset_name, preset_tools in TOOL_PRESETS.items():
                if self.enabled_tools == set(preset_tools):
                    print(f"GitLab MCP: Using preset '{preset_name}'", file=sys.stderr)
                    break
        
        return self._mcp.run(**kwargs)
    
    def __getattr__(self, name):
        """Proxy other attributes to the wrapped MCP instance."""
        return getattr(self._mcp, name)