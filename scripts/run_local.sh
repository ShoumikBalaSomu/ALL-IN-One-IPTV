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
    echo "  -d, --detached   Run in detached mode"
}

DETACHED=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage; exit 0 ;;
        -d|--detached) DETACHED=true ;;
        *) echo -e "${RED}Unknown parameter passed: $1${NC}"; usage; exit 1 ;;
    esac
    shift
done

echo -e "${GREEN}Starting local environment with Docker Compose...${NC}"

cd "$(dirname "$0")/../docker"

if [ "$DETACHED" = true ]; then
    docker-compose up -d
    echo -e "${GREEN}Started in detached mode.${NC}"
else
    docker-compose up
fi
