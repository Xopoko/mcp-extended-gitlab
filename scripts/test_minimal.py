#!/usr/bin/env python3
"""Simple test to verify the tool testing framework works."""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.test_all_tools import ToolTester


async def test_minimal_tools():
    """Test a few basic read-only tools."""
    # Check for token
    if not os.getenv("GITLAB_PRIVATE_TOKEN"):
        print("Error: GITLAB_PRIVATE_TOKEN environment variable is required")
        return
    
    print("Testing minimal GitLab API tools...")
    print("-" * 50)
    
    async with ToolTester() as tester:
        # Test a few basic tools that don't require specific resources
        basic_tools = [
            "get_current_user",  # Should always work
            "list_projects",     # Should return user's projects
            "list_users",        # Should return users (might be limited)
            "search_globally"    # Search with a simple query
        ]
        
        for tool_name in basic_tools:
            print(f"\nTesting {tool_name}...")
            
            # Get tool info
            all_tools = tester.get_all_tools()
            if tool_name not in all_tools:
                print(f"  ERROR: Tool '{tool_name}' not found!")
                continue
                
            tool_info = all_tools[tool_name]
            
            # Test the tool
            result = await tester.test_tool(tool_name, tool_info)
            
            if result.skip_reason:
                print(f"  SKIPPED: {result.skip_reason}")
            elif result.success:
                print(f"  SUCCESS: Completed in {result.duration:.2f}s")
                if result.response:
                    # Show sample of response
                    if isinstance(result.response, list):
                        print(f"  Response: List with {len(result.response)} items")
                    elif isinstance(result.response, dict):
                        keys = list(result.response.keys())[:5]
                        print(f"  Response keys: {keys}")
            else:
                print(f"  FAILED: {result.error}")
    
    print("\n" + "-" * 50)
    print("Test completed!")


if __name__ == "__main__":
    asyncio.run(test_minimal_tools())