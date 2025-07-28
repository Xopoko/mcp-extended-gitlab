# GitLab Suggestions Guide

This guide explains how to create GitLab suggestions using MCP Extended GitLab. Suggestions allow reviewers to propose code changes that can be applied with a single click.

## Overview

GitLab suggestions are special inline comments that contain proposed code changes. They use a specific markdown syntax that GitLab recognizes and renders as an applicable patch.

## Suggestion Syntax

### Single-line Suggestions

For suggesting changes to a single line:

```markdown
This line could be improved:

```suggestion
improved_code_here
```
```

### Multi-line Suggestions

For suggesting changes to multiple lines:

```markdown
This block needs refactoring:

```suggestion:-2+3
line 1 of new code
line 2 of new code
line 3 of new code
```
```

The format `-2+3` means "remove 2 lines and add 3 lines" (starting from the line where the comment is placed).

## Using with MCP Extended GitLab

The `create_new_merge_request_thread` tool supports creating suggestions by including the suggestion syntax in the comment body.

### Example: Single-line Suggestion

```python
position = {
    "base_sha": "abc123...",
    "head_sha": "def456...",
    "start_sha": "ghi789...",
    "position_type": "text",
    "new_path": "src/main.py",
    "new_line": 42
}

body = """Consider using a guard clause here:

```suggestion
if not value:
    return None
```"""

await create_new_merge_request_thread(
    project_id="85",
    merge_request_iid="4328",
    body=body,
    position=json.dumps(position)
)
```

### Example: Multi-line Suggestion

```python
# For a 3-line change
body = """This function could be simplified:

```suggestion:-2+1
return x > 0 and y > 0
```"""

# Position on the last line of the range
position = {
    "base_sha": "abc123...",
    "head_sha": "def456...",
    "start_sha": "ghi789...",
    "position_type": "text",
    "new_path": "src/utils.py",
    "new_line": 45  # The third line of the 3-line block
}
```

## Test Scripts

### 1. Basic Suggestion Test

```bash
# Single-line suggestion
python scripts/test_suggestions.py 85 4328

# Multi-line suggestion
python scripts/test_suggestions.py 85 4328 --multi

# Specific file and line
python scripts/test_suggestions.py 85 4328 --file "src/main.py" --line 42
```

### 2. Verify Suggestions

```bash
python scripts/verify_suggestions.py
```

This will check if your suggestions were created correctly and can be applied.

## Important Notes

1. **Line Context**: The suggestion must be placed on an actual changed line in the diff
2. **Syntax Precision**: The markdown syntax must be exact - GitLab is strict about formatting
3. **Multi-line Math**: For multi-line suggestions, the numbers must match the actual lines being replaced/added
4. **Apply Permission**: Users need appropriate permissions to apply suggestions

## Common Patterns

### Adding Error Handling

```suggestion
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return None
```

### Adding Type Hints (Python)

```suggestion:-0+0
def process_data(items: List[str]) -> Dict[str, int]:
```

### Using Optional Chaining (Swift)

```suggestion
let value = object?.property?.method() ?? defaultValue
```

### Adding Null Checks (JavaScript)

```suggestion
if (value !== null && value !== undefined) {
    processValue(value);
}
```

## Troubleshooting

### "Invalid suggestion format"
- Check the markdown syntax is exactly correct
- Ensure there are no extra spaces in the suggestion block markers

### "Cannot apply suggestion"
- The target lines may have changed since the suggestion was created
- Check if there are conflicts with other changes

### "Line not found"
- The suggestion must target lines that exist in the diff
- Use the test scripts to find valid line numbers

## Best Practices

1. **Keep suggestions focused** - One logical change per suggestion
2. **Explain the why** - Add context before the suggestion block
3. **Test locally** - Ensure the suggested code actually works
4. **Consider style** - Match the project's coding standards
5. **Be constructive** - Frame suggestions positively

## Integration Example

```python
async def review_merge_request(project_id, mr_iid):
    """Review MR and create suggestions for improvements."""
    
    # Get MR diffs
    diffs = await get_mr_diffs(project_id, mr_iid)
    
    for diff in diffs:
        if diff["new_path"].endswith(".py"):
            # Check for missing type hints
            for line_num, line in enumerate_diff_lines(diff):
                if "def " in line and "->" not in line:
                    await create_suggestion(
                        project_id, mr_iid,
                        file_path=diff["new_path"],
                        line=line_num,
                        suggestion=add_type_hint(line),
                        comment="Consider adding type hints"
                    )
```

## Summary

GitLab suggestions are a powerful feature for code review. With MCP Extended GitLab, you can:
- Create single-line suggestions for simple fixes
- Create multi-line suggestions for larger refactors
- Automate code review suggestions
- Integrate with CI/CD for automated improvement proposals

The test scripts demonstrate all these capabilities with real examples that can be applied directly in the GitLab UI.