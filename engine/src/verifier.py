"""
Verifier — High-Performance Concurrent Stream Health & Latency Checker.

Features:
1. Ultra-fast asyncio worker pool (500 workers).
2. Domain Circuit Breaker (Blacklists failed hosts after 3 consecutive timeouts).
3. Latency measurement (ms) for host speed ranking.
"""

import asyncio
import time
from typing import List, Dict
from urllib.parse import urlparse

import aiohttp
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

from .parser import Stream
from .utils import logger

# Global domain failure tracker for Circuit Breaker
DOMAIN_FAILURES: Dict[str, int] = {}
MAX_DOMAIN_FAILURES = 3

def extract_host(url: str) -> str:
    """Extract scheme + netloc from stream URL."""
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return ""

async def check_stream(
    session: aiohttp.ClientSession,
    stream: Stream,
    timeout: int = 3,
) -> bool:
    """Check if a single stream URL is alive via HTTP HEAD request with Circuit Breaker and latency profiling."""
    host = extract_host(stream.url)

    # Circuit Breaker: Skip host if it failed repeatedly
    if host and DOMAIN_FAILURES.get(host, 0) >= MAX_DOMAIN_FAILURES:
        stream.latency_ms = 9999.0
        return False

    start_time = time.perf_counter()
    try:
        async with session.head(
            stream.url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            ssl=False,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (VLC/3.0.18)"}
        ) as resp:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            is_ok = resp.status < 400
            if is_ok:
                stream.latency_ms = elapsed_ms
                if host:
                    DOMAIN_FAILURES[host] = 0 # Reset on success
            else:
                stream.latency_ms = 9999.0
                if host:
                    DOMAIN_FAILURES[host] = DOMAIN_FAILURES.get(host, 0) + 1
            return is_ok
    except (aiohttp.ClientError, asyncio.TimeoutError, Exception):
        stream.latency_ms = 9999.0
        if host:
            DOMAIN_FAILURES[host] = DOMAIN_FAILURES.get(host, 0) + 1
        return False


async def verify_streams(
    streams: List[Stream],
    workers: int = 500,
    timeout: int = 3,
) -> List[Stream]:
    """
    Verify a list of streams concurrently with Domain Circuit Breaker and Latency Ranking.

    Args:
        streams: List of Stream objects to verify.
        workers: Maximum concurrent verification requests (default 500).
        timeout: Per-stream timeout in seconds (default 3s).

    Returns:
        List of streams that responded successfully.
    """
    if not streams:
        return []

    alive: List[Stream] = []
    semaphore = asyncio.Semaphore(workers)
    connector = aiohttp.TCPConnector(
        limit=workers,
        ttl_dns_cache=300,
        enable_cleanup_closed=True,
        ssl=False
    )

    async with aiohttp.ClientSession(connector=connector) as session:

        async def bounded_check(stream: Stream) -> tuple[Stream, bool]:
            async with semaphore:
                result = await check_stream(session, stream, timeout)
                return stream, result

        tasks = [bounded_check(s) for s in streams]

        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]Verifying & Latency Profiling..."),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeRemainingColumn(),
        ) as progress:
            task_id = progress.add_task("Verifying", total=len(tasks))

            for coro in asyncio.as_completed(tasks):
                stream, is_alive = await coro
                if is_alive:
                    alive.append(stream)
                progress.advance(task_id)

    dead = len(streams) - len(alive)
    logger.info(f"Verification complete: {len(alive)} alive, {dead} dead ({len(DOMAIN_FAILURES)} hosts tracked)")
    return alive
