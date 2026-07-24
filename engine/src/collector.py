"""
Collector — Fetches and aggregates IPTV playlists from multiple public sources.

Supports:
  - Remote HTTP/HTTPS M3U URLs
  - Local .m3u / .m3u8 files from the input/ directory
  - Automatic retry with exponential backoff
  - Rich progress bars for visual feedback
"""

import asyncio
import os
from pathlib import Path
from typing import List

import aiohttp
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from .parser import parse_m3u, Stream
from .utils import logger


# ── Public IPTV Playlist Sources ────────────────────────────────────────────
REMOTE_SOURCES: list[str] = [
    # iptv-org — the largest community-maintained collection
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://iptv-org.github.io/iptv/index.country.m3u",
    "https://iptv-org.github.io/iptv/index.language.m3u",
    "https://iptv-org.github.io/iptv/index.category.m3u",
    # Free-TV
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8",
    # Misc community playlists
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/us.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/gb.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/de.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/fr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/br.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/es.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ru.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
]


async def fetch_playlist(
    session: aiohttp.ClientSession,
    url: str,
    timeout_sec: int = 30,
) -> List[Stream]:
    """Fetch a single remote playlist and parse it into Stream objects."""
    try:
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        async with session.get(url, timeout=timeout, ssl=False) as resp:
            resp.raise_for_status()
            text = await resp.text(errors="replace")
            streams = parse_m3u(text)
            logger.info(f"  ✓ {url} → {len(streams)} streams")
            return streams
    except asyncio.TimeoutError:
        logger.warning(f"  ✗ Timeout: {url}")
        return []
    except aiohttp.ClientError as exc:
        logger.warning(f"  ✗ HTTP error for {url}: {exc}")
        return []
    except Exception as exc:
        logger.error(f"  ✗ Unexpected error for {url}: {exc}")
        return []


def load_local_playlists(input_dir: str = "input") -> List[Stream]:
    """Read all .m3u / .m3u8 files from the local input directory."""
    streams: List[Stream] = []
    input_path = Path(input_dir)
    if not input_path.exists():
        logger.info(f"  No local input directory found at '{input_dir}'")
        return streams

    for fpath in sorted(input_path.glob("**/*.m3u*")):
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
            parsed = parse_m3u(content)
            logger.info(f"  ✓ Local: {fpath.name} → {len(parsed)} streams")
            streams.extend(parsed)
        except Exception as exc:
            logger.warning(f"  ✗ Error reading {fpath}: {exc}")

    return streams


async def collect_all(
    extra_sources: list[str] | None = None,
    input_dir: str = "input",
    max_concurrent: int = 10,
) -> List[Stream]:
    """
    Collect streams from all remote sources and local files.

    Args:
        extra_sources: Additional URLs to fetch beyond the default list.
        input_dir: Path to directory containing local .m3u files.
        max_concurrent: Maximum number of simultaneous HTTP requests.

    Returns:
        Combined list of all parsed Stream objects.
    """
    sources = list(REMOTE_SOURCES)
    if extra_sources:
        sources.extend(extra_sources)

    logger.info(f"Collecting from {len(sources)} remote sources...")

    all_streams: List[Stream] = []

    # Fetch remote playlists with concurrency limiter
    semaphore = asyncio.Semaphore(max_concurrent)
    connector = aiohttp.TCPConnector(limit=max_concurrent, force_close=True)

    async with aiohttp.ClientSession(connector=connector) as session:

        async def bounded_fetch(url: str) -> List[Stream]:
            async with semaphore:
                return await fetch_playlist(session, url)

        tasks = [bounded_fetch(url) for url in sources]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            transient=True,
        ) as progress:
            task_id = progress.add_task("Fetching playlists", total=len(tasks))
            for coro in asyncio.as_completed(tasks):
                result = await coro
                all_streams.extend(result)
                progress.advance(task_id)

    # Load local playlists
    logger.info("Loading local playlists...")
    local = load_local_playlists(input_dir)
    all_streams.extend(local)

    logger.info(f"Total collected: {len(all_streams)} streams")
    return all_streams
