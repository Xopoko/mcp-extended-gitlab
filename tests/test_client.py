"""Tests for the GitLab client."""

import os
from unittest.mock import Mock, AsyncMock, patch

import pytest
import httpx
from httpx import Response

from mcp_extended_gitlab.client import GitLabClient, GitLabConfig


class TestGitLabConfig:
    """Test GitLab configuration."""
    
    def test_config_with_token(self):
        """Test creating config with token."""
        config = GitLabConfig(
            base_url="https://gitlab.example.com/api/v4",
            private_token="test-token"
        )
        
        assert config.base_url == "https://gitlab.example.com/api/v4"
        assert config.private_token == "test-token"
    
    def test_config_from_env(self):
        """Test creating config from environment variables."""
        with patch.dict(os.environ, {
            'GITLAB_BASE_URL': 'https://custom.gitlab.com/api/v4',
            'GITLAB_PRIVATE_TOKEN': 'env-token'
        }):
            config = GitLabConfig(
                base_url=os.getenv("GITLAB_BASE_URL"),
                private_token=os.getenv("GITLAB_PRIVATE_TOKEN")
            )
            
            assert config.base_url == "https://custom.gitlab.com/api/v4"
            assert config.private_token == "env-token"
    
    def test_config_defaults(self):
        """Test config with default values."""
        config = GitLabConfig(
            base_url="https://gitlab.com/api/v4",
            private_token="token"
        )
        
        assert config.base_url == "https://gitlab.com/api/v4"


class TestGitLabClient:
    """Test GitLab client functionality."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        config = GitLabConfig(
            base_url="https://gitlab.example.com/api/v4",
            private_token="test-token"
        )
        return GitLabClient(config)
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock response."""
        response = Mock(spec=Response)
        response.status_code = 200
        response.headers = {"content-type": "application/json"}
        response.json = Mock(return_value={"id": 1, "name": "test"})
        response.raise_for_status = Mock()
        return response
    
    def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.config.base_url == "https://gitlab.example.com/api/v4"
        assert client.config.private_token == "test-token"
        assert isinstance(client.client, httpx.AsyncClient)
    
    def test_client_headers(self, client):
        """Test that client sets correct headers."""
        headers = client.client.headers
        
        assert headers["PRIVATE-TOKEN"] == "test-token"
        assert "application/json" in headers["Accept"]
    
    @pytest.mark.asyncio
    async def test_get_request(self, client, mock_response):
        """Test GET request."""
        with patch.object(client.client, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            result = await client.get("/projects")
            
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            
            assert args[0] == "https://gitlab.example.com/api/v4/projects"
            assert result == {"id": 1, "name": "test"}
    
    @pytest.mark.asyncio
    async def test_get_with_params(self, client, mock_response):
        """Test GET request with parameters."""
        with patch.object(client.client, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            params = {"archived": True, "simple": True}
            result = await client.get("/projects", params=params)
            
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            
            assert kwargs.get('params') == params
    
    @pytest.mark.asyncio
    async def test_post_request(self, client, mock_response):
        """Test POST request."""
        with patch.object(client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            data = {"name": "New Project", "path": "new-project"}
            result = await client.post("/projects", json_data=data)
            
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            assert args[0] == "https://gitlab.example.com/api/v4/projects"
            assert kwargs.get('json') == data
            assert result == {"id": 1, "name": "test"}
    
    @pytest.mark.asyncio
    async def test_put_request(self, client, mock_response):
        """Test PUT request."""
        with patch.object(client.client, 'put', new_callable=AsyncMock) as mock_put:
            mock_put.return_value = mock_response
            
            data = {"name": "Updated Project"}
            result = await client.put("/projects/1", json_data=data)
            
            mock_put.assert_called_once()
            args, kwargs = mock_put.call_args
            
            assert args[0] == "https://gitlab.example.com/api/v4/projects/1"
            assert kwargs.get('json') == data
    
    @pytest.mark.asyncio
    async def test_delete_request(self, client, mock_response):
        """Test DELETE request."""
        mock_response.status_code = 204
        mock_response.json = Mock(side_effect=ValueError)  # No content
        
        with patch.object(client.client, 'delete', new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response
            
            result = await client.delete("/projects/1")
            
            mock_delete.assert_called_once()
            args, kwargs = mock_delete.call_args
            
            assert args[0] == "https://gitlab.example.com/api/v4/projects/1"
            assert result == {}  # Empty dict for 204 responses
    
    @pytest.mark.asyncio
    async def test_error_handling(self, client):
        """Test error handling."""
        error_response = Mock(spec=Response)
        error_response.status_code = 404
        error_response.headers = {"content-type": "application/json"}
        error_response.json = Mock(return_value={"message": "404 Not Found"})
        error_response.raise_for_status = Mock(side_effect=httpx.HTTPStatusError(
            "Client error", request=Mock(), response=error_response
        ))
        
        with patch.object(client.client, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = error_response
            
            with pytest.raises(httpx.HTTPStatusError):
                await client.get("/projects/999999")
    
    @pytest.mark.asyncio
    async def test_close(self, client):
        """Test client close method."""
        close_mock = AsyncMock()
        client.client.aclose = close_mock
        
        await client.close()
        
        close_mock.assert_called_once()
    
    def test_url_building(self, client):
        """Test URL building."""
        # Test with leading slash
        url = client._build_url("/projects")
        assert url == "https://gitlab.example.com/api/v4/projects"
        
        # Test without leading slash
        url = client._build_url("projects")
        assert url == "https://gitlab.example.com/api/v4/projects"
        
        # Test with nested path
        url = client._build_url("/projects/1/issues")
        assert url == "https://gitlab.example.com/api/v4/projects/1/issues"
    
    @pytest.mark.asyncio
    async def test_pagination_headers(self, client):
        """Test handling of pagination headers."""
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.headers = {
            "content-type": "application/json",
            "x-total": "100",
            "x-total-pages": "10",
            "x-per-page": "10",
            "x-page": "1",
            "x-next-page": "2"
        }
        mock_response.json = Mock(return_value=[{"id": 1}, {"id": 2}])
        mock_response.raise_for_status = Mock()
        
        with patch.object(client.client, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            result = await client.get("/projects")
            
            # Result should be the JSON response
            assert result == [{"id": 1}, {"id": 2}]
            
            # Could extend client to return pagination info if needed


class TestClientIntegration:
    """Integration tests for client with real-like scenarios."""
    
    @pytest.mark.asyncio
    async def test_project_crud_flow(self):
        """Test a complete CRUD flow for projects."""
        config = GitLabConfig(
            base_url="https://gitlab.example.com/api/v4",
            private_token="test-token"
        )
        client = GitLabClient(config)
        
        # Mock responses for CRUD operations
        create_response = Mock(spec=Response)
        create_response.status_code = 201
        create_response.headers = {"content-type": "application/json"}
        create_response.json = Mock(return_value={"id": 123, "name": "Test Project"})
        create_response.raise_for_status = Mock()
        
        read_response = Mock(spec=Response)
        read_response.status_code = 200
        read_response.headers = {"content-type": "application/json"}
        read_response.json = Mock(return_value={"id": 123, "name": "Test Project", "description": ""})
        read_response.raise_for_status = Mock()
        
        update_response = Mock(spec=Response)
        update_response.status_code = 200
        update_response.headers = {"content-type": "application/json"}
        update_response.json = Mock(return_value={"id": 123, "name": "Test Project", "description": "Updated"})
        update_response.raise_for_status = Mock()
        
        delete_response = Mock(spec=Response)
        delete_response.status_code = 204
        delete_response.headers = {}
        delete_response.json = Mock(side_effect=ValueError)
        delete_response.raise_for_status = Mock()
        
        with patch.object(client.client, 'post', new_callable=AsyncMock) as mock_post, \
             patch.object(client.client, 'get', new_callable=AsyncMock) as mock_get, \
             patch.object(client.client, 'put', new_callable=AsyncMock) as mock_put, \
             patch.object(client.client, 'delete', new_callable=AsyncMock) as mock_delete:
            
            mock_post.return_value = create_response
            mock_get.return_value = read_response
            mock_put.return_value = update_response
            mock_delete.return_value = delete_response
            
            # Create
            project = await client.post("/projects", json_data={"name": "Test Project"})
            assert project["id"] == 123
            
            # Read
            project = await client.get(f"/projects/{project['id']}")
            assert project["name"] == "Test Project"
            
            # Update
            project = await client.put(f"/projects/{project['id']}", json_data={"description": "Updated"})
            assert project["description"] == "Updated"
            
            # Delete
            result = await client.delete(f"/projects/{project['id']}")
            assert result == {}
            
        await client.close()


if __name__ == "__main__":
    # Quick test
    config = GitLabConfig(
        base_url="https://gitlab.com/api/v4",
        private_token="test-token"
    )
    client = GitLabClient(config)
    
    print(f"Client initialized with base URL: {client.config.base_url}")
    print(f"Headers: {dict(client.client.headers)}")