#!/usr/bin/env python
"""Test runner script for MCP Extended GitLab."""

import sys
import subprocess
from pathlib import Path


def run_tests():
    """Run the test suite with various options."""
    
    # Default test command
    cmd = ["pytest"]
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "unit":
            # Run only unit tests
            cmd.extend(["-m", "unit"])
        elif sys.argv[1] == "integration":
            # Run only integration tests  
            cmd.extend(["-m", "integration"])
        elif sys.argv[1] == "openapi":
            # Run only OpenAPI compliance tests
            cmd.extend(["-m", "openapi", "tests/test_openapi_compliance.py"])
        elif sys.argv[1] == "coverage":
            # Run with coverage report
            cmd.extend(["--cov-report=html", "--open-cov"])
        elif sys.argv[1] == "fast":
            # Run without slow tests
            cmd.extend(["-m", "not slow"])
        elif sys.argv[1] == "specific":
            # Run specific test file
            if len(sys.argv) > 2:
                cmd.append(f"tests/{sys.argv[2]}")
            else:
                print("Please specify a test file")
                return 1
        else:
            # Pass through any other arguments
            cmd.extend(sys.argv[1:])
    
    # Add color output
    cmd.append("--color=yes")
    
    # Run the tests
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())