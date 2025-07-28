#!/usr/bin/env python3
"""Simple test for inline comments using only standard library."""

import json
import urllib.request
import urllib.parse
import ssl
import sys
import os
from typing import Dict, Any, Optional

# Configuration
GITLAB_BASE_URL = os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4")
GITLAB_TOKEN = os.getenv("GITLAB_PRIVATE_TOKEN")

if not GITLAB_TOKEN:
    print("Error: GITLAB_PRIVATE_TOKEN environment variable is required")
    print("Please set: export GITLAB_PRIVATE_TOKEN='your-token-here'")
    sys.exit(1)

# Disable SSL verification for testing (not recommended for production)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def make_request(method: str, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make a request to GitLab API."""
    url = f"{GITLAB_BASE_URL}{path}"
    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN,
        "Content-Type": "application/json"
    }
    
    request_data = None
    if data:
        request_data = json.dumps(data).encode('utf-8')
    
    request = urllib.request.Request(url, data=request_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(request, context=ssl_context) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        sys.exit(1)


def test_inline_comment(project_id: str, mr_iid: str):
    """Test creating an inline comment."""
    print(f"Testing inline comment on MR !{mr_iid} in project {project_id}")
    print("-" * 60)
    
    # Get MR info
    mr_info = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}")
    print(f"Merge Request: {mr_info['title']}")
    print(f"Author: {mr_info['author']['name']}")
    print(f"State: {mr_info['state']}")
    print()
    
    # Get diff information
    print("Fetching diff information...")
    diff_info = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}/diffs")
    
    # Debug output
    print(f"Diff response type: {type(diff_info)}")
    if isinstance(diff_info, list):
        print(f"Got {len(diff_info)} diffs")
        diffs = diff_info
    elif isinstance(diff_info, dict) and "diffs" in diff_info:
        diffs = diff_info["diffs"]
        print(f"Got {len(diffs)} diffs from dict")
    else:
        print(f"Unexpected diff format: {json.dumps(diff_info, indent=2)[:500]}")
        return
    
    print(f"Found {len(diffs)} changed files")
    
    # Debug: Look at first diff structure
    if diffs:
        print(f"\nFirst diff keys: {list(diffs[0].keys())}")
    
    # Use the first file with added lines
    file_path = None
    line_number = None
    
    for i, diff in enumerate(diffs):
        # Check if diff has content and a new_path
        if diff.get("diff") and diff.get("new_path"):
            # Check if this diff has additions
            diff_content = diff["diff"]
            if "+" in diff_content and not diff_content.startswith("Binary files"):
                file_path = diff["new_path"]
                print(f"\nExamining file {i+1}/{len(diffs)}: {file_path}")
                
                # Parse diff to find first added line
                lines = diff_content.split('\n')
                current_line = 0
                for line in lines:
                    if line.startswith("@@"):
                        # Parse line numbers from diff header
                        import re
                        match = re.search(r'\+(\d+)', line)
                        if match:
                            current_line = int(match.group(1)) - 1
                    elif line.startswith("+") and not line.startswith("+++"):
                        current_line += 1
                        line_number = current_line
                        print(f"Found added line at line {line_number}: {line[1:].strip()[:50]}...")
                        break
                    elif not line.startswith("-"):
                        current_line += 1
                
                if line_number:
                    break
    
    if not file_path or not line_number:
        print("Could not find a suitable file/line to comment on")
        return
    
    # Get MR versions for SHA information
    print("\nFetching MR versions for SHA information...")
    versions = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}/versions")
    
    if not versions or len(versions) == 0:
        print("No versions found")
        return
    
    latest_version = versions[0]
    base_sha = latest_version.get("base_commit_sha")
    start_sha = latest_version.get("start_commit_sha")
    head_sha = latest_version.get("head_commit_sha")
    
    print(f"Base SHA: {base_sha}")
    print(f"Start SHA: {start_sha}")
    print(f"Head SHA: {head_sha}")
    
    # Create inline comment
    comment_text = f"Test inline comment on line {line_number} of {file_path} - Created via MCP Extended GitLab"
    
    position = {
        "base_sha": base_sha,
        "start_sha": start_sha,
        "head_sha": head_sha,
        "position_type": "text",
        "new_path": file_path,
        "new_line": line_number
    }
    
    data = {
        "body": comment_text,
        "position": position
    }
    
    print(f"\nCreating inline comment on line {line_number}...")
    print(f"Comment: {comment_text}")
    
    result = make_request("POST", f"/projects/{project_id}/merge_requests/{mr_iid}/discussions", data)
    
    print("\n✅ Successfully created inline comment!")
    print(f"Discussion ID: {result['id']}")
    
    # Show the created comment details
    if result.get("notes") and len(result["notes"]) > 0:
        note = result["notes"][0]
        print(f"Comment ID: {note['id']}")
        print(f"Author: {note['author']['name']}")
        print(f"Created at: {note['created_at']}")
        
        # Check if it's positioned correctly
        if note.get("position"):
            pos = note["position"]
            print(f"Position: Line {pos.get('new_line', pos.get('old_line'))} in {pos.get('new_path', pos.get('old_path'))}")
    
    # Verify by fetching discussions
    print("\n" + "-" * 60)
    print("Verifying by fetching discussions...")
    discussions = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}/discussions")
    
    inline_count = 0
    for discussion in discussions:
        if discussion.get("notes") and discussion["notes"][0].get("position"):
            inline_count += 1
            if discussion["id"] == result["id"]:
                print(f"✅ Found our comment in discussions (ID: {discussion['id']})")
    
    print(f"\nTotal inline discussions: {inline_count}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_inline_comment_simple.py PROJECT_ID MR_IID")
        sys.exit(1)
    
    if not GITLAB_TOKEN:
        print("Error: GITLAB_PRIVATE_TOKEN environment variable is required")
        print("Set it with: export GITLAB_PRIVATE_TOKEN='your-token'")
        sys.exit(1)
    
    print(f"Using GitLab token: {GITLAB_TOKEN[:10]}...")
    
    project_id = sys.argv[1]
    mr_iid = sys.argv[2]
    
    test_inline_comment(project_id, mr_iid)