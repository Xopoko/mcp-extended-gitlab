#!/usr/bin/env python3
"""Verify multi-line inline comments."""

import json
import urllib.request
import ssl
import sys
import os


def verify_multiline_comments():
    """Verify the multi-line comments we created."""
    base_url = os.getenv("GITLAB_BASE_URL", "https://gitlab.com/api/v4")
    token = os.getenv("GITLAB_PRIVATE_TOKEN", "your-token-here")
    project_id = "85"
    mr_iid = "4328"
    
    # Discussion IDs to check
    discussion_ids = [
        "af83ab7f6a1ce34e0761c199ef640032806ad693",
        "40966f07b8bb4dfd61eeb8b1454ec4296820ebcf"
    ]
    
    headers = {
        "Private-Token": token,
        "Content-Type": "application/json"
    }
    
    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    print("Verifying multi-line inline comments...")
    print("=" * 60)
    
    # Get all discussions
    url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/discussions"
    request = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(request, context=ssl_context) as response:
            discussions = json.loads(response.read().decode('utf-8'))
        
        found_count = 0
        for discussion in discussions:
            if discussion['id'] in discussion_ids:
                found_count += 1
                print(f"\n✅ Found discussion: {discussion['id']}")
                
                if discussion.get('notes'):
                    note = discussion['notes'][0]
                    print(f"   Type: {note.get('type', 'Unknown')}")
                    print(f"   Author: {note['author']['username']}")
                    
                    if note.get('position'):
                        pos = note['position']
                        print(f"   File: {pos.get('new_path', pos.get('old_path'))}")
                        
                        # Check for line_range - the key indicator of multi-line comment
                        if pos.get('line_range'):
                            lr = pos['line_range']
                            start = lr.get('start', {})
                            end = lr.get('end', {})
                            start_line = start.get('new_line', start.get('old_line'))
                            end_line = end.get('new_line', end.get('old_line'))
                            
                            print(f"   🎯 MULTI-LINE COMMENT CONFIRMED!")
                            print(f"   Line range: {start_line} to {end_line}")
                            print(f"   Total lines: {end_line - start_line + 1}")
                        else:
                            print(f"   Single line: {pos.get('new_line', pos.get('old_line'))}")
        
        print(f"\n\nSummary: Found {found_count} of {len(discussion_ids)} discussions")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    verify_multiline_comments()