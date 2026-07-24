#!/usr/bin/env bash
# ALL-IN-One IPTV — Local Execution Script
set -eo pipefail

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}⚡ Running High-Performance Playlist Engine...${NC}"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup script..."
    ./scripts/setup.sh
fi

source venv/bin/activate
python3 -m engine.src.main "$@"

echo -e "${GREEN}🎉 Engine execution completed successfully! Check output/ directory.${NC}"
