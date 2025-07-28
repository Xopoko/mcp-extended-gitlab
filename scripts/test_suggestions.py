#!/usr/bin/env python3
"""Test creating GitLab suggestions in inline comments."""

import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import sys
import argparse
from typing import Dict, Any, Optional, List, Tuple


def make_api_request(url: str, token: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make an API request to GitLab."""
    headers = {
        "Private-Token": token,
        "Content-Type": "application/json"
    }
    
    # Create SSL context that doesn't verify certificates (for self-signed certs)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    request = urllib.request.Request(url, headers=headers, method=method)
    
    if data and method in ["POST", "PUT"]:
        request.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(request, context=ssl_context) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"API Error {e.code}: {error_body}")
        raise


def get_mr_versions(base_url: str, token: str, project_id: str, mr_iid: str) -> Dict[str, Any]:
    """Get merge request versions to obtain SHA information."""
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/versions"
    versions = make_api_request(url, token)
    return versions[0] if versions else {}


def get_mr_diffs(base_url: str, token: str, project_id: str, mr_iid: str) -> List[Dict[str, Any]]:
    """Get merge request diff information."""
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/diffs"
    return make_api_request(url, token)


def extract_code_context(diff_text: str, target_line: int, context_lines: int = 2) -> Tuple[List[str], int]:
    """Extract code context around a specific line."""
    lines = diff_text.split('\n')
    current_line = 0
    code_lines = []
    line_mapping = {}  # Maps actual line numbers to code_lines indices
    
    for line in lines:
        if line.startswith("@@"):
            # Parse line numbers from diff header
            import re
            match = re.search(r'\+(\d+)', line)
            if match:
                current_line = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            current_line += 1
            code_lines.append((current_line, line[1:]))  # Remove the + prefix
            line_mapping[current_line] = len(code_lines) - 1
        elif not line.startswith("-") and not line.startswith("@@") and not line.startswith("\\"):
            current_line += 1
            code_lines.append((current_line, line[1:] if line.startswith(" ") else line))
            line_mapping[current_line] = len(code_lines) - 1
    
    # Find the target line and extract context
    if target_line in line_mapping:
        idx = line_mapping[target_line]
        start_idx = max(0, idx - context_lines)
        end_idx = min(len(code_lines), idx + context_lines + 1)
        
        context = []
        for i in range(start_idx, end_idx):
            context.append(code_lines[i][1])
        
        return context, idx - start_idx
    
    return [], -1


def create_single_line_suggestion(
    base_url: str,
    token: str,
    project_id: str,
    mr_iid: str,
    file_path: str,
    line_number: int,
    original_line: str,
    suggested_line: str,
    comment_text: str,
    version_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a single-line suggestion."""
    
    # Construct the suggestion syntax
    suggestion_body = f"""{comment_text}

```suggestion
{suggested_line}
```"""
    
    # Position for the inline comment
    position = {
        "base_sha": version_info["base_commit_sha"],
        "start_sha": version_info["start_commit_sha"],
        "head_sha": version_info["head_commit_sha"],
        "position_type": "text",
        "new_path": file_path,
        "new_line": line_number
    }
    
    data = {
        "body": suggestion_body,
        "position": position
    }
    
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/discussions"
    return make_api_request(url, token, "POST", data)


def create_multi_line_suggestion(
    base_url: str,
    token: str,
    project_id: str,
    mr_iid: str,
    file_path: str,
    start_line: int,
    end_line: int,
    original_lines: List[str],
    suggested_lines: List[str],
    comment_text: str,
    version_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a multi-line suggestion."""
    
    # Calculate the range
    lines_to_change = end_line - start_line + 1
    
    # Construct the multi-line suggestion syntax
    suggestion_body = f"""{comment_text}

```suggestion:-{lines_to_change - 1}+{len(suggested_lines) - 1}
{chr(10).join(suggested_lines)}
```"""
    
    # Position for the inline comment (on the last line of the range)
    position = {
        "base_sha": version_info["base_commit_sha"],
        "start_sha": version_info["start_commit_sha"],
        "head_sha": version_info["head_commit_sha"],
        "position_type": "text",
        "new_path": file_path,
        "new_line": end_line
    }
    
    data = {
        "body": suggestion_body,
        "position": position
    }
    
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/discussions"
    return make_api_request(url, token, "POST", data)


def main():
    parser = argparse.ArgumentParser(description="Test GitLab suggestions in merge requests")
    parser.add_argument("project_id", help="Project ID")
    parser.add_argument("mr_iid", help="Merge request IID")
    parser.add_argument("--file", help="Specific file to comment on")
    parser.add_argument("--line", type=int, help="Line number for single-line suggestion")
    parser.add_argument("--start-line", type=int, help="Start line for multi-line suggestion")
    parser.add_argument("--end-line", type=int, help="End line for multi-line suggestion")
    parser.add_argument("--multi", action="store_true", help="Create multi-line suggestion")
    parser.add_argument("--token", default=os.getenv("GITLAB_PRIVATE_TOKEN", ""), help="GitLab token")
    parser.add_argument("--base-url", default=os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4"), help="GitLab API base URL")
    
    args = parser.parse_args()
    
    print(f"Testing GitLab suggestions on MR !{args.mr_iid} in project {args.project_id}")
    print("=" * 60)
    
    try:
        # Get MR info
        mr_url = f"{args.base_url}/projects/{args.project_id}/merge_requests/{args.mr_iid}"
        mr_info = make_api_request(mr_url, args.token)
        print(f"MR Title: {mr_info['title']}")
        print(f"Author: {mr_info['author']['name']}")
        print()
        
        # Get version info
        print("Getting version information...")
        version_info = get_mr_versions(args.base_url, args.token, args.project_id, args.mr_iid)
        if not version_info:
            print("Error: Could not get version information")
            return
        
        # Get diffs
        print("Getting diff information...")
        diffs = get_mr_diffs(args.base_url, args.token, args.project_id, args.mr_iid)
        
        if not diffs:
            print("No diffs found!")
            return
        
        print(f"Found {len(diffs)} changed files\n")
        
        # Select file
        target_file = args.file
        if not target_file:
            # Find a Swift or Python file with changes
            for diff in diffs:
                if diff.get("added_lines", 0) > 0:
                    if diff["new_path"].endswith(('.swift', '.py', '.js', '.rb')):
                        target_file = diff["new_path"]
                        print(f"Selected file: {target_file}")
                        break
            
            if not target_file:
                target_file = diffs[0]["new_path"]
                print(f"Using first file: {target_file}")
        
        # Find the file diff
        file_diff = None
        for diff in diffs:
            if diff["new_path"] == target_file:
                file_diff = diff
                break
        
        if not file_diff:
            print(f"File {target_file} not found in diffs")
            return
        
        # Parse the diff to find suitable lines
        diff_lines = file_diff.get("diff", "").split('\n')
        current_line = 0
        added_lines = []
        
        for i, line in enumerate(diff_lines):
            if line.startswith("@@"):
                import re
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1)) - 1
            elif line.startswith("+") and not line.startswith("+++"):
                current_line += 1
                added_lines.append((current_line, line[1:]))  # Store line number and content
            elif not line.startswith("-"):
                current_line += 1
        
        if not added_lines:
            print("No added lines found in the file")
            return
        
        if args.multi or (args.start_line and args.end_line):
            # Multi-line suggestion
            if args.start_line and args.end_line:
                start_line = args.start_line
                end_line = args.end_line
            else:
                # Auto-select first 3 lines
                start_line = added_lines[0][0]
                end_line = added_lines[min(2, len(added_lines)-1)][0]
            
            print(f"\nCreating multi-line suggestion for lines {start_line}-{end_line}...")
            
            # Extract original lines
            original_lines = []
            for line_num, content in added_lines:
                if start_line <= line_num <= end_line:
                    original_lines.append(content)
            
            # Create suggested improvements
            suggested_lines = []
            for line in original_lines:
                # Simple improvements based on common patterns
                improved = line
                
                # Add type hints for Python
                if target_file.endswith('.py') and 'def ' in line and '->' not in line:
                    improved = line.rstrip() + ' -> Any'
                # Add guard for Swift
                elif target_file.endswith('.swift') and 'let ' in line and '?' not in line and '!' not in line:
                    if '=' in line:
                        parts = line.split('=')
                        improved = parts[0].rstrip() + '? =' + parts[1]
                # Add semicolon for JavaScript
                elif target_file.endswith('.js') and line.strip() and not line.rstrip().endswith((';', '{', '}')):
                    improved = line.rstrip() + ';'
                # Add .freeze for Ruby constants
                elif target_file.endswith('.rb') and line.strip().startswith(line.strip().upper()):
                    if '=' in line and not '.freeze' in line:
                        improved = line.rstrip() + '.freeze'
                
                suggested_lines.append(improved)
            
            comment = "Here's a suggestion to improve this code block:"
            
            result = create_multi_line_suggestion(
                args.base_url,
                args.token,
                args.project_id,
                args.mr_iid,
                target_file,
                start_line,
                end_line,
                original_lines,
                suggested_lines,
                comment,
                version_info
            )
            
            print("\n✅ Successfully created multi-line suggestion!")
            
        else:
            # Single-line suggestion
            if args.line:
                # Find the specified line
                target_line = None
                for line_num, content in added_lines:
                    if line_num == args.line:
                        target_line = (line_num, content)
                        break
                
                if not target_line:
                    print(f"Line {args.line} not found in added lines")
                    return
            else:
                # Use first added line
                target_line = added_lines[0]
            
            line_number, original_line = target_line
            print(f"\nCreating single-line suggestion for line {line_number}...")
            print(f"Original: {original_line.strip()}")
            
            # Create a suggested improvement
            suggested_line = original_line
            
            # Simple improvements based on file type
            if target_file.endswith('.swift'):
                # Add optional chaining
                if '!' in original_line and 'print' not in original_line:
                    suggested_line = original_line.replace('!', '?')
                    comment = "Consider using optional chaining instead of force unwrapping"
                # Add private modifier
                elif original_line.strip().startswith(('func ', 'var ', 'let ')) and 'private' not in original_line:
                    suggested_line = original_line.replace('func ', 'private func ').replace('var ', 'private var ').replace('let ', 'private let ')
                    comment = "Consider making this private if it's not used outside this scope"
                else:
                    suggested_line = original_line.rstrip() + " // TODO: Review this line"
                    comment = "This line might need review"
            
            elif target_file.endswith('.py'):
                # Add type hints
                if 'def ' in original_line and ':' in original_line and '->' not in original_line:
                    suggested_line = original_line.replace(':', ' -> None:')
                    comment = "Consider adding type hints for better code clarity"
                else:
                    suggested_line = original_line.rstrip() + "  # TODO: Add documentation"
                    comment = "Consider adding documentation"
            
            else:
                # Generic improvement
                suggested_line = original_line.rstrip() + " // FIXME: Review this implementation"
                comment = "This line might need review"
            
            print(f"Suggested: {suggested_line.strip()}")
            
            result = create_single_line_suggestion(
                args.base_url,
                args.token,
                args.project_id,
                args.mr_iid,
                target_file,
                line_number,
                original_line,
                suggested_line,
                comment,
                version_info
            )
            
            print("\n✅ Successfully created single-line suggestion!")
        
        # Display result
        if result.get("id"):
            print(f"Discussion ID: {result['id']}")
            
            if result.get("notes") and len(result["notes"]) > 0:
                note = result["notes"][0]
                print(f"Comment ID: {note['id']}")
                
                # Check if it's recognized as a suggestion
                if "```suggestion" in note.get("body", ""):
                    print("✅ Suggestion format confirmed!")
                    print("\nThe suggestion can now be applied directly from the GitLab UI")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()