#!/usr/bin/env python3
"""Simple script to verify multi-line comments"""

import os
import json
import requests
from datetime import datetime

# Get environment variables
token = os.environ.get('GITLAB_PRIVATE_TOKEN')
base_url = os.environ.get('GITLAB_BASE_URL', 'https://gitlab.com/api/v4')

if not token:
    print("ERROR: GITLAB_PRIVATE_TOKEN environment variable not set")
    print("\nTo verify the multi-line comments, you need to:")
    print("1. Set your GitLab token: export GITLAB_PRIVATE_TOKEN='your-token'")
    print("2. Run this script again: python3 verify_simple.py")
    exit(1)

# The discussion IDs from our creation
discussion_ids = [
    'af83ab7f6a1ce34e0761c199ef640032806ad693',
    '40966f07b8bb4dfd61eeb8b1454ec4296820ebcf'
]

print(f"Fetching discussions from merge request...")
print(f"Project: 63992990")
print(f"Merge Request: 1")
print(f"Looking for discussion IDs: {discussion_ids}")

# Fetch discussions
try:
    response = requests.get(
        f'{base_url}/projects/63992990/merge_requests/1/discussions',
        headers={'PRIVATE-TOKEN': token}
    )
    
    if response.status_code != 200:
        print(f"\nError {response.status_code}: {response.text}")
        exit(1)
    
    discussions = response.json()
    print(f"\nTotal discussions found: {len(discussions)}")
    
    # Find our multi-line comments
    found_count = 0
    for disc in discussions:
        disc_id = disc.get('id', '')
        if disc_id in discussion_ids:
            found_count += 1
            print(f"\n{'='*70}")
            print(f"✅ Found Discussion ID: {disc_id}")
            
            for note in disc.get('notes', []):
                created = note.get('created_at', '')
                if created:
                    # Parse and format the date
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    created_formatted = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                else:
                    created_formatted = 'Unknown'
                
                print(f"\nNote Details:")
                print(f"  Author: {note.get('author', {}).get('username', 'Unknown')}")
                print(f"  Created: {created_formatted}")
                print(f"  Body: {note.get('body', '')[:80]}...")
                
                pos = note.get('position', {})
                if pos:
                    line_range = pos.get('line_range')
                    if line_range:
                        print(f"\n  🎯 MULTI-LINE COMMENT CONFIRMED!")
                        start = line_range.get('start', {})
                        end = line_range.get('end', {})
                        
                        start_line = start.get('new_line', 'N/A')
                        end_line = end.get('new_line', 'N/A')
                        
                        print(f"  File: {pos.get('new_path', 'Unknown')}")
                        print(f"  Line Range: {start_line} to {end_line}")
                        
                        if isinstance(start_line, int) and isinstance(end_line, int):
                            lines_covered = end_line - start_line + 1
                            print(f"  Lines Covered: {lines_covered}")
                    else:
                        print(f"\n  ❌ This is a single-line comment")
                        print(f"  Line: {pos.get('new_line', 'N/A')}")
    
    print(f"\n{'='*70}")
    print(f"Summary: Found {found_count} of {len(discussion_ids)} expected multi-line discussions")
    
    if found_count < len(discussion_ids):
        print("\n⚠️  Some discussions were not found. They may have been deleted or the IDs are incorrect.")

except Exception as e:
    print(f"\nError occurred: {type(e).__name__}: {e}")
    print("\nPlease ensure:")
    print("1. Your GITLAB_PRIVATE_TOKEN has appropriate permissions")
    print("2. The project and merge request IDs are correct")
    print("3. You have access to the repository")