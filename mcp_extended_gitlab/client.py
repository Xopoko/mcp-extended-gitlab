"""GitLab API client with authentication and request handling."""

import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel


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
            "Private-Token": self.config.private_token,
            "Content-Type": "application/json"
        }
        
        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers=self.headers,
            timeout=self.config.timeout
        )
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()
    
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an authenticated request to GitLab API."""
        url = endpoint if endpoint.startswith('http') else endpoint
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                data=data,
                files=files
            )
            response.raise_for_status()
            
            # Handle different response types
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return {"content": response.text, "status_code": response.status_code}
                
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_data = e.response.json()
                error_detail = str(error_data)
            except:
                error_detail = e.response.text
                
            raise Exception(
                f"GitLab API error {e.response.status_code}: {error_detail}"
            )
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", endpoint, params=params)
    
    async def post(
        self, 
        endpoint: str, 
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", endpoint, json_data=json_data, data=data, files=files)
    
    async def put(
        self, 
        endpoint: str, 
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", endpoint, json_data=json_data, data=data)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", endpoint, params=params)
    
    async def head(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a HEAD request."""
        return await self.request("HEAD", endpoint, params=params)