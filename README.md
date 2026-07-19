# ALL-IN-One-IPTV Ecosystem

![License](https://img.shields.io/github/license/ShoumikBalaSomu/ALL-IN-One-IPTV)
![Last Update](https://img.shields.io/github/last-commit/ShoumikBalaSomu/ALL-IN-One-IPTV)
![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Windows%20%7C%20Linux-blue)

The ultimate, fully automated IPTV ecosystem. This repository features a highly concurrent Python link aggregator, an intelligent Android Local Proxy for mesh P2P streaming, and a high-performance Flutter Multi-View Player.

## 📺 Auto-Updating M3U Playlists

Our GitHub Actions pipeline scrapes, deduplicates, and health-checks thousands of IPTV links every 6 hours to ensure zero dead streams. 

Simply copy and paste one of the following URLs into your favorite IPTV Player (e.g., Tivimate, OTT Navigator, or our custom player!):

👉 **[Healthy Verified Playlist (Recommended)](https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u)**  
*This list has been actively pinged and contains only live, working streams.*

👉 **[Raw Combined Playlist (All Links)](https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/combined_by_country.m3u)**  
*This is the raw scraped list before health checks are applied.*

---

## 📱 Download the Apps

We have built a state-of-the-art IPTV Player (Flutter) and a Local Mesh Proxy (Kotlin) that slash buffering using local P2P networking and AI-driven stream healing.

**[Download the latest APKs from the GitHub Releases tab!](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/releases)**

---

## 🛠️ Build Locally From Source

If you are a developer and want to compile the Android apps locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV.git
   cd ALL-IN-One-IPTV
   ```

2. Run the automated local build script (requires Flutter and Java 17):
   ```bash
   bash build_local.sh
   ```

The script will automatically compile both the `app_player` and the `app_proxy` and output the paths to the generated APKs.

---

## 🏗️ Repository Architecture
- `/backend`: The asynchronous Python scraping, health-checking, DRM-vault, and AI-healing infrastructure.
- `/app_player`: The cross-platform Flutter application featuring AV1 decoding and Multi-View Grid rendering.
- `/app_proxy`: The Android Kotlin application running a Ktor server for LAN P2P stream relaying.
