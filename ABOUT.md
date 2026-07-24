# 📖 About ALL-IN-ONE IPTV

**ALL-IN-ONE IPTV** was born from a simple need: reliable, easily accessible, and organized IPTV streams. The landscape of free IPTV is scattered, frequently broken, and difficult to navigate. We aimed to change that.

## 🌟 Our Vision

To build the most resilient and automated ecosystem for global open IPTV content, ensuring high availability, metadata richness, and seamless user experiences across all devices.

## 🏗️ Architecture Deep Dive

The project consists of several decoupled but highly synergistic components:

1. **The Harvester (Scraping Layer):** Written in Python using `aiohttp` and `BeautifulSoup4`, it asynchronously crawls known repositories, forums, and directories for M3U and M3U8 links.
2. **The Forge (Processing Layer):** Normalizes stream data. It extracts logos, categorizes by country/language using natural language processing heuristics, and deduplicates identical streams.
3. **The Sentinel (Validator Layer):** Uses FFprobe and lightweight HTTP headers to check stream viability at scale. Streams are tested for latency, codec information, and stability.
4. **The Gateway (Delivery Layer):** Serves the processed playlists via static GitHub Pages and a dynamic FastAPI service for advanced querying.

## 🛠️ Technology Choices Rationale

- **Python 3.12+**: Selected for its mature async ecosystem (`asyncio`, `aiohttp`), which is critical for parallel stream validation and scraping.
- **FastAPI**: Chosen for the backend due to its speed, automatic Swagger UI generation, and native asynchronous support.
- **Flutter**: The obvious choice for our mobile and desktop client applications, allowing a single codebase to target iOS, Android, Windows, macOS, and Linux with native performance.
- **Docker**: Ensures reproducibility across environments, enabling users to spin up their own personal IPTV aggregation nodes effortlessly.

## 🤝 Community & Team

We believe in the power of open-source. This project thrives on community contributions—whether it's adding a new source to the scraper, improving the regex for stream parsing, or fixing UI bugs in the web player.
