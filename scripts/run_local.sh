#!/usr/bin/env bash
set -eo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Running engine locally...${NC}"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup.sh first..."
    ./scripts/setup.sh
fi

source venv/bin/activate
python -m engine.src

echo -e "${GREEN}Engine execution completed!${NC}"
