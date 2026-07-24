#!/usr/bin/env bash
set -eo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Setting up GitHub Actions...${NC}"

# Ensure we have git
if ! command -v git &> /dev/null; then
    echo "git could not be found. Please install git."
    exit 1
fi

# Make scripts executable
chmod +x scripts/*.sh build_local.sh gh_setup.sh

echo -e "${GREEN}GitHub setup complete! Workflows are ready to be triggered.${NC}"
