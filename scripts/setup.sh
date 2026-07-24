#!/usr/bin/env bash
# ALL-IN-One IPTV — Environment Setup Script
set -eo pipefail

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🚀 Setting up ALL-IN-One IPTV Development Environment...${NC}"

# Python environment
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
if [ -f "engine/requirements.txt" ]; then
    echo -e "${GREEN}Installing engine requirements...${NC}"
    pip install -r engine/requirements.txt
fi

# Create directories
echo -e "${GREEN}Creating directory structure...${NC}"
mkdir -p input output logs docker scripts apps/app_player apps/app_proxy .github/workflows .github/pages docs/assets

echo -e "${CYAN}✅ Setup complete! Virtual environment activated.${NC}"
