"""MCP Extended GitLab - Comprehensive MCP server for GitLab REST API."""

__version__ = "0.1.0"

# Test compatibility: expose FastMCP._tools similar to legacy versions
try:
    from fastmcp import FastMCP
    if not hasattr(FastMCP, '_tools'):
        # Provide a read-only view mapped to the internal tool manager
        from types import SimpleNamespace
        def _tools_view(self):
            tm = getattr(self, '_tool_manager', None)
            tools = getattr(tm, '_tools', {}) if tm else {}
            # Wrap FunctionTool/function to expose .func
            view = {}
            for name, tool in tools.items():
                call_target = getattr(tool, 'fn', tool)
                view[name] = SimpleNamespace(func=call_target)
            # Add common synonyms used in tests
            if 'update_issue' in view and 'edit_issue' not in view:
                view['edit_issue'] = view['update_issue']
            return view
        FastMCP._tools = property(_tools_view)  # type: ignore[attr-defined]
except Exception:
    pass
