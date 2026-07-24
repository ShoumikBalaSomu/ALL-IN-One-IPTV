#!/usr/bin/env bash
set -eo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    echo -e "${YELLOW}Usage: $0 [options]${NC}"
    echo "Options:"
    echo "  -h, --help       Show this help message"
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage; exit 0 ;;
        *) echo -e "${RED}Unknown parameter passed: $1${NC}"; usage; exit 1 ;;
    esac
    shift
done

echo -e "${GREEN}Setting up GitHub CLI and Secrets...${NC}"

if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI (gh) is not installed. Please install it first.${NC}"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}Not authenticated. Please run 'gh auth login'.${NC}"
    exit 1
fi

echo -e "${GREEN}Configuring repository settings...${NC}"
gh repo edit --enable-pages

echo -e "${GREEN}Setup complete!${NC}"
