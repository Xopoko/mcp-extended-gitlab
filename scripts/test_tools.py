#!/usr/bin/env python3
"""Test individual tools or tool sets."""

import asyncio
import click
import json
from typing import Optional, Dict, Any

from mcp_extended_gitlab.core import GitLabClient, get_config
from mcp_extended_gitlab.core.exceptions import MCPGitLabError


async def test_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single tool by calling the GitLab API."""
    client = GitLabClient()
    
    try:
        # Map tool names to API endpoints (simplified example)
        endpoint_map = {
            "list_projects": "/projects",
            "get_project": f"/projects/{params.get('project_id', '')}",
            "list_issues": f"/projects/{params.get('project_id', '')}/issues" if params.get('project_id') else "/issues",
            "list_users": "/users",
            "get_current_user": "/user",
        }
        
        endpoint = endpoint_map.get(tool_name)
        if not endpoint:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # Make API call
        if tool_name.startswith("list_"):
            # Add pagination params for list operations
            params = {
                "per_page": params.get("per_page", 10),
                "page": params.get("page", 1)
            }
            result = await client.get(endpoint, params=params)
        else:
            result = await client.get(endpoint)
        
        return result
        
    finally:
        await client.close()


@click.command()
@click.argument("tool_name")
@click.option("--params", "-p", help="Tool parameters as JSON")
@click.option("--output", "-o", type=click.Choice(["json", "pretty", "summary"]), default="pretty")
def test(tool_name: str, params: Optional[str], output: str):
    """Test a specific tool."""
    # Parse parameters
    tool_params = {}
    if params:
        try:
            tool_params = json.loads(params)
        except json.JSONDecodeError as e:
            click.echo(f"Error parsing parameters: {e}", err=True)
            return
    
    click.echo(f"Testing tool: {tool_name}")
    if tool_params:
        click.echo(f"Parameters: {json.dumps(tool_params, indent=2)}")
    
    try:
        # Run async test
        result = asyncio.run(test_tool(tool_name, tool_params))
        
        # Output results
        if output == "json":
            click.echo(json.dumps(result, indent=2))
        elif output == "summary":
            if isinstance(result, list):
                click.echo(f"\nReturned {len(result)} items")
                if result:
                    click.echo(f"First item keys: {list(result[0].keys())}")
            else:
                click.echo(f"\nReturned object with keys: {list(result.keys())}")
        else:  # pretty
            if isinstance(result, list):
                click.echo(f"\nResults ({len(result)} items):\n")
                for i, item in enumerate(result[:5]):
                    if "name" in item:
                        click.echo(f"  {i+1}. {item['name']} (ID: {item.get('id', 'N/A')})")
                    else:
                        click.echo(f"  {i+1}. ID: {item.get('id', 'N/A')}")
                
                if len(result) > 5:
                    click.echo(f"  ... and {len(result) - 5} more")
            else:
                click.echo(f"\nResult:\n")
                for key, value in list(result.items())[:10]:
                    if isinstance(value, (dict, list)):
                        click.echo(f"  {key}: <{type(value).__name__}>")
                    else:
                        click.echo(f"  {key}: {value}")
                
                if len(result) > 10:
                    click.echo(f"  ... and {len(result) - 10} more fields")
        
        click.echo("\n✅ Tool test successful!")
        
    except MCPGitLabError as e:
        click.echo(f"\n❌ GitLab error: {e.message}", err=True)
        if e.details:
            click.echo(f"Details: {json.dumps(e.details, indent=2)}", err=True)
    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)


if __name__ == "__main__":
    test()