#!/usr/bin/env python3
"""Test creating multi-line inline comments on GitLab merge requests."""

import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import sys
import argparse
from typing import Dict, Any, Optional, Tuple


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


def get_mr_diffs(base_url: str, token: str, project_id: str, mr_iid: str) -> Dict[str, Any]:
    """Get merge request diff information."""
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/diffs"
    return make_api_request(url, token)


def find_line_range(diff_text: str, start_line: int = 1, num_lines: int = 5) -> Tuple[int, int]:
    """Find a suitable line range in the diff for multi-line comment."""
    lines = diff_text.split('\n')
    current_line = 0
    added_lines = []
    
    for line in lines:
        if line.startswith("@@"):
            # Parse line numbers from diff header
            import re
            match = re.search(r'\+(\d+)', line)
            if match:
                current_line = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            current_line += 1
            added_lines.append(current_line)
        elif not line.startswith("-"):
            current_line += 1
    
    # Find a range of consecutive added lines
    if len(added_lines) >= num_lines:
        # Try to find the requested start line
        if start_line in added_lines:
            idx = added_lines.index(start_line)
            end_idx = min(idx + num_lines - 1, len(added_lines) - 1)
            return start_line, added_lines[end_idx]
        else:
            # Use first available range
            return added_lines[0], added_lines[num_lines - 1]
    elif added_lines:
        # Use whatever lines we have
        return added_lines[0], added_lines[-1]
    
    return 0, 0


def create_multiline_comment(
    base_url: str,
    token: str,
    project_id: str,
    mr_iid: str,
    file_path: str,
    start_line: int,
    end_line: int,
    comment_text: str,
    version_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a multi-line inline comment."""
    
    # Construct position object for multi-line comment
    position = {
        "base_sha": version_info["base_commit_sha"],
        "start_sha": version_info["start_commit_sha"],
        "head_sha": version_info["head_commit_sha"],
        "position_type": "text",
        "new_path": file_path,
        "new_line": end_line,  # End line for the comment
        "line_range": {
            "start": {
                "line_code": f"{version_info['head_commit_sha']}_{start_line}_{start_line}",
                "type": "new",
                "new_line": start_line
            },
            "end": {
                "line_code": f"{version_info['head_commit_sha']}_{end_line}_{end_line}",
                "type": "new", 
                "new_line": end_line
            }
        }
    }
    
    data = {
        "body": comment_text,
        "position": position
    }
    
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/discussions"
    return make_api_request(url, token, "POST", data)


def main():
    parser = argparse.ArgumentParser(description="Test multi-line inline comments on GitLab MR")
    parser.add_argument("project_id", help="Project ID")
    parser.add_argument("mr_iid", help="Merge request IID")
    parser.add_argument("--file", help="Specific file to comment on")
    parser.add_argument("--start-line", type=int, help="Start line number")
    parser.add_argument("--end-line", type=int, help="End line number")
    parser.add_argument("--lines", type=int, default=3, help="Number of lines to comment on (default: 3)")
    parser.add_argument("--comment", default="Multi-line test comment from MCP Extended GitLab", help="Comment text")
    parser.add_argument("--token", default=os.getenv("GITLAB_PRIVATE_TOKEN", ""), help="GitLab token")
    parser.add_argument("--base-url", default=os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4"), help="GitLab API base URL")
    
    args = parser.parse_args()
    
    print(f"Testing multi-line inline comment on MR !{args.mr_iid} in project {args.project_id}")
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
        
        print(f"Head SHA: {version_info['head_commit_sha'][:8]}...")
        
        # Get diffs
        print("\nGetting diff information...")
        diffs = get_mr_diffs(args.base_url, args.token, args.project_id, args.mr_iid)
        
        if not diffs:
            print("No diffs found!")
            return
        
        print(f"Found {len(diffs)} changed files")
        
        # Select file
        target_file = args.file
        if not target_file:
            # Find a file with enough added lines
            print("\nAnalyzing files for suitable changes:")
            for diff in diffs:
                added = diff.get("added_lines", 0)
                removed = diff.get("removed_lines", 0)
                has_diff = bool(diff.get("diff"))
                print(f"  {diff['new_path']}: +{added}/-{removed} lines, has_diff={has_diff}")
                # Try any file with a diff if we can't find one with enough additions
                if has_diff and not target_file:
                    target_file = diff["new_path"]
                if added >= args.lines:
                    target_file = diff["new_path"]
                    print(f"\nSelected file: {target_file} (+{added} lines)")
                    break
        
        if not target_file:
            print("Could not find a suitable file with enough changes")
            return
        
        # Find the file diff
        file_diff = None
        for diff in diffs:
            if diff["new_path"] == target_file:
                file_diff = diff
                break
        
        if not file_diff:
            print(f"File {target_file} not found in diffs")
            return
        
        # Determine line range
        if args.start_line and args.end_line:
            start_line = args.start_line
            end_line = args.end_line
        else:
            # Find suitable line range
            start_line, end_line = find_line_range(
                file_diff.get("diff", ""),
                args.start_line or 1,
                args.lines
            )
        
        if not start_line or not end_line:
            print("Could not find suitable line range for comment")
            return
        
        print(f"\nCreating multi-line comment on lines {start_line}-{end_line}...")
        print(f"Comment: {args.comment}")
        
        # Create the comment
        result = create_multiline_comment(
            args.base_url,
            args.token,
            args.project_id,
            args.mr_iid,
            target_file,
            start_line,
            end_line,
            f"{args.comment}\n\nThis comment covers lines {start_line} to {end_line}",
            version_info
        )
        
        print("\n✅ Successfully created multi-line inline comment!")
        print(f"Discussion ID: {result['id']}")
        
        if result.get("notes") and len(result["notes"]) > 0:
            note = result["notes"][0]
            print(f"Comment ID: {note['id']}")
            
            # Check position details
            if note.get("position"):
                pos = note["position"]
                print(f"\nPosition details:")
                print(f"  File: {pos.get('new_path', pos.get('old_path'))}")
                print(f"  Line: {pos.get('new_line', pos.get('old_line'))}")
                
                # Check line range
                if pos.get("line_range"):
                    lr = pos["line_range"]
                    start = lr.get("start", {})
                    end = lr.get("end", {})
                    print(f"  Line range: {start.get('new_line', '?')} to {end.get('new_line', '?')}")
                    print("  ✅ Multi-line comment confirmed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()