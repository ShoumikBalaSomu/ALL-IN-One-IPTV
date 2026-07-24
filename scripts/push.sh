#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: $0 <commit-message>"
    exit 1
fi

echo -e "${GREEN}Formatting and linting...${NC}"
# Add linting commands here if applicable

echo -e "${GREEN}Committing and pushing to GitHub...${NC}"
git add .
git commit -m "$1"
git push

echo -e "${GREEN}Successfully pushed!${NC}"
