#!/usr/bin/env python3
"""Test tool filtering to verify only selected tools are registered."""

import os
import sys
from mcp_extended_gitlab.filtered_mcp import FilteredMCP
from mcp_extended_gitlab.api.core import projects, users, issues

# Test 1: No filtering (all tools)
print("=== Test 1: No filtering ===")
os.environ.pop('GITLAB_ENABLED_TOOLS', None)
mcp1 = FilteredMCP("test1")
projects.register(mcp1)
users.register(mcp1)
issues.register(mcp1)
print(f"Registered tools: {len(mcp1._mcp._tools)}")
print(f"Tool names: {list(mcp1._mcp._tools.keys())[:5]}...")

# Test 2: Filter to only 3 tools
print("\n=== Test 2: Filtered to 3 tools ===")
os.environ['GITLAB_ENABLED_TOOLS'] = "list_projects,get_user,list_issues"
mcp2 = FilteredMCP("test2")
projects.register(mcp2)
users.register(mcp2)
issues.register(mcp2)
print(f"Registered tools: {len(mcp2._mcp._tools)}")
print(f"Tool names: {list(mcp2._mcp._tools.keys())}")
print(f"Skipped tools: {len(mcp2._skipped_tools)}")

# Test 3: Using preset
print("\n=== Test 3: Using 'minimal' preset ===")
os.environ['GITLAB_ENABLED_TOOLS'] = "minimal"
mcp3 = FilteredMCP("test3")
projects.register(mcp3)
users.register(mcp3)
issues.register(mcp3)
print(f"Registered tools: {len(mcp3._mcp._tools)}")
print(f"Tool names: {list(mcp3._mcp._tools.keys())}")