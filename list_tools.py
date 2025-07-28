#!/usr/bin/env python3
"""List all available tools in MCP Extended GitLab."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_extended_gitlab.tool_registry import MODULE_REGISTRY, TOOL_PRESETS
from importlib import import_module
import inspect

def get_all_tools():
    """Get all tool names from all modules."""
    tools_by_category = {}
    
    for category, modules in MODULE_REGISTRY.items():
        tools_by_category[category] = []
        
        for module_name in modules:
            try:
                # Import the module
                module = import_module(f"mcp_extended_gitlab.api.{category}.{module_name}")
                
                # Find all functions decorated with @mcp.tool()
                for name, obj in inspect.getmembers(module):
                    if inspect.iscoroutinefunction(obj) and not name.startswith('_') and name != 'get_gitlab_client' and name != 'register':
                        tools_by_category[category].append(name)
            except Exception as e:
                print(f"Error loading {category}.{module_name}: {e}", file=sys.stderr)
    
    return tools_by_category

def main():
    print("# MCP Extended GitLab - Available Tools\n")
    
    # Show presets
    print("## Tool Presets\n")
    for preset_name, tools in TOOL_PRESETS.items():
        print(f"### {preset_name} ({len(tools)} tools)")
        print(f"Use with: `GITLAB_ENABLED_TOOLS=\"{preset_name}\"`")
        print("```")
        for tool in sorted(tools)[:10]:  # Show first 10
            print(f"- {tool}")
        if len(tools) > 10:
            print(f"... and {len(tools) - 10} more")
        print("```\n")
    
    # Show all tools by category
    print("\n## All Tools by Category\n")
    tools_by_category = get_all_tools()
    
    for category, tools in sorted(tools_by_category.items()):
        if tools:
            print(f"### {category} ({len(tools)} tools)")
            print("```")
            for tool in sorted(tools):
                print(f"{tool}")
            print("```\n")
    
    # Show example of custom tool selection
    print("\n## Custom Tool Selection Examples\n")
    print("To use specific tools, use their exact names:")
    print("```bash")
    print('# Comma-separated list')
    print('GITLAB_ENABLED_TOOLS="list_projects,get_project,list_issues,create_issue"')
    print()
    print('# JSON array')
    print('GITLAB_ENABLED_TOOLS=\'["list_projects","get_project","list_merge_requests"]\'')
    print("```")

if __name__ == "__main__":
    main()