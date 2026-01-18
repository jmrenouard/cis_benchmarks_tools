#!/bin/bash
#
# CIS Benchmarks Audit - Wrapper Script
# 
# This script provides convenient shortcuts for running CIS audits
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_SCRIPT="${SCRIPT_DIR}/cis_audit.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if dependencies are installed
check_dependencies() {
    python3 -c "import yaml" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Installing dependencies...${NC}"
        
        # Check if we're in a virtual environment
        if [ -n "$VIRTUAL_ENV" ]; then
            pip install -r "${SCRIPT_DIR}/requirements.txt" || {
                echo -e "${RED}Failed to install dependencies${NC}"
                exit 1
            }
        else
            pip install --user -r "${SCRIPT_DIR}/requirements.txt" || {
                echo -e "${RED}Failed to install dependencies${NC}"
                echo -e "${YELLOW}Tip: Consider using a virtual environment${NC}"
                exit 1
            }
        fi
    fi
}

# Show usage
usage() {
    echo "CIS Benchmarks Audit Tool - Wrapper Script"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  quick               Run quick audit with default checks (HTML report)"
    echo "  full                Run comprehensive audit with all checks"
    echo "  minimal             Run minimal audit with basic checks"
    echo "  custom <config>     Run audit with custom config file"
    echo "  help                Show this help message"
    echo ""
    echo "Options (for custom command):"
    echo "  -f, --format        Report format: json, html, or text (default: html)"
    echo "  -o, --output        Output filename (without extension)"
    echo ""
    echo "Examples:"
    echo "  $0 quick"
    echo "  $0 full"
    echo "  $0 custom my_config.yaml -f json -o my_report"
    echo ""
}

# Main execution
case "$1" in
    quick)
        echo -e "${GREEN}Running quick CIS audit...${NC}"
        check_dependencies
        python3 "$AUDIT_SCRIPT" --use-defaults -f html -o "cis_quick_audit_$(date +%Y%m%d_%H%M%S)"
        ;;
    
    full)
        echo -e "${GREEN}Running comprehensive CIS audit...${NC}"
        check_dependencies
        if [ -f "${SCRIPT_DIR}/config/default_checks.yaml" ]; then
            python3 "$AUDIT_SCRIPT" -c "${SCRIPT_DIR}/config/default_checks.yaml" \
                -f html -o "cis_full_audit_$(date +%Y%m%d_%H%M%S)"
        else
            echo -e "${YELLOW}Config file not found, using defaults...${NC}"
            python3 "$AUDIT_SCRIPT" --use-defaults -f html -o "cis_full_audit_$(date +%Y%m%d_%H%M%S)"
        fi
        ;;
    
    minimal)
        echo -e "${GREEN}Running minimal CIS audit...${NC}"
        check_dependencies
        if [ -f "${SCRIPT_DIR}/config/minimal_checks.yaml" ]; then
            python3 "$AUDIT_SCRIPT" -c "${SCRIPT_DIR}/config/minimal_checks.yaml" \
                -f html -o "cis_minimal_audit_$(date +%Y%m%d_%H%M%S)"
        else
            echo -e "${RED}Minimal config file not found${NC}"
            exit 1
        fi
        ;;
    
    custom)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Config file required for custom audit${NC}"
            usage
            exit 1
        fi
        
        CONFIG_FILE="$2"
        shift 2
        
        if [ ! -f "$CONFIG_FILE" ]; then
            echo -e "${RED}Error: Config file not found: $CONFIG_FILE${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}Running custom CIS audit with $CONFIG_FILE...${NC}"
        check_dependencies
        python3 "$AUDIT_SCRIPT" -c "$CONFIG_FILE" "$@"
        ;;
    
    help|--help|-h)
        usage
        ;;
    
    *)
        echo -e "${RED}Invalid command: $1${NC}"
        echo ""
        usage
        exit 1
        ;;
esac

exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}Audit completed successfully!${NC}"
else
    echo -e "${YELLOW}Audit completed with failures. Review the report for details.${NC}"
fi

exit $exit_code
