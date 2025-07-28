#!/usr/bin/env python3
"""Example usage of the GitLab API tool testing framework."""

import asyncio
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.test_all_tools import ToolTester, TestSummary


async def example_1_test_specific_tools():
    """Example 1: Test specific tools."""
    print("Example 1: Testing specific tools")
    print("=" * 50)
    
    async with ToolTester() as tester:
        # Test only these specific tools
        tools_to_test = ["list_projects", "get_current_user", "list_issues"]
        
        summary = await tester.test_tools(
            tools_filter=tools_to_test,
            verbose=True
        )
        
        # Print summary
        print(f"\nTested {summary.tested} tools:")
        print(f"  Passed: {summary.passed}")
        print(f"  Failed: {summary.failed}")
        print(f"  Skipped: {summary.skipped}")


async def example_2_test_category():
    """Example 2: Test all tools in a category."""
    print("\n\nExample 2: Testing CI/CD category")
    print("=" * 50)
    
    async with ToolTester() as tester:
        summary = await tester.test_tools(
            categories=["ci_cd"],
            verbose=False  # Less verbose output
        )
        
        # Generate text report
        report = tester.generate_report(summary, format="text")
        print(report)


async def example_3_test_preset_with_json():
    """Example 3: Test preset and save JSON report."""
    print("\n\nExample 3: Testing minimal preset with JSON output")
    print("=" * 50)
    
    async with ToolTester() as tester:
        summary = await tester.test_tools(
            preset="minimal",
            verbose=True
        )
        
        # Generate JSON report
        json_report = tester.generate_report(summary, format="json")
        
        # Save to file
        output_file = "minimal_test_report.json"
        Path(output_file).write_text(json_report)
        print(f"\nJSON report saved to: {output_file}")


async def example_4_custom_test_logic():
    """Example 4: Custom test logic with specific parameters."""
    print("\n\nExample 4: Custom test with specific parameters")
    print("=" * 50)
    
    async with ToolTester() as tester:
        # Get all available tools
        all_tools = tester.get_all_tools()
        
        # Find tools that start with "create_"
        create_tools = [name for name in all_tools.keys() if name.startswith("create_")]
        print(f"Found {len(create_tools)} 'create' tools")
        
        # Test only safe create operations
        safe_create_tools = [
            tool for tool in create_tools 
            if "issue" in tool or "comment" in tool or "note" in tool
        ]
        
        if safe_create_tools:
            print(f"Testing {len(safe_create_tools)} safe create tools...")
            summary = await tester.test_tools(
                tools_filter=safe_create_tools[:3],  # Test only first 3
                stop_on_error=True,
                verbose=True
            )
            
            # Check results
            for category, results in summary.results_by_category.items():
                for result in results:
                    if result.success:
                        print(f"✓ {result.tool_name} - {result.duration:.2f}s")
                    else:
                        print(f"✗ {result.tool_name} - {result.error or result.skip_reason}")


async def example_5_analyze_tools():
    """Example 5: Analyze available tools without testing."""
    print("\n\nExample 5: Analyzing available tools")
    print("=" * 50)
    
    async with ToolTester() as tester:
        all_tools = tester.get_all_tools()
        
        # Count tools by category
        category_counts = {}
        for tool_name, tool_info in all_tools.items():
            category = tool_info["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"Total tools available: {len(all_tools)}")
        print("\nTools by category:")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count} tools")
        
        # Find tools with no required parameters
        no_params_tools = []
        for tool_name, tool_info in all_tools.items():
            params = tool_info["parameters"]
            required_params = [p for p, info in params.items() if info["required"]]
            if not required_params:
                no_params_tools.append(tool_name)
        
        print(f"\nTools with no required parameters: {len(no_params_tools)}")
        print("Examples:", no_params_tools[:5])


async def main():
    """Run all examples."""
    # Check for GitLab token
    if not os.getenv("GITLAB_PRIVATE_TOKEN"):
        print("Error: GITLAB_PRIVATE_TOKEN environment variable is required")
        print("Set it with: export GITLAB_PRIVATE_TOKEN='your-token'")
        return
    
    # Run examples
    await example_1_test_specific_tools()
    await example_2_test_category()
    await example_3_test_preset_with_json()
    await example_4_custom_test_logic()
    await example_5_analyze_tools()


if __name__ == "__main__":
    asyncio.run(main())