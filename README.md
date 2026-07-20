# ALL-IN-One-IPTV

Welcome to the **ALL-IN-One-IPTV** project. Our dream is providing an all-in-one IPTV Helper, archiving, and improving all IPTV tools. This repository combines and improves freely available IPTV playlists, groups them, removes duplicates, and ensures dead links are removed in real-time.

## Features

- **Automated Collection & Aggregation**: Collects playlists automatically from publicly available sources and updates on GitHub via GitHub Actions.
- **Smart Deduplication**: Removes identical URLs and intelligently folds duplicate channels based on titles.
- **Cookie Preservation**: Recognizes channels that require authentication (cookies, tokens) and preserves them.
- **Health Check / Probing**: Parallely checks all combined links to see if they are alive (HTTP status).
- **Group By Country**: Channels are properly grouped into categories or countries.
- **User Input & Encryption**: Supports custom user playlists (plain or encrypted).

## Disclaimer

**Legal Notice:**
We do not own, host, or broadcast any of the streams or playlists provided in this repository. We are only collecting and aggregating publicly available playlists from the internet. This project is meant for educational and organizational purposes only. Please use this responsibly and ensure you comply with your local laws.

## Playlists Generated

1. `output/combined_by_country.m3u` - Aggregated and folded playlists.
2. `output/checked_combined_by_country.m3u` - Only contains streams that are actively alive at the time of the latest update.

## Apps & UI Included in this Repository

This repository includes a complete ecosystem of tools and applications:

1. **Flutter Unified Player (`app_player`)**: A cross-platform app (Windows, Linux, Android) featuring:
   - **Movie/Series Section**: Netflix-like premium UI/UX.
   - **IPTV Section**: OTT Navigator-like features with EPG toggles, glassmorphism UI, Category sidebars, and smooth channel lists.
2. **Web Player (`web-player`)**: A Vite-based React player providing the same premium experience for browsers.
3. **Android Optimizer Proxy (`app_proxy`)**: A companion Android app acting as an interceptor. It provides:
   - Real-time stream folding (HTTP HEAD testing).
   - Dynamic redirecting to the best performing link without dead streams.
   - Premium Jetpack Compose UI for VPN and Proxy management.
4. **Custom Input Support**: Place your encrypted or unencrypted `.m3u` files in the `input/` folder, and the aggregator will merge them.

## Future Works

- **Torrent IPTV (P2P)**: Implementing a peer-to-peer streaming logic to ensure zero buffering by distributing stream loads across viewers.

## Thanks & Credits

Special thanks to all the playlist maintainers whose publicly available lists we aggregate:
- @sm-monirulislam
- @abusaeeidx
- @Mrbotrx
- @johirxofficial
- @tahsinulmohsin
- @ashik4u
- @opensourceflix
- @sanjoykb
- @alberttartas
- @Love4vn
- And all other open-source contributors!

## License
MIT License. See the `LICENSE` file for more details.
