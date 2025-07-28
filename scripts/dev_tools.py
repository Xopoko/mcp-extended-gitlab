#!/usr/bin/env python3
"""Development tools for MCP Extended GitLab."""

import asyncio
import click
import json
from typing import List, Optional
from pathlib import Path
import ast
import re

from mcp_extended_gitlab.tools.registry import TOOL_PRESETS, ToolCategory
from mcp_extended_gitlab.core import Config


@click.group()
def cli():
    """Development tools for MCP Extended GitLab."""
    pass


@cli.command()
@click.option("--category", type=click.Choice([c.value for c in ToolCategory]), help="Filter by category")
@click.option("--output", type=click.Choice(["list", "json", "markdown"]), default="list")
def list_tools(category: Optional[str], output: str):
    """List all available tools."""
    tools = []
    
    # Scan all API modules for tools
    api_dir = Path(__file__).parent.parent / "mcp_extended_gitlab" / "api"
    
    for py_file in api_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        with open(py_file) as f:
            content = f.read()
            
        # Find all @mcp.tool() decorated functions
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if (isinstance(decorator, ast.Call) and 
                        isinstance(decorator.func, ast.Attribute) and
                        decorator.func.attr == "tool"):
                        
                        # Extract tool info
                        tool_info = {
                            "name": node.name,
                            "module": str(py_file.relative_to(api_dir.parent)),
                            "description": ast.get_docstring(node) or "No description",
                            "category": py_file.parent.name
                        }
                        
                        if not category or tool_info["category"] == category:
                            tools.append(tool_info)
    
    # Output results
    if output == "json":
        click.echo(json.dumps(tools, indent=2))
    elif output == "markdown":
        click.echo("# Available Tools\n")
        for cat in sorted(set(t["category"] for t in tools)):
            click.echo(f"\n## {cat.title()}\n")
            cat_tools = [t for t in tools if t["category"] == cat]
            for tool in sorted(cat_tools, key=lambda t: t["name"]):
                click.echo(f"- **{tool['name']}**: {tool['description'].split('.')[0]}")
    else:
        for tool in sorted(tools, key=lambda t: (t["category"], t["name"])):
            click.echo(f"{tool['category']}/{tool['name']}: {tool['description'].split('.')[0]}")
    
    click.echo(f"\nTotal tools: {len(tools)}")


@cli.command()
def list_presets():
    """List available tool presets."""
    click.echo("Available tool presets:\n")
    
    for preset_name, tool_names in TOOL_PRESETS.items():
        click.echo(f"{preset_name} ({len(tool_names)} tools):")
        click.echo(f"  {', '.join(tool_names[:5])}", end="")
        if len(tool_names) > 5:
            click.echo(f"... and {len(tool_names) - 5} more")
        else:
            click.echo()
        click.echo()


@cli.command()
@click.argument("preset")
def show_preset(preset: str):
    """Show tools in a specific preset."""
    if preset not in TOOL_PRESETS:
        click.echo(f"Error: Unknown preset '{preset}'")
        click.echo(f"Available presets: {', '.join(TOOL_PRESETS.keys())}")
        return
    
    tools = TOOL_PRESETS[preset]
    click.echo(f"Tools in '{preset}' preset ({len(tools)} total):\n")
    
    for i, tool in enumerate(sorted(tools), 1):
        click.echo(f"{i:3d}. {tool}")


@cli.command()
@click.option("--check", is_flag=True, help="Check current configuration")
def config(check: bool):
    """Manage configuration."""
    if check:
        try:
            cfg = Config()
            click.echo("Configuration valid!")
            click.echo(f"\nSettings:")
            click.echo(f"  GitLab URL: {cfg.gitlab_base_url}")
            click.echo(f"  Token: {'*' * 10}{cfg.gitlab_private_token[-4:] if cfg.gitlab_private_token else 'NOT SET'}")
            click.echo(f"  Timeout: {cfg.http_timeout}s")
            click.echo(f"  Log level: {cfg.log_level}")
            
            if cfg.enabled_tools:
                click.echo(f"  Enabled tools: {len(cfg.enabled_tools)} tools")
            elif cfg.tool_preset:
                click.echo(f"  Tool preset: {cfg.tool_preset}")
            else:
                click.echo(f"  Enabled tools: ALL")
                
        except Exception as e:
            click.echo(f"Configuration error: {e}", err=True)
            return
    else:
        click.echo("Configuration environment variables:")
        click.echo("  GITLAB_PRIVATE_TOKEN    - GitLab private access token (required)")
        click.echo("  GITLAB_BASE_URL         - GitLab API URL (default: https://gitlab.com/api/v4)")
        click.echo("  GITLAB_ENABLED_TOOLS    - Tool filter (preset name, tool list, or JSON array)")
        click.echo("  GITLAB_HTTP_TIMEOUT     - HTTP timeout in seconds (default: 30)")
        click.echo("  GITLAB_LOG_LEVEL        - Log level (default: WARNING)")


@cli.command()
@click.argument("tool_names", nargs=-1, required=True)
def check_tools(tool_names: List[str]):
    """Check if specific tools exist."""
    # This would scan the codebase for the tools
    click.echo(f"Checking tools: {', '.join(tool_names)}")
    # Implementation would check if tools exist


@cli.command()
@click.option("--format", type=click.Choice(["simple", "detailed"]), default="simple")
def stats(format: str):
    """Show project statistics."""
    api_dir = Path(__file__).parent.parent / "mcp_extended_gitlab" / "api"
    
    stats = {
        "modules": 0,
        "tools": 0,
        "categories": set(),
        "files": 0
    }
    
    for py_file in api_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        stats["files"] += 1
        stats["categories"].add(py_file.parent.name)
        
        with open(py_file) as f:
            content = f.read()
            
        # Count @mcp.tool() decorators
        tool_count = content.count("@mcp.tool(")
        stats["tools"] += tool_count
        
        if tool_count > 0:
            stats["modules"] += 1
    
    if format == "detailed":
        click.echo("MCP Extended GitLab Statistics\n")
        click.echo(f"API Files: {stats['files']}")
        click.echo(f"Modules with tools: {stats['modules']}")
        click.echo(f"Total tools: {stats['tools']}")
        click.echo(f"Categories: {len(stats['categories'])}")
        click.echo(f"  - {', '.join(sorted(stats['categories']))}")
        click.echo(f"\nPresets: {len(TOOL_PRESETS)}")
        for preset, tools in TOOL_PRESETS.items():
            click.echo(f"  - {preset}: {len(tools)} tools")
    else:
        click.echo(f"Tools: {stats['tools']} | Modules: {stats['modules']} | Categories: {len(stats['categories'])}")


if __name__ == "__main__":
    cli()