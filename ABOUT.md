# 🚀 ABOUT — ALL-IN-One IPTV Monorepo Empire

```
  █████╗ ██╗     ██╗     ██╗███╗   ██╗     ██████╗ ███╗   ██╗███████╗    ██╗██████╗ ████████╗██╗   ██╗
 ██╔══██╗██║     ██║     ██║████╗  ██║    ██╔═══██╗████╗  ██║██╔════╝    ██║██╔══██╗╚══██╔══╝██║   ██║
 ███████║██║     ██║     ██║██╔██╗ ██║    ██║   ██║██╔██╗ ██║█████╗      ██║██████╔╝   ██║   ██║   ██║
 ██╔══██║██║     ██║     ██║██║╚██╗██║    ██║   ██║██║╚██╗██║██╔══╝      ██║██╔═══╝    ██║   ╚██╗ ██╔╝
 ██║  ██║███████╗███████╗██║██║ ╚████║    ╚██████╔╝██║ ╚████║███████╗    ██║██║        ██║    ╚████╔╝ 
 ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝╚═╝        ╚═╝     ╚═══╝  
```

> **The World's Most Advanced Open-Source IPTV Ecosystem**: Autonomous Backend Aggregator, Parallel Health Verifier, Smart Stream Fallback Matrix, Cross-Platform Unified Player, Native Android Local Proxy, and Glassmorphic Web App Portal.

---

## 🛰️ Mission & Vision

**ALL-IN-One IPTV** was engineered to solve the fundamental flaws of legacy IPTV playlist repositories:
1. **Broken Stream Link Decay**: Legacy M3U playlists degrade within 48 hours. Our **500-Worker Parallel Async Verifier & Domain Circuit Breaker** tests 10,000+ alive domains in under 90 seconds, filtering dead hosts automatically.
2. **Duplicate Channel Spam**: Instead of listing 20 duplicate instances of "HBO", our **Smart Channel Merger** folds duplicates into a single channel entry with **latency-ranked fallback stream mirrors**.
3. **Buffering & Stalling**: Our **1.5s Smart Fallback Engine** inside the Flutter Player and Native Android Proxy automatically detects stream errors and redirects playback to the fastest alive mirror seamlessly.

---

## ⚡ Ecosystem Core Modules

| Module | Location | Description | Tech Stack |
| :--- | :--- | :--- | :--- |
| **Backend Engine** | [`engine/src/`](engine/src/) | Scraper, Verifier, Deduplicator, EPG, Search, Encryption, IPFS | Python 3.11/3.14, `aiohttp`, `rich` |
| **Flutter Player** | [`apps/app_player/`](apps/app_player/) | Glassmorphic Media Player with EPG Guide & Netflix VOD | Flutter 3.27, Dart, `media_kit`, Riverpod |
| **Android Proxy** | [`apps/app_proxy/`](apps/app_proxy/) | Foreground Service Ktor Server hosting `http://127.0.0.1:8080` | Kotlin 2.0, Ktor, Jetpack Compose, Coroutines |
| **Web App Portal** | [`docs/`](docs/) | Glassmorphic HLS.js Browser Player with PIN `0171` Controls | HTML5, CSS3, JavaScript, HLS.js |
| **Google Colab** | [`colab/`](colab/) | Cloud Aggregation & AES-256-GCM Playlist Encryption Notebooks | Jupyter Notebook, Python |

---

## 🛡️ License & DMCA Statement

This project is licensed under the [MIT License](LICENSE). Read [LEGAL.md](LEGAL.md) and [DISCLAIMER.md](DISCLAIMER.md) for copyright and compliance policies.
