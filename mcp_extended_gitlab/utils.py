"""Utility functions for MCP Extended GitLab."""

from typing import Any, Dict, List, Union


def wrap_response(data: Union[Dict[str, Any], List[Any]]) -> Dict[str, Any]:
    """
    Wrap API responses to ensure they are always dictionaries.
    
    FastMCP requires structured_content to be a dict or None.
    When GitLab API returns a list, we wrap it in a dictionary.
    
    Args:
        data: The response data from GitLab API
        
    Returns:
        Dictionary containing the response data
    """
    if isinstance(data, list):
        return {"items": data, "count": len(data)}
    return data