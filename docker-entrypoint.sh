#!/bin/bash
set -e

# Check if required environment variables are set
if [ -z "$GITLAB_PRIVATE_TOKEN" ]; then
    echo "Error: GITLAB_PRIVATE_TOKEN environment variable is not set"
    echo "Please set it using: export GITLAB_PRIVATE_TOKEN=your-token"
    exit 1
fi

# Optional: Wait for dependencies if needed
# sleep 5

echo "Starting MCP Extended GitLab server..."
echo "GitLab URL: ${GITLAB_BASE_URL:-https://gitlab.com/api/v4}"

# Execute the main command
exec "$@"