#!/usr/bin/env python3
"""Test inline comment creation using MCP tools directly."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.test_all_tools import ToolTester


async def test_mr_inline_comment(project_id: str = "85", mr_iid: str = "4328"):
    """Test creating inline comment on merge request using MCP tools."""
    
    print(f"Testing inline comment on MR !{mr_iid} in project {project_id}")
    print("=" * 60)
    
    async with ToolTester() as tester:
        # Get all tools
        all_tools = tester.get_all_tools()
        
        # First, get MR diff to find files and lines
        print("\n1. Getting merge request diff...")
        
        # We'll need to use the GitLab client directly for getting diffs
        # since there might not be a specific MCP tool for it
        client = tester.client
        
        try:
            # Get MR info
            mr_info = await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}")
            print(f"   MR Title: {mr_info['title']}")
            print(f"   Author: {mr_info['author']['name']}")
            
            # Get diffs
            diff_info = await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}/diffs")
            diffs = diff_info.get("diffs", [])
            
            if not diffs:
                print("   No diffs found!")
                return
            
            print(f"   Found {len(diffs)} changed files")
            
            # Pick the first file with additions
            target_file = None
            target_line = None
            
            for diff in diffs:
                if diff.get("added_lines", 0) > 0:
                    target_file = diff["new_path"]
                    
                    # Parse diff to find first added line
                    if diff.get("diff"):
                        lines = diff["diff"].split('\n')
                        current_line = 0
                        
                        for line in lines:
                            if line.startswith("@@"):
                                # Extract line number from diff header
                                import re
                                match = re.search(r'\+(\d+)', line)
                                if match:
                                    current_line = int(match.group(1)) - 1
                            elif line.startswith("+") and not line.startswith("+++"):
                                current_line += 1
                                target_line = current_line
                                print(f"\n   Target file: {target_file}")
                                print(f"   Target line: {target_line}")
                                print(f"   Line content: {line[1:].strip()[:60]}...")
                                break
                            elif not line.startswith("-"):
                                current_line += 1
                        
                        if target_line:
                            break
            
            if not target_file or not target_line:
                print("   Could not find suitable file/line for comment")
                return
            
            # Get MR versions for SHA information
            print("\n2. Getting merge request versions for SHA info...")
            versions = await client.get(f"/projects/{project_id}/merge_requests/{mr_iid}/versions")
            
            if not versions or len(versions) == 0:
                print("   No versions found!")
                return
            
            latest_version = versions[0]
            base_sha = latest_version.get("base_commit_sha")
            start_sha = latest_version.get("start_commit_sha") 
            head_sha = latest_version.get("head_commit_sha")
            
            print(f"   Base SHA: {base_sha[:8]}...")
            print(f"   Head SHA: {head_sha[:8]}...")
            
            # Construct position object
            position = {
                "base_sha": base_sha,
                "start_sha": start_sha,
                "head_sha": head_sha,
                "position_type": "text",
                "new_path": target_file,
                "new_line": target_line
            }
            
            position_json = json.dumps(position)
            
            # Now use the MCP tool to create inline comment
            print("\n3. Creating inline comment using MCP tool...")
            
            if "create_new_merge_request_thread" in all_tools:
                tool_info = all_tools["create_new_merge_request_thread"]
                
                # Prepare parameters
                params = {
                    "project_id": project_id,
                    "merge_request_iid": mr_iid,
                    "body": f"Test inline comment on line {target_line} - Created via MCP Extended GitLab",
                    "position": position_json
                }
                
                print(f"   Parameters: {json.dumps(params, indent=2)}")
                
                # Call the tool
                result = await tool_info["function"](**params)
                
                print("\n✅ Successfully created inline comment!")
                print(f"   Discussion ID: {result['id']}")
                
                if result.get("notes") and len(result["notes"]) > 0:
                    note = result["notes"][0]
                    print(f"   Comment ID: {note['id']}")
                    print(f"   Author: {note['author']['name']}")
                    
                    if note.get("position"):
                        pos = note["position"]
                        print(f"   Position confirmed: Line {pos.get('new_line')} in {pos.get('new_path')}")
            else:
                print("   ERROR: create_new_merge_request_thread tool not found!")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MCP tool for inline MR comments")
    parser.add_argument("--project", "-p", default="85", help="Project ID (default: 85)")
    parser.add_argument("--mr", "-m", default="4328", help="Merge request IID (default: 4328)")
    
    args = parser.parse_args()
    
    # Check for GitLab token
    if not os.getenv("GITLAB_PRIVATE_TOKEN"):
        print("Error: GITLAB_PRIVATE_TOKEN environment variable is required")
        sys.exit(1)
    
    await test_mr_inline_comment(args.project, args.mr)


if __name__ == "__main__":
    asyncio.run(main())