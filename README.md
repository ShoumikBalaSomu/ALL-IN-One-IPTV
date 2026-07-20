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

## Future Plans (Apps & UI)

We are planning to build an ultimate web and cross-platform app (Windows, Linux, Android) which will include:
1. **Movie/Series Section**: Netflix-like premium UI/UX.
2. **IPTV Section**: OTT Navigator-like features with EPG, Sorting, Blocking, Folding, and Numbering.
3. **Advanced Proxy & Optimizer App**: A companion app to provide real-time dead-link removal and optimal proxy to any standard IPTV player.

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
