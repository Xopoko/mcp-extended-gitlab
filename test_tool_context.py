#!/usr/bin/env python3
"""Test script to verify tool filtering and context usage in MCP."""

import os
import sys
import asyncio
from mcp_extended_gitlab.server import get_mcp_server
from mcp_extended_gitlab.filtered_mcp import FilteredMCP
from fastmcp import FastMCP

def count_registered_tools(mcp):
    """Count tools registered in the MCP instance."""
    # Try different ways to access tools
    if hasattr(mcp, '_tools'):
        return len(mcp._tools)
    elif hasattr(mcp, 'server') and hasattr(mcp.server, 'tools'):
        return len(mcp.server.tools)
    else:
        # Try to find tools through introspection
        for attr_name in dir(mcp):
            attr = getattr(mcp, attr_name)
            if isinstance(attr, dict) and 'list_projects' in str(attr):
                return len(attr)
    return 0

def test_no_filter():
    """Test with no filtering - all tools should be registered."""
    print("\n=== Test 1: No Filter (All Tools) ===")
    if 'GITLAB_ENABLED_TOOLS' in os.environ:
        del os.environ['GITLAB_ENABLED_TOOLS']
    
    mcp = get_mcp_server()
    tool_count = count_registered_tools(mcp)
    print(f"Registered tools: {tool_count}")
    
    # Check if FilteredMCP has skipped tools info
    if hasattr(mcp, '_skipped_tools'):
        print(f"Skipped tools: {len(mcp._skipped_tools)}")
    
    return tool_count

def test_minimal_preset():
    """Test with minimal preset - only essential tools."""
    print("\n=== Test 2: Minimal Preset ===")
    os.environ['GITLAB_ENABLED_TOOLS'] = 'minimal'
    
    mcp = get_mcp_server()
    tool_count = count_registered_tools(mcp)
    print(f"Registered tools: {tool_count}")
    
    if hasattr(mcp, '_skipped_tools'):
        print(f"Skipped tools: {len(mcp._skipped_tools)}")
    
    return tool_count

def test_specific_tools():
    """Test with specific tools only."""
    print("\n=== Test 3: Specific Tools ===")
    os.environ['GITLAB_ENABLED_TOOLS'] = 'list_projects,get_project,list_issues'
    
    mcp = get_mcp_server()
    tool_count = count_registered_tools(mcp)
    print(f"Registered tools: {tool_count}")
    
    if hasattr(mcp, '_skipped_tools'):
        print(f"Skipped tools: {len(mcp._skipped_tools)}")
    
    return tool_count

def inspect_mcp_internals(mcp):
    """Inspect MCP instance to understand its structure."""
    print("\n=== MCP Internal Structure ===")
    print(f"Type: {type(mcp)}")
    print(f"MRO: {type(mcp).__mro__}")
    
    # List all attributes
    attrs = dir(mcp)
    print(f"\nTotal attributes: {len(attrs)}")
    
    # Look for tool-related attributes
    tool_attrs = [attr for attr in attrs if 'tool' in attr.lower()]
    print(f"\nTool-related attributes: {tool_attrs}")
    
    # Check for specific attributes
    for attr in ['_tools', 'tools', 'server', '_mcp']:
        if hasattr(mcp, attr):
            value = getattr(mcp, attr)
            print(f"\n{attr}: {type(value)}")
            if isinstance(value, dict):
                print(f"  Dict keys sample: {list(value.keys())[:5]}")
            elif hasattr(value, '__dict__'):
                print(f"  Object attrs: {list(vars(value).keys())[:10]}")

def main():
    """Run all tests."""
    print("Testing MCP Tool Filtering and Context Usage")
    print("=" * 50)
    
    # Test different configurations
    all_tools_count = test_no_filter()
    minimal_count = test_minimal_preset()
    specific_count = test_specific_tools()
    
    # Summary
    print("\n=== Summary ===")
    print(f"All tools: {all_tools_count}")
    print(f"Minimal preset: {minimal_count}")
    print(f"Specific tools: {specific_count}")
    print(f"\nContext reduction:")
    if all_tools_count > 0:
        print(f"  Minimal: {(1 - minimal_count/all_tools_count)*100:.1f}% reduction")
        print(f"  Specific: {(1 - specific_count/all_tools_count)*100:.1f}% reduction")
    
    # Inspect internals
    print("\n" + "=" * 50)
    os.environ['GITLAB_ENABLED_TOOLS'] = 'minimal'
    mcp = get_mcp_server()
    inspect_mcp_internals(mcp)

if __name__ == "__main__":
    main()