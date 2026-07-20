# About ALL-IN-One-IPTV

## 🌟 Our Vision

The dream behind **ALL-IN-One-IPTV** is to create the ultimate, uncompromising ecosystem for open-source IPTV consumption. We noticed that while there are thousands of great IPTV playlists scattered across GitHub and the internet, finding working links, maintaining them, and viewing them in a premium interface was an incredibly frustrating experience.

We aim to solve this by providing:
1. **An automated pipeline** that constantly scrapes, merges, and validates streams.
2. **Premium client applications** that rival commercial streaming giants (like Netflix).
3. **Advanced proxy tools** that silently fix broken streams in the background before they even buffer.

## 🛠 Architecture

### The Aggregator
At the core of the project is a Python-based aggregator (`aggregator.py`). 
- It reads from over 40+ recognized community repositories.
- It can read personal, encrypted, or unencrypted local `.m3u` files from the `input/` folder.
- It uses asynchronous `aiohttp` requests to ping thousands of video streams in seconds without downloading the video payload (using HTTP HEAD requests).

### The Clients
We didn't want users to be stuck with clunky, outdated UI. 
- The **Flutter App (`app_player`)** provides native performance across Windows, Linux, and Android. It features complex UI paradigms like Glassmorphism and dynamic hero transitions.
- The **Web App (`web-player`)** ensures that anyone with a browser can access the platform instantly.

### The Optimizer
The **Android Proxy (`app_proxy`)** acts as a local interceptor. When a user clicks a channel, the proxy intercepts the request, tests multiple known fallback URLs for that channel concurrently, and redirects the video player to the fastest responding server.

---

## ⚖️ Legal & Compliance

**ALL-IN-One-IPTV is an aggregator tool.** 

- We **DO NOT** own any of the media servers, streams, or content linked in these playlists.
- We **DO NOT** host any video files. 
- We **DO NOT** sell access to IPTV. 

This repository simply provides a software ecosystem and compiles a list of hyperlinks that are already publicly available on the internet (primarily gathered from other open-source GitHub repositories).

If you are a copyright owner and believe a link in our aggregated lists infringes upon your rights, please note that removing the link from our aggregator will not remove the stream from the internet, as we do not host it. However, we are happy to blacklist specific URLs from our aggregator upon request.

---

## 🤝 Contributing

We welcome contributions! Whether it's adding a new UI feature to the Flutter app, optimizing the Python aggregator's concurrency, or adding support for new streaming protocols (like Torrent IPTV), please feel free to open a Pull Request.

### Maintainers
* **ShoumikBalaSomu** - Lead Developer & Architect
