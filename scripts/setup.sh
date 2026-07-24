#!/usr/bin/env bash
set -eo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Setting up development environment...${NC}"

# Python environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
if [ -f "engine/requirements.txt" ]; then
    pip install -r engine/requirements.txt
fi

# Create directories
echo "Creating necessary directories..."
mkdir -p input output logs docker scripts .github/workflows .github/pages app

echo -e "${GREEN}Setup complete!${NC}"
