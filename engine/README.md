# 🔧 IPTV Engine

Modular Python engine for collecting, combining, deduplicating, and verifying IPTV playlists.

## Quick Start

```bash
cd engine
pip install -r requirements.txt

# Run full pipeline (collect → combine → verify)
python -m src.main

# Skip verification (faster)
python -m src.main --no-verify

# Custom directories
python -m src.main --input my_playlists --output results

# Decrypt encrypted playlists
python -m src.main --decrypt-key YOUR_64_CHAR_HEX_KEY
```

## Architecture

```
src/
├── main.py          # Pipeline orchestrator
├── collector.py     # Fetch playlists from URLs + local files
├── parser.py        # Parse M3U/M3U8 format
├── combiner.py      # Export to M3U format
├── deduplicator.py  # Remove duplicate URLs
├── grouper.py       # Group channels by country
├── folder.py        # Fold similar channels
├── verifier.py      # Parallel link health checker
├── encryption.py    # AES-256-GCM encrypt/decrypt
└── utils.py         # Helpers (logging, normalization, etc.)
```

## Pipeline

1. **Collect** — Fetch 60+ remote playlists + read local files (supports .m3u, .m3u8, .enc)
2. **Parse** — Extract channels with full metadata (cookies, headers, TVG info)
3. **Deduplicate** — Remove exact URL duplicates, preserve special channels
4. **Group** — Auto-detect country and group channels
5. **Fold** — Merge same channel from multiple sources
6. **Export** — Write `combined_by_country.m3u`
7. **Verify** — Parallel host-level health check → `checked_combined_by_country.m3u`

## Input

Drop your playlists in `engine/input/`:
- `.m3u` / `.m3u8` — Plain text playlists
- `.enc` — AES-256-GCM encrypted (requires `--decrypt-key`)

## Output

Generated in `engine/output/`:
- `combined_by_country.m3u` — All channels, grouped by country
- `checked_combined_by_country.m3u` — Only verified working links

## Adding Playlists

Edit `src/collector.py` and add URLs to `DEFAULT_PLAYLISTS`.

## Performance

- 100 concurrent HTTP requests by default
- Host-level checking (if one URL from host works, all work)
- Typically verifies 50,000+ channels in under 5 minutes