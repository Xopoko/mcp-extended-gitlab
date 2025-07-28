# Breaking Changes

## Parameter Type Changes for MCP Compatibility

Due to limitations in the MCP (Model Context Protocol) framework with complex nested objects, several API parameters have been changed from accepting dictionary/list objects to accepting JSON strings. This affects the following tools:

### Discussion/Thread Creation Tools

#### `create_new_merge_request_thread`
- **Old**: Individual position parameters (`base_sha`, `start_sha`, `head_sha`, etc.)
- **New**: Single `position` parameter as JSON string
- **Example**:
  ```python
  position='{"base_sha": "...", "start_sha": "...", "head_sha": "...", "position_type": "text", "new_path": "file.txt", "new_line": 10}'
  ```

#### `create_new_issue_thread` and `create_new_commit_thread`
- **Old**: `position: Optional[Any]`
- **New**: `position: Optional[str]` (JSON string)

### Protected Branches Tools

#### `protect_repository_branch` and `update_protected_branch`
- **Old**: `allowed_to_push`, `allowed_to_merge`, `allowed_to_unprotect` as `List[Dict[str, Any]]`
- **New**: These parameters now accept JSON strings
- **Example**:
  ```python
  allowed_to_push='[{"access_level": 40}]'
  ```

### Feature Flags Tools

#### `create_feature_flag` and `edit_feature_flag`
- **Old**: `strategies: Optional[List[Dict[str, Any]]]`
- **New**: `strategies: Optional[str]` (JSON string)
- **Example**:
  ```python
  strategies='[{"name": "userWithId", "parameters": {"userIds": "1,2,3"}}]'
  ```

### Integration Tools

#### `activate_integration`
- **Old**: `config: Optional[Dict[str, Any]]`
- **New**: `config: Optional[str]` (JSON string)
- **Example**:
  ```python
  config='{"token": "...", "url": "..."}'
  ```

### Release Tools

#### `create_release`
- **Old**: `assets: Optional[Dict[str, Any]]`
- **New**: `assets: Optional[str]` (JSON string)
- **Example**:
  ```python
  assets='{"links": [{"name": "asset1", "url": "https://..."}]}'
  ```

## Migration Guide

When using these tools through MCP, you must now:

1. Convert dictionary/list parameters to JSON strings before passing them
2. Ensure proper escaping of quotes in JSON strings
3. Handle JSON parsing errors gracefully

### Example Migration

**Before:**
```python
# This would fail with MCP
position = {
    "base_sha": "abc123",
    "start_sha": "abc123", 
    "head_sha": "def456",
    "position_type": "text",
    "new_path": "file.txt",
    "new_line": 10
}
```

**After:**
```python
# This works with MCP
import json
position = json.dumps({
    "base_sha": "abc123",
    "start_sha": "abc123",
    "head_sha": "def456", 
    "position_type": "text",
    "new_path": "file.txt",
    "new_line": 10
})
```

## Why These Changes?

The MCP framework has limitations when passing complex nested objects (dictionaries containing lists, lists of dictionaries, etc.) as parameters. By accepting JSON strings instead, we can:

1. Maintain full API compatibility with GitLab
2. Work within MCP's constraints
3. Provide a consistent interface for complex parameters

These changes only affect how parameters are passed through MCP - the underlying GitLab API calls remain unchanged.