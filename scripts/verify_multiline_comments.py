#!/usr/bin/env python3
"""Verify that multi-line comments were created successfully"""

import asyncio
import os
import sys
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_extended_gitlab.api.core.merge_requests import get_gitlab_client


async def verify_multiline_comments():
    """Verify the multi-line comments we created"""
    client = await get_gitlab_client()
    
    # The discussion IDs from our creation
    discussion_ids = [
        'af83ab7f6a1ce34e0761c199ef640032806ad693',
        '40966f07b8bb4dfd61eeb8b1454ec4296820ebcf'
    ]
    
    # Get all discussions
    response = await client._make_request(
        'GET',
        '/projects/63992990/merge_requests/1/discussions'
    )
    
    if response.status_code != 200:
        print(f"Error fetching discussions: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    discussions = response.json()
    print(f"Total discussions found: {len(discussions)}")
    
    # Find our multi-line comments
    found_count = 0
    for disc in discussions:
        disc_id = disc.get('id', '')
        if disc_id in discussion_ids:
            found_count += 1
            print(f"\n{'='*70}")
            print(f"Discussion ID: {disc_id}")
            print(f"Individual Note: {disc.get('individual_note', False)}")
            
            for note in disc.get('notes', []):
                print(f"\nNote ID: {note.get('id')}")
                print(f"Author: {note.get('author', {}).get('username')}")
                print(f"Created: {note.get('created_at')}")
                print(f"Body preview: {note.get('body', '')[:100]}...")
                
                pos = note.get('position', {})
                if pos:
                    print(f"\nPosition Details:")
                    print(f"  Position Type: {pos.get('position_type')}")
                    print(f"  File Path: {pos.get('new_path')}")
                    
                    line_range = pos.get('line_range')
                    if line_range:
                        print(f"\n  ✅ MULTI-LINE COMMENT CONFIRMED!")
                        start = line_range.get('start', {})
                        end = line_range.get('end', {})
                        
                        print(f"\n  Line Range:")
                        print(f"    Start Line: {start.get('new_line')} (type: {start.get('type')})")
                        print(f"    End Line: {end.get('new_line')} (type: {end.get('type')})")
                        
                        lines_covered = (end.get('new_line', 0) - start.get('new_line', 0) + 1)
                        print(f"    Total Lines Covered: {lines_covered}")
                        
                        # Show line codes if available
                        if start.get('line_code'):
                            print(f"\n  Line Codes:")
                            print(f"    Start: {start.get('line_code')}")
                            print(f"    End: {end.get('line_code')}")
                    else:
                        print(f"\n  ❌ Single line comment")
                        print(f"  Line: {pos.get('new_line')}")
    
    print(f"\n\nSummary: Found {found_count} of {len(discussion_ids)} expected multi-line discussions")
    
    # Also check if we can fetch individual discussions
    print(f"\n{'='*70}")
    print("Attempting to fetch individual discussions:")
    
    for disc_id in discussion_ids:
        response = await client._make_request(
            'GET',
            f'/projects/63992990/merge_requests/1/discussions/{disc_id}'
        )
        if response.status_code == 200:
            print(f"\n✅ Successfully fetched discussion {disc_id}")
            disc = response.json()
            if 'notes' in disc and len(disc['notes']) > 0:
                note = disc['notes'][0]
                if 'position' in note and 'line_range' in note['position']:
                    line_range = note['position']['line_range']
                    start_line = line_range['start']['new_line']
                    end_line = line_range['end']['new_line']
                    print(f"   Multi-line range: {start_line} to {end_line}")
        else:
            print(f"\n❌ Failed to fetch discussion {disc_id}: {response.status_code}")


if __name__ == "__main__":
    asyncio.run(verify_multiline_comments())