<div align="center">
  
# 📺 ALL-IN-One-IPTV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/ShoumikBalaSomu/ALL-IN-One-IPTV)](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/issues)
[![GitHub stars](https://img.shields.io/github/stars/ShoumikBalaSomu/ALL-IN-One-IPTV)](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/stargazers)
[![Update Playlists](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/actions/workflows/update.yml/badge.svg)](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/actions)

**The ultimate, automated IPTV helper, aggregator, and cross-platform ecosystem.**  
*Our dream is to provide the best all-in-one IPTV solution by combining, optimizing, and organizing publicly available IPTV playlists into a single, high-performance experience.*

[**Read More About The Project**](./ABOUT.md)

</div>

---

## ⚡ Core Features

- **🤖 Automated Aggregation:** Automatically collects and merges playlists from various public repositories daily via GitHub Actions.
- **🧹 Smart Deduplication:** Intelligently folds identical channels based on titles and removes duplicate URLs.
- **🍪 Cookie Preservation:** Automatically detects and preserves channels requiring authentication tokens or cookies.
- **🏥 Parallel Health Checks:** Validates thousands of streams concurrently using HTTP HEAD requests to ensure you only get working links.
- **🌍 Geo-Organization:** Automatically groups channels by country and category for a clean EPG experience.
- **📁 Custom Input Support:** Place your own `.m3u` or `.m3u8` playlists (encrypted or unencrypted) in the `input/` folder to seamlessly merge them with the master list.

---

## 📦 Generated Playlists

You can plug these directly into your favorite IPTV player! They are updated automatically.

| Playlist Type | Description | Link |
| --- | --- | --- |
| 🌍 **Combined & Folded** | The massive master list with duplicates grouped by country. | [Download M3U](https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/combined_by_country.m3u) |
| ✅ **Checked & Alive** | The strictly checked version. Dead links are removed. | [Download M3U](https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u) |

---

## 📱 Ecosystem Apps included

This repository isn't just a playlist aggregator; it contains a suite of premium applications designed to give you the best viewing experience:

### 1. Flutter Unified Player (`app_player/`)
A cross-platform application built with Flutter (Windows, Linux, Android) providing a premium viewing experience:
- 🎬 **Movie/Series Section:** Features a stunning, Netflix-inspired UI with hero banners and carousels.
- 📺 **Live TV Section:** Inspired by OTT Navigator, featuring glassmorphism, category sidebars, and an integrated EPG.
- 🔗 **Multi-Source Support:** Accepts Xtream Codes, MAC Portal, Emby/Jellyfin, Plex, and standard M3U links.

### 2. Android Optimizer Proxy (`app_proxy/`)
A background interceptor app for Android, built with Jetpack Compose:
- 🚀 **Real-time Stream Folding:** Tests fallback URLs instantly to ensure zero downtime.
- 🔀 **Dynamic Redirection:** Redirects your player to the healthiest stream.
- 🛡️ **VPN/Proxy Integration:** Beautiful control center for OpenVPN integration.

### 3. Web Player (`web-player/`)
A Vite + React-based frontend providing the same premium unified experience directly in your browser.

---

## 🚀 Future Roadmap

- [ ] **Torrent IPTV (P2P):** Implement WebRTC/Libtorrent peer-to-peer streaming to distribute loads across viewers, effectively eliminating buffering for highly watched channels.
- [ ] **Advanced EPG Scraping:** Automated syncing of EPG data for obscure regional channels.

---

## 🙏 Acknowledgements & Credits

This project stands on the shoulders of giants. We want to extend our deepest gratitude to the incredible open-source playlist maintainers:

`@sm-monirulislam` • `@abusaeeidx` • `@Mrbotrx` • `@johirxofficial` • `@tahsinulmohsin` • `@ashik4u` • `@opensourceflix` • `@sanjoykb` • `@alberttartas` • `@Love4vn` • `@BuddyChewChew` • `@alex4528y` • `@judy-gotv` 

*And all other open-source contributors making free IPTV accessible to everyone!*

---

## ⚖️ Legal Disclaimer

**We do not own, host, or broadcast any of the streams or playlists provided in this repository.** We are exclusively aggregating publicly available, free-to-air links found across the internet. This project is meant for educational and organizational purposes only. Please use this responsibly and ensure you comply with your local copyright laws. See [ABOUT.md](./ABOUT.md) for more details.

---

<div align="center">
  <i>Built with ❤️ for the open-source community.</i>
</div>
