# GitLab Inline Comments Testing Guide

This guide explains how to test inline comments (line-specific comments) on GitLab merge requests using MCP Extended GitLab.

## Overview

Inline comments allow you to comment on specific lines of code in a merge request diff. The MCP Extended GitLab server provides the `create_new_merge_request_thread` tool for this purpose.

## Prerequisites

1. Set your GitLab token:
   ```bash
   export GITLAB_PRIVATE_TOKEN="your-gitlab-private-token"
   ```

2. You need:
   - A project ID (e.g., `85`)
   - A merge request IID (e.g., `4328`)
   - The merge request should have some changes/diff

## Quick Test

### Using the test script:

```bash
# Test with default values (project 85, MR 4328)
python scripts/test_inline_comment.py 85 4328

# Test with specific file and line
python scripts/test_inline_comment.py 85 4328 --file "src/main.py" --line 42 --comment "This needs refactoring"

# Using MCP tool directly
python scripts/test_mr_inline_comment_mcp.py --project 85 --mr 4328
```

## How Inline Comments Work

### Position Object

To create an inline comment, you need a position object with these fields:

```json
{
  "base_sha": "abc123...",      // Base commit SHA
  "start_sha": "def456...",     // Start commit SHA  
  "head_sha": "ghi789...",      // Head commit SHA
  "position_type": "text",      // Type of position
  "new_path": "src/file.py",    // File path (for additions)
  "new_line": 42               // Line number (for additions)
}
```

For deletions, use `old_path` and `old_line` instead.

### Using the MCP Tool

The `create_new_merge_request_thread` tool accepts:

```python
{
    "project_id": "85",
    "merge_request_iid": "4328", 
    "body": "Your comment text",
    "position": '{"base_sha": "...", "head_sha": "...", ...}'  # JSON string
}
```

## Examples

### 1. Simple Inline Comment

```python
# Using test script
python scripts/test_inline_comment.py 85 4328
```

This will:
- Fetch the MR diff
- Find the first added line
- Create a comment on that line

### 2. Comment on Specific File/Line

```python
python scripts/test_inline_comment.py 85 4328 \
    --file "app/models/user.rb" \
    --line 125 \
    --comment "Consider adding validation here"
```

### 3. Using MCP Tool in Your Code

```python
import json

# Position for inline comment
position = {
    "base_sha": "abc123...",
    "head_sha": "def456...", 
    "start_sha": "ghi789...",
    "position_type": "text",
    "new_path": "src/main.py",
    "new_line": 42
}

# Create the comment
await create_new_merge_request_thread(
    project_id="85",
    merge_request_iid="4328",
    body="This line needs error handling",
    position=json.dumps(position)
)
```

## Troubleshooting

### Common Issues

1. **"Invalid position"**: The SHA values don't match the current MR state
   - Solution: Fetch fresh SHA values from `/merge_requests/{iid}/versions`

2. **"File not found"**: The file path doesn't exist in the diff
   - Solution: Check exact file paths in the MR diff

3. **"Line not found"**: The line number is out of range
   - Solution: Verify line numbers in the actual diff

### Getting SHA Values

```python
# Get MR versions
versions = await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}/versions")
latest = versions[0]

base_sha = latest["base_commit_sha"]
start_sha = latest["start_commit_sha"]
head_sha = latest["head_commit_sha"]
```

### Finding Valid Lines

```python
# Get MR diff
diff_info = await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}/diffs")

for diff in diff_info["diffs"]:
    print(f"File: {diff['new_path']}")
    print(f"Added lines: {diff['added_lines']}")
    # Parse diff["diff"] to find exact line numbers
```

## Integration with Test Framework

The inline comment functionality is integrated with the main test framework:

```bash
# Test the create_new_merge_request_thread tool specifically
python scripts/test_all_tools.py -t create_new_merge_request_thread \
    --test-project 85 \
    --verbose
```

## Best Practices

1. **Always verify the MR state** before creating comments
2. **Use fresh SHA values** - they change with each push
3. **Check file paths exactly** - they're case-sensitive
4. **Test on non-production MRs** first
5. **Handle errors gracefully** - positions can become invalid

## API Reference

### create_new_merge_request_thread

Creates a new discussion thread on a merge request, optionally as an inline comment.

**Parameters:**
- `project_id` (required): Project ID or URL-encoded path
- `merge_request_iid` (required): MR internal ID
- `body` (required): Comment text
- `commit_id` (optional): Specific commit SHA
- `created_at` (optional): ISO 8601 timestamp
- `position` (optional): JSON string for inline positioning

**Returns:**
- Discussion object with ID, notes array, and position info