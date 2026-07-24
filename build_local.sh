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
    echo "  -c, --clean      Clean before building"
    echo "  -t, --test       Run tests before building"
}

CLEAN=false
RUN_TESTS=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage; exit 0 ;;
        -c|--clean) CLEAN=true ;;
        -t|--test) RUN_TESTS=true ;;
        *) echo -e "${RED}Unknown parameter passed: $1${NC}"; usage; exit 1 ;;
    esac
    shift
done

echo -e "${GREEN}Starting local build process...${NC}"

if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}Cleaning output directories...${NC}"
    rm -rf output/
    mkdir -p output/
fi

if [ "$RUN_TESTS" = true ]; then
    echo -e "${YELLOW}Running tests...${NC}"
    python -m unittest discover -s engine
fi

echo -e "${GREEN}Building Docker images...${NC}"
docker build -t iptv-engine:latest -f docker/Dockerfile .
docker build -t iptv-transcoder:latest -f docker/Dockerfile.transcoder .

echo -e "${GREEN}Build completed successfully!${NC}"
