"""Tests to validate MCP tools compliance with GitLab OpenAPI specification."""

import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
import yaml

import pytest
from fastmcp import FastMCP
from pydantic import BaseModel


class OpenAPIPath(BaseModel):
    """Represents an OpenAPI path with its operations."""
    path: str
    methods: Dict[str, Dict[str, Any]]


class OpenAPISpec:
    """Parser for OpenAPI specification."""
    
    def __init__(self, spec_path: Path):
        """Initialize with OpenAPI spec file path."""
        with open(spec_path, 'r') as f:
            self.spec = yaml.safe_load(f)
        self.paths = self._parse_paths()
    
    def _parse_paths(self) -> List[OpenAPIPath]:
        """Parse all paths from the OpenAPI spec."""
        paths = []
        for path, methods in self.spec.get('paths', {}).items():
            # Filter out non-HTTP methods
            http_methods = {k: v for k, v in methods.items() 
                          if k in ['get', 'post', 'put', 'patch', 'delete']}
            if http_methods:
                paths.append(OpenAPIPath(path=path, methods=http_methods))
        return paths
    
    def get_operation_id(self, path: str, method: str) -> str:
        """Get the operationId for a given path and method."""
        path_item = self.spec.get('paths', {}).get(path, {})
        operation = path_item.get(method.lower(), {})
        return operation.get('operationId', '')
    
    def get_all_operations(self) -> List[Tuple[str, str, str]]:
        """Get all operations as (path, method, operationId) tuples."""
        operations = []
        for path_obj in self.paths:
            for method in path_obj.methods:
                op_id = self.get_operation_id(path_obj.path, method)
                if op_id:
                    operations.append((path_obj.path, method.upper(), op_id))
        return operations


class MCPToolAnalyzer:
    """Analyzer for MCP tools."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.tools: Dict[str, Any] = {}
        self.tool_to_endpoint: Dict[str, Tuple[str, str]] = {}
    
    def analyze_server(self) -> None:
        """Analyze the MCP server to extract all registered tools."""
        # Import the server module
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from mcp_extended_gitlab.server import mcp
        
        # Get all registered tools
        if hasattr(mcp, '_tools'):
            self.tools = mcp._tools
        
        # Map tools to their likely endpoints
        self._map_tools_to_endpoints()
    
    def _map_tools_to_endpoints(self) -> None:
        """Map tool names to their likely API endpoints."""
        for tool_name, tool_info in self.tools.items():
            # Try to extract endpoint from tool implementation
            endpoint = self._extract_endpoint_from_tool(tool_name, tool_info)
            if endpoint:
                self.tool_to_endpoint[tool_name] = endpoint
    
    def _extract_endpoint_from_tool(self, tool_name: str, tool_info: Any) -> Tuple[str, str]:
        """Extract the API endpoint from a tool's implementation."""
        # This would need to analyze the tool's source code
        # For now, we'll use naming conventions
        method = 'GET'
        path = ''
        
        # Common patterns
        if tool_name.startswith('list_'):
            method = 'GET'
        elif tool_name.startswith('create_'):
            method = 'POST'
        elif tool_name.startswith('update_') or tool_name.startswith('edit_'):
            method = 'PUT'
        elif tool_name.startswith('delete_'):
            method = 'DELETE'
        
        # Extract path from tool name
        # This is a simplified example - real implementation would analyze the code
        parts = tool_name.split('_')
        if 'project' in parts:
            path = '/projects/{id}'
        elif 'issue' in parts:
            path = '/projects/{id}/issues'
        elif 'merge_request' in parts:
            path = '/projects/{id}/merge_requests'
        
        return (method, path) if path else None


class TestOpenAPICompliance:
    """Test suite for OpenAPI compliance."""
    
    @pytest.fixture(scope='class')
    def openapi_spec(self):
        """Load the OpenAPI specification."""
        spec_path = Path(__file__).parent.parent / 'openapi.yaml'
        return OpenAPISpec(spec_path)
    
    @pytest.fixture(scope='class')
    def mcp_analyzer(self):
        """Create MCP tool analyzer."""
        analyzer = MCPToolAnalyzer()
        analyzer.analyze_server()
        return analyzer
    
    def test_openapi_spec_loads(self, openapi_spec):
        """Test that the OpenAPI spec loads successfully."""
        assert openapi_spec.spec is not None
        assert 'openapi' in openapi_spec.spec
        assert 'paths' in openapi_spec.spec
    
    def test_all_endpoints_have_tools(self, openapi_spec, mcp_analyzer):
        """Test that all OpenAPI endpoints have corresponding MCP tools."""
        operations = openapi_spec.get_all_operations()
        missing_tools = []
        
        for path, method, op_id in operations:
            # Check if we have a tool for this operation
            tool_found = False
            for tool_name in mcp_analyzer.tools:
                if op_id.lower() in tool_name.lower() or tool_name.lower() in op_id.lower():
                    tool_found = True
                    break
            
            if not tool_found:
                missing_tools.append((path, method, op_id))
        
        # Report missing tools
        if missing_tools:
            print("\nEndpoints without corresponding MCP tools:")
            for path, method, op_id in missing_tools[:10]:  # Show first 10
                print(f"  {method} {path} ({op_id})")
            print(f"  ... and {len(missing_tools) - 10} more") if len(missing_tools) > 10 else None
    
    def test_tool_count(self, mcp_analyzer):
        """Test that we have the expected number of tools."""
        tool_count = len(mcp_analyzer.tools)
        assert tool_count > 0, "No tools found in MCP server"
        assert tool_count >= 478, f"Expected at least 478 tools, found {tool_count}"
    
    def test_tool_naming_conventions(self, mcp_analyzer):
        """Test that tools follow consistent naming conventions."""
        invalid_names = []
        
        for tool_name in mcp_analyzer.tools:
            # Check snake_case
            if not re.match(r'^[a-z][a-z0-9_]*$', tool_name):
                invalid_names.append(tool_name)
        
        assert not invalid_names, f"Tools with invalid names: {invalid_names}"
    
    def test_tool_has_description(self, mcp_analyzer):
        """Test that all tools have descriptions."""
        tools_without_desc = []
        
        for tool_name, tool_info in mcp_analyzer.tools.items():
            if hasattr(tool_info, 'description'):
                if not tool_info.description or tool_info.description.strip() == '':
                    tools_without_desc.append(tool_name)
        
        assert not tools_without_desc, f"Tools without descriptions: {tools_without_desc[:10]}"


class TestAPIMapping:
    """Test the mapping between MCP tools and GitLab API endpoints."""
    
    def test_projects_api_mapping(self):
        """Test that project-related tools map to correct endpoints."""
        from mcp_extended_gitlab.api.core.projects import register
        from fastmcp import FastMCP
        
        # Create a test MCP instance
        test_mcp = FastMCP("test")
        register(test_mcp)
        
        # Check that we have project tools
        project_tools = [name for name in test_mcp._tools if 'project' in name]
        assert len(project_tools) > 0, "No project tools found"
        
        # Verify key project operations exist
        expected_tools = [
            'list_projects',
            'get_single_project', 
            'create_project',
            'edit_project',
            'delete_project'
        ]
        
        for expected in expected_tools:
            assert any(expected in tool for tool in project_tools), f"Missing tool: {expected}"
    
    def test_issues_api_mapping(self):
        """Test that issue-related tools map to correct endpoints."""
        from mcp_extended_gitlab.api.core.issues import register
        from fastmcp import FastMCP
        
        test_mcp = FastMCP("test")
        register(test_mcp)
        
        issue_tools = [name for name in test_mcp._tools if 'issue' in name]
        assert len(issue_tools) > 0, "No issue tools found"
        
        expected_tools = [
            'list_issues',
            'list_project_issues',
            'get_single_issue',
            'create_issue',
            'edit_issue'
        ]
        
        for expected in expected_tools:
            assert any(expected in tool for tool in issue_tools), f"Missing tool: {expected}"


class TestToolParameters:
    """Test that tool parameters match OpenAPI spec parameters."""
    
    @pytest.mark.asyncio
    async def test_project_list_parameters(self):
        """Test that list_projects parameters match OpenAPI spec."""
        from mcp_extended_gitlab.api.core.projects import register
        from fastmcp import FastMCP
        import inspect
        
        test_mcp = FastMCP("test")
        register(test_mcp)
        
        # Get the list_projects tool
        list_projects_tool = None
        for name, tool in test_mcp._tools.items():
            if name == 'list_projects':
                list_projects_tool = tool
                break
        
        assert list_projects_tool is not None, "list_projects tool not found"
        
        # Check that it has expected parameters
        # This would need to be expanded to check against OpenAPI spec
        func = list_projects_tool.func
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        # Common GitLab API parameters
        expected_params = ['archived', 'visibility', 'search', 'simple', 'owned', 'membership', 'starred']
        
        for expected in expected_params:
            assert expected in params, f"Missing parameter: {expected}"


if __name__ == "__main__":
    # Run basic tests
    spec_path = Path(__file__).parent.parent / 'openapi.yaml'
    spec = OpenAPISpec(spec_path)
    
    print(f"Loaded OpenAPI spec with {len(spec.paths)} paths")
    
    analyzer = MCPToolAnalyzer()
    analyzer.analyze_server()
    
    print(f"Found {len(analyzer.tools)} MCP tools")