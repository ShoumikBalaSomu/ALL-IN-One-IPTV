#!/bin/bash
# ALL-IN-One-IPTV — Local Setup Script
# Run this to set up the project for local development

set -e

echo "🚀 ALL-IN-One-IPTV — Local Setup"
echo "=================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check Python
echo -e "\n${BLUE}[1/5] Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON${NC}"
else
    echo "✗ Python3 not found. Please install Python 3.10+ first."
    exit 1
fi

# Install engine dependencies
echo -e "\n${BLUE}[2/5] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt -q
pip3 install -r engine/requirements.txt -q
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Create directories
echo -e "\n${BLUE}[3/5] Creating directories...${NC}"
mkdir -p input output engine/input engine/output
echo -e "${GREEN}✓ Directories created${NC}"

# Check Node.js (for Electron player)
echo -e "\n${BLUE}[4/5] Checking Node.js (optional, for Electron player)...${NC}"
if command -v node &> /dev/null; then
    NODE=$(node --version)
    echo -e "${GREEN}✓ $NODE${NC}"
else
    echo "⚠ Node.js not found. Electron player won't work without it."
fi

# Check Flutter (for mobile player)
echo -e "\n${BLUE}[5/5] Checking Flutter (optional, for mobile player)...${NC}"
if command -v flutter &> /dev/null; then
    FLUTTER=$(flutter --version | head -1)
    echo -e "${GREEN}✓ $FLUTTER${NC}"
else
    echo "⚠ Flutter not found. Mobile player won't work without it."
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Quick commands:"
echo "  python3 aggregator.py              # Run aggregator"
echo "  python3 -m engine.src.main          # Run modular engine"
echo "  python3 -m engine.src.main --no-verify  # Skip verification (fast)"
echo ""
echo "Drop your custom playlists in: input/"
echo "Output will be in: output/"