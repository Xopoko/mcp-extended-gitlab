"""GitLab API client with authentication and request handling."""

import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from .utils import wrap_response


class GitLabConfig(BaseModel):
    """GitLab configuration model."""
    
    base_url: str = "https://gitlab.com/api/v4"
    private_token: Optional[str] = None
    timeout: int = 30
    

class GitLabClient:
    """GitLab API client for making authenticated requests."""
    
    def __init__(self, config: Optional[GitLabConfig] = None):
        """Initialize GitLab client with configuration."""
        self.config = config or GitLabConfig()
        
        # Load token from environment if not provided
        if not self.config.private_token:
            self.config.private_token = os.getenv("GITLAB_PRIVATE_TOKEN")
            
        if not self.config.private_token:
            raise ValueError(
                "GitLab private token is required. Set GITLAB_PRIVATE_TOKEN "
                "environment variable or provide it in config."
            )
            
        self.headers = {
            "PRIVATE-TOKEN": self.config.private_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers=self.headers,
            timeout=self.config.timeout
        )

    def _build_url(self, endpoint: str) -> str:
        """Build a full URL from base_url and endpoint without losing path segments."""
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        ep = endpoint.lstrip("/")
        return f"{self.config.base_url.rstrip('/')}/{ep}"
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()
    
    async def _handle_response(self, response: httpx.Response) -> Any:
        """Return JSON data when available, {} for 204, else text payload."""
        response.raise_for_status()
        if response.status_code == 204:
            return {}
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        return {"content": response.text, "status_code": response.status_code}
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        url = self._build_url(endpoint)
        response = await self.client.get(url, params=params)
        return await self._handle_response(response)
    
    async def post(
        self, 
        endpoint: str, 
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request."""
        url = self._build_url(endpoint)
        response = await self.client.post(url, json=json_data, data=data, files=files)
        return await self._handle_response(response)
    
    async def put(
        self, 
        endpoint: str, 
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        url = self._build_url(endpoint)
        response = await self.client.put(url, json=json_data, data=data)
        return await self._handle_response(response)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request."""
        url = self._build_url(endpoint)
        response = await self.client.delete(url, params=params)
        return await self._handle_response(response)
    
    async def head(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a HEAD request."""
        url = self._build_url(endpoint)
        response = await self.client.head(url, params=params)
        return await self._handle_response(response)

    async def close(self) -> None:
        await self.client.aclose()
