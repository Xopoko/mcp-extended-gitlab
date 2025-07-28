#!/usr/bin/env python3
"""Test creating inline comments on specific lines in merge request diffs."""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_extended_gitlab.client import GitLabClient, GitLabConfig


async def get_merge_request_diff(client: GitLabClient, project_id: str, mr_iid: str) -> Dict[str, Any]:
    """Get merge request diff information."""
    return await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}/diffs")


async def get_merge_request_versions(client: GitLabClient, project_id: str, mr_iid: str) -> Dict[str, Any]:
    """Get merge request versions (for getting SHA information)."""
    return await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}/versions")


async def create_inline_comment(
    client: GitLabClient,
    project_id: str,
    mr_iid: str,
    file_path: str,
    line_number: int,
    comment_text: str,
    line_type: str = "new",  # "new" or "old"
    base_sha: Optional[str] = None,
    start_sha: Optional[str] = None,
    head_sha: Optional[str] = None
) -> Dict[str, Any]:
    """Create an inline comment on a specific line in a merge request.
    
    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        mr_iid: Merge request IID
        file_path: Path to the file in the diff
        line_number: Line number to comment on
        comment_text: Text of the comment
        line_type: "new" for additions, "old" for deletions
        base_sha: Base commit SHA (optional, will fetch if not provided)
        start_sha: Start commit SHA (optional, will fetch if not provided)
        head_sha: Head commit SHA (optional, will fetch if not provided)
    """
    
    # If SHAs not provided, fetch them from MR versions
    if not all([base_sha, start_sha, head_sha]):
        versions = await get_merge_request_versions(client, project_id, mr_iid)
        if versions and len(versions) > 0:
            latest_version = versions[0]
            base_sha = base_sha or latest_version.get("base_commit_sha")
            start_sha = start_sha or latest_version.get("start_commit_sha")
            head_sha = head_sha or latest_version.get("head_commit_sha")
    
    # Construct position object for inline comment
    position = {
        "base_sha": base_sha,
        "start_sha": start_sha,
        "head_sha": head_sha,
        "position_type": "text",
        "new_path": file_path if line_type == "new" else None,
        "old_path": file_path if line_type == "old" else None,
        "new_line": line_number if line_type == "new" else None,
        "old_line": line_number if line_type == "old" else None
    }
    
    # Remove None values
    position = {k: v for k, v in position.items() if v is not None}
    
    # Create the discussion with inline comment
    data = {
        "body": comment_text,
        "position": position
    }
    
    return await client.post(
        f"/projects/{project_id}/merge_requests/{mr_iid}/discussions",
        json_data=data
    )


async def test_inline_comment(
    project_id: str,
    mr_iid: str,
    file_path: Optional[str] = None,
    line_number: Optional[int] = None,
    comment_text: Optional[str] = None
):
    """Test creating an inline comment on a merge request."""
    
    config = GitLabConfig(
        base_url=os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4"),
        private_token=os.getenv("GITLAB_PRIVATE_TOKEN")
    )
    
    async with GitLabClient(config) as client:
        print(f"Testing inline comment on MR !{mr_iid} in project {project_id}")
        print("-" * 60)
        
        try:
            # First, get MR info
            mr_info = await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}")
            print(f"Merge Request: {mr_info['title']}")
            print(f"Author: {mr_info['author']['name']}")
            print(f"State: {mr_info['state']}")
            print()
            
            # Get diff information
            print("Fetching diff information...")
            diff_info = await get_merge_request_diff(client, project_id, mr_iid)
            
            if not diff_info or "diffs" not in diff_info:
                print("No diffs found in merge request")
                return
            
            diffs = diff_info["diffs"]
            print(f"Found {len(diffs)} changed files")
            
            # If no file specified, show available files
            if not file_path:
                print("\nChanged files:")
                for i, diff in enumerate(diffs):
                    print(f"  {i+1}. {diff['new_path']} (+{diff['added_lines']} -{diff['removed_lines']})")
                
                # Use the first file with changes as example
                if diffs:
                    file_path = diffs[0]["new_path"]
                    print(f"\nUsing first file for example: {file_path}")
            
            # Find the specified file in diffs
            file_diff = None
            for diff in diffs:
                if diff["new_path"] == file_path or diff["old_path"] == file_path:
                    file_diff = diff
                    break
            
            if not file_diff:
                print(f"File {file_path} not found in merge request diff")
                return
            
            print(f"\nFile: {file_path}")
            print(f"Changes: +{file_diff['added_lines']} -{file_diff['removed_lines']}")
            
            # If no line specified, find first added line
            if not line_number and file_diff.get("diff"):
                lines = file_diff["diff"].split('\n')
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
            
            if not line_number:
                print("Could not find a suitable line to comment on")
                return
            
            # Default comment text if not provided
            if not comment_text:
                comment_text = f"Test inline comment on line {line_number} of {file_path}"
            
            # Create the inline comment
            print(f"\nCreating inline comment on line {line_number}...")
            print(f"Comment: {comment_text}")
            
            result = await create_inline_comment(
                client=client,
                project_id=project_id,
                mr_iid=mr_iid,
                file_path=file_path,
                line_number=line_number,
                comment_text=comment_text,
                line_type="new"  # Commenting on added lines
            )
            
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
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Main function to run the test."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test inline comments on GitLab merge requests")
    parser.add_argument("project_id", help="Project ID (e.g., 85)")
    parser.add_argument("mr_iid", help="Merge request IID (e.g., 4328)")
    parser.add_argument("--file", "-f", help="File path to comment on")
    parser.add_argument("--line", "-l", type=int, help="Line number to comment on")
    parser.add_argument("--comment", "-c", help="Comment text", 
                       default="Test inline comment from MCP Extended GitLab")
    
    args = parser.parse_args()
    
    # Check for GitLab token
    if not os.getenv("GITLAB_PRIVATE_TOKEN"):
        print("Error: GITLAB_PRIVATE_TOKEN environment variable is required")
        print("Set it with: export GITLAB_PRIVATE_TOKEN='your-token'")
        sys.exit(1)
    
    await test_inline_comment(
        project_id=args.project_id,
        mr_iid=args.mr_iid,
        file_path=args.file,
        line_number=args.line,
        comment_text=args.comment
    )


if __name__ == "__main__":
    asyncio.run(main())