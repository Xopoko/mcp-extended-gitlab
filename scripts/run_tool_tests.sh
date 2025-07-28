#!/bin/bash
# Helper script to run GitLab API tool tests with common scenarios

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if GITLAB_PRIVATE_TOKEN is set
if [ -z "$GITLAB_PRIVATE_TOKEN" ]; then
    echo -e "${RED}Error: GITLAB_PRIVATE_TOKEN environment variable is not set${NC}"
    echo "Please set it with: export GITLAB_PRIVATE_TOKEN='your-token'"
    exit 1
fi

# Default values
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_SCRIPT="$SCRIPT_DIR/test_all_tools.py"
CONFIG_FILE="$SCRIPT_DIR/test_config.json"

# Function to show usage
show_usage() {
    echo "Usage: $0 [scenario|options]"
    echo ""
    echo "Scenarios:"
    echo "  quick          - Run quick smoke test with minimal tools"
    echo "  core           - Test core GitLab features"
    echo "  ci_cd          - Test CI/CD related tools"
    echo "  read_only      - Test only read operations (safe)"
    echo "  all            - Test all tools"
    echo ""
    echo "Options:"
    echo "  --tools        - Test specific tools (comma-separated)"
    echo "  --category     - Test specific category"
    echo "  --preset       - Use tool preset (minimal, core, ci_cd, devops, admin)"
    echo "  --project ID   - Set test project ID"
    echo "  --group ID     - Set test group ID"
    echo "  --json         - Output JSON report"
    echo "  --markdown     - Output Markdown report"
    echo "  --save FILE    - Save report to file"
    echo ""
    echo "Examples:"
    echo "  $0 quick"
    echo "  $0 --tools list_projects,get_project"
    echo "  $0 --category core --json --save report.json"
    echo "  $0 read_only --project 12345"
}

# Parse command line arguments
SCENARIO=""
EXTRA_ARGS=""

case "$1" in
    quick)
        echo -e "${GREEN}Running quick smoke test...${NC}"
        python "$TEST_SCRIPT" --preset minimal --stop-on-error --verbose
        ;;
    core)
        echo -e "${GREEN}Testing core GitLab features...${NC}"
        python "$TEST_SCRIPT" --category core --verbose
        ;;
    ci_cd)
        echo -e "${GREEN}Testing CI/CD tools...${NC}"
        python "$TEST_SCRIPT" --category ci_cd --verbose
        ;;
    read_only)
        echo -e "${GREEN}Testing read-only operations...${NC}"
        # Extract read-only tools from config
        TOOLS=$(python -c "
import json
with open('$CONFIG_FILE') as f:
    config = json.load(f)
    print(','.join(config['test_scenarios']['read_only']['tools']))
")
        python "$TEST_SCRIPT" $(echo $TOOLS | sed 's/,/ -t /g' | sed 's/^/-t /') --verbose
        ;;
    all)
        echo -e "${YELLOW}Testing ALL tools (this may take a while)...${NC}"
        python "$TEST_SCRIPT" --verbose
        ;;
    --tools)
        shift
        TOOLS=$(echo $1 | sed 's/,/ -t /g' | sed 's/^/-t /')
        python "$TEST_SCRIPT" $TOOLS "${@:2}"
        ;;
    --category)
        shift
        python "$TEST_SCRIPT" --category "$@"
        ;;
    --preset)
        shift
        python "$TEST_SCRIPT" --preset "$@"
        ;;
    --project)
        shift
        export GITLAB_TEST_PROJECT_ID="$1"
        shift
        python "$TEST_SCRIPT" "$@"
        ;;
    --group)
        shift
        export GITLAB_TEST_GROUP_ID="$1"
        shift
        python "$TEST_SCRIPT" "$@"
        ;;
    --json)
        shift
        python "$TEST_SCRIPT" --format json "$@"
        ;;
    --markdown)
        shift
        python "$TEST_SCRIPT" --format markdown "$@"
        ;;
    --save)
        shift
        OUTPUT_FILE="$1"
        shift
        python "$TEST_SCRIPT" --output "$OUTPUT_FILE" "$@"
        ;;
    -h|--help|"")
        show_usage
        exit 0
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_usage
        exit 1
        ;;
esac