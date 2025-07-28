#!/usr/bin/env python3
"""Comprehensive testing script for all GitLab API tools.

This script can test all 478+ tools in the MCP Extended GitLab server by:
1. Dynamically discovering all registered tools
2. Calling each tool with appropriate parameters
3. Validating responses and handling errors
4. Generating test reports
"""

import asyncio
import click
import json
import os
import sys
import time
import inspect
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_extended_gitlab.client import GitLabClient, GitLabConfig
from mcp_extended_gitlab.tool_registry import (
    MODULE_REGISTRY, 
    build_tool_to_module_map,
    get_tools_by_category,
    TOOL_PRESETS
)
from mcp_extended_gitlab.server import mcp
from fastmcp import FastMCP


@dataclass
class ToolTestResult:
    """Result of testing a single tool."""
    tool_name: str
    module: str
    category: str
    success: bool
    duration: float
    error: Optional[str] = None
    response: Optional[Dict[str, Any]] = None
    params_used: Dict[str, Any] = field(default_factory=dict)
    skip_reason: Optional[str] = None


@dataclass
class TestSummary:
    """Summary of all test results."""
    total_tools: int = 0
    tested: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: List[Tuple[str, str]] = field(default_factory=list)
    duration: float = 0.0
    results_by_category: Dict[str, List[ToolTestResult]] = field(default_factory=lambda: defaultdict(list))


class ToolTester:
    """Test runner for GitLab API tools."""
    
    def __init__(self, config: Optional[GitLabConfig] = None):
        """Initialize the tool tester."""
        self.config = config or GitLabConfig(
            base_url=os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4"),
            private_token=os.getenv("GITLAB_PRIVATE_TOKEN")
        )
        self.client = GitLabClient(self.config)
        self.test_project_id = os.getenv("GITLAB_TEST_PROJECT_ID")
        self.test_group_id = os.getenv("GITLAB_TEST_GROUP_ID")
        self.test_user_id = os.getenv("GITLAB_TEST_USER_ID")
        
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.close()
    
    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        """Discover all registered tools from the MCP server."""
        tools = {}
        
        # Get tool to module mapping
        tool_to_module = build_tool_to_module_map()
        tools_by_category = get_tools_by_category()
        
        # Extract tools from the MCP server
        for tool_name in mcp._tools.keys():
            module_name = tool_to_module.get(tool_name, "unknown")
            
            # Determine category
            category = "unknown"
            for cat, tool_list in tools_by_category.items():
                if tool_name in tool_list:
                    category = cat
                    break
            
            # Get tool function and parameters
            tool_func = mcp._tools[tool_name]
            sig = inspect.signature(tool_func)
            
            tools[tool_name] = {
                "module": module_name,
                "category": category,
                "function": tool_func,
                "signature": sig,
                "parameters": self._extract_parameters(sig)
            }
            
        return tools
    
    def _extract_parameters(self, sig: inspect.Signature) -> Dict[str, Dict[str, Any]]:
        """Extract parameter information from function signature."""
        params = {}
        
        for name, param in sig.parameters.items():
            if name in ["self", "cls"]:
                continue
                
            param_info = {
                "required": param.default == inspect.Parameter.empty,
                "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"
            }
            
            # Extract Field metadata if available
            if hasattr(param.default, "description"):
                param_info["description"] = param.default.description
                param_info["default"] = param.default.default
            elif param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
                
            params[name] = param_info
            
        return params
    
    def _get_test_params(self, tool_name: str, parameters: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Optional[str]]:
        """Generate appropriate test parameters for a tool."""
        params = {}
        skip_reason = None
        
        # Handle tools that require specific resources
        if "project_id" in parameters and parameters["project_id"]["required"]:
            if not self.test_project_id:
                skip_reason = "No test project ID configured"
                return params, skip_reason
            params["project_id"] = self.test_project_id
            
        if "group_id" in parameters and parameters["group_id"]["required"]:
            if not self.test_group_id:
                skip_reason = "No test group ID configured"
                return params, skip_reason
            params["group_id"] = self.test_group_id
            
        if "user_id" in parameters and parameters["user_id"]["required"]:
            if not self.test_user_id:
                skip_reason = "No test user ID configured"
                return params, skip_reason
            params["user_id"] = self.test_user_id
        
        # Handle other required parameters with sensible defaults
        for param_name, param_info in parameters.items():
            if param_name in params:
                continue
                
            if param_info["required"]:
                # Provide sensible defaults based on parameter name/type
                if "id" in param_name and param_name not in ["project_id", "group_id", "user_id"]:
                    skip_reason = f"Cannot provide test value for required parameter: {param_name}"
                    return params, skip_reason
                elif param_name in ["name", "title", "description"]:
                    params[param_name] = f"Test {param_name}"
                elif param_name == "content":
                    params[param_name] = "Test content"
                elif param_name == "path":
                    params[param_name] = "test-path"
                elif param_name == "ref":
                    params[param_name] = "main"
                elif param_name == "sha":
                    skip_reason = f"Cannot provide test value for required parameter: {param_name}"
                    return params, skip_reason
                elif "url" in param_name:
                    params[param_name] = "https://example.com"
                elif param_info["type"] == "bool":
                    params[param_name] = False
                elif param_info["type"] == "int":
                    params[param_name] = 1
        
        # Add pagination limits for list operations
        if tool_name.startswith("list_") or tool_name.startswith("search_"):
            params["per_page"] = 5
            params["page"] = 1
            
        return params, skip_reason
    
    async def test_tool(self, tool_name: str, tool_info: Dict[str, Any]) -> ToolTestResult:
        """Test a single tool."""
        start_time = time.time()
        
        # Get test parameters
        params, skip_reason = self._get_test_params(tool_name, tool_info["parameters"])
        
        if skip_reason:
            return ToolTestResult(
                tool_name=tool_name,
                module=tool_info["module"],
                category=tool_info["category"],
                success=False,
                duration=0.0,
                skip_reason=skip_reason
            )
        
        try:
            # Call the tool
            result = await tool_info["function"](**params)
            
            duration = time.time() - start_time
            
            return ToolTestResult(
                tool_name=tool_name,
                module=tool_info["module"],
                category=tool_info["category"],
                success=True,
                duration=duration,
                response=result,
                params_used=params
            )
            
        except Exception as e:
            duration = time.time() - start_time
            
            return ToolTestResult(
                tool_name=tool_name,
                module=tool_info["module"],
                category=tool_info["category"],
                success=False,
                duration=duration,
                error=str(e),
                params_used=params
            )
    
    async def test_tools(
        self, 
        tools_filter: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        preset: Optional[str] = None,
        stop_on_error: bool = False,
        verbose: bool = False
    ) -> TestSummary:
        """Test multiple tools based on filters."""
        # Discover all tools
        all_tools = self.get_all_tools()
        
        # Apply filters
        tools_to_test = self._filter_tools(all_tools, tools_filter, categories, preset)
        
        # Initialize summary
        summary = TestSummary(total_tools=len(all_tools))
        start_time = time.time()
        
        # Test each tool
        for tool_name, tool_info in tools_to_test.items():
            if verbose:
                click.echo(f"Testing {tool_name}...", nl=False)
            
            result = await self.test_tool(tool_name, tool_info)
            
            # Update summary
            summary.tested += 1
            summary.results_by_category[result.category].append(result)
            
            if result.skip_reason:
                summary.skipped += 1
                if verbose:
                    click.echo(f" SKIPPED ({result.skip_reason})")
            elif result.success:
                summary.passed += 1
                if verbose:
                    click.echo(f" ✓ ({result.duration:.2f}s)")
            else:
                summary.failed += 1
                summary.errors.append((tool_name, result.error or "Unknown error"))
                if verbose:
                    click.echo(f" ✗ ({result.error})")
                
                if stop_on_error:
                    break
        
        summary.duration = time.time() - start_time
        return summary
    
    def _filter_tools(
        self,
        all_tools: Dict[str, Dict[str, Any]],
        tools_filter: Optional[List[str]],
        categories: Optional[List[str]],
        preset: Optional[str]
    ) -> Dict[str, Dict[str, Any]]:
        """Filter tools based on criteria."""
        if preset and preset in TOOL_PRESETS:
            # Use preset tool list
            preset_tools = set(TOOL_PRESETS[preset])
            return {k: v for k, v in all_tools.items() if k in preset_tools}
        
        filtered = all_tools
        
        if tools_filter:
            # Filter by specific tool names
            filtered = {k: v for k, v in filtered.items() if k in tools_filter}
            
        if categories:
            # Filter by categories
            filtered = {k: v for k, v in filtered.items() if v["category"] in categories}
            
        return filtered
    
    def generate_report(self, summary: TestSummary, format: str = "text") -> str:
        """Generate a test report."""
        if format == "json":
            return self._generate_json_report(summary)
        elif format == "markdown":
            return self._generate_markdown_report(summary)
        else:
            return self._generate_text_report(summary)
    
    def _generate_text_report(self, summary: TestSummary) -> str:
        """Generate a text format report."""
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("GitLab API Tools Test Report")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Duration: {summary.duration:.2f} seconds")
        lines.append("")
        
        # Overall summary
        lines.append("Summary:")
        lines.append(f"  Total Tools: {summary.total_tools}")
        lines.append(f"  Tested: {summary.tested}")
        lines.append(f"  Passed: {summary.passed} ({summary.passed/summary.tested*100:.1f}%)")
        lines.append(f"  Failed: {summary.failed}")
        lines.append(f"  Skipped: {summary.skipped}")
        lines.append("")
        
        # Results by category
        lines.append("Results by Category:")
        for category, results in sorted(summary.results_by_category.items()):
            passed = sum(1 for r in results if r.success and not r.skip_reason)
            failed = sum(1 for r in results if not r.success and not r.skip_reason)
            skipped = sum(1 for r in results if r.skip_reason)
            lines.append(f"  {category}: {passed} passed, {failed} failed, {skipped} skipped")
        lines.append("")
        
        # Failed tools
        if summary.errors:
            lines.append("Failed Tools:")
            for tool_name, error in summary.errors:
                lines.append(f"  - {tool_name}: {error}")
            lines.append("")
        
        # Skipped tools
        skipped_tools = []
        for results in summary.results_by_category.values():
            skipped_tools.extend([(r.tool_name, r.skip_reason) for r in results if r.skip_reason])
        
        if skipped_tools:
            lines.append("Skipped Tools:")
            skip_reasons = defaultdict(list)
            for tool_name, reason in skipped_tools:
                skip_reasons[reason].append(tool_name)
            
            for reason, tools in skip_reasons.items():
                lines.append(f"  {reason}: {len(tools)} tools")
                if len(tools) <= 5:
                    for tool in tools:
                        lines.append(f"    - {tool}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    def _generate_json_report(self, summary: TestSummary) -> str:
        """Generate a JSON format report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "duration": summary.duration,
            "summary": {
                "total_tools": summary.total_tools,
                "tested": summary.tested,
                "passed": summary.passed,
                "failed": summary.failed,
                "skipped": summary.skipped,
                "success_rate": summary.passed / summary.tested * 100 if summary.tested > 0 else 0
            },
            "categories": {},
            "errors": [{"tool": tool, "error": error} for tool, error in summary.errors],
            "results": []
        }
        
        # Add category summaries and detailed results
        for category, results in summary.results_by_category.items():
            passed = sum(1 for r in results if r.success and not r.skip_reason)
            failed = sum(1 for r in results if not r.success and not r.skip_reason)
            skipped = sum(1 for r in results if r.skip_reason)
            
            report["categories"][category] = {
                "tested": len(results),
                "passed": passed,
                "failed": failed,
                "skipped": skipped
            }
            
            for result in results:
                report["results"].append({
                    "tool": result.tool_name,
                    "module": result.module,
                    "category": result.category,
                    "success": result.success,
                    "duration": result.duration,
                    "error": result.error,
                    "skip_reason": result.skip_reason,
                    "params_used": result.params_used
                })
        
        return json.dumps(report, indent=2)
    
    def _generate_markdown_report(self, summary: TestSummary) -> str:
        """Generate a Markdown format report."""
        lines = []
        lines.append("# GitLab API Tools Test Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Duration:** {summary.duration:.2f} seconds")
        lines.append("")
        
        # Summary table
        lines.append("## Summary")
        lines.append("")
        lines.append("| Metric | Value | Percentage |")
        lines.append("|--------|-------|------------|")
        lines.append(f"| Total Tools | {summary.total_tools} | 100% |")
        lines.append(f"| Tested | {summary.tested} | {summary.tested/summary.total_tools*100:.1f}% |")
        lines.append(f"| Passed | {summary.passed} | {summary.passed/summary.tested*100:.1f}% |")
        lines.append(f"| Failed | {summary.failed} | {summary.failed/summary.tested*100:.1f}% |")
        lines.append(f"| Skipped | {summary.skipped} | {summary.skipped/summary.tested*100:.1f}% |")
        lines.append("")
        
        # Category breakdown
        lines.append("## Results by Category")
        lines.append("")
        lines.append("| Category | Tested | Passed | Failed | Skipped |")
        lines.append("|----------|--------|--------|--------|---------|")
        
        for category, results in sorted(summary.results_by_category.items()):
            passed = sum(1 for r in results if r.success and not r.skip_reason)
            failed = sum(1 for r in results if not r.success and not r.skip_reason)
            skipped = sum(1 for r in results if r.skip_reason)
            lines.append(f"| {category} | {len(results)} | {passed} | {failed} | {skipped} |")
        
        lines.append("")
        
        # Failed tools
        if summary.errors:
            lines.append("## Failed Tools")
            lines.append("")
            for tool_name, error in summary.errors:
                lines.append(f"- **{tool_name}**: `{error}`")
            lines.append("")
        
        return "\n".join(lines)


@click.command()
@click.option("--tools", "-t", multiple=True, help="Specific tools to test")
@click.option("--category", "-c", multiple=True, 
              type=click.Choice(["core", "ci_cd", "security", "devops", "registry", 
                               "integrations", "monitoring", "admin"]),
              help="Test tools from specific categories")
@click.option("--preset", "-p", 
              type=click.Choice(["minimal", "core", "ci_cd", "devops", "admin"]),
              help="Use a predefined tool preset")
@click.option("--format", "-f", 
              type=click.Choice(["text", "json", "markdown"]), 
              default="text",
              help="Output format for the report")
@click.option("--output", "-o", type=click.Path(), help="Save report to file")
@click.option("--stop-on-error", is_flag=True, help="Stop testing on first error")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed progress")
@click.option("--test-project", envvar="GITLAB_TEST_PROJECT_ID", 
              help="GitLab project ID for testing")
@click.option("--test-group", envvar="GITLAB_TEST_GROUP_ID",
              help="GitLab group ID for testing")
@click.option("--test-user", envvar="GITLAB_TEST_USER_ID",
              help="GitLab user ID for testing")
def test_tools(tools, category, preset, format, output, stop_on_error, verbose,
               test_project, test_group, test_user):
    """Test GitLab API tools with various options.
    
    Examples:
        # Test all tools
        python test_all_tools.py
        
        # Test specific tools
        python test_all_tools.py -t list_projects -t get_project
        
        # Test by category
        python test_all_tools.py -c core -c ci_cd
        
        # Test using preset
        python test_all_tools.py -p minimal
        
        # Generate JSON report
        python test_all_tools.py -f json -o report.json
        
        # Test with specific project/group/user
        python test_all_tools.py --test-project 123 --test-group 456
    """
    
    # Check for GitLab token
    if not os.getenv("GITLAB_PRIVATE_TOKEN"):
        click.echo("Error: GITLAB_PRIVATE_TOKEN environment variable is required", err=True)
        sys.exit(1)
    
    # Set test resource IDs
    if test_project:
        os.environ["GITLAB_TEST_PROJECT_ID"] = test_project
    if test_group:
        os.environ["GITLAB_TEST_GROUP_ID"] = test_group
    if test_user:
        os.environ["GITLAB_TEST_USER_ID"] = test_user
    
    # Run tests
    async def run():
        async with ToolTester() as tester:
            summary = await tester.test_tools(
                tools_filter=list(tools) if tools else None,
                categories=list(category) if category else None,
                preset=preset,
                stop_on_error=stop_on_error,
                verbose=verbose
            )
            
            # Generate report
            report = tester.generate_report(summary, format=format)
            
            # Output report
            if output:
                Path(output).write_text(report)
                click.echo(f"Report saved to {output}")
            else:
                click.echo(report)
            
            # Exit with appropriate code
            if summary.failed > 0:
                sys.exit(1)
    
    # Run the async function
    asyncio.run(run())


if __name__ == "__main__":
    test_tools()