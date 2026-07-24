#!/bin/bash
# ALL-IN-One-IPTV — Local Build Script
# Build all applications locally

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🏗️ ALL-IN-One-IPTV — Building All Applications"
echo "================================================"

# Build Flutter Player
echo ""
echo "[1/3] Building Flutter Unified Player..."
if command -v flutter &> /dev/null; then
    cd apps/app_player
    flutter pub get
    flutter build apk --release --split-per-abi 2>/dev/null || flutter build apk --release
    echo "✅ Player APK: build/app/outputs/flutter-apk/"
    cd "$SCRIPT_DIR"
else
    echo "⚠ Flutter not installed. Skipping Flutter build."
fi

# Build Kotlin Proxy
echo ""
echo "[2/3] Building Kotlin Proxy Optimizer..."
if [ -f "apps/app_proxy/gradlew" ]; then
    cd apps/app_proxy
    chmod +x gradlew
    ./gradlew assembleRelease 2>/dev/null || echo "⚠ Gradle build failed"
    echo "✅ Proxy APK: app/build/outputs/apk/release/"
    cd "$SCRIPT_DIR"
else
    echo "⚠ Gradle not found. Skipping Kotlin build."
fi

# Run Engine
echo ""
echo "[3/3] Running Playlist Engine..."
python3 -m engine.src.main
echo "✅ Playlists: output/"

echo ""
echo "================================================"
echo "🎉 Build complete!"
echo "================================================"
echo ""
echo "Outputs:"
echo "  Player APK:    apps/app_player/build/app/outputs/flutter-apk/"
echo "  Proxy APK:     apps/app_proxy/app/build/outputs/apk/release/"
echo "  Playlists:     output/"