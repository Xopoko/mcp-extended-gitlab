# User Guides

This directory contains how-to guides and tutorials for using MCP Extended GitLab effectively.

## Available Guides

- **[Testing Tools Guide](./TESTING_TOOLS.md)** - Comprehensive guide for testing GitLab API tools
- **[Inline Comments Guide](./INLINE_COMMENTS_GUIDE.md)** - Creating inline code comments on merge requests
- **[Suggestions Guide](./SUGGESTIONS_GUIDE.md)** - Creating GitLab suggestions for code improvements

## Quick How-To's

### Testing Tools

```bash
# Quick test with minimal tools
./scripts/run_tool_tests.sh quick

# Test specific tools
python scripts/test_all_tools.py -t list_projects -t get_project

# Test by category
python scripts/test_all_tools.py -c core --verbose
```

### Creating Inline Comments

```python
# Single-line comment
python scripts/test_inline_comment.py 85 4328 --line 42

# Multi-line comment  
python scripts/test_multiline_comment.py 85 4328 --lines 5
```

### Creating Suggestions

```python
# Single-line suggestion
python scripts/test_suggestions.py 85 4328

# Multi-line suggestion
python scripts/test_suggestions.py 85 4328 --multi
```

## Common Workflows

### 1. Code Review Automation

Use inline comments and suggestions to automate code review:

1. List merge requests: `list_merge_requests`
2. Get MR diff: Use custom script or API
3. Create inline comments with suggestions
4. Mark threads as resolved

### 2. Issue Management

Automate issue workflows:

1. Search for issues: `search_in_project`
2. Create/update issues: `create_issue`, `update_issue`
3. Add labels: `add_labels_to_issue`
4. Assign users: `update_issue` with assignee_ids

### 3. CI/CD Management

Monitor and manage pipelines:

1. List pipelines: `list_pipelines`
2. Check status: `get_pipeline`
3. Retry failed: `retry_pipeline`
4. View jobs: `list_pipeline_jobs`

## Best Practices

1. **Use Tool Filtering**: Enable only needed tools to reduce context usage
2. **Test First**: Always test tools with read operations before writes
3. **Handle Errors**: Check for API errors and rate limits
4. **Use Pagination**: For large result sets, use page/per_page parameters
5. **Batch Operations**: Some operations can be batched for efficiency

## Need Help?

- Check the [API Reference](../api/) for tool details
- See [Setup Documentation](../setup/) for configuration help
- Review [Development Docs](../development/) for architecture info