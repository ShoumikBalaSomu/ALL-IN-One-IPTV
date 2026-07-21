# 📋 Changelog

All notable changes to the **ALL-IN-One-IPTV** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### 🎯 Planned
- **Torrent IPTV (P2P WebRTC)** — Zero-buffering P2P streaming
- **AI-powered channel categorization** — Auto-classify using ML
- **Adaptive bitrate selection** — Quality based on bandwidth
- **Multi-language EPG** — Extended TV guide with search
- **Cast support** — Chromecast, DLNA, AirPlay
- **Stream recording** — Record live TV
- **Web-based player** — Browser-native player
- **iOS app** — Swift/SwiftUI native player
- **Docker self-host** — Deploy your own engine

---

## [1.0.0] - 2026-07-21

### 🚀 Released

#### Aggregator Engine
- ✅ Async Python aggregator with 60+ playlist sources
- ✅ M3U parser with full cookie & HTTP header support
- ✅ Smart deduplication (URL-based + channel-name-based)
- ✅ Country-based grouping with auto-detection
- ✅ Channel folding (merge duplicates, keep all working URLs)
- ✅ Parallel link health verification (50 concurrent checks)
- ✅ Host-level health checking (if one URL from host works, all do)
- ✅ Local playlist input support (`input/` folder)
- ✅ Encrypted playlist support (AES-256-GCM)

#### Flutter Unified Player
- ✅ Cross-platform player (Android, Windows, Linux, macOS)
- ✅ Netflix-style Cinema VOD mode
- ✅ OTT Navigator-style Live TV with EPG
- ✅ Multiple input sources (M3U URL, Xtream Codes, MAC portal)
- ✅ libVLC-backed playback via media_kit
- ✅ Isar local database for favorites/settings
- ✅ Riverpod state management
- ✅ Glassmorphism UI with particle animations
- ✅ Picture-in-Picture mode
- ✅ Parental controls with PIN
- ✅ Channel favorites system

#### Kotlin Proxy Optimizer
- ✅ Jetpack Compose UI with cyberpunk dashboard
- ✅ Background proxy service
- ✅ Real-time stream interception & fallback routing
- ✅ Live bandwidth monitoring
- ✅ Canvas-drawn reactor animations
- ✅ Proxy & VPN support

#### Web Player
- ✅ Full web-based player (docs/)
- ✅ HLS.js streaming support
- ✅ 4-view architecture: Splash, Live TV, VOD Cinema, Proxy Dashboard
- ✅ Custom video controls
- ✅ Particle background animation
- ✅ Responsive design

#### Backend Services
- ✅ Async scraper (`services/backend/scraper.py`)
- ✅ EPG matcher with fuzzy string matching
- ✅ Token vault for DRM descrambling (JioTV plugin)
- ✅ Stream healer — auto-discover fallback URLs via GitHub search
- ✅ FFmpeg transcoder API (NVENC GPU-accelerated)
- ✅ IPFS publisher for decentralized playlist hosting
- ✅ Google Colab AES-256-GCM encryptor

#### DevOps & CI/CD
- ✅ Auto-update playlists daily via GitHub Actions
- ✅ Multi-platform APK/EXE build & release workflow
- ✅ GitHub Pages deployment
- ✅ Docker Compose for transcoder farm
- ✅ Comprehensive `.gitignore`

#### Documentation
- ✅ Complete README with architecture diagrams
- ✅ Detailed ABOUT.md with vision & philosophy
- ✅ Full legal disclaimer (LEGAL.md)
- ✅ Security guidelines (SECURITY.md)
- ✅ MIT License
- ✅ Credits to all playlist maintainers (CREDITS.md)
- ✅ Contributing guidelines (CONTRIBUTING.md)

---

## [0.2.0] - 2026-07-15

### Added
- Favorites and Parental Controls to Android App
- Favorites, PiP, and Parental Controls to Web Player
- GitHub Action to build APKs and update README with Download buttons
- Massive SPA update bridging Flutter and Compose UIs to Web Player
- Functional Web Player deployed to docs folder

---

## [0.1.0] - 2026-07-10

### Initial Development
- Repository reorganization into logical folders (apps, services, docker)
- Core aggregator implementation
- Initial Flutter player scaffolding
- Initial Kotlin proxy app scaffolding
- Basic CI/CD workflows
- Docker configuration
- Core documentation

---

## Version Numbering Scheme

| Part | Description | Example |
|------|-------------|---------|
| **MAJOR** | Breaking changes, major new features | `2.0.0` |
| **MINOR** | New features (backward compatible) | `1.1.0` |
| **PATCH** | Bug fixes, improvements | `1.0.1` |

---

<div align="center">

**Full commit history:** [GitHub Commits](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/commits/main)

</div>