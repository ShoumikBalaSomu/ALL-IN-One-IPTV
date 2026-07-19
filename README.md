# ALL-IN-One-IPTV Ecosystem

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Update Playlists](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/actions/workflows/update.yml/badge.svg)

Welcome to the **ALL-IN-One-IPTV** repository! This project aims to build a complete, production-ready open-source IPTV ecosystem.

## Phase 1: Automated Playlist Aggregator

This repository currently hosts the Automated Playlist Aggregator. It is a highly concurrent Python script designed to run on GitHub Actions. It fetches various IPTV playlists from multiple sources, deduplicates them, groups channels by country, checks stream health, and outputs optimized `.m3u` playlists.

### Outputs
- `output/Combined_by_Country.m3u`: All unique streams from the sources grouped by country.
- `output/Checked_Combined_by_Country.m3u`: Only the streams that passed a real-time health check.

### How it works
1. **Auto-Collect & Combine:** Fetches all defined M3U URLs.
2. **Deduplication:** Removes duplicate stream URLs.
3. **Health Checking:** Concurrently checks stream vitality to filter out dead links.
4. **Automation:** A GitHub Action runs daily to update the generated playlists.

### Usage
You can drop any `.m3u` or `.m3u8` files into the `input/` folder and push to the repository. The GitHub action will automatically pick them up, process them along with the main sources, and update the `output/` folder.

## Acknowledgments
We would like to thank all the playlist maintainers whose public playlists are aggregated here:
- sm-monirulislam
- abusaeeidx
- xfireflix
- Mrbotrx
- tahsinulmohsin
- ashik4u
- opensourceflix
- alberttartas
- iptv-org
- and many others!

## Future Phases
- **Phase 2:** Cross-Platform IPTV & VOD Player
- **Phase 3:** Playlist Optimizer Local Proxy App

## Disclaimer
Please read our [LEGAL.md](LEGAL.md) before using this repository.
