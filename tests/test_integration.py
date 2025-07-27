"""Integration tests for MCP Extended GitLab."""

import asyncio
from unittest.mock import patch, AsyncMock

import pytest
from fastmcp import FastMCP

from mcp_extended_gitlab.server import mcp
from mcp_extended_gitlab.client import GitLabClient


class TestServerIntegration:
    """Test the integrated MCP server."""
    
    def test_server_initialization(self):
        """Test that the server initializes correctly."""
        assert mcp is not None
        assert hasattr(mcp, '_tools')
        assert len(mcp._tools) > 0
    
    def test_all_domains_loaded(self):
        """Test that tools from all domains are loaded."""
        tool_names = list(mcp._tools.keys())
        
        # Check for tools from each domain
        domain_keywords = {
            'core': ['project', 'issue', 'merge_request', 'user', 'group'],
            'ci_cd': ['pipeline', 'runner', 'variable'],
            'security': ['protected', 'deploy_key', 'deploy_token'],
            'devops': ['environment', 'deployment', 'feature_flag'],
            'registry': ['package', 'container'],
            'monitoring': ['error', 'analytics', 'statistics'],
            'admin': ['license', 'system_hook']
        }
        
        for domain, keywords in domain_keywords.items():
            domain_tools = []
            for keyword in keywords:
                domain_tools.extend([name for name in tool_names if keyword in name])
            
            assert len(domain_tools) > 0, f"No tools found for domain: {domain}"
    
    @pytest.mark.asyncio
    async def test_tool_execution_mock(self, mock_gitlab_client, mock_project_response):
        """Test executing a tool with mocked client."""
        with patch('mcp_extended_gitlab.api.core.projects.get_gitlab_client') as mock_get_client:
            # Setup mock
            mock_get_client.return_value = mock_gitlab_client
            mock_gitlab_client.get = AsyncMock(return_value=[mock_project_response])
            
            # Get the list_projects tool
            list_projects = None
            for name, tool in mcp._tools.items():
                if name == 'list_projects':
                    list_projects = tool
                    break
            
            assert list_projects is not None
            
            # Execute the tool
            result = await list_projects.func()
            
            # Verify
            assert result == [mock_project_response]
            mock_gitlab_client.get.assert_called_once()


class TestDomainIntegration:
    """Test integration between different domains."""
    
    @pytest.mark.asyncio
    async def test_project_issue_integration(self, mock_gitlab_client, mock_project_response, mock_issue_response):
        """Test integration between projects and issues."""
        with patch('mcp_extended_gitlab.api.core.projects.get_gitlab_client') as mock_get_client_projects, \
             patch('mcp_extended_gitlab.api.core.issues.get_gitlab_client') as mock_get_client_issues:
            
            # Setup mocks
            mock_get_client_projects.return_value = mock_gitlab_client
            mock_get_client_issues.return_value = mock_gitlab_client
            
            # Mock project creation
            mock_gitlab_client.post = AsyncMock(return_value=mock_project_response)
            
            # Get create_project tool
            create_project = None
            for name, tool in mcp._tools.items():
                if name == 'create_project':
                    create_project = tool
                    break
            
            # Create project
            project = await create_project.func(
                name="Test Project",
                path="test-project"
            )
            
            assert project['id'] == 1
            
            # Mock issue creation
            mock_gitlab_client.post = AsyncMock(return_value=mock_issue_response)
            
            # Get create_issue tool
            create_issue = None
            for name, tool in mcp._tools.items():
                if name == 'create_issue':
                    create_issue = tool
                    break
            
            # Create issue in project
            issue = await create_issue.func(
                project_id=str(project['id']),
                title="Test Issue"
            )
            
            assert issue['project_id'] == project['id']
    
    @pytest.mark.asyncio
    async def test_ci_cd_integration(self, mock_gitlab_client):
        """Test CI/CD tools integration."""
        with patch('mcp_extended_gitlab.api.ci_cd.pipelines.get_gitlab_client') as mock_get_client_pipelines, \
             patch('mcp_extended_gitlab.api.ci_cd.variables.get_gitlab_client') as mock_get_client_variables:
            
            # Setup mocks
            mock_get_client_pipelines.return_value = mock_gitlab_client
            mock_get_client_variables.return_value = mock_gitlab_client
            
            # Mock responses
            pipeline_response = {
                "id": 1,
                "status": "success",
                "ref": "main",
                "sha": "abc123"
            }
            
            variable_response = {
                "key": "TEST_VAR",
                "value": "test_value",
                "protected": False
            }
            
            mock_gitlab_client.get = AsyncMock(side_effect=[
                [pipeline_response],  # list pipelines
                [variable_response]   # list variables
            ])
            
            # Get tools
            list_pipelines = None
            list_variables = None
            
            for name, tool in mcp._tools.items():
                if name == 'list_project_pipelines':
                    list_pipelines = tool
                elif name == 'list_project_variables':
                    list_variables = tool
            
            # Execute tools
            pipelines = await list_pipelines.func(project_id="1")
            variables = await list_variables.func(project_id="1")
            
            assert len(pipelines) == 1
            assert pipelines[0]['status'] == 'success'
            assert len(variables) == 1
            assert variables[0]['key'] == 'TEST_VAR'


class TestToolChaining:
    """Test chaining multiple tools together."""
    
    @pytest.mark.asyncio
    async def test_create_project_with_features(self, mock_gitlab_client):
        """Test creating a project and enabling features."""
        with patch('mcp_extended_gitlab.api.core.projects.get_gitlab_client') as mock_get_client_projects, \
             patch('mcp_extended_gitlab.api.security.protected_branches.get_gitlab_client') as mock_get_client_branches, \
             patch('mcp_extended_gitlab.api.devops.environments.get_gitlab_client') as mock_get_client_envs:
            
            # Setup mocks
            mock_get_client_projects.return_value = mock_gitlab_client
            mock_get_client_branches.return_value = mock_gitlab_client
            mock_get_client_envs.return_value = mock_gitlab_client
            
            # Mock responses
            project_response = {"id": 1, "name": "Test Project"}
            branch_response = {"name": "main", "protected": True}
            env_response = {"id": 1, "name": "production", "external_url": "https://prod.example.com"}
            
            mock_gitlab_client.post = AsyncMock(side_effect=[
                project_response,  # create project
                branch_response,   # protect branch
                env_response      # create environment
            ])
            
            # Get tools
            tools = {}
            for name, tool in mcp._tools.items():
                if name in ['create_project', 'create_protected_branch', 'create_new_environment']:
                    tools[name] = tool
            
            # Execute workflow
            # 1. Create project
            project = await tools['create_project'].func(
                name="Test Project",
                path="test-project"
            )
            
            # 2. Protect main branch
            protected_branch = await tools['create_protected_branch'].func(
                project_id=str(project['id']),
                name="main"
            )
            
            # 3. Create production environment
            environment = await tools['create_new_environment'].func(
                project_id=str(project['id']),
                name="production",
                external_url="https://prod.example.com"
            )
            
            # Verify workflow
            assert project['id'] == 1
            assert protected_branch['protected'] is True
            assert environment['name'] == 'production'
            
            # Verify correct number of API calls
            assert mock_gitlab_client.post.call_count == 3


class TestErrorScenarios:
    """Test error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_authentication_error(self, mock_gitlab_client):
        """Test handling authentication errors."""
        with patch('mcp_extended_gitlab.api.core.projects.get_gitlab_client') as mock_get_client:
            mock_get_client.return_value = mock_gitlab_client
            
            # Mock 401 error
            mock_gitlab_client.get = AsyncMock(side_effect=Exception("401 Unauthorized"))
            
            # Get list_projects tool
            list_projects = None
            for name, tool in mcp._tools.items():
                if name == 'list_projects':
                    list_projects = tool
                    break
            
            # Execute and expect error
            with pytest.raises(Exception) as exc_info:
                await list_projects.func()
            
            assert "401 Unauthorized" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_resource_not_found(self, mock_gitlab_client):
        """Test handling resource not found errors."""
        with patch('mcp_extended_gitlab.api.core.projects.get_gitlab_client') as mock_get_client:
            mock_get_client.return_value = mock_gitlab_client
            
            # Mock 404 error
            mock_gitlab_client.get = AsyncMock(side_effect=Exception("404 Project Not Found"))
            
            # Get get_single_project tool
            get_project = None
            for name, tool in mcp._tools.items():
                if name == 'get_single_project':
                    get_project = tool
                    break
            
            # Execute and expect error
            with pytest.raises(Exception) as exc_info:
                await get_project.func(project_id="999999")
            
            assert "404 Project Not Found" in str(exc_info.value)


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""
    
    @pytest.mark.asyncio
    async def test_devops_workflow(self, mock_gitlab_client):
        """Test a complete DevOps workflow."""
        # This test simulates:
        # 1. Creating a project
        # 2. Adding CI/CD variables
        # 3. Creating environments
        # 4. Running a pipeline
        # 5. Creating a deployment
        
        with patch('mcp_extended_gitlab.api.core.projects.get_gitlab_client') as mock_projects, \
             patch('mcp_extended_gitlab.api.ci_cd.variables.get_gitlab_client') as mock_variables, \
             patch('mcp_extended_gitlab.api.devops.environments.get_gitlab_client') as mock_envs, \
             patch('mcp_extended_gitlab.api.ci_cd.pipelines.get_gitlab_client') as mock_pipelines, \
             patch('mcp_extended_gitlab.api.devops.deployments.get_gitlab_client') as mock_deployments:
            
            # Setup all mocks
            for mock in [mock_projects, mock_variables, mock_envs, mock_pipelines, mock_deployments]:
                mock.return_value = mock_gitlab_client
            
            # Mock responses
            responses = {
                'project': {"id": 1, "name": "DevOps Project"},
                'variable': {"key": "API_KEY", "value": "secret"},
                'environment': {"id": 1, "name": "staging"},
                'pipeline': {"id": 100, "status": "pending", "ref": "main"},
                'deployment': {"id": 1, "status": "success", "environment": {"name": "staging"}}
            }
            
            # Setup mock responses in order
            mock_gitlab_client.post = AsyncMock(side_effect=[
                responses['project'],
                responses['variable'],
                responses['environment'],
                responses['pipeline'],
                responses['deployment']
            ])
            
            # Get all needed tools
            tools = {}
            tool_names = [
                'create_project',
                'create_project_variable',
                'create_new_environment',
                'create_new_pipeline',
                'create_deployment'
            ]
            
            for name, tool in mcp._tools.items():
                if name in tool_names:
                    tools[name] = tool
            
            # Execute DevOps workflow
            # 1. Create project
            project = await tools['create_project'].func(
                name="DevOps Project",
                path="devops-project"
            )
            
            # 2. Add CI/CD variable
            variable = await tools['create_project_variable'].func(
                project_id=str(project['id']),
                key="API_KEY",
                value="secret",
                protected=True
            )
            
            # 3. Create staging environment
            environment = await tools['create_new_environment'].func(
                project_id=str(project['id']),
                name="staging"
            )
            
            # 4. Create pipeline
            pipeline = await tools['create_new_pipeline'].func(
                project_id=str(project['id']),
                ref="main"
            )
            
            # 5. Create deployment
            deployment = await tools['create_deployment'].func(
                project_id=str(project['id']),
                environment="staging",
                sha="abc123",
                ref="main"
            )
            
            # Verify complete workflow
            assert project['name'] == "DevOps Project"
            assert variable['key'] == "API_KEY"
            assert environment['name'] == "staging"
            assert pipeline['ref'] == "main"
            assert deployment['environment']['name'] == "staging"
            
            # Verify all API calls were made
            assert mock_gitlab_client.post.call_count == 5


if __name__ == "__main__":
    # Quick integration test
    print(f"MCP Server has {len(mcp._tools)} tools registered")
    
    # List some tools by domain
    domains = {
        'Projects': ['project'],
        'Issues': ['issue'],
        'CI/CD': ['pipeline', 'runner'],
        'Security': ['protected', 'deploy']
    }
    
    for domain, keywords in domains.items():
        tools = []
        for keyword in keywords:
            tools.extend([name for name in mcp._tools.keys() if keyword in name])
        print(f"\n{domain}: {len(tools)} tools")
        for tool in tools[:3]:
            print(f"  - {tool}")
        if len(tools) > 3:
            print(f"  ... and {len(tools) - 3} more")