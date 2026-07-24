#!/usr/bin/env bash
set -eo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    echo -e "${YELLOW}Usage: $0 -m \"Commit message\"${NC}"
    echo "Options:"
    echo "  -h, --help       Show this help message"
    echo "  -m, --message    Commit message (required)"
}

COMMIT_MSG=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage; exit 0 ;;
        -m|--message) COMMIT_MSG="$2"; shift ;;
        *) echo -e "${RED}Unknown parameter passed: $1${NC}"; usage; exit 1 ;;
    esac
    shift
done

if [ -z "$COMMIT_MSG" ]; then
    echo -e "${RED}Error: Commit message is required.${NC}"
    usage
    exit 1
fi

echo -e "${GREEN}Staging changes...${NC}"
git add .

echo -e "${GREEN}Committing changes...${NC}"
git commit -m "$COMMIT_MSG"

echo -e "${GREEN}Pushing to remote...${NC}"
git push origin HEAD

echo -e "${GREEN}Push completed successfully!${NC}"
