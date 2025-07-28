# Scripts

This directory contains utility scripts for testing and development.

## Testing Scripts

### Tool Testing
- **test_all_tools.py** - Comprehensive testing framework for all GitLab API tools
- **run_tool_tests.sh** - Convenient wrapper for common test scenarios
- **test_config.json** - Configuration for test scenarios and resources

### Inline Comments Testing
- **test_inline_comment.py** - Test single-line inline comments
- **test_multiline_comment.py** - Test multi-line inline comments
- **test_suggestions.py** - Test GitLab suggestions

### Verification Scripts
- **verify_suggestions.py** - Verify created suggestions
- **verify_multiline.py** - Verify multi-line comments

### Other Utilities
- **list_tools.py** - List all available MCP tools
- **setup_claude.sh** - Setup script for Claude configuration
- **example_usage.py** - Examples of using the testing framework

## Usage Examples

```bash
# Quick test
./run_tool_tests.sh quick

# Test specific tools
python test_all_tools.py -t list_projects -t get_project

# Test inline comments
python test_inline_comment.py PROJECT_ID MR_IID

# List all available tools
python list_tools.py
```

See [Testing Tools Guide](../docs/guides/TESTING_TOOLS.md) for comprehensive documentation.