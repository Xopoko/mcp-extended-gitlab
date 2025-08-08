#!/usr/bin/env python3
"""Dump mapping of original (pre-normalized) tool names to standardized names.

Usage:
  python scripts/dump_tool_name_map.py          # Markdown table
  python scripts/dump_tool_name_map.py --json   # JSON output
"""

import argparse
import json
from typing import Dict


def load_mapping() -> Dict[str, str]:
    # Import server and access the FilteredMCP instance
    from mcp_extended_gitlab.server import mcp

    mapping: Dict[str, str] = {}
    # Underlying tools are in _mcp._tool_manager._tools as FunctionTool
    tm = getattr(mcp._mcp, "_tool_manager", None)
    tools = getattr(tm, "_tools", {}) if tm else {}

    for std_name, ft in tools.items():
        # FunctionTool holds the original Python function at .fn
        fn = getattr(ft, "fn", None)
        if fn is None:
            continue
        orig = getattr(fn, "_orig_name", None) or getattr(fn, "__name__", None)
        if not orig:
            continue
        mapping.setdefault(orig, std_name)

    # Also include explicit aliases defined by FilteredMCP (if any)
    aliases = getattr(mcp, "_aliases", {})
    for orig, std in aliases.items():
        mapping.setdefault(orig, std)

    return dict(sorted(mapping.items(), key=lambda kv: kv[0]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print JSON mapping")
    args = parser.parse_args()

    mapping = load_mapping()

    if args.json:
        print(json.dumps(mapping, indent=2, sort_keys=True))
        return

    # Markdown table
    print("| Original Name | Standardized Name |")
    print("|---|---|")
    for orig, std in mapping.items():
        print(f"| `{orig}` | `{std}` |")


if __name__ == "__main__":
    main()

