# ALL-IN-One-IPTV: Optimizer & Player Ecosystem 🚀

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Build Status](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/actions/workflows/update.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Android-lightgrey)

Welcome to the **ALL-IN-One-IPTV** ecosystem—an advanced, automated pipeline for aggregating, optimizing, and flawlessly streaming free, publicly available IPTV channels. 

This project aims to solve the biggest pain points in IPTV streaming: dead links, endless buffering, and terrible UI/UX. By combining a highly concurrent automated backend, a dynamic local proxy engine, and a premium "Two-Faced" cross-platform player, we've created the ultimate zero-buffer entertainment experience.

---

## 🌟 Ecosystem Features

### 1. Automated Playlist Aggregator (The Backend)
Powered by GitHub Actions, our Python backend runs asynchronously every 6 hours to fetch over 70+ public M3U sources. It automatically:
*   **Deduplicates & Folds:** Groups identical channels from different sources into a single logical channel with multiple fallback URLs.
*   **Health Checks:** Aggressively pings the underlying hosts in real-time, instantly discarding dead streams and preventing IP bans via intelligent rate-limiting.
*   **Generates Optimized Output:** Outputs a pristine, highly available `checked_combined_by_country.m3u` containing only live streams.

### 2. Ultimate Cross-Platform Player (Phase 2)
Built with **Flutter** and powered by **media_kit** (libVLC/FFmpeg), ensuring flawless hardware-accelerated video decoding across Windows, Linux, and Android.
*   **"Two-Faced" UI:** Automatically shifts between a cinematic "Netflix-style" UI for VOD (Movies & Series) and a lightning-fast "OTT Navigator-style" UI for Live TV.
*   **Smart Fallback Engine:** If a stream dies mid-broadcast, the player instantly and transparently switches to the next folded fallback URL—without closing your video.

### 3. Playlist Optimizer Local Proxy (Phase 3)
A native Android background service (Ktor Server) that intercepts your streams before they hit your player.
*   **Zero-Buffer Routing:** Concurrently pings all available fallback URLs for a channel when you press "Play" and instantly redirects (HTTP 302) to the fastest active server.
*   **OpenVPN Split Tunneling:** Route geographically locked streams through a VPN while keeping local, high-speed streams (like BDIX) on your direct network.

---

## 🛠️ Quick Start & Local Testing

Want to contribute or test the ecosystem locally before pushing? Here's how to spin it up.

### Prerequisites
*   Python 3.11+
*   Flutter SDK (3.22+)
*   Android Studio (for building the Proxy App)

### 1. Run the Backend Aggregator (Python)
```bash
git clone https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV.git
cd ALL-IN-One-IPTV
pip install aiohttp
python scraper.py
python folder.py
python checker.py
# The optimized playlist will be available in output/checked_combined_by_country.m3u
```

### 2. Run the Cross-Platform Player (Flutter)
```bash
cd player/
flutter pub get
dart run build_runner build  # Generate local Isar database bindings
flutter run -d linux         # Change 'linux' to 'windows' or your connected Android device
```

### 3. Run the Local Proxy (Android)
Open the `/proxy_app` directory in Android Studio. Sync the Gradle files, select your emulator or physical device, and press Run.

---

## 🛡️ Security & UX Best Practices
*   **Absolute Privacy:** This ecosystem contains **zero tracking, telemetry, or analytics**. What you watch stays entirely on your local device.
*   **Intelligent Caching:** EPG data and playlists are cached locally via high-speed databases (Isar/Room) to minimize network load and API rate limits.
*   **Graceful Degradation:** Our UI is built to handle network timeouts elegantly. If an API fails, the app seamlessly defaults to cached data without crashing.

---

## 🔮 Future Roadmap (Phase 4 & Beyond)
*   [ ] **Torrent & P2P Integration:** Integration of WebTorrent and Acestream protocols directly into the player to enable decentralized, peer-to-peer streaming. This ensures zero-buffering even on highly congested live sports streams.
*   [ ] **AI Metadata Fetcher:** Utilizing local, small-language models to clean up messy channel names and automatically assign TMDB metadata.
*   [ ] **Automated Docker Deployment:** A one-click Docker image to host the entire aggregator and proxy stack on a home NAS (e.g., Unraid/TrueNAS).

---

## 🙏 Special Thanks & Acknowledgments
This project stands on the shoulders of the incredible open-source IPTV community. We extend our deepest gratitude to the maintainers of the public playlists and data sources utilized in our aggregator:
*   [iptv-org](https://github.com/iptv-org/iptv)
*   [SM-Live-TV (sm-monirulislam)](https://github.com/sm-monirulislam)
*   [abusaeeidx](https://github.com/abusaeeidx)
*   [Free-TV](https://github.com/Free-TV/IPTV)
*   [BuddyChewChew](https://github.com/BuddyChewChew)
*   [Love4vn](https://github.com/Love4vn)
*   *...and all other contributors dedicating their time to keep public streams alive!*

---
*Created with ❤️ by ShoumikBalaSomu and the Open Source Community.*
