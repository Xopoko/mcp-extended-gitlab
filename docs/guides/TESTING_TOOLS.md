# GitLab API Tools Testing Scripts

This directory contains scripts for testing all 478+ GitLab API tools in the MCP Extended GitLab server.

## Overview

The testing framework allows you to:
- Test all GitLab API tools automatically
- Test specific tools, categories, or presets
- Generate reports in text, JSON, or Markdown format
- Configure test resources and scenarios
- Run safe read-only tests or destructive tests

## Scripts

### `test_all_tools.py`

The main testing script that can test any or all GitLab API tools.

**Features:**
- Dynamic tool discovery from the MCP server
- Intelligent parameter generation for testing
- Multiple filtering options (tools, categories, presets)
- Comprehensive error handling and reporting
- Support for different output formats

**Usage:**
```bash
# Test all tools
python test_all_tools.py

# Test specific tools
python test_all_tools.py -t list_projects -t get_project

# Test by category
python test_all_tools.py -c core -c ci_cd

# Test using preset
python test_all_tools.py -p minimal

# Generate JSON report
python test_all_tools.py -f json -o report.json

# Test with specific project/group/user
python test_all_tools.py --test-project 123 --test-group 456
```

### `run_tool_tests.sh`

Convenient wrapper script for common testing scenarios.

**Usage:**
```bash
# Run quick smoke test
./run_tool_tests.sh quick

# Test core features
./run_tool_tests.sh core

# Test CI/CD tools
./run_tool_tests.sh ci_cd

# Test read-only operations (safe)
./run_tool_tests.sh read_only

# Test all tools
./run_tool_tests.sh all
```

### `test_config.json`

Configuration file for test resources and scenarios.

## Setup

1. **Set GitLab Token:**
   ```bash
   export GITLAB_PRIVATE_TOKEN="your-gitlab-private-token"
   ```

2. **Set Test Resources (Optional):**
   ```bash
   export GITLAB_TEST_PROJECT_ID="your-test-project-id"
   export GITLAB_TEST_GROUP_ID="your-test-group-id"
   export GITLAB_TEST_USER_ID="your-test-user-id"
   ```

3. **Run Tests:**
   ```bash
   # Quick test
   ./run_tool_tests.sh quick
   
   # Or use Python directly
   python test_all_tools.py --preset minimal --verbose
   ```

## Test Categories

Tools are organized into these categories:
- **core**: Essential GitLab features (projects, issues, MRs, users, etc.)
- **ci_cd**: CI/CD features (pipelines, runners, variables, lint)
- **security**: Security features (protected branches, deploy keys/tokens)
- **devops**: DevOps features (environments, deployments, feature flags)
- **registry**: Package and container registries
- **monitoring**: Analytics, error tracking, statistics
- **integrations**: Third-party service integrations
- **admin**: Administrative features (license, system hooks)

## Test Presets

Pre-defined tool sets for common scenarios:
- **minimal**: Essential tools only (~15 tools)
- **core**: All core GitLab features (~100 tools)
- **ci_cd**: CI/CD related tools (~50 tools)
- **devops**: DevOps tools (~40 tools)
- **admin**: Admin tools (~20 tools)

## Report Formats

### Text Report (Default)
```
============================================================
GitLab API Tools Test Report
============================================================
Generated: 2024-01-10 14:30:00
Duration: 45.23 seconds

Summary:
  Total Tools: 478
  Tested: 15
  Passed: 12 (80.0%)
  Failed: 2
  Skipped: 1
...
```

### JSON Report
```json
{
  "timestamp": "2024-01-10T14:30:00",
  "duration": 45.23,
  "summary": {
    "total_tools": 478,
    "tested": 15,
    "passed": 12,
    "failed": 2,
    "skipped": 1,
    "success_rate": 80.0
  },
  ...
}
```

### Markdown Report
```markdown
# GitLab API Tools Test Report

**Generated:** 2024-01-10 14:30:00
**Duration:** 45.23 seconds

## Summary

| Metric | Value | Percentage |
|--------|-------|------------|
| Total Tools | 478 | 100% |
| Tested | 15 | 3.1% |
...
```

## Safety Considerations

1. **Read-Only Tests**: Use the `read_only` scenario for safe testing:
   ```bash
   ./run_tool_tests.sh read_only
   ```

2. **Test Resources**: Always use dedicated test projects/groups:
   ```bash
   export GITLAB_TEST_PROJECT_ID="test-project-id"
   ```

3. **Skip Destructive Tools**: Configure in `test_config.json`:
   ```json
   "skip_tools": [
     "delete_project",
     "delete_group",
     "delete_user"
   ]
   ```

## Troubleshooting

1. **Authentication Error**: Ensure `GITLAB_PRIVATE_TOKEN` is set correctly
2. **Missing Test Resources**: Set test IDs for tools that require them
3. **Rate Limiting**: Use `--stop-on-error` to avoid hitting rate limits
4. **Permission Errors**: Ensure your token has necessary permissions

## Examples

### Test Minimal Tools with JSON Report
```bash
python test_all_tools.py --preset minimal --format json --output minimal_test.json
```

### Test Specific Tools Verbosely
```bash
python test_all_tools.py -t list_projects -t create_issue -t list_pipelines --verbose
```

### Test Core Features with Markdown Report
```bash
./run_tool_tests.sh core --markdown --save core_test_report.md
```

### Safe Production Test
```bash
# Only tests read operations
./run_tool_tests.sh read_only --project YOUR_PROJECT_ID
```