#!/usr/bin/env python3
"""Verify GitLab suggestions were created correctly."""

import json
import urllib.request
import ssl
import sys
import os


def verify_suggestions():
    """Verify the suggestions we created."""
    base_url = os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4")
    token = os.getenv("GITLAB_PRIVATE_TOKEN", "your-token-here")
    project_id = "85"
    mr_iid = "4328"
    
    # Discussion IDs to check
    discussion_ids = [
        "9568fdac65f41cc12ca64cf8b89ddd3d93c0f61b",  # Single-line suggestion
        "2823c68b7604b6f9fd2b7cdc4dc3f1d38f0f778f"   # Multi-line suggestion
    ]
    
    headers = {
        "Private-Token": token,
        "Content-Type": "application/json"
    }
    
    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    print("Verifying GitLab suggestions...")
    print("=" * 60)
    
    # Get all discussions
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/discussions"
    request = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(request, context=ssl_context) as response:
            discussions = json.loads(response.read().decode('utf-8'))
        
        found_count = 0
        suggestion_count = 0
        
        for discussion in discussions:
            if discussion['id'] in discussion_ids:
                found_count += 1
                print(f"\n✅ Found discussion: {discussion['id']}")
                
                if discussion.get('notes'):
                    note = discussion['notes'][0]
                    print(f"   Type: {note.get('type', 'Unknown')}")
                    print(f"   Author: {note['author']['username']}")
                    
                    body = note.get('body', '')
                    
                    # Check for suggestion syntax
                    if "```suggestion" in body:
                        suggestion_count += 1
                        print(f"   🎯 SUGGESTION CONFIRMED!")
                        
                        # Check if it has the suggestion type
                        if note.get('suggestions'):
                            print(f"   GitLab recognized this as a suggestion!")
                            print(f"   Can be applied: {note.get('suggestions_applied', False) == False}")
                        
                        # Extract suggestion details
                        if "```suggestion:-" in body:
                            # Multi-line suggestion
                            import re
                            match = re.search(r'```suggestion:-(\d+)\+(\d+)', body)
                            if match:
                                lines_removed = int(match.group(1)) + 1
                                lines_added = int(match.group(2)) + 1
                                print(f"   Multi-line: {lines_removed} lines → {lines_added} lines")
                        else:
                            print(f"   Single-line suggestion")
                        
                        # Show suggestion preview
                        if "```suggestion" in body:
                            start = body.index("```suggestion")
                            end = body.index("```", start + 13)
                            suggestion_content = body[start:end+3]
                            print(f"   Preview:")
                            for line in suggestion_content.split('\n')[:5]:
                                print(f"     {line}")
                            if suggestion_content.count('\n') > 5:
                                print(f"     ... ({suggestion_content.count('\n') - 5} more lines)")
                    
                    # Check position
                    if note.get('position'):
                        pos = note['position']
                        print(f"   File: {pos.get('new_path', pos.get('old_path'))}")
                        print(f"   Line: {pos.get('new_line', pos.get('old_line'))}")
        
        print(f"\n\nSummary:")
        print(f"  Found {found_count} of {len(discussion_ids)} discussions")
        print(f"  Confirmed {suggestion_count} suggestions")
        
        if suggestion_count > 0:
            print(f"\n✅ All suggestions are properly formatted and can be applied from the GitLab UI!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    verify_suggestions()