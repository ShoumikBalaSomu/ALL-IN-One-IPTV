# 📜 CHANGELOG — ALL-IN-One IPTV Monorepo

All notable changes to this project are documented in this file.

---

## [v2.1.0] — 2026-07-24 (AGI-Era Ecosystem Milestone)

### 🚀 Added
- **500-Worker Engine Verifier & Host Circuit Breaker**: Slashing stream health check execution time from 45+ minutes to under 90 seconds.
- **Smart Channel Merger & Latency Ranker**: Auto-folds duplicate channels into single M3U entries with latency-ranked fallback stream mirrors (`#EXTVLCOPT:fallback=...`).
- **AGI-Era Cyber Canvas Portal**: Web Player featuring interactive 60-node particle canvas matrix animation, Orbitron sci-fi typography, and HUD stream health telemetry.
- **Acestream / Magnet P2P Bridge**: Converts `acestream://` and `magnet:?xt=urn:btih:` links into local proxy streams (`http://127.0.0.1:8080/p2p/{infohash}`).
- **Xtream Codes API & Server Emulation**: Connects to Xtream Code portals and emulates `/player_api.php` locally for third-party player login.
- **Stream Quality Classifier**: Auto-detects and tags resolution (`4K`, `FHD 1080p`, `HD 720p`, `SD`, `60FPS`).
- **Parental Controls & System PIN (`0171`)**: Integrated adult channel classification and PIN authorization modal.
- **Custom 3D Glass Prism App Launcher Icons**: Replaced default launcher icons across `mipmap` density suites (`mdpi`, `hdpi`, `xhdpi`, `xxhdpi`, `xxxhdpi`).

### ⚡ Performance & Optimization
- Concurrency control added to `.github/workflows/update.yml` with `cancel-in-progress: true` and strict `timeout-minutes: 15`.
- Purged 37 redundant legacy files to unify monorepo layout around `apps/` and `engine/`.
- 100% unit test pass rate across 21 test cases.

---

## [v2.0.0] — 2026-07-20 (Phase 2 Monorepo Overhaul)

### 🚀 Added
- Flutter Cross-Platform Media Player (`apps/app_player`) with Glassmorphism navigation shell, EPG TV guide, and Netflix VOD grid.
- Native Android Proxy application (`apps/app_proxy`) with Foreground Service hosting Ktor Netty server.