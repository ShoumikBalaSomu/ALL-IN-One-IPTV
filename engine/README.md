# ALL-IN-ONE IPTV Engine

Modern, async-powered IPTV engine designed to collect, verify, deduplicate, and organize IPTV playlists.

## Features

- **Asynchronous Processing**: Powered by `asyncio` and `aiohttp` for high-performance scraping and verifying.
- **Smart M3U Parsing**: Extracts `tvg-id`, `tvg-name`, `tvg-logo`, `group-title`, etc.
- **Concurrent Stream Health Checking**: Validates streams quickly using customizable workers.
- **Fuzzy Deduplication**: Removes duplicate streams based on URL and title similarity.
- **Beautiful CLI**: Uses `rich` for elegant output and progress tracking.
- **Structured Logging**: Uses `structlog` for machine-readable logging.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the engine via:

```bash
python -m src
```
