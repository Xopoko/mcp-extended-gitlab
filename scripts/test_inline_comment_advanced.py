#!/usr/bin/env python3
"""Advanced test for inline comments with better line selection."""

import json
import urllib.request
import urllib.parse
import ssl
import sys
import os
from typing import Dict, Any, Optional, List, Tuple

# Configuration
GITLAB_BASE_URL = os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4")
GITLAB_TOKEN = os.getenv("GITLAB_PRIVATE_TOKEN")

# Disable SSL verification for testing (not recommended for production)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def make_request(method: str, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
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


def find_interesting_line(diff_content: str) -> Optional[Tuple[int, str, str]]:
    """Find an interesting line to comment on (e.g., function definition, class, important logic).
    
    Returns: (line_number, line_content, suggested_comment)
    """
    lines = diff_content.split('\n')
    current_line = 0
    
    # Patterns to look for
    patterns = [
        ("func ", "Swift function"),
        ("class ", "Class definition"),
        ("struct ", "Struct definition"),
        ("def ", "Python function"),
        ("function ", "Function definition"),
        ("if ", "Conditional logic"),
        ("for ", "Loop"),
        ("import ", "Import statement"),
        ("assert", "Assertion"),
        ("test", "Test code"),
    ]
    
    for line in lines:
        if line.startswith("@@"):
            # Parse line numbers from diff header
            import re
            match = re.search(r'\+(\d+)', line)
            if match:
                current_line = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            current_line += 1
            line_content = line[1:].strip()
            
            # Check for interesting patterns
            for pattern, description in patterns:
                if pattern.lower() in line_content.lower() and len(line_content) > 10:
                    comment = f"Inline comment on {description}: This line contains {pattern.strip()}"
                    return (current_line, line_content, comment)
        elif not line.startswith("-"):
            current_line += 1
    
    # If no interesting pattern found, return first meaningful added line
    current_line = 0
    for line in lines:
        if line.startswith("@@"):
            import re
            match = re.search(r'\+(\d+)', line)
            if match:
                current_line = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            current_line += 1
            line_content = line[1:].strip()
            if len(line_content) > 5 and not line_content.startswith("//"):
                return (current_line, line_content, "Test inline comment on this line")
        elif not line.startswith("-"):
            current_line += 1
    
    return None


def test_inline_comment(project_id: str, mr_iid: str, target_file: Optional[str] = None, target_line: Optional[int] = None):
    """Test creating an inline comment."""
    print(f"🔍 Testing inline comment on MR !{mr_iid} in project {project_id}")
    print("=" * 70)
    
    # Get MR info
    mr_info = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}")
    print(f"📋 Merge Request: {mr_info['title']}")
    print(f"👤 Author: {mr_info['author']['name']}")
    print(f"📊 State: {mr_info['state']}")
    print(f"🔗 Web URL: {mr_info['web_url']}")
    print()
    
    # Get diff information
    print("📥 Fetching diff information...")
    diffs = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}/diffs")
    
    if not isinstance(diffs, list):
        print("❌ Unexpected diff format")
        return
    
    print(f"📁 Found {len(diffs)} changed files")
    
    # Find file and line to comment on
    file_path = None
    line_number = None
    line_content = None
    comment_text = None
    
    if target_file and target_line:
        # Use specified file and line
        for diff in diffs:
            if diff.get("new_path") == target_file:
                file_path = target_file
                line_number = target_line
                comment_text = f"Inline comment on line {line_number} of {file_path}"
                print(f"\n✅ Using specified file and line: {file_path}:{line_number}")
                break
    else:
        # Find an interesting line to comment on
        print("\n🔎 Looking for interesting lines to comment on...")
        
        for i, diff in enumerate(diffs):
            if diff.get("diff") and diff.get("new_path"):
                diff_content = diff["diff"]
                if "+" in diff_content and not diff_content.startswith("Binary files"):
                    result = find_interesting_line(diff_content)
                    if result:
                        line_number, line_content, suggested_comment = result
                        file_path = diff["new_path"]
                        comment_text = f"{suggested_comment} - Created via MCP Extended GitLab"
                        print(f"\n✅ Found interesting line in {file_path}")
                        print(f"   Line {line_number}: {line_content[:80]}...")
                        break
    
    if not file_path or not line_number:
        print("\n❌ Could not find a suitable file/line to comment on")
        return
    
    # Get MR versions for SHA information
    print("\n📤 Fetching MR versions for SHA information...")
    versions = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}/versions")
    
    if not versions or len(versions) == 0:
        print("❌ No versions found")
        return
    
    latest_version = versions[0]
    base_sha = latest_version.get("base_commit_sha")
    start_sha = latest_version.get("start_commit_sha")
    head_sha = latest_version.get("head_commit_sha")
    
    print(f"   Base SHA: {base_sha[:8]}...")
    print(f"   Start SHA: {start_sha[:8]}...")
    print(f"   Head SHA: {head_sha[:8]}...")
    
    # Create inline comment
    if not comment_text:
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
    
    print(f"\n💬 Creating inline comment...")
    print(f"   File: {file_path}")
    print(f"   Line: {line_number}")
    print(f"   Comment: {comment_text}")
    
    result = make_request("POST", f"/projects/{project_id}/merge_requests/{mr_iid}/discussions", data)
    
    print("\n✅ Successfully created inline comment!")
    print(f"   Discussion ID: {result['id']}")
    
    # Show the created comment details
    if result.get("notes") and len(result["notes"]) > 0:
        note = result["notes"][0]
        print(f"   Comment ID: {note['id']}")
        print(f"   Author: {note['author']['name']}")
        print(f"   Created at: {note['created_at']}")
        
        # Check if it's positioned correctly
        if note.get("position"):
            pos = note["position"]
            print(f"   Position: Line {pos.get('new_line', pos.get('old_line'))} in {pos.get('new_path', pos.get('old_path'))}")
    
    # Verify by fetching discussions
    print("\n" + "=" * 70)
    print("🔍 Verifying by fetching all discussions...")
    discussions = make_request("GET", f"/projects/{project_id}/merge_requests/{mr_iid}/discussions")
    
    inline_count = 0
    regular_count = 0
    
    for discussion in discussions:
        if discussion.get("notes") and discussion["notes"][0].get("position"):
            inline_count += 1
            if discussion["id"] == result["id"]:
                print(f"✅ Found our comment in discussions (ID: {discussion['id']})")
        else:
            regular_count += 1
    
    print(f"\n📊 Discussion Summary:")
    print(f"   Total discussions: {len(discussions)}")
    print(f"   Inline discussions: {inline_count}")
    print(f"   Regular discussions: {regular_count}")
    
    print(f"\n🎉 Test completed successfully!")
    print(f"🔗 View the comment: {mr_info['web_url']}#note_{result['notes'][0]['id']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test inline comments on GitLab merge requests")
    parser.add_argument("project_id", help="Project ID (e.g., 85)")
    parser.add_argument("mr_iid", help="Merge request IID (e.g., 4328)")
    parser.add_argument("--file", "-f", help="Specific file path to comment on")
    parser.add_argument("--line", "-l", type=int, help="Specific line number to comment on")
    
    args = parser.parse_args()
    
    if not GITLAB_TOKEN:
        print("❌ Error: GITLAB_PRIVATE_TOKEN environment variable is required")
        print("   Set it with: export GITLAB_PRIVATE_TOKEN='your-token'")
        sys.exit(1)
    
    print(f"🔑 Using GitLab token: {GITLAB_TOKEN[:10]}...")
    print(f"🌐 GitLab API: {GITLAB_BASE_URL}")
    print()
    
    test_inline_comment(
        project_id=args.project_id,
        mr_iid=args.mr_iid,
        target_file=args.file,
        target_line=args.line
    )