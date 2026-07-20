#!/bin/bash
echo "Starting local builds for ALL-IN-One-IPTV..."

echo "[1/2] Building Flutter Player App..."
cd app_player
flutter pub get
flutter build apk --release
cd ..
echo "Player APK built at: app_player/build/app/outputs/flutter-apk/app-release.apk"

echo "[2/2] Building Kotlin Proxy App..."
cd app_proxy
chmod +x gradlew
./gradlew assembleRelease
cd ..
echo "Proxy APK built at: app_proxy/app/build/outputs/apk/release/app-release.apk"

echo "Done! Both APKs are ready for deployment."
