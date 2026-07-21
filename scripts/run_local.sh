#!/bin/bash
# ALL-IN-One-IPTV — Run Locally
# Run the full aggregation pipeline locally

set -e

echo "📡 ALL-IN-One-IPTV — Running Pipeline"
echo "======================================"

# Run the modular engine
cd "$(dirname "$0")/.."

if [ "$1" == "--fast" ]; then
    echo "⚡ Fast mode (no link verification)..."
    python3 -m engine.src.main --no-verify "$@"
else
    echo "🔍 Full mode (with link verification)..."
    python3 -m engine.src.main "$@"
fi

echo ""
echo "📁 Output files:"
ls -lh output/*.m3u 2>/dev/null || echo "No output files found."

echo ""
echo "🌐 Preview (first 10 channels):"
head -30 output/combined_by_country.m3u 2>/dev/null || echo "No combined playlist found."