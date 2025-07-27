"""Pytest configuration and fixtures."""

import asyncio
import os
from pathlib import Path
from unittest.mock import Mock, AsyncMock

import pytest
from fastmcp import FastMCP

from mcp_extended_gitlab.client import GitLabClient, GitLabConfig


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_gitlab_config():
    """Create a mock GitLab configuration."""
    return GitLabConfig(
        base_url="https://gitlab.example.com/api/v4",
        private_token="test-token-123"
    )


@pytest.fixture
def mock_gitlab_client(mock_gitlab_config):
    """Create a mock GitLab client."""
    return GitLabClient(mock_gitlab_config)


@pytest.fixture
def test_mcp():
    """Create a test MCP instance."""
    return FastMCP("test-mcp")


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = Mock()
    response.status_code = 200
    response.headers = {"content-type": "application/json"}
    response.json = Mock(return_value={"success": True})
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def api_modules_path(project_root):
    """Get the API modules directory path."""
    return project_root / 'mcp_extended_gitlab' / 'api'


@pytest.fixture
def openapi_spec_path(project_root):
    """Get the OpenAPI specification file path."""
    return project_root / 'openapi.yaml'


# Mock GitLab API responses for common operations
@pytest.fixture
def mock_project_response():
    """Mock response for a project."""
    return {
        "id": 1,
        "name": "Test Project",
        "path": "test-project",
        "description": "A test project",
        "visibility": "private",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "web_url": "https://gitlab.example.com/test-project",
        "namespace": {
            "id": 1,
            "name": "test-user",
            "path": "test-user"
        }
    }


@pytest.fixture
def mock_issue_response():
    """Mock response for an issue."""
    return {
        "id": 1,
        "iid": 1,
        "project_id": 1,
        "title": "Test Issue",
        "description": "This is a test issue",
        "state": "opened",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "labels": ["bug", "test"],
        "author": {
            "id": 1,
            "username": "test-user",
            "name": "Test User"
        }
    }


@pytest.fixture
def mock_merge_request_response():
    """Mock response for a merge request."""
    return {
        "id": 1,
        "iid": 1,
        "project_id": 1,
        "title": "Test Merge Request",
        "description": "This is a test merge request",
        "state": "opened",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "source_branch": "feature-branch",
        "target_branch": "main",
        "author": {
            "id": 1,
            "username": "test-user",
            "name": "Test User"
        }
    }


@pytest.fixture
def mock_user_response():
    """Mock response for a user."""
    return {
        "id": 1,
        "username": "test-user",
        "name": "Test User",
        "email": "test@example.com",
        "state": "active",
        "avatar_url": "https://gitlab.example.com/uploads/user/avatar/1/avatar.png",
        "web_url": "https://gitlab.example.com/test-user",
        "created_at": "2024-01-01T00:00:00Z",
        "bio": "Test user bio",
        "location": "Test Location",
        "public_email": "test@example.com",
        "is_admin": False
    }


# Test data generators
@pytest.fixture
def generate_project_data():
    """Generate test project data."""
    def _generate(name="Test Project", **kwargs):
        data = {
            "name": name,
            "path": name.lower().replace(" ", "-"),
            "description": f"Description for {name}",
            "visibility": "private"
        }
        data.update(kwargs)
        return data
    return _generate


@pytest.fixture
def generate_issue_data():
    """Generate test issue data."""
    def _generate(title="Test Issue", **kwargs):
        data = {
            "title": title,
            "description": f"Description for {title}",
            "labels": ["test"]
        }
        data.update(kwargs)
        return data
    return _generate


# Async mock helpers
@pytest.fixture
def async_mock():
    """Create an async mock."""
    return AsyncMock()


@pytest.fixture
def mock_async_client():
    """Create a mock async HTTP client."""
    client = AsyncMock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.put = AsyncMock()
    client.patch = AsyncMock()
    client.delete = AsyncMock()
    client.aclose = AsyncMock()
    return client


# Environment setup
@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables."""
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ['GITLAB_BASE_URL'] = 'https://test.gitlab.com/api/v4'
    os.environ['GITLAB_PRIVATE_TOKEN'] = 'test-token'
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)