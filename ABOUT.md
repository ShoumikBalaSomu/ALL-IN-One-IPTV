<div align="center">

# 📖 About ALL-IN-One-IPTV

*Understanding the Vision, Architecture, and Mission behind the Ultimate Ecosystem.*

<br/>

<img src="https://img.shields.io/badge/Architecture-Python_|_Flutter_|_Kotlin_|_React-blue?style=for-the-badge"/>

</div>

---

## 🌟 Our Vision

The dream behind **ALL-IN-One-IPTV** is to create the ultimate, uncompromising ecosystem for open-source IPTV consumption. We noticed that while there are thousands of great IPTV playlists scattered across GitHub and the internet, finding working links, maintaining them, and viewing them in a premium interface was an incredibly frustrating experience.

We aim to solve this by providing:
1. **An Automated Pipeline:** That constantly scrapes, merges, and validates streams.
2. **Premium Client Applications:** That rival commercial streaming giants like Netflix or Amazon Prime.
3. **Advanced Proxy Tools:** That silently fix broken streams in the background before they even buffer on your screen.

---

## 🛠 Project Architecture

We utilize a diverse tech stack to ensure peak performance across the board.

### 🐍 The Aggregator (`aggregator.py`)
- Reads from over 40+ recognized community repositories.
- Can ingest personal, encrypted, or unencrypted local `.m3u` files from the `input/` folder.
- Leverages asynchronous `aiohttp` requests to ping thousands of video streams in seconds using HTTP `HEAD` requests, strictly evaluating response health without wasting bandwidth.

### 📱 The Native Clients (`app_player/`)
We discarded standard UI frameworks in favor of building bespoke aesthetic experiences.
- **Flutter Framework:** Provides native desktop and mobile performance.
- **Glassmorphism & Micro-animations:** Our UI feels alive, responding smoothly to user interactions.

### 🛡️ The Optimizer (`app_proxy/`)
- A Kotlin backend that intercepts video requests. 
- When a user clicks a channel, the proxy intercepts the request, tests multiple known fallback URLs for that channel concurrently, and redirects the video player to the fastest responding server instantly.

---

## 🤝 Contributing

This is a community-driven project! We welcome contributions ranging from adding a new UI feature to the Flutter app, optimizing the Python aggregator's concurrency, or bringing our Torrent IPTV dream to life.

### Lead Architect
* **ShoumikBalaSomu**

---

## ⚖️ Legal & Compliance

**ALL-IN-One-IPTV is strictly an aggregator and UI toolset.** 

* ❌ We **DO NOT** own any of the media servers, streams, or content linked in these playlists.
* ❌ We **DO NOT** host any video files. 
* ❌ We **DO NOT** sell access to IPTV. 

This repository simply provides a software ecosystem and compiles a list of hyperlinks that are already publicly available on the internet (primarily gathered from other open-source GitHub repositories).

*If you are a copyright owner and believe a link in our aggregated lists infringes upon your rights, please note that removing the link from our aggregator will not remove the stream from the internet, as we do not host it. However, we are happy to permanently blacklist specific URLs from our aggregator upon request.*
