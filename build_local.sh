#!/usr/bin/env bash
set -eo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Building all components locally...${NC}"

if [ ! -d "engine" ]; then
    echo -e "${RED}Error: engine directory not found. Must be run from project root.${NC}"
    exit 1
fi

echo "Building Docker image..."
docker build -t iptv-engine:latest -f docker/Dockerfile .

echo "Building Flutter apps..."
if command -v flutter >/dev/null 2>&1; then
    cd app || { echo -e "${RED}app directory not found${NC}"; exit 1; }
    flutter build linux
    flutter build apk
    cd ..
else
    echo -e "${RED}Flutter not installed. Skipping app build.${NC}"
fi

echo -e "${GREEN}Build complete!${NC}"
